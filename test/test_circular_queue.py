'''
Created on Jun 8, 2019

@author: bren
'''
import unittest
from Warehouse.circular_queue import CircularQueue, RandomizedCircularQueue
from numpy.random import seed, randint, shuffle



class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testCircularQueue(self):
        cq = CircularQueue(range(5))
        for i in range(5):
            cqi = cq.item
            self.assertEqual(cqi, i, 'queue should return {}, is {}'.format(i, cqi))
            
    def testRandomizedCircularQueue(self):
        cq = RandomizedCircularQueue(range(5))
        self.assertEqual(cq.seed, 1, 'seed SBE 1, is {}'.format(cq.seed))
        r = [o for o in range(5)]
        seed(cq.seed)
        shuffle(r)
        cqs = [cq.item for _ in range(5)]
        for i, s in zip(r, cqs):
            self.assertEqual(i, s, 'cq.item should return {}, is {}'.format(i, s))

        cq = RandomizedCircularQueue(range(5))
        self.assertEqual(cq.seed, 2, 'seed SBE 2, is {}'.format(cq.seed))
        r = [o for o in range(5)]
        seed(cq.seed)
        shuffle(r)
        cqs = [cq.item for _ in range(5)]
        for i, s in zip(r, cqs):
            self.assertEqual(i, s, 'cq.item should return {}, is {}'.format(i, s))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCircularQueue']
    unittest.main()
