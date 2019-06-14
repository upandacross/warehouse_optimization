from Warehouse.Inventory import Inventory

class Order:
    """
    Order contains order_lines which contain order_items
    
    Assumptions:
        It is permissable to add items to order that are not in Inventory
"""

    from collections import namedtuple
    order_item = namedtuple('order_item', ('line_no', 'item_no', 'qty', 'status'))

    __last_order_no = 0
    
    __inventory = Inventory()
    
    
    @classmethod
    def clear(cls):
        '''
        clear needed to keep unit tests independent
'''
        cls.__last_order_no = 0
        pass # for debugging
    
    @classmethod
    def last_order_no(cls):
        return cls.__last_order_no


    def __init__(self):
        Order.__last_order_no += 1
        self.__order_no__ = 0 + Order.__last_order_no
        self.__lines = []
        self.__last_line_no = 0


    def add_line(self, item_no=None, qty=None):
        assert item_no is not None,\
            'Order Line SBE instantiated with item_no and qty'
        assert isinstance(item_no, int) and item_no > 0,\
            'item_no must be int > 0, is {}'.format(item_no)
        assert isinstance(qty, int) and qty > 0,\
            'qty must be int > 0, is {}'.format(qty)
        
        # not sure I'm ready for this assert:
        # assert item_no in Order.__inventory, 'attemted to add item not in inventory: {}'.format(item_no)
        
        self.__last_line_no += 1
        line = Order.order_item(0 + self.__last_line_no, item_no, qty, 'ordered')
        self.__lines.append((line))
        

    def __repr__(self):
        return('order_no: {}, {} lines'.format(self.__order_no__,
                                                len(self.__lines)))

    @property
    def order_no(self):
        return self.__order_no__

    @order_no.setter
    def order_no(self, *argv):
        assert 0 == 1, 'order number set by init'

    @property
    def lines(self):
        return self.__lines

    @lines.setter
    def lines(self, *args):
        assert 0 == 1, 'order line items set by add_line method'


