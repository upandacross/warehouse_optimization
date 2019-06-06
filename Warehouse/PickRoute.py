'''
Created on May 28, 2019

@author: bren
'''
from collections import OrderedDict
from Warehouse.Bin import Bin
from Warehouse.Inventory import Inventory
from Warehouse.Order import Order
from Warehouse.Warehouse import Warehouse
from builtins import isinstance

class PickRoute:
    '''
    classdocs
    '''
    
    __inventory = Inventory()


    def __init__(self, wh, order):
        '''
        Constructor
        '''
        assert isinstance(wh, Warehouse), 'wh must be instance of Warehouse+'
        assert isinstance(order, Order), 'order must be instance of Order'
        self.__order = order
        self.__order_lines = order.lines
        
        self.__pick_bins = set()
        self.__pick_items = set()
        for l in self.order_lines:
            item_locations = PickRoute.__inventory.stock[l.item_no]
            if item_locations is None:
                # silently ignore items not in inventory
                # but monkey-patch note that item not in inventory
                l.status = 'not in inventory'
            else:
                self.__pick_items.add(l.item_no)
                for item_location in item_locations:
                    self.__pick_bins.add(Bin.get_bin_by_location(item_location))

        self.__wh = wh
        self.__route = OrderedDict()
        self.__route_distance = 0
        
        self.__calc_route()
        


    def __calc_route(self):
        pick_items = self.__pick_items.copy()
        pick_bins = self.__pick_bins.copy()
        
        # first one starts from dock, ends on nearest to first rack, side a, first bin
        to_bin = min(self.__pick_bins)
        from_bin = self.__wh.dock
        self.__route_distance += self.bin_to_bin_distance(from_bin, to_bin)
        self.__route[(from_bin.location, to_bin.location)] = self.__route_distance
        pick_items.remove(to_bin.item)
        pick_bins.remove(to_bin)
        # pick closest to 
        while len(pick_items) > 0:
            from_bin = to_bin
            min_bin_dist = 1e10
            for check_bin in sorted(pick_bins):
                if check_bin.item not in pick_items:
                    continue # already picked this item
                d = self.bin_to_bin_distance(from_bin, check_bin)
                if d < min_bin_dist:
                    min_bin_dist = d 
                    to_bin = check_bin
            if check_bin is not None:
                self.__route_distance += min_bin_dist
                self.__route[(from_bin.location, to_bin.location)] = min_bin_dist
                try:
                    pick_items.remove(to_bin.item)
                except Exception as e:
                    print(e)
                pick_bins.remove(to_bin)
            pass # for debugging
        
        # last step is to dock
        from_bin = to_bin
        to_bin = self.__wh.dock
        self.__route_distance += self.bin_to_bin_distance(from_bin, to_bin)
        self.__route[(from_bin.location, to_bin.location)] = self.__route_distance
        return None
        
        
    def bin_to_bin_distance(self, from_bin, to_bin):
        '''Manhattan distance, not Euclidian
        call with two Bin class instances
'''
        assert isinstance(from_bin, Bin) and isinstance(to_bin, Bin), 'both arguments must be instance of Bin class'
        rack_diff = to_bin.rack_no - from_bin.rack_no
        if (rack_diff == 0 and from_bin.bin_side == to_bin.bin_side) or\
           (rack_diff == 1 and (from_bin.bin_side, to_bin.bin_side) == ('b', 'a')):
            lat_distance = abs(from_bin.lat - to_bin.lat)
            #from_long = from_bin.long if from_bin.bin_side == 'b' else from_bin.long - 1
            #to_long = to_bin.long if to_bin.bin_side == 'b' else to_bin.long - 1
            #lng_distance = abs(from_long - to_long)
            lng_distance = abs(from_bin.long - to_bin.long)
        else:
            r = self.wh.racks[to_bin.rack_no - 1]
            nc_to = r.nearest_cap(to_bin)
            r = self.wh.racks[from_bin.rack_no - 1]
            nc_from = r.nearest_cap(from_bin)
            
            dist_from_bin_2_nc_to = abs(from_bin.lat - nc_to.lat)   + \
                                    abs(from_bin.long - nc_to.long)
            dist_to_bin_2_nc_from = abs(to_bin.lat   - nc_from.lat) + \
                                    abs(to_bin.long   - nc_from.long)
                                    
            if dist_from_bin_2_nc_to > dist_to_bin_2_nc_from:
                nc_min = nc_from 
            else:
                nc_min = nc_to
            lat_distance = abs(from_bin.lat -  nc_min.lat)  + abs(to_bin.lat -  nc_min.lat)
            lng_distance = abs(from_bin.long - nc_min.long) + abs(to_bin.long - nc_min.long)

        return lat_distance + lng_distance
        

 
    def loc_to_loc_distance(self, from_loc, to_loc):
        '''Manhattan distance, not Euclidian
        call with two Bin class instances
'''
        assert isinstance(from_loc, Bin.Bin_Location) and isinstance(to_loc, Bin.Bin_Location),\
                'both arguments must be instance of Bin class'
        from_bin = Bin.get_bin_by_location(from_loc)
        to_bin   = Bin.get_bin_by_location(to_loc)
        return self.bin_to_bin_distance(from_bin, to_bin) 

        
    def __repr__(self):
        rtn = 'PickRoute: Order: {},\nproute, distance:\n{}'.format(self.order.__repr__(),
                                                                     '\n'.join(['\tfrom.to: {} dist: {}'.format(ft, d)
                                                                                for ft, d in self.__route.items()
                                                                                ])
                                                                     )
        return rtn
    
    
    @property
    def wh(self):
        return self.__wh
    
    @wh.setter
    def wh(self, args):
        raise RuntimeError('warehouse is set by init')
    
    
    @property
    def order_lines(self):
        return self.__order_lines
    
    @order_lines.setter
    def order_lines(self, args):
        raise RuntimeError('order_lines is set by init')
    
    
    @property
    def order(self):
        return self.__order
    
    @order.setter
    def order(self, args):
        raise RuntimeError('order attribute set by init')
    
    
    @property
    def pick_bins(self):
        return self.__pick_bins

    @pick_bins.setter
    def pick_bins(self):
        raise RuntimeError('PickRoute pick_bins attribute set by init')
    

    @property
    def route(self):
        if self.__route is None:
            self.__route = PickRoute.__calc_route(self.order)
        return [s for s in self.__route]

    @route.setter
    def route(self):
        raise RuntimeError('PickRoute route attribute set by init')
    
    
    @property
    def route_distance(self):
        return self.__route_distance
    
    @route_distance.setter
    def route_distance(self, args):
        raise RuntimeError('route_distance attribute set by init')
    
