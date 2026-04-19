class VendingMachine:
    def __init__(self):
        self.coins = 0
        self.inventory = [5, 5, 5]  # initial inventory for each item

    def get_coins(self):
        # return the current number of coins
        return self.coins
        
    def insert_coin(self, coin):
        # edge case: if the coin is not valid, return False
        if coin != 1:
            return False
        # add the coin value to the total coins
        self.coins += coin
        return True
    
    def return_coins(self):
        # return the current coins and reset to 0
        coins_to_return = self.coins
        self.coins = 0
        return coins_to_return
    
    def get_inventory(self):
        # return the current inventory
        return self.inventory
    
    def get_item_quantity(self, id):
        # edge case: if the id is out of bounds, return -1
        if id < 0 or id >= len(self.inventory):
            return -1
        # return the quantity of the specified item
        return self.inventory[id]

    def purchase_item(self, id):
        # edge case: id is out of bounds
        if id < 0 or id >= len(self.inventory):
            return 'OUT_OF_BOUNDS', None
        # edge case: item is out of stock
        if self.inventory[id] <= 0:
            return 'OUT_OF_STOCK', None
        # edge case: user does not have enough coins
        if self.coins < 2:
            return 'INSUFFICIENT_COINS', None
        # process the purchase
        self.coins -= 2  # cost of the item is 2 coins
        dispensed_coins = self.return_coins()  # return any remaining coins to the user
        self.inventory[id] -= 1  # reduce inventory by 1
        # return 'SUCCESS' to indicate a successful purchase
        return 'SUCCESS', dispensed_coins