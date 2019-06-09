from collections import Iterable
from collections import deque
from numpy.random import shuffle, randint, seed


class CircularQueue:
    '''A class created with an iterable of objects that are to be accessed
sequentially and, when the last object is returned, the next access returns 
the first item. This process continues without end.
'''

    __name__ = 'CircularQueue'

    def __init__(self, items):
        assert isinstance(items, Iterable), 'items argument must be iterable'
        self.__myitems = []
        self.__items = self.prepItems(items)
        
    def prepItems(self, items):
        return [o for o in items]


    @property
    def item(self):
        if self.itemsLen() == 0:
            self.__myitems = deque(self.__items)
        return self.__myitems.popleft()
    
    def itemsLen(self):
        return len(self.__myitems)
    
class RandomizedCircularQueue(CircularQueue):
    '''A subclass of CircularQueue that randomizes order of items before queuing them.
Each instance receives a sequential integer used as a seed for np.random to support 
unit testing.
'''
    __seed = 1
    __name__ = 'RandomizedCircularQueue'
    
    def __init__(self, items):
        self.__myseed = randint(10000)
        self.__seed = RandomizedCircularQueue.__seed
        RandomizedCircularQueue.__seed += 1
        super().__init__(items)
        pass # for debugging


    # override parent method
    def prepItems(self, items):
        seed(self.seed)
        rtn = [o for o in items]
        shuffle(rtn)
        return rtn
        

    @property
    def seed(self):
        return self.__seed
    
