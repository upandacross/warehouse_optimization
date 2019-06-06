'''
Created on May 27, 2019

@author: bren
'''
import sys
import unittest
from Warehouse.Bin import Bin
from Warehouse.Inventory import Inventory


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testSingleton(self):
        i = Inventory()
        i.clear()
        i2 = Inventory()
        self.assertIs(i.stock, i2.stock, 'singleton test fails')
        self.assertEqual(len(i.stock.keys()), 0, 'inventory SBE empty, found {} items'.format(len(i.stock.keys())))
    

    def testUpdateStock(self):
        r_no = 3
        i_no = 3
        location = Bin.Bin_Location(rack_no=r_no, side='a', bin_no=1)
        i = Inventory()
        i.clear()
        i.update_bin(item_no=i_no, location=location, qty=10)
        self.assertEqual(Inventory.__repr__(Inventory()), str(Inventory()), '__repr__ != __string__')
        self.assertEqual(len(i.stock), 1, 'inventory SBE empty, found {} items'\
                                            .format(len(i.stock)))


    def testAddItem(self):
        b = Bin(rack_no=1, side='b', bin_no=2)
        itm_no = 3
        qty = 30
        i = Inventory()
        i.clear()
        i.update_bin(location=b.location, item_no=itm_no, qty=qty)
        self.assertEqual(i.get_stock_qty(location=b.location), (itm_no, qty), \
                "item {} at {} SBE qty {}, is {}".format(itm_no, qty, b.location, 
                                                         i.get_stock_qty(location=b.location)))
        b = Bin.get_bin_by_location(b.location)
        self.assertEqual(b.item, itm_no, \
                            'location ({} item/qty SBE {}, is {}'.format(b.location, (itm_no, qty),
                                                                         (b.item, b.count)))


    def testSingletonDefaultDict(self):
        i = Inventory()
        i.clear()
        i2 = Inventory()
        self.assertIs(i.stock, i2.stock, 'singleton test fails')
        self.assertEqual(len(i.stock), 0, 'inventory SBE empty, found {} items'\
                                        .format(i.stock.keys()))
    

    def testUpdateStockSeparateSides(self):
        b = Bin(rack_no=1, side='a', bin_no=1)
        b.__count = 0
        i = Inventory()
        i.clear()
        Inventory.update_bin(location=b.location, item_no=1, qty=10)
        self.assertEqual(Inventory.__repr__(Inventory()), str(Inventory()), '__repr__ != __string__')
        self.assertEqual(len(i.stock), 1, 'inventory SBE empty, found {} items'.format(len(i.stock)))
        self.assertEqual(Bin.get_bin_by_location(b.location).count, 10, 'location ({} item SBE 10, is {}'\
                            .format(b.location, Bin.get_bin_by_location(b.location)))

        
        b = Bin(rack_no=1, side='b', bin_no=2)
        location = b.location
        i.update_bin(location=location, item_no=1, qty=20)
        (itm, q) = i.get_stock_qty(location=location)
        self.assertEqual(itm, 1, 'item at location {} SBE 1, is {}'.format(location, itm))
        self.assertEqual(q, 20, "item {} at {} SBE qty 20, is {}".format(1, location, q))
    
    
    def testExceptions(self):
        i = Inventory()
        i.clear()
        try:
            i.stock = dict()
            raise ValueError('stock rack_no should have raised exception')
        except ValueError as v:
            print(v)
            sys.exit(-1)
        except Exception as e:
            pass
               
    def testReprStr(self):
        i = Inventory()
        r = i.__repr__()
        s = i.__str__()
        self.assertEqual(r, s, 'repr "{}" not eq str "{}"'.format(r, s))
        
        
    def testClear(self):
        b = Bin(rack_no=1, side='a', bin_no=1)
        b.__count = 0
        i = Inventory()
        i.clear()
        Inventory.update_bin(location=b.location, item_no=1, qty=10)
        self.assertEqual(len(i.stock), 1, 'SBE only 1 item in inventory stock, is {}'.format(len(i.stock)))
        i.clear()
        self.assertEqual(len(i.stock), 0, 'SBE no1 items in inventory stock after clear, is {}'.format(len(i.stock)))
        
