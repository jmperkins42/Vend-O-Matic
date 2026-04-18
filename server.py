import http.server
import json

# global variables to keep up with vending machine state
coins = 0
inventory = [5,5,5]

# HTTP request handler for the vending machine server that implements the required API endpoints
class Handler(http.server.BaseHTTPRequestHandler):      

    # endpoint to get the quantity of each item in the vending machine, or the quantity of a specific item if an id is provided
    def do_GET (self):
        # reference to global variable inventory
        global inventory
        # base inventory endpoint returns the quantity of each item in the vending machine as a JSON array
        if self.path == '/inventory':
            # converts inventory list to JSON and encodes it as bytes
            encoded_body = json.dumps(inventory).encode()
            # sends http status of 200 OK
            self.send_response(200) 
            # sends header indicating content type (json) and content length in bytes
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', len(encoded_body))
            # sends blank line to indicate end of headers
            self.end_headers()
            # writes the encoded body to the response body
            self.wfile.write(encoded_body) 

        # alternate inventory endpoint returns the quantity of a specific item in the vending machine as a JSON object with a single key "quantity"
        elif self.path.startswith('/inventory/'):
            try:
                # gets id from path and trys to convert it to an integer
                id = int(self.path.split('/')[-1])
            except ValueError:
                # edge case: if the id is not a valid integer, return a 400 Bad Request response
                self.send_response(400)
                self.end_headers()
                return
            if id < 0 or id >= len(inventory):
                # edge case: if the id is out of bounds, return a 400 Bad Request response
                self.send_response(400)
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
            # edge case: if the path is not recognized, return a 400 Bad Request response
            self.send_response(400)
            self.end_headers()
    
    # endpoint to add coins to the vending machine, or to purchase an item if an id is provided in the path and the request body contains a coin value of 2 or more
    def do_PUT(self):
        # reference to global variables
        global coins
        global inventory
        # base path for adding coins
        if self.path == '/':
            # gets the content length from the request headers, defaulting to 0 if not provided
            content_length = int(self.headers.get('Content-Length', 0))
            # edge case: if the content length is 0 (no request body), return a 400 Bad Request response
            if content_length == 0:
                self.send_response(400)
                self.end_headers()
                return
            
            # reads the request body and parses it as JSON to get the coin value, then adds it to the total coins
            # rfile.read(content_length) reads the specified number of bytes from the request body and returns it as a bytes object, 
            # which is then decoded to a string by json.loads
            body = json.loads(self.rfile.read(content_length))
            # edge case: if the coin value is not 1, return a 400 Bad Request response
            # this is because the vending machine only accepts 1 coin at a time
            if body['coin'] != 1:
                self.send_response(400)
                self.end_headers()
                return
            coins += body['coin']

            self.send_response(204)
            self.send_header('Content-Type', 'application/json')
            # sends the current number of coins as a custom header "X-Coins" in the response
            self.send_header('X-Coins', str(coins))
            self.end_headers()
        # alternate path for purchasing an item from the vending machine
        elif self.path.startswith('/inventory/'):
            try:
                # gets id from path and trys to convert it to an integer
                id = int(self.path.split('/')[-1])
            except ValueError:
                # edge case: if the id is not a valid integer, return a 400 Bad Request response
                self.send_response(400)
                self.end_headers()
                return
            if id < 0 or id >= len(inventory):
                # edge case: if the id is out of bounds, return a 400 Bad Request response
                self.send_response(400)
                self.end_headers()
                return
            if inventory[id] <= 0:
                # required edge case: if the item is out of stock, return a 404 Not Found response with the current number of coins in the "X-Coins" header
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                # sends the current number of coins as a custom header "X-Coins" in the response
                self.send_header('X-Coins', str(coins))
                self.end_headers()
                return
            if coins < 2:
                # required edge case: if the user does not have enough coins to purchase the item, return a 403 Forbidden response with the current number of coins in the "X-Coins" header
                self.send_response(403)
                self.send_header('Content-Type', 'application/json')
                # sends the current number of coins as a custom header "X-Coins" in the response
                self.send_header('X-Coins', str(coins))
                self.end_headers()
                return
            # if the purchase is successful, return a 200 OK response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            # sends the number of coins to be returned after purchase
            self.send_header('X-Coins', str(coins-2))
            # sends the current inventory of the purchased item after purchase
            self.send_header('X-Inventory', str(inventory[id]-1))
            self.end_headers()
            # update coins to reflect purchase and coins returned to user
            coins = 0
            # update inventory to reflect purchase
            inventory[id] -= 1
            
        else:
            # edge case: if the path is not recognized, return a 404 Not Found response
            self.send_response(404)
            self.end_headers()

    # endpoint to reset the number of coins in the vending machine to 0
    def do_DELETE(self):
        # reference to global variable coins
        global coins

        self.send_response(204)
        self.send_header('Content-Type', 'application/json')
        # sends the number of coins to be returned as a custom header "X-Coins" in the response
        self.send_header('X-Coins', str(coins))
        self.end_headers()
        # resets the number of coins to 0 after returning them to the user
        coins = 0
            
# starts the HTTP server on localhost at port 8080 using the Handler class to handle incoming requests
if __name__ == '__main__':
    print('Server started on http://localhost:8080')
    print('awaiting requests...')
    http.server.HTTPServer(('localhost', 8080), Handler).serve_forever()
    

