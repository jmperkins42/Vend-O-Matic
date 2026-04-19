import requests

BASE_URL = 'http://localhost:8080'

def test_insert_coin():
    # insert a valid coin
    response = requests.put(f'{BASE_URL}/', json={'coin': 1})
    assert response.status_code == 204
    assert int(response.headers['X-Coins']) > 0
    
    # insert an invalid coin
    response = requests.put(f'{BASE_URL}/', json={'coin': 5})
    assert response.status_code == 400

    #insert an invalid coin with non-integer value
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
    assert int(response.headers['X-Coins']) == 1

def test_get_inventory():
    response = requests.get(f'{BASE_URL}/inventory')
    assert response.status_code == 200
    inventory = response.json()
    assert isinstance(inventory, list)
    assert len(inventory) == 3

def test_get_item_quantity():
    # valid item id
    response = requests.get(f'{BASE_URL}/inventory/0')
    assert response.status_code == 200
    quantity = response.json()
    assert isinstance(quantity, int)

    # invalid item id (out of bounds)
    response = requests.get(f'{BASE_URL}/inventory/10')
    assert response.status_code == 400