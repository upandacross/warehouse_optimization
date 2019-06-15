'''
Created on May 28, 2019

@author: bren
'''
from itertools import product
import numpy as np
import os
import unittest
from Warehouse.Bin import Bin
from Warehouse.Inventory import Inventory
from Warehouse.Order import Order
from Warehouse.PickRoute import PickRoute
from Warehouse.Warehouse import Warehouse
from Box2D.Box2D import b2AssertException

class Test(unittest.TestCase):
    Warehouse.clear()
    wh = Warehouse(5, 5)
    rack_count, bin_count = wh.racks_bins
    bins_total = rack_count * bin_count * 2

    inv = Inventory()
    num_items = bins_total
    o = None
    order_lines = 5
    setup_calls = 0

    
    def setUp(self):
        Test.setup_calls += 1
        # print('setup call number {}'.format(Test.setup_calls))
        
        np.random.seed(42)
        
        Test.wh = Test.wh.reset(5, 5)
        self.wh = Test.wh
        Test.inv.clear()
        rsb = [(r, s, b) for r, s, b in product(range(1, 5 + 1, 1),
                                                list('ab'),
                                                range(1, 5 + 1, 1))]
        np.random.seed(42)
        np.random.shuffle(rsb)
        for i, (r, s, bn) in enumerate(rsb):
            if s == 'a':
                b = self.wh.racks[r - 1].bins_a[bn]
            else: # s == 'b'
                b = self.wh.racks[r - 1].bins_b[bn]
            self.wh.update_stock(i + 1, (i + 1) * 10, b.location)


        np.random.seed(42)
        Test.o = Order()
        np.random.seed(42)
        for i, q in zip(np.random.choice(range(1, Test.num_items + 1), size=Test.order_lines, replace=False),
                        np.random.randint(1, Test.num_items + 1, size=Test.order_lines)):
            Test.o.add_line(item_no=int(i), qty=int(q))

        racks = self.wh.racks
        b = racks[0].bins_a[1]
        self.assertEqual(b.item, 26, 'rack 1, bin @ {}, item SBE 26, is {}'.format(b.location, b.item))
        # print(b)
        b = racks[1].bins_a[1]
        self.assertEqual(b.item, 41, 'rack 1, bin @ {}, item SBE 41, is {}'.format(b.location, b.item))
        # print(b)
        b = racks[1].bins_b[1]
        self.assertEqual(b.item, 20, 'rack 1, bin @ {}, item SBE 29, is {}'.format(b.location, b.item))
        # print(b)
        


    def tearDown(self):
        pass


    def testInit(self):
        # print('testInit')
        pr = PickRoute(Test.wh, self.o)
        self.assertEqual(len(pr.wh.racks), 5, 'warehouse should have 5 racks, is {}'.format(len(pr.wh.racks)))
        self.assertEqual(len(self.o.lines), Test.order_lines, 'order lines SBE {}, is {}'.format(Test.order_lines,
                                                                                                 len(self.o.lines)))
        self.assertEqual(len(pr.pick_bins), Test.order_lines, \
                            'order pick_bins SBE {}, is {}'.format(Test.order_lines,
                                                                   len(pr.pick_bins)))
        
        
    def testBinsDistance(self):
        # print('testBinsDistance')
        b1 = Bin(rack_no=1, side='b', bin_no=1)
        b2 = Bin(rack_no=1, side='a', bin_no=5)
        pr = PickRoute(Test.wh, self.o)
        d = pr.bin_to_bin_distance(b1, b2)
        print('from {} to {} dist: {}'.format(b1.location, b2.location, d))
        #expected = 16
        #self.assertEqual(d, expected, '{} to {} SBE [], is {}'\
        #                    .format(b1.location, b2.location, expected, d))

        
        b1 = Bin(rack_no=1, side='b', bin_no=1)
        b2 = Bin(rack_no=2, side='a', bin_no=1)
        pr = PickRoute(Test.wh, self.o)
        d = pr.bin_to_bin_distance(b1, b2)
        print('from {} to {} dist: {}'.format(b1.location, b2.location, d))
        #expected = 16
        #self.assertEqual(d, expected, '{} to {} SBE [], is {}'\
        #                    .format(b1.location, b2.location, expected, d))

        
        b1 = Bin(rack_no=1, side='a', bin_no=4)
        b2 = Bin(rack_no=4, side='b', bin_no=5)
        pr = PickRoute(Test.wh, self.o)
        d = pr.bin_to_bin_distance(b1, b2)
        print('from {} to {} dist: {}'.format(b1.location, b2.location, d))
        #expected = 16
        #self.assertEqual(d, expected, '{} to {} SBE [], is {}'\
        #                    .format(b1.location, b2.location, expected, d))

        
        b1 = Bin(rack_no=3, side='a', bin_no=0)
        b2 = Bin(rack_no=4, side='b', bin_no=5)
        pr = PickRoute(Test.wh, self.o)
        d = pr.bin_to_bin_distance(b1, b2)
        print('from dock {} to {} dist: {}'.format(b1.location, b2.location, d))
        #expected = 16
        #self.assertEqual(d, expected, '{} to {} SBE [], is {}'\
        #                    .format(b1.location, b2.location, expected, d))

        
    def testRoute(self):
        # print('testRoute')
        np.random.seed(42)
        pr = PickRoute(Test.wh, self.o)
        expected_steps = 46
        if pr.route_distance != expected_steps:
            print('route distance {:d} SBE {} {}'.format(pr.route_distance,
                                                         expected_steps,
                                                         'maybe next time?' \
                                                         if pr.route_distance != expected_steps \
                                                         else ''))
        # print(os.path.curdir)
        # I'm missing a random.seed somewhere
        self.assertEqual(pr.route_distance, expected_steps,
                         'route_distince SBE {}, is {}'\
                            .format(expected_steps, pr.route_distance))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()