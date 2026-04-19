import requests

BASE_URL = 'http://localhost:8080'

def test_insert_coin():
    # insert a valid coin
    response = requests.put(f'{BASE_URL}/', json={'coin': 1})
    assert response.status_code == 204
    # user should have at least 1 coin after an insert
    assert int(response.headers['X-Coins']) > 0
    
    # insert an invalid coin (value not 1)
    response = requests.put(f'{BASE_URL}/', json={'coin': 5})
    assert response.status_code == 400

    # insert an invalid coin with non-integer value (not 1)
    response = requests.put(f'{BASE_URL}/', json={'coin': 'one'})
    assert response.status_code == 400

    # insert a coin with no body
    response = requests.put(f'{BASE_URL}/', headers={'Content-Type': 'application/json'})
    assert response.status_code == 400

def test_return_coins():
    # clear any existing coins by returning them
    requests.delete(f'{BASE_URL}/')
    # insert a coin first
    requests.put(f'{BASE_URL}/', json={'coin': 1})
    
    # return coins
    response = requests.delete(f'{BASE_URL}/')
    assert response.status_code == 204
    # should return the number of coins that were in the machine, which is 1
    assert int(response.headers['X-Coins']) == 1

def test_get_inventory():
    # gets total inventory of all items in the vending machine
    response = requests.get(f'{BASE_URL}/inventory')
    assert response.status_code == 200
    inventory = response.json()
    # inventory should be a list of 3 items (since we have 3 items in our vending machine)
    assert isinstance(inventory, list)
    assert len(inventory) == 3

def test_get_item_quantity():
    # valid item id
    response = requests.get(f'{BASE_URL}/inventory/0')
    assert response.status_code == 200
    # the quantity should be an integer representing how many of that item are left in the vending machine
    quantity = response.json()
    assert isinstance(quantity, int)

    # invalid item id (out of bounds)
    response = requests.get(f'{BASE_URL}/inventory/10')
    assert response.status_code == 400

def test_purchase_item():
    # insert coins first
    requests.put(f'{BASE_URL}/', json={'coin': 1})
    requests.put(f'{BASE_URL}/', json={'coin': 1})
    
    # valid purchase
    response = requests.put(f'{BASE_URL}/inventory/0')
    assert response.status_code == 200
    # the purchase uses all coins, so there should be 0 coins left after the purchase
    assert int(response.headers['X-Coins']) == 0
    # the inventory remaining should be a non-negative integer
    assert int(response.headers['X-Inventory-Remaining']) >= 0
    # the response body should indicate that 1 item was dispensed
    assert response.json() == {"quantity": 1}
    
    # invalid purchase (not enough coins)
    response = requests.put(f'{BASE_URL}/inventory/0')
    # response code should be 403 Forbidden due to insufficient coins
    assert response.status_code == 403
    # the user would have 0 or 1 coins left over
    assert int(response.headers['X-Coins']) < 2

    # invalid purchase (invalid item id)
    response = requests.put(f'{BASE_URL}/inventory/10')
    # response code should be 400 Bad Request due to invalid item id
    assert response.status_code == 400

    # invalid purchase (out of stock)
    # we must empty the inventory of an item first before we can test this case
    # repeat 5 times since the intitial inventory of each item is 5
    for _ in range(5):
        requests.put(f'{BASE_URL}/', json={'coin': 1})
        requests.put(f'{BASE_URL}/', json={'coin': 1})
        requests.put(f'{BASE_URL}/inventory/1')
    # with the inventory now empty, we can test the out of stock case
    response = requests.put(f'{BASE_URL}/inventory/1')
    # response code should be 404 Not Found due to item being out of stock
    assert response.status_code == 404
    # the user would have 0 or 1 coins left over
    assert int(response.headers['X-Coins']) < 2  

