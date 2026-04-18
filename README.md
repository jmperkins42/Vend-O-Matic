# Vending Machine API

A simple vending machine API built with Python and Flask.

## Requirements

- Python 3.6+

## Setup

1. Clone the repository
2. Navigate to the project folder
3. Create and activate a virtual environment:
   
   python -m venv venv

   Mac/Linux:
   source venv/bin/activate
   
   Windows:
   venv\Scripts\activate

4. Install dependencies:
   
   pip install -r requirements.txt

5. Run the server:
   
   python server.py

   Or with auto-reload during development:
   
   flask --app server.py run --port 8080 --debug

The server will start on http://localhost:8080

## Stopping the Server
Press CTRL+C to stop the server, then run `deactivate` to exit the virtual environment.

## Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| PUT | / | Insert a coin |
| DELETE | / | Return all coins |
| GET | /inventory | Get all item quantities |
| GET | /inventory/:id | Get quantity of a specific item |
| PUT | /inventory/:id | Purchase an item |

## Notes

- All requests and responses use `application/json`
- The machine only accepts one quarter at a time `{ "coin": 1 }`
- Items cost 2 quarters each
- Inventory is initialized to 5 of each of 3 items on server start
- Unused coins are returned after a purchase via the `X-Coins` response header