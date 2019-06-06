'''
Created on May 27, 2019

@author: bren
'''
import sys
import unittest
from Warehouse.Rack import Rack
from Warehouse.Inventory import Inventory


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testInit(self):
        r = Rack(rack_no=1, bin_count=5)
        self.assertEqual(r.bin_count, 5, 'bin_count SBE 5, is {}'.format(r.bin_count))
        self.assertEqual(r.rack_no, 1, 'rack_no SBE 1, is {}'.format(r.rack_no))
        self.assertEqual(len(r.bins_a), 5, 'side a SBE 5 bins, is {}'.format(len(r.bins_a)))
        self.assertEqual(len(r.bins_b), 5, 'side b SBE 5 bins, is {}'.format(len(r.bins_b)))

        b = r.bins_a[1]
        self.assertEqual(b.bin_no, 1, 'bin_no SBE 1, is {}'.format(b.bin_no))
        self.assertIsNone(b.item, 'item SBE None, is {}'.format(b.item))
        self.assertEqual(b.count, 0, 'count SBE 0, is {}'.format(b.count))
        self.assertEqual(b.lat, b.bin_no + 1, 'lat SBE {}, is {}'.format(b.bin_no + 1, b.lat))
        self.assertEqual(b.bin_side, 'a', 'bin_side SBE "a", is {}'.format(b.bin_side))
        self.assertEqual(b.rack_no, 1, 'rack_no SBE "a", is {}'.format(b.rack_no))
        self.assertEqual(b.long, 1, 'long SBE 1, is {}'.format((r.rack_no * 3) - 2))
        for bins, side in zip((r.bins_a, r.bins_b), list('ab')):
            for b in bins.values():
                self.assertIsNone(b.item, 'bin,side {} item SBE None, is {}'.format((b.bin_no, b.bin_side), b.item))
                self.assertEqual(b.count, 0, 'bin,side {} count SBE 0, is {}'.format((b.bin_no, b.bin_side), b.count))



    def testNearestCap(self):
        r = Rack(rack_no=1, bin_count=5)
        
        b = r.bins_a[1]
        nc = r.nearest_cap(b)
        self.assertEqual((nc.lat, nc.long), (0, 1), 'nearest cap for bin {} SBE (7, 1), is {}'\
                         .format(b.location, (nc.lat, nc.long)))
        b = r.bins_a[2]
        nc = r.nearest_cap(b)
        self.assertEqual((nc.lat, nc.long), (0, 1), 'nearest cap for bin {} SBE (7, 1), is {}'\
                         .format(b.location, (nc.lat, nc.long)))
        b = r.bins_a[4]
        nc = r.nearest_cap(b)
        self.assertEqual((nc.lat, nc.long), (7, 1), 'nearest cap for bin {} SBE (7, 1), is {}'\
                         .format(b.location, (nc.lat, nc.long)))
        b = r.bins_a[5]
        nc = r.nearest_cap(b)
        self.assertEqual((nc.lat, nc.long), (7, 1), 'nearest cap for bin {} SBE (7, 1), is {}'\
                         .format(b.location, (nc.lat, nc.long)))

        b = r.bins_b[1]
        nc = r.nearest_cap(b)
        self.assertEqual((nc.lat, nc.long), (0, 2), 'nearest cap for bin {} SBE (7, 1), is {}'\
                         .format(b.location, (nc.lat, nc.long)))
        b = r.bins_b[2]
        nc = r.nearest_cap(b)
        self.assertEqual((nc.lat, nc.long), (0, 2), 'nearest cap for bin {} SBE (7, 1), is {}'\
                         .format(b.location, (nc.lat, nc.long)))
        b = r.bins_b[4]
        nc = r.nearest_cap(b)
        self.assertEqual((nc.lat, nc.long), (7, 2), 'nearest cap for bin {} SBE (7, 1), is {}'\
                         .format(b.location, (nc.lat, nc.long)))
        b = r.bins_b[5]
        nc = r.nearest_cap(b)
        self.assertEqual((nc.lat, nc.long), (7, 2), 'nearest cap for bin {} SBE (7, 1), is {}'\
                         .format(b.location, (nc.lat, nc.long)))
        
    
    
    def testExceptions(self):
        r = Rack(rack_no=1, bin_count=5)
        try:
            r.rack_no = 2
            raise ValueError('setting rack_no should have raised exception')
        except ValueError as v:
            print(v)
            sys.exit(-1)

        except Exception as e:
            pass
        try:
            r.bin_count = 2
            raise ValueError('setting bin_count should have raised exception')
        except ValueError as v:
            print(v)
            sys.exit(-1)
        except Exception as e:
            pass
        try:
            r.bins_a = 2
            raise ValueError('setting bins_a should have raised exception')
        except ValueError as v:
            print(v)
            sys.exit(-1)
        except Exception as e:
            pass
        try:
            r.bins_b = 2
            raise ValueError('setting bins_b should have raised exception')
        except ValueError as v:
            print(v)
            sys.exit(-1)
        except Exception as e:
            pass
        try:
            r.add_bin(None)
            raise ValueError('adding bin to rack after init should have raised exception')
        except ValueError as v:
            print(v)
            sys.exit(-1)
        except Exception as e:
            pass

    def testRackBin(self):
        r = Rack(rack_no=1, bin_count=5)
        ba = r.bins_a[1]
        self.assertEqual(ba.bin_no, 1, 'bins_a.bin[1].bin_no SBE 1, is {}'.format(ba.bin_no))
        self.assertEqual(ba.bin_side, 'a', 'bins_a.bin[1].bin_side SBE "a", is {}'.format(ba.bin_side))
        nc = r.nearest_cap(ba)
        self.assertEqual((nc.lat, nc.long), (0, 1),
                         'nearest cap lat/log for bins_a.bin[1] SBE (0, 1), is {}'.format((nc.lat, nc.long)))
        
        bb = r.bins_b[5]
        self.assertEqual(bb.bin_no, 5, 'bins_b.bin[5].bin_no SBE 5, is {}'.format(ba.bin_no))
        self.assertEqual(bb.bin_side, 'b', 'bins_b.bin[5].bin_side SBE "a", is {}'.format(ba.bin_side))
        nc = r.nearest_cap(bb)
        self.assertEqual((nc.lat, nc.long), (7, 2),
                         'nearest cap lat/log for bins_a.bin[1] SBE (7, 1), is {}'.format((nc.lat, nc.long)))
        
    def testStockingRackBins(self):
        Inventory.clear()

        r = Rack(rack_no=1, bin_count=5)
        for b in r.bins_a.values():
            b.stock_bin(item_no=b.bin_no, item_count=b.bin_no * 10)
        for b in r.bins_b.values():
            b.stock_bin(item_no=b.bin_no, item_count=b.bin_no * 20)
        
        for b in r.bins_a.values():
            self.assertEqual(b.item, b.bin_no, 'bin @ {}  item SBE {}, is {}'.format(b.location,
                                                                                     b.bin_no,
                                                                                     b.item))
            self.assertEqual(b.count, b.bin_no * 10, 'bin @ {}  count SBE {}, is {}'.format(b.location,
                                                                                            b.bin_no * 10,
                                                                                            b.count))
        for b in r.bins_b.values():
            self.assertEqual(b.item, b.bin_no, 'bin @ {}  item SBE {}, is {}'.format(b.location,
                                                                                     b.bin_no,
                                                                                     b.item))
            self.assertEqual(b.count, b.bin_no * 20, 'bin @ {}  count SBE {}, is {}'.format(b.location,
                                                                                            b.bin_no * 20,
                                                                                            b.count))
        inv = Inventory()
        # Inventory.__stock[item_no][location]
        for b in r.bins_a.values():
            (i, q) = inv.get_stock_qty(location=b.location)
            self.assertEqual((i, q), (b.item, b.count), 'inventory item/qty for bin @ {}  item SBE {}, is {}'.format(b.location,
                                                                                                 (b.item, b.count),
                                                                                                 (i, q)))
        for b in r.bins_b.values():
            (i, q) = inv.get_stock_qty(location=b.location)
            self.assertEqual((i, q), (b.item, b.count), 'inventory qty for bin @ {}  item SBE {}, is {}'.format(b.location,
                                                                                                 (b.item, b.count),
                                                                                                 (i, q)))
            
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()