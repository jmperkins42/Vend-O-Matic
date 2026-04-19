from flask import Flask, jsonify, request
from vendlogic import VendingMachine
app = Flask(__name__)
vending_machine = VendingMachine()

# endpoint to insert a coin
@app.route('/', methods=['PUT'])
def insert_coin():
    # gets the req body as JSON
    body = request.get_json()
    # edge case: req body is missing or has invalid value
    if not vending_machine.insert_coin(body['coin']):
        return '', 400
    # send sucessful response
    response = app.make_response(('', 204))
    # send current coins in custom header "X-Coins"
    response.headers['X-Coins'] = str(vending_machine.get_coins())
    return response

@app.route('/', methods=['DELETE'])
def return_coins():
    # send successful response with current coins in custom header "X-Coins"
    response = app.make_response(('', 204))
    response.headers['X-Coins'] = str(vending_machine.get_coins())
    # reset coins to 0 after returning them to the user
    vending_machine.return_coins()
    return response

@app.route('/inventory', methods=['GET'])
def get_inventory():
    # send successful response with inventory as JSON array in the response body
    return jsonify(vending_machine.get_inventory()), 200

@app.route('/inventory/<int:id>', methods=['GET'])
def get_item_quantity(id):
    quantity = vending_machine.get_item_quantity(id)
    # edge case: if the id is out of bounds, return a 400 Bad Request response
    if quantity == -1:
        return '', 400
    # send successful response with quantity as JSON in the response body
    return jsonify(quantity), 200

@app.route('/inventory/<int:id>', methods=['PUT'])
def purchase_item(id):
    num_vended = 0
    result = vending_machine.purchase_item(id)
    # edge case: if the id is out of bounds, return a 400 Bad Request response
    if result == 'OUT_OF_BOUNDS':
        return '', 400
    # edge case: if the item is out of stock,
    # return a 404 Not Found response with the current number of coins in the "X-Coins" header
    if result == 'OUT_OF_STOCK':
        response = app.make_response(('', 404))
        response.headers['X-Coins'] = str(vending_machine.get_coins())
        return response
    # edge case: if the user does not have enough coins to purchase the item,
    # return a 403 Forbidden response with the current number of coins in the "X-Coins" header
    if result == 'INSUFFICIENT_COINS':
        response = app.make_response(('', 403))
        response.headers['X-Coins'] = str(vending_machine.get_coins())
        return response
    # if the purchase is successful, return a 200 OK response 
    response = app.make_response(('', 200))
    # respond with coins remaining after purchase
    response.headers['X-Coins'] = str(vending_machine.get_coins())
    # respond with current inventory of purchased item after purchase
    response.headers['X-Inventory-Remaining'] = str(vending_machine.get_item_quantity(id))
    num_vended += 1
    response.body = {"quantity": num_vended}
    vending_machine.return_coins()  # return coins after purchase
    return response
    
# run the Flask app on port 8080    
if __name__ == '__main__':
    app.run(port=8080)
