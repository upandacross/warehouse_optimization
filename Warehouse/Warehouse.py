from Warehouse.Bin import Bin
from Warehouse.Inventory import Inventory
from Warehouse.Rack import Rack

class Warehouse:
    '''
A warehouse has inventory, racks, and a dock. Racks contain bins. Warehouse assigns a
lat / long to bins to allow computation of distance traveled from one bin to another.

The init args are:
    racks, int > 0 for how many racks are in warehouse
    bins, int > 0 for how many bins are in each rack
    
Assumptions:
    coordinates of warehouse's lower-left corner is (0, 0)
    dock is single location with lat == 0 and long centered WRT number of racks 
    bins_a[1] and bins_[1] are for bin 1
    shortest route from one bin to another goes through the rack end (cap) closest to the destination bin
'''

    __instance = None
    __inventory = Inventory()

    @classmethod
    def clear(cls):
        Inventory.clear()

    @classmethod
    def reset(cls, racks, bins):
        cls.__instance = None                      # clear __instance so __init__ doen't fail
        cls.__instance = Warehouse(racks=racks, bins=bins)    # Now the initialization can be called
        Inventory.clear()
        return cls.__instance

    def __init__(self, racks=None, bins=None):

        if type(self).__instance is None:
            # Initialization
            assert isinstance(racks, int) and racks > 0, \
                'number of racks must be int > 0'
            assert isinstance(bins, int) and bins > 0, \
                'number of bins must be int > 0'

            type(self).__instance = self

            dock_rack = round((racks / 2) + .1) # friggin "Banker's rounding!
            self.__dock = Bin(rack_no=dock_rack, side='a', bin_no=0)
            self.__dock.nearest_cap = self.__dock
            self.__dock.nearest_cap_distance = 0
            self.__racks_bins = (racks, bins)
            self.__racks = [Rack(rack_no = x, bin_count=bins) 
                            for x in range(1, racks + 1, 1)]
            self.__bins = [list(r.bins_a.values()) + list(r.bins_b.values())
                           for r in self.__racks][0]
        else:
            self.__dict__ = Warehouse.__instance.__dict__

    def __repr__(self):
        return '''racks: {}, dock (lat, long): {}, inventory has {:,d} item_no, {:,d} quantities'''\
                .format(len(self.__racks), (self.__dock.lat, self.__dock.long),
                        len(Warehouse.__inventory.stock),
                        sum(b.count for b in Bin.bin_locations.values()))
    

    @classmethod
    def update_stock(cls, item_no, qty, location):
        '''
        Use Inventory.update_stock if called w/o location or with location == None so qty will be divided among bins holding item
        Use Inventory.update_bin if called with location
'''
        assert isinstance(location, Bin.Bin_Location), 'update_stock SBE called with nlocation = None or instance of Bin_Location'
        cls.__inventory.update_bin(location, item_no, qty)


    def get_stock_qty(self, item_no):
        return Warehouse.__inventory.get_stock_qty(item_no)


    @property
    def racks(self):
        return self.__racks

    @racks.setter
    def racks(self, *args):
        assert 1 == 0, 'racks attribute set by init only'
        return

    @property
    def racks_bins(self):
        return self.__racks_bins

    @racks_bins.setter
    def racks_bins(self, args):
        assert 0 == 1, 'number of racks and bins fixed at instantiation'

    @property
    def dock(self):
        return self.__dock

    @dock.setter
    def dock(self, *arg):
        assert 1 == 0, 'dock lat/long set by init only'

    @property
    def stock(self):
        return Warehouse.__inventory.stock
    
    @property
    def inventory(self):
        return self.__inventory
    
    @inventory.setter
    def inventory(self, args):
        raise RuntimeError('inventory attribute set by init')
