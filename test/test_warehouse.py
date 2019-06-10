'''
Created on May 28, 2019

@author: bren
'''
from itertools import product
import sys
import unittest

from Warehouse.Bin import Bin
from Warehouse.Inventory import Inventory
from Warehouse.Warehouse import Warehouse


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testInit(self):
        Warehouse.clear()
        w = Warehouse(5, 5)
        self.assertEqual(len(w.racks), 5, 'w should have 5 racks, is {}'.format(w.racks))
        self.assertEqual(w.racks_bins, (5, 5), 'racks_bin SBE (5, 50, is {}'.format(w.racks_bins))
        self.assertEqual((w.dock.lat, w.dock.long), (0, 7), \
                         'dock_lat_long SBE (0, 7), is {}'.format((w.dock.lat,
                                                                   w.dock.long)))
        self.assertEqual(w.__repr__(), 'racks: 5, dock (lat, long): (0, 7), inventory has 0 item_no, 0 quantities',
                         'repr should not be "{}"'.format(w.__repr__()))
                         
        
    def testUpdateStockSingle(self):
        Warehouse.clear()
        w = Warehouse(5, 5)
        b = w.racks[0].bins_a[1]
        w.update_stock(1, 40, b.location)
        _, q = w.get_stock_qty(1)
        assert q == 40, 'item 1 qty SBE {} but is {}'.format(40, q)
    
                         
        
    def testExceptions(self):
        Warehouse.clear()
        w = Warehouse(5, 5)

        try:
            # confirm 2nd instantiation w/o clear() raises exception
            Warehouse(2, 2)
            raise RuntimeError('second and subsequent instantiations of warehouse should raise exception')
        except ValueError as v:
            print(v)
            sys.exit(-1)
        except Exception as e:
            pass
    
        # these should raise exceptions
        try:
            w.racks = 1
            raise RuntimeError('setting racks should raise exception')
        except ValueError as v:
            print(v)
            sys.exit(-1)
        except Exception as e:
            pass

        try:
            w.dock_lat_long = (0,0)
            raise RuntimeError('setting dock_lat_long should raise exception')
        except ValueError as v:
            print(v)
            sys.exit(-1)
        except Exception as e:
            pass


    def testReset(self):
        Warehouse.clear()
        # New warehouse configuration with reset() that combines clear() and init(racks, bins)
        try:
            # test reset allowing warehouse reconfiguration
            w = Warehouse.reset(5, 5)
            self.assertEqual(len(w.racks), 5, 'racks SBE 5 but is {}'.format(len(w.racks)))
            self.assertEqual((w.dock.lat, w.dock.long), (0, 7), \
                'dock lat/long SBE (0, 7), is {}'.format((w.dock.lat,
                                                          w.dock.long)))
        except Exception as e:
            print(e)
            sys.exit(-1)


    def testStockingRackBins(self):
        Inventory.clear()
        Warehouse.clear()
        wh = Warehouse(5, 5)

        for i, (r, s, bn) in enumerate(product(range(1, 5 + 1, 1),
                                   list('ab'),
                                    range(1, 5 + 1, 1))):
            if s == 'a':
                b = wh.racks[r - 1].bins_a[bn]
            else: # s == 'b'
                b = wh.racks[r - 1].bins_b[bn]
            wh.update_stock(i + 1, (i + 1) * 10, b.location)
            _, q = wh.get_stock_qty(i + 1)
            self.assertEqual(q, (i + 1) * 10, 'inventory qty for item {}  item SBE {}, is {}'.format(i,
                                                                                               (i + 1) * 10,
                                                                                               q))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testInit']
    unittest.main()