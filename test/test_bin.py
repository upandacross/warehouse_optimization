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
        Inventory.clear()


    def tearDown(self):
        pass

    def testInit(self):
        b = Bin(rack_no=1, side='b', bin_no=3)
        self.assertEqual(b.rack_no, 1, 'rack_no SBE 1, is {}'.format(b.rack_no))
        self.assertEqual(b.bin_no, 3, 'bin_no SBE 3, is {}'.format(b.bin_no))
        self.assertEqual(b.bin_side, 'b', 'bin_no SBE "b", is {}'.format(b.bin_side))
        self.assertEqual(b.location, Bin.Bin_Location(1, 'b', 3), 'bin_no SBE {}, is {}'.format(Bin.Bin_Location(1, 'b', 3),
                                                                                                b.location))
        self.assertEqual(b.lat, 4, 'bin_no SBE 4, is {}'.format(b.lat))
        self.assertEqual(b.long, 2, 'bin_no SBE 2, is {}'.format(b.long))
        self.assertIsNone(b.item, 'item SBE None, is {}'.format(b.item))
        self.assertEqual(b.count, 0, 'bin_no SBE 0, is {}'.format(b.count))
        


    def testInitMissing(self):
        # confirm argument testing
        try:
            t = 'rack_no'
            _ = Bin(side='a', bin_no=1, item=1, count=10)
            raise ValueError('missing {} SBE exception'.format(t))
        except ValueError:
            print(t)
            sys.exit(-1)
        except Exception:
            pass
        try:
            t = 'bin_no'
            _ = Bin(rack_no=1, side='a', item=1, count=10)
            raise ValueError('missing {} SBE exception'.format(t))
        except ValueError:
            print(t)
            sys.exit(-1)
        except Exception:
            pass
        try:
            t = 'side'
            _ = Bin(rack_no=1, bin_no=1, item=1, count=10)
            raise ValueError('missing {} SBE exception'.format(t))
        except ValueError:
            print(t)
            sys.exit(-1)
        except Exception:
            pass


    def testGetBinByLocation(self):        
        # confirm initialization of attributes
        b = Bin(rack_no=1, side='b', bin_no=5, item=2, count=10)
        location = b.location
        b = Bin.get_bin_by_location(location)
        self.assertEqual( (1, 'b', 5), (location.rack, location.side, location.bin_no),\
            'bin rack_no, side, bin_no SBE (1, "b", 5), is {}'\
            .format((location.rack, location.side, location.bin_no)))
        self.assertEqual((6, 2), (b.lat, b.long), \
            'bin lat/long SBE {}, is{}'.format((2, 0), (b.lat, b.long)))
    
        b = Bin(rack_no=1, side='a', bin_no=1, item=1, count=10)
        location = b.location
        b = Bin.get_bin_by_location(location)
        self.assertEqual((1, 'a', 1), (location.rack, location.side, location.bin_no),\
            'bin rack_no, side, bin_no SBE (1, "a", a), is {}'\
            .format((location.rack, location.side, location.bin_no)))
        self.assertEqual((2, 1), (b.lat, b.long), \
            'bin lat/long SBE {}, is{}'.format((2, 0), (b.lat, b.long)))

        b = Bin.get_bin_by_location(location)
        b.stock_bin(item_no=2, item_count=30) # removes prior item (1) replacing with item 2
        self.assertEqual((2, 1, 1, 'a', 30), (b.item, 
                                  b.bin_no, b.rack_no, b.bin_side,
                                  b.count),\
            'item and count SBE (1, 30), is {}'.format((b.item, b.count)))

        
    def testExceptions(self):
        b = Bin(rack_no=1, side='a', bin_no=1,
                item=1, count=10)
        
        try:
            b.rack_no = 2
            raise ValueError('trying to set rack_no should raise exception')
        except ValueError as ve:
            print(ve)
            sys.exit(-1)
        except:
            pass
        
        try:
            b.bin_no = 2
            raise ValueError('trying to set bin_no should raise exception')
        except ValueError as ve:
            print(ve)
            sys.exit(-1)
        except:
            pass
        
        try:
            b.bin_side = 'b'
            raise ValueError('trying to set bin_side should raise exception')
        except ValueError as ve:
            print(ve)
            sys.exit(-1)
        except:
            pass
        
        try:
            b.location = (1, 'a', 1)
            raise ValueError('trying to set location should raise exception')
        except ValueError as ve:
            print(ve)
            sys.exit(-1)
        except:
            pass
        
        try:
            b.lat = (1, 'a', 1)
            raise ValueError('trying to set lat should raise exception')
        except ValueError as ve:
            print(ve)
            sys.exit(-1)
        except:
            pass
        
        try:
            b.long = (1, 'a', 1)
            raise ValueError('trying to set long should raise exception')
        except ValueError as ve:
            print(ve)
            sys.exit(-1)
        except:
            pass
            
        try:
            b.item = (1, 'a', 1)
            raise ValueError('trying to set item should raise exception')
        except ValueError as ve:
            print(ve)
            sys.exit(-1)
        except:
            pass
            
        try:
            b.count = (1, 'a', 1)
            raise ValueError('trying to set count should raise exception')
        except ValueError as ve:
            print(ve)
            sys.exit(-1)
        except:
            pass
            

    def testBinLocation(self):
        bl1 = Bin.Bin_Location(1, 'a', 1)
        bl2 = Bin.Bin_Location(1, 'a', 1)
        self.assertEqual(bl1, bl2, '{} SBE equal {}'.format(bl1, bl2))
        bl2 = Bin.Bin_Location(1, 'a', 2)
        self.assertNotEqual(bl1, bl2, '{} SBE not equal {}'.format(bl1, bl2))
        self.assertLess(bl1, bl2, '{} SBE LT {}'.format(bl1, bl2))
        
        
    def testDropBin(self):
        # del Bin.__bin_locations[location]
        Bin.clear()
        self.assertEqual(Bin.bin_locations(), 0, 'clear method should reset class list of prior Bin instances')
        bl1 = Bin(rack_no=1, side='a', bin_no=1)
        bl2 = Bin(rack_no=1, side='a', bin_no=2)
        self.assertEqual(Bin.bin_locations(), 2, 
                         'class list of Bin instances SBE len 2, is {}'\
                         .format(Bin.bin_locations()))
        Bin.drop_bin(bl1.location)
        self.assertEqual(Bin.bin_locations(), 1, 
                         'class list of Bin instances SBE len 1 after drop_bin, is {}'\
                         .format(Bin.bin_locations()))
        self.assertEqual(bl2, Bin.get_bin_by_location(bl2.location), 
                         'bin at {} should still be in bin instance list after drop'\
                         .format(bl2.location))
        
                         
            