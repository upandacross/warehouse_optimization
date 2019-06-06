'''
Created on May 28, 2019

@author: bren
'''
import imp
import sys
import unittest
import Warehouse
from Warehouse.Order import Order


class TestOrder(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testInit(self):
        Order.clear()

        o1 = Order()
        self.assertEqual(o1.order_no, 1, 'first order SBE order_no 1, is {}'.format(o1.order_no))
        o2 = Order()
        self.assertEqual(o2.order_no, 2, 'first order SBE order_no 2, is {}'.format(o2.order_no))
        self.assertEqual(len(o1.get_orders()), 2, 'SBE 2 orders, is {}'.format(len(o1.get_orders())))


    def testAddLine(self):
        # add lines - line number should increment
        Order.clear()

        o = Order()
        o.add_line(item_no=1, qty=50)
        o.add_line(item_no=2, qty=73)
        lines = o.lines
        self.assertEqual(len(lines), 2, 'SBE 2 lines in order, is {}'.format(len(lines)))
        for ln, (l, itmn_q) in enumerate(zip(lines, ((1, 50), (2, 73)))):
             self.assertEqual((l.item_no, l.qty), itmn_q, 'line_no {} - item_no, qty SBE {}, is {}'.format(ln, itmn_q, itmn_q))


    def testException(self):
        o = Order()
        
        try:
            o.lines = []
            raise ValueError('trying to set lines should raise exception')
        except ValueError as e:
            print(e)
            sys.exit(-1)
        except Exception:
            pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()