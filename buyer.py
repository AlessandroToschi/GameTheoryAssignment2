import numpy as np
from enum import IntEnum
from time import sleep

COMMON_VALUE = 100
STANDARD_DEVIATION = 20.0

class OfferResult(IntEnum):
    RAISE = 1
    LEAVE = 2

class Distribution(IntEnum):
    GAUSSIAN = 1
    UNIFORM = 2

class Buyer(object):
    def __init__(self, ID, common_value=100, distribution=Distribution.GAUSSIAN):
        if distribution == Distribution.GAUSSIAN:
            self.__value = round(common_value + np.random.normal(loc=0, scale=STANDARD_DEVIATION))
        elif distribution == Distribution.UNIFORM:
            self.__value = round(common_value + np.random.uniform(-STANDARD_DEVIATION, STANDARD_DEVIATION + 1.0))
        else:
            self.__value = round(common_value)
        self.__ID = ID
    
    def raise_offer(self, current_value):
        sleep(float(np.random.randint(50, 300)) / 1000.0)
        if current_value < self.__value:
            return (OfferResult.RAISE, current_value + 1)
        else:
            return (OfferResult.LEAVE, 0)

    value = property(lambda self: self.__value)
    ID = property(lambda self: self.__ID)


if __name__ == "__main__":
    x = [Buyer(i + 1).value for i in range(10)]
    print(x)
    print(len(set(x)))