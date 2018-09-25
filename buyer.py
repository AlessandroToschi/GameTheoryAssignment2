import numpy as np
from enum import IntEnum

COMMON_VALUE = 100
STANDARD_DEVIATION = 15.0

class OfferResult(IntEnum):
    RAISE = 1
    LEAVE = 2

class Distribution(IntEnum):
    GAUSSIAN = 1
    UNIFORM = 2

class Buyer(object):
    def __init__(self, common_value=100, distribution=Distribution.GAUSSIAN):
        if distribution == Distribution.GAUSSIAN:
            self.__value = round(common_value + np.random.normal(loc=0, scale=STANDARD_DEVIATION))
        elif distribution == Distribution.UNIFORM:
            self.__value = round(common_value + np.random.uniform(-STANDARD_DEVIATION, STANDARD_DEVIATION + 1.0))
        else:
            self.__value = round(common_value)
    
    def raise_offer(self, current_value):
        if current_value < self.__value:
            return (RAISE, current_value + 1)
        else:
            return (LEAVE, 0)

    value = property(lambda self: self.__value)


if __name__ == "__main__":
    x = [Buyer().value for _ in range(10)]
    print(x)
    print(len(set(x)))