from buyer import Buyer, Distribution, OfferResult
import threading

BUYERS = 10

class Auction(object):
    def __init__(self, reserve_price=0):
        if reserve_price >= 0:
            self.__reserve_price = reserve_price
        else:
            raise ValueError("Reserve price must be greater or equal to zero.")
        self._buyers = self.__create_buyers()
        self._lock = threading.Lock()
    
    def __create_buyers(self):
        buyers = [Buyer(ID + 1) for ID in range(BUYERS)]
        while(len(set([x.value for x in buyers])) < BUYERS):
            buyers = [Buyer(ID + 1) for ID in range(BUYERS)]
        return buyers
    
    def simulate(self):
        NotImplementedError("This method can be called only by specialized children.")
    
    reserve_price = property(lambda self: self.__reserve_price)

class EnglishAuction(Auction):
    def __init__(self, reserve_price=0):
        Auction.__init__(self, reserve_price=reserve_price)
    
    def offer_pooling(self, queue, current_value, buyer):
        result, value = buyer.raise_offer(current_value)
        if result == OfferResult.RAISE:
            with self._lock:
                queue.append((buyer.ID, result, value))

    def simulate(self):
        stop = False
        current_offer = 0
        results = []
        threads = []
        max_offering = 0
        max_buyer_offering = ""
        print("English auction is ready to start, with a starting offer of 0.")
        print("{} buyers are attending.".format(BUYERS))
        while(stop == False):
            results.clear()
            threads.clear()
            print("Who offers " + str(current_offer + 1) + "?")
            for buyer in self._buyers:
                buyer_thread = threading.Thread(target=self.offer_pooling, args=(results, current_offer, buyer))
                threads.append(buyer_thread)
                buyer_thread.start()
            for thread in threads:
                thread.join()
            if len(results) == 0:
                if max_offering >= self.reserve_price:
                    print("Player {} has won the auction with an offer of {}!".format(max_buyer_offering, max_offering))
                else:
                    print("The trade can't be done, the max offer is {} but the reserve price is {}".format(max_offering, self.reserve_price))
                stop = True
            else:
                if max_buyer_offering == results[0][0] and len(results) == 1:
                    if max_offering >= self.reserve_price:
                        print("Player {} has won the auction with an offer of {}!".format(max_buyer_offering, max_offering))
                    else:
                        print("The trade can't be done, the max offer is {} but the reserve price is {}".format(max_offering, self.reserve_price))
                    stop = True
                    continue
                print("Player {} has offered {}".format(results[0][0], results[0][2]))
                max_offering = results[0][2]
                max_buyer_offering = results[0][0]
                current_offer = max_offering
            print("\n")
        for buyer in self._buyers:
            print("{} {}".format(buyer.ID, buyer.value))
            
class DutchAuction(Auction):
    def __init__(self, reserve_price=0):
        Auction.__init__(self, reserve_price=reserve_price)
        
    def simulate(self):
        max_value = max([x.value for x in self._buyers])
        current_value = max_value + 20
        stop = False
        print("Dutch auction is ready to start, with a starting offer of {}.".format(current_value))
        print("10 buyers are attending.")
        while(stop == False):
            print("Who is offering {}?".format(current_value))
            if max_value == current_value:
                if max_value >= self.reserve_price:
                    ID = [x.ID for x in self._buyers if x.value == max_value][0]
                    print("Player {} has won the auction with an offer of {}!".format(ID, current_value))
                else:
                    print("The trade can't be done, the max offer is {} but the reserve price is {}".format(current_value, self.reserve_price))
                stop = True
            else:
                current_value -= 1

class SealedBidFirstPriceAuction(Auction):
    def __init__(self, reserve_price=0):
        Auction.__init__(self, reserve_price=reserve_price)

    def simulate(self):
        max_value = max([x.value for x in self._buyers])
        print("Sealed-Bid First Price auction is ready to start, please prepare your bids.")
        print("{} buyers are attending.".format(BUYERS))
        [print("{} {}".format(x.ID, x.value)) for x in self._buyers ]
        if max_value >= self.reserve_price:
            ID = [x.ID for x in self._buyers if x.value == max_value][0]
            print("Player {} has won the auction with an offer of {}!".format(ID, max_value))
        else:
            print("The trade can't be done, the max offer is {} but the reserve price is {}".format(max_value, self.reserve_price))

class VickreyAuction(Auction):
    def __init__(self, reserve_price=0):
        Auction.__init__(self, reserve_price=reserve_price)

    def simulate(self):
        max_value = max([x.value for x in self._buyers])
        second_max_value = max([x.value for x in self._buyers if x.value != max_value])
        print("Vickrey auction is ready to start, please prepare your bids.")
        print("{} buyers are attending.".format(BUYERS))
        [print("{} {}".format(x.ID, x.value)) for x in self._buyers ]
        if max_value >= self.reserve_price:
            if  second_max_value >= self.reserve_price:
                ID = [x.ID for x in self._buyers if x.value == max_value][0]
                print("Player {} has won the auction with an offer of {}! Price to pay: {}".format(ID, max_value, second_max_value))
            else: 
                print("The trade can't be done, the price to pay is {} but the reserve price is {}".format(second_max_value, self.reserve_price))
        else:
            print("The trade can't be done, the max offer is {} but the reserve price is {}".format(max_value, self.reserve_price))


if __name__ == "__main__":
    ea = EnglishAuction(reserve_price=50)
    #ea.simulate()

    da = DutchAuction()
    #da.simulate()

    sb = SealedBidFirstPriceAuction()
    #sb.simulate()

    vik = VickreyAuction()
    vik.simulate()