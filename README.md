# Byte-Restaurant-Chatbot

## Project Description
Byte-Restaurant-Chatbot is an AI-powered chatbot designed to assist customers at Demo Diner, an upscale casual dining restaurant. It provides menu information, takes orders, and handles customer inquiries with a sophisticated and warm demeanor.

## Features
- **Menu Assistance**: Answers questions about menu items, prices, and ingredients.
- **Order Taking**: Collects and confirms customer orders with a clear and concise flow.
- **Dietary Guidance**: Helps customers with dietary needs navigate the menu.
- **Order Management**: Tracks and updates order statuses via a dashboard.
- **Contextual Responses**: Provides thoughtful recommendations and acknowledges special occasions.

## Tech Stack
- **Language**: Python
- **Framework**: Flask
- **LLM**: Groq (Llama 3.3 70B Versatile)
- **Data Storage**: JSON files (`menu.json`, `orders.json`)
- **Environment Management**: `dotenv`
- **Frontend**: HTML templates

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/aliii-codes/Byte-Restaurant-Chatbot.git
   cd Byte-Restaurant-Chatbot
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Fill in GROQ_API_KEY in .env
   ```
4. Run the application:
   ```bash
   python app.py
   ```

## Usage
1. **Chat with Byte**: Access the chatbot via the `/` route in your browser or send POST requests to `/chat` with a JSON body containing `message` and optional `history`.
2. **View Orders**: Access the orders dashboard via the `/dashboard` route or retrieve orders via the `/orders` API endpoint.
3. **Update Order Status**: Send a POST request to `/orders/<order_id>/status` with a JSON body containing the new `status`.

## Project Structure
```
Byte-Restaurant-Chatbot/
├── app.py
├── menu.json
├── orders.json
├── templates/
│   ├── index.html
│   └── dashboard.html
└── .env
```

## License
This project is licensed under the [MIT License](LICENSE).
```
