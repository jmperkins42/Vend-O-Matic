from flask import Flask, jsonify, request
app = Flask(__name__)

# global variables to keep up with vending machine state
coins = 0
inventory = [5,5,5]

# endpoint to insert a coin
@app.route('/', methods=['PUT'])
def insert_coin():
    # reference to global variable coins
    global coins
    # gets the req body as JSON
    body = request.get_json()
    # edge case: req body is missing or has invalid value
    if not body or body.get('coin') != 1:
        return '', 400
    # add the coin value from the req body to the total coins
    coins += body['coin']
    # send sucessful response
    response = app.make_response(('', 204))
    # send current coins in custom header "X-Coins"
    response.headers['X-Coins'] = str(coins)
    return response

@app.route('/', methods=['DELETE'])
def return_coins():
    # reference to global variable coins
    global coins
    # send successful response with current coins in custom header "X-Coins"
    response = app.make_response(('', 204))
    response.headers['X-Coins'] = str(coins)
    # reset coins to 0 after returning them to the user
    coins = 0
    return response

@app.route('/inventory', methods=['GET'])
def get_inventory():
    # send successful response with inventory as JSON array in the response body
    return jsonify(inventory), 200

@app.route('/inventory/<int:id>', methods=['GET'])
def get_item_quantity(id):
    # edge case: if the id is out of bounds, return a 400 Bad Request response
    if id < 0 or id >= len(inventory):
        return '', 400
    # send successful response with quantity as JSON in the response body
    return jsonify(inventory[id]), 200

@app.route('/inventory/<int:id>', methods=['PUT'])
def purchase_item(id):
    # reference to global variables
    global coins
    # edge case: if the id is out of bounds, return a 400 Bad Request response
    if id < 0 or id >= len(inventory):
        return '', 400
    # edge case: if the item is out of stock,
    # return a 404 Not Found response with the current number of coins in the "X-Coins" header
    if inventory[id] <= 0:
        response = app.make_response(('', 404))
        response.headers['X-Coins'] = str(coins)
        return response
    # edge case: if the user does not have enough coins to purchase the item,
    # return a 403 Forbidden response with the current number of coins in the "X-Coins" header
    if coins < 2:
        response = app.make_response(('', 403))
        response.headers['X-Coins'] = str(coins)
        return response
    # if the purchase is successful, return a 200 OK response 
    response.headers['X-Coins'] = str(coins-2)
    # respond with current inventory of purchased item after purchase
    response.headers['X-Inventory'] = str(inventory[id]-1)
    # update coins to reflect purchase and coins returned to user
    coins = 0
    # update inventory to reflect purchase
    inventory[id] -= 1
    return response
    
# run the Flask app on port 8080    
if __name__ == '__main__':
    app.run(port=8080)
