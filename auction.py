import buyer

BUYERS = 10

class Auction(object):
    def __init__(self, reserve_price=0):
        if reserve_price >= 0:
            self.__reserve_price = reserve_price
        else:
            raise ValueError("Reserve price must be greater or equal to zero.")
        self.__buyers = [Buyer() for _ in range(BUYERS)]
    
    def simulate(self):
        NotImplementedError("This method can be called only by specialized children.")
    
    reserve_price = property(lambda self: self.__reserve_price)