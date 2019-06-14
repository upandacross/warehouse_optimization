from _collections import defaultdict
from functools import total_ordering
import numpy

class Bin:
    
    __bin_locations = defaultdict(lambda: None) # Bin.__bin_location[location] = Bin
    
    
    @classmethod
    def clear(cls):
        cls.__bin_locations = defaultdict(lambda: None) # Bin.__bin_location[location] = Bin
        
        
    @classmethod
    def get_bin_by_location(cls, location):
        assert isinstance(location, Bin.Bin_Location), 'get_bin_by_location to be called with Bin.Bin_Location instance'
        return Bin.__bin_locations[location]
    
    
    @classmethod
    def drop_bin(cls, location):
        assert isinstance(location, Bin.Bin_Location), 'drop_bin to be called with Bin.Bin_Location instance'
        try:
            del Bin.__bin_locations[location]
        except:
            pass
    

    @classmethod    
    def bin_locations(cls):
        return len(cls.__bin_locations)



    # start internal class Bin_location
    @total_ordering
    class Bin_Location:
        
        __name__ = 'Bin_Llocation'
        
        def __init__(self, rack_no, side, bin_no):
            assert isinstance(rack_no, int) and rack_no > 0, 'rack_no must be int > 0'
            assert isinstance(side, str) and side in ['a', 'b'], 'side must be str in ["a", "b"]'
            assert isinstance(bin_no, int) and bin_no >= 0, 'bin_no must be int >= 0'
            self.__rack = rack_no
            self.__side = side
            self.__bin_no = bin_no
            
        
        def __lt__(self, other):
            assert isinstance(other, type(self))
            return (self.rack, self.side, self.bin_no) < (other.rack, other.side, other.bin_no)
        
        
        def __eq__(self, other):
            assert isinstance(other, type(self))
            return (self.rack, self.side, self.bin_no) == (other.rack, other.side, other.bin_no)
        
        
        def __hash__(self):
            return hash('{:02d}{:1s}{:02d}'.format(self.rack, self.side, self.bin_no))
        
        
        def __repr__(self):
            return 'rack: {}, side: {}, bin_no: {}'.format(self.rack, self.side, self.bin_no)


        @property
        def rack(self):
            return self.__rack
        
        @rack.setter 
        def rack(self, args=None):
            raise RuntimeError('rack attribute set by init')
        
        @property
        def side(self):
            return self.__side
        
        @side.setter 
        def side(self, args=None):
            raise RuntimeError('side attribute set by init')
        
        @property
        def bin_no(self):
            return self.__bin_no
                
        @bin_no.setter 
        def bin_no(self, args=None):
            raise RuntimeError('bin_no attribute set by init')

        # end of class Bin_Location
        

    # start methods for class Bin
    def __init__(self, rack_no, side, bin_no,
                 item=None, count=0):
        assert isinstance(rack_no, int) and rack_no > 0,\
            'rack_no must be int > 0'
        assert isinstance(bin_no, int) and bin_no >= 0,\
            'bin_no must be int >= 0'
        assert isinstance(side, str) and side in list('ab'),\
            'side must be int > 0'
        assert isinstance(bin_no, int) and bin_no >= 0,\
            'bin_no must be int >= 0'
        if item is not None:
            assert isinstance(item, int) and item > 0,\
                'item must be int > 0'
        assert isinstance(count, int) and count >= 0,\
            'count must be int >= 0'

        self.__rack_no = rack_no
        self.__bin_side = side # a or b
        self.__bin_no = bin_no
        self.__location = Bin.Bin_Location(rack_no, side, bin_no)
        lat = bin_no + 1 if bin_no > 0 else 0 # dock is bin_no 0 at lat 0
        long = (rack_no * 3) - 2 if side == 'a' else (rack_no * 3) - 1
        self.__lat_long = numpy.array([lat, long])
        self.__item = item
        self.__count = count

        Bin.__bin_locations[self.location] = self

    def stock_bin(self, item_no, item_count):
        '''
        add item_count of items in bin
        if item_no is != bin.item, replace bin.item, bin.count with item_no, item_count (not added to)
        SBE called from Inventory class where this bin instance lives
'''
        assert isinstance(item_no, int) and item_no > 0, 'item_no must be int > 0'
        assert isinstance(item_count, int), 'item_count must be int, can be +/-'
        self.__count = item_count if self.item != item_no else self.__count + item_count
        if self.__count < 0:
            self.__count = 0
        self.__item = item_no


    def __lt__(self, other):
        assert isinstance(other, type(self))
        return (self.location) < (other.location)
    
    
    def __repr__(self):
        rtn =  'rack_no: {}, bin_no: {}, bin_side: {} '\
                .format(self.__rack_no, self.__bin_no, self.__bin_side)
        rtn += 'lat: {}, long: {}, item: {}, count: {} '\
                 .format(self.__lat_long[0], self.__lat_long[1],
                         self.__item, self.__count)

        return rtn

    
    @property
    def rack_no(self):
        return self.__rack_no

    @rack_no.setter
    def rack_no(self, *arg):
        raise RuntimeError('rack number set when added to rack')

    @property
    def bin_no(self):
        return self.__bin_no

    @bin_no.setter
    def bin_no(self, *arg):
        raise RuntimeError('bin number set when added to rack')

    @property
    def bin_side(self):
        return self.__bin_side

    @bin_side.setter
    def bin_side(self, *arg):
        raise RuntimeError('bin side set when added to rack')

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, *arg):
        raise RuntimeError('bin location set by init')

    @property
    def lat_long(self):
        return self.__lat_long

    @property
    def lat(self):
        return self.__lat_long[0]

    @lat.setter
    def lat(self, *args):
        raise RuntimeError('lat set when added to rack ')

    @property
    def long(self):
        return self.__lat_long[1]

    @long.setter
    def long(self, *args):
        raise RuntimeError('long set when added to rack ')

    @property
    def item(self):
        return self.__item

    @item.setter
    def item(self, *args):
        raise RuntimeError("item and count set by instance's stock_bin method")

    @property
    def count(self):
        return self.__count

    @count.setter
    def count(self, args):
        raise RuntimeError("item and count set by instance's stock_bin method")

