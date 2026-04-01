from flask import Flask, request, jsonify, render_template
from groq import Groq
import json, os, datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

with open("menu.json", "r") as f:
    menu = json.load(f)

# Auto-create orders.json with empty array
if not os.path.exists("orders.json"):
    with open("orders.json", "w") as f:
        json.dump([], f)
else:
    # Fix corrupted orders.json
    try:
        with open("orders.json", "r") as f:
            content = f.read().strip()
        if not content or content == "{}":
            with open("orders.json", "w") as f:
                json.dump([], f)
    except:
        with open("orders.json", "w") as f:
            json.dump([], f)

SYSTEM_PROMPT = f"""
Role:
You are "Byte", the sophisticated AI waiter of Demo Diner — an upscale casual dining experience known for bold flavors and warm elegance.

Task:
Assist guests with questions about the menu, pricing, ingredients, dietary needs, hours, and location.
You CAN take orders. When a guest wants to order, collect their items and confirm.

Order Flow:
1. When a guest mentions ordering items, summarize what they want clearly.
2. Ask them to confirm with a simple "yes" or "confirm".
3. Once confirmed, respond with EXACTLY this JSON on its own line (nothing before or after on that line):
ORDER_CONFIRMED:{{"items": [...], "total": X.XX, "note": "any special note or empty string"}}
4. After that line, add a warm confirmation message to the guest.

Context:
Demo Diner is a refined yet welcoming restaurant offering Starters, Mains, Drinks, and Desserts.

Opening Hours:
- Monday to Friday: 11:00 AM – 10:00 PM
- Saturday & Sunday: 10:00 AM – 11:00 PM
- Current date and time: {datetime.datetime.now().strftime("%A, %B %d %Y — %I:%M %p")}

Location:
123 Food Street, Downtown City. Parking available. Near City Central Metro Station.

Full Menu:
{json.dumps(menu, indent=2)}

Reasoning:
Read between the lines of what the guest is asking.
If they seem undecided, guide them with a confident recommendation.
If they have dietary needs, navigate the menu thoughtfully.
If they seem to be celebrating something, acknowledge it warmly.
When confirming an order, calculate the total accurately from menu prices.

Stop Conditions:
- Only discuss the menu, hours, location, dining experience, and orders.
- Never break character.
- If asked about anything unrelated, decline gracefully.

Output:
- Speak with quiet confidence — warm but refined, never overly casual.
- Keep replies concise but never rushed.
- Keep replies medium sized, don't respond with long paragraphs
- End with a thoughtful follow-up when natural.
"""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "").strip()
    history = data.get("history", [])

    if not user_message:
        return jsonify({"reply": "Please type something!"}), 400

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += history
    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=400,
            temperature=0.7
        )
        full_reply = response.choices[0].message.content

        
        order_data = None
        clean_lines = []

        for line in full_reply.split("\n"):
            stripped = line.strip()
            if stripped.startswith("ORDER_CONFIRMED:"):
                try:
                    json_str = stripped[len("ORDER_CONFIRMED:"):].strip()
                    order_data = json.loads(json_str)
                except Exception as parse_err:
                    print("JSON parse error:", parse_err)
            else:
                clean_lines.append(line)

        clean_reply = "\n".join(clean_lines).strip()

        # Save order
        if order_data:
            try:
                with open("orders.json", "r") as f:
                    orders = json.load(f)
            except:
                orders = []

            new_order = {
                "id": len(orders) + 1,
                "items": order_data.get("items", []),
                "total": order_data.get("total", 0),
                "note": order_data.get("note", ""),
                "status": "pending",
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            orders.append(new_order)

            with open("orders.json", "w") as f:
                json.dump(orders, f, indent=2)

        return jsonify({"reply": clean_reply, "order_confirmed": order_data is not None})

    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"}), 500

@app.route("/orders", methods=["GET"])
def get_orders():
    try:
        with open("orders.json", "r") as f:
            orders = json.load(f)
        return jsonify(orders)
    except Exception as e:
        print("Orders error:", e)
        return jsonify([])

@app.route("/orders/<int:order_id>/status", methods=["POST"])
def update_status(order_id):
    try:
        data = request.json
        new_status = data.get("status")

        with open("orders.json", "r") as f:
            orders = json.load(f)

        for order in orders:
            if order["id"] == order_id:
                order["status"] = new_status
                break

        with open("orders.json", "w") as f:
            json.dump(orders, f, indent=2)

        return jsonify({"success": True})
    except Exception as e:
        print("Update status error:", e)
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)