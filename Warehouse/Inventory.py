from collections import defaultdict

from Warehouse.Bin import Bin
    
class Inventory:
    '''
A singleton class, Inventory serves much like a factory using closure to return instances that
refer to a single hidden class within of which there is a single instance. References to the
hidden attributes are accomplished by a custom __getattr__ method. Updates to the
hidden attributes are accomplished by a custom __setattr__ method.

There are no arguments to __init__.

Assumptions:
    each bin location contains only one item and, therefore each location occurs once in the inventory
'''

    __stock = defaultdict(set) # Inventory.__stock[item] = locations that can be bassed to Bin.get_bin_by_location(location)

    def __init__(self):
        pass
    
        
    @classmethod
    def clear(cls):
        cls.__stock = defaultdict(set) # cls.__stock[item] = location
        
    
    @classmethod
    def update_bin(cls, location, item_no, qty):
        '''
        add or subtract qty in bin at location
        if item being updated != item in bin at location, bin.__item, bin.__count = item_no, qty
        
        Assumption:
            if called to update bin with new item, then all inbins with old item will be replaced everywhere. 
                Use Bin.__stock_bin to update individual bins but be sure to only update bin instances that live in Inventory
'''
        assert isinstance(location, Bin.Bin_Location), 'location SBE instance of Bin.Bin_Location, is {}'.format(location.__class__)
        assert isinstance(qty, int), 'qty mst be int'
        assert isinstance(item_no, int) and item_no > 0, 'item_no must be int > 0'
        
        b = Bin.get_bin_by_location(location)
        if b is None:
            b = Bin(rack_no=location.rack, side=location.side, bin_no=location.bin_no)
        if b.item != item_no:
            try:
                cls.__stock[item_no].discard(location)
            except:
                pass
        b.stock_bin(item_no, qty)
        cls.__stock[item_no].add(b.location)
        pass
    @classmethod
    def get_location_bin(cls, location):
        assert isinstance(location, Bin.Bin_Location), 'location must be an Bin.Bin_Location, is {}'.format(location)
        b = Bin.get_bin_by_location(location)
        return b


    @classmethod
    def get_stock_qty(cls, item_no=None, location=None):
        '''
        First, if location is not None return bin.count @ location, otherwise check item_no is not None
        If item_no is not None, return quantity of item_no at all location.
        If both item_no and location are None or both are Not None, error
'''
        assert item_no is not None or location is not None, 'either item_no or location are not None'
        assert item_no is None or location is None, \
            'either item_no or location are not None, NOT both'
        if location is not None:
            b = Bin.get_bin_by_location(location)
            return (b.item, b.count) # it is caller's responsibility to check b.item == item_no
        
        elif item_no is None or item_no not in cls.__stock: # item_no is not None by assertion above
            return (item_no, 0)
        else:
            return (item_no, sum([Bin.get_bin_by_location(loc).count for loc in cls.__stock[item_no]]))


    def __repr__(self):
        if len(self.stock.values()) > 0:
            qty = sum(
                      [sum(Bin.get_bin_by_location(loc).count for loc in Inventory.__stock[itm]
                           )
                       for itm in Inventory.__stock.keys()
                       ]
                      )
        else:
            qty = 0
        return 'Inventory: {:,d} items, {:,d} total quantity'\
                .format(len(self.stock), qty)


    def __str__(self):
        return Inventory.__repr__(self)


    @property
    def stock(self):
        return type(self).__stock

    @stock.setter
    def stock(self, args):
        raise RuntimeError('stock is maintained in inventory via Bin stocking')
