from collections import defaultdict
from Warehouse.Bin import Bin
from Warehouse.Inventory import Inventory
import numpy as np

class Rack:
    '''
    Instantiation:
        Rack(rack_no = int > 0, bin_count = int > 0)
        
    Method Notes:
        bins_a and bins_b are dicts of bins and accessed by bin_no as key
'''

    _inventory = Inventory()


    def __init__(self, rack_no, bin_count):
        assert isinstance(rack_no, int) and rack_no > 0,\
            'rack_no must be int > 0'
        assert isinstance(bin_count, int) and bin_count > 0,\
            'bin_count must be int > 0'
        self.__rack_no = rack_no
        self.__bin_count = bin_count
        self.__top_cap_lat = bin_count + 2 # always with fixed # of bins
        self.__bottom_cap_lat = 1 # always
        self.__bins_a = dict() # access via bin_no
        self.__bins_b = dict() # access via bin_no
        
        for bin_no in range(1, bin_count + 1, 1):
            self.__bins_a[bin_no] = Bin(rack_no=self.rack_no, side='a', bin_no=bin_no)
            self.__bins_b[bin_no] = Bin(rack_no=self.rack_no, side='b', bin_no=bin_no)
    
    def __repr__(self):
            return '''rack_no {}, bin_count: {}, \
top_cap_lat: {:2d}, bottom_cap_lat: {}'''\
                    .format(self.__rack_no, self.__bin_count, self.__top_cap_lat,
                            self.__bottom_cap_lat)


    def nearest_cap(self, b):
        (dist_bottom, dist_top) = (b.bin_no, self.bin_count - b.bin_no + 1)
        if dist_bottom > dist_top:
            bin_no = self.bin_count + 1
        else:
            bin_no = 0
        return Bin(rack_no=self.rack_no, side=b.bin_side, bin_no=bin_no)

    
    @property
    def rack_no(self):
        return self.__rack_no
    
    @rack_no.setter
    def rack_no(self, *arg, **varg):
        raise RuntimeError('rack_no is {} and can not be reset'.format(self.rack_no))

    @property
    def bins_a(self):
        return self.__bins_a
    
    @bins_a.setter
    def bins_a(self, *arg):
        raise RuntimeError('setting bin arrays by init')

    @property
    def bins_b(self):
        return self.__bins_b
    
    @bins_b.setter
    def bins_b(self, *arg):
        raise RuntimeError('setting bin arrays by init')

    @property
    def bin_count(self):
        return self.__bin_count
    
    @bin_count.setter
    def bin_count(self, *argv):
        raise RuntimeError('bin_count only gets set when adding bin(s)')
        
    
