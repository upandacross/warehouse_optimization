class genStock:
    def __init__(self, items_len):
        self.__mystock = []
        self.__items = [s for s in range(items_len + 1)]
        self.__myseed = np.random.randint(10000)
        
    def getStock(self):
        if len(self.__mystock) == 0:
            np.random.seed(self.__myseed)
            self.__mystock = np.random.choice(self.__items, size=len(self.__items),
                                              replace=False)
            self.__mystock = deque(self.__mystock)
        return self.__mystock.pop()
    
    @property
    def items(self):
        return self.__items
    
    @property
    def mystock(self):
        return self.__mystock
    
    @mystock.deleter
    def items(self):
        np.random.seed(self.__myseed)
        self.__mystock = np.random.choice(self.__items, size=len(self.__items),
                                          replace=False)
    
            
