import http.server
import json

# global variables to keep up with vending machine state
coins = 0
inventory = [5,5,5]

# HTTP request handler for the vending machine server that implements the required API endpoints
class Handler(http.server.BaseHTTPRequestHandler):      

    # endpoint to get the quantity of each item in the vending machine, or the quantity of a specific item if an id is provided
    def do_GET (self):
        if self.path == '/inventory':
            encoded_body = json.dumps(inventory).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', len(encoded_body))
            self.end_headers()
            self.wfile.write(encoded_body)
        elif self.path.startswith('/inventory/'):
            try:
                id = int(self.path.split('/')[-1])
            except ValueError:
                self.send_response(404)
                self.end_headers()
                return
            if id < 0 or id >= len(inventory):
                self.send_response(404)
                self.end_headers()
                return
            quantity = inventory[id]
            encoded_body = json.dumps(quantity).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', len(encoded_body))
            self.end_headers()
            self.wfile.write(encoded_body)
        else:
            self.send_response(404)
            self.end_headers()
    
    # endpoint to add coins to the vending machine, or to purchase an item if an id is provided in the path and the request body contains a coin value of 2 or more

    def do_PUT(self):
        global coins
        if self.path == '/':
            content_length = int(self.headers['Content-Length'])
            body = json.loads(self.rfile.read(content_length))
            coins += body['coin']

            self.send_response(204)
            self.send_header('Content-Type', 'application/json')
            self.send_header('X-Coins', str(coins))
            self.end_headers()
        elif self.path.startswith('/inventory/'):
            try:
                id = int(self.path.split('/')[-1])
            except ValueError:
                self.send_response(404)
                self.end_headers()
                return
            if id < 0 or id >= len(inventory):
                self.send_response(404)
                self.end_headers()
                return
            if inventory[id] <= 0:
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.send_header('X-Coins', str(coins))
                self.end_headers()
                return
            if coins < 2:
                self.send_response(403)
                self.send_header('Content-Type', 'application/json')
                self.send_header('X-Coins', str(coins))
                self.end_headers()
                return
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('X-Coins', str(coins-2))
            self.send_header('X-Inventory', str(inventory[id]-1))
            self.end_headers()
            coins -= 2
            inventory[id] -= 1
            
        else:
            self.send_response(404)
            self.end_headers()

    # endpoint to reset the number of coins in the vending machine to 0
    def do_DELETE(self):
        global coins

        self.send_response(204)
        self.send_header('Content-Type', 'application/json')
        self.send_header('X-Coins', str(coins))
        self.end_headers()
        coins = 0
            
            
if __name__ == '__main__':
    http.server.HTTPServer(('localhost', 8080), Handler).serve_forever()

