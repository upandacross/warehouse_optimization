#!/home/bren/miniconda3/bin/python3.7
# encoding: utf-8
'''
runWhOpt 

	run genetic algorithm to find inventory stocking that minimizes distance traveled to pick orders
	
	examples:
	
		runWhOPt 5 5 # run simulation of warehouse with 5 racks of 5 bins on each side

@author:     user_name

@copyright:  2019 TLA. All rights reserved.

@license:    MIT

@contact:    user_email
@deffield    updated: Updated
'''

from collections.abc import Iterable
import heapq
from itertools import product
import multiprocessing
import numpy as np
from numpy import array as nparray, roll
from numpy.random import choice, randint, random, seed
import os
import pickle
import sys
from time import ctime
from Warehouse.Individual import Individual
from Warehouse.Order import Order
from Warehouse.PickRoute import PickRoute
from Warehouse.Warehouse import Warehouse


from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter


__all__ = []
__version__ = 0.1
__date__ = '2019-06-17'
__updated__ = '2019-06-17'

DEBUG = 0
TESTRUN = 0 # will only evaluate fitness of limited number of pop, cross-over, mutate
RESULTS = 1 # print stats for each gen
PROFILE = 0

class CLIError(Exception):
	'''Generic exception to raise and log different fatal errors.'''
	def __init__(self, msg):
		super(CLIError).__init__(type(self))
		self.msg = "E: %s" % msg
	def __str__(self):
		return self.msg
	def __unicode__(self):
		return self.msg

def main(argv=None): # IGNORE:C0111
	'''Command line options.'''

	if argv is None:
		argv = sys.argv
	else:
		sys.argv.extend(argv)

	program_name = os.path.basename(sys.argv[0])
	program_version = "v%s" % __version__
	program_build_date = str(__updated__)
	program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
	program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
	program_license = '''%s

	Created by user_name on %s.
	Copyright 2019 organization_name. All rights reserved.

	Licensed under the Apache License 2.0
	http://www.apache.org/licenses/LICENSE-2.0

	Distributed on an "AS IS" basis without warranties
	or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

	try:
		# Setup argument parser
		parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
		parser.add_argument("racks", type=int,
						help="intiger number of warehouse racks")
		parser.add_argument("-v", "--verbose", dest="verbose", action="count",
						help="set verbosity level [default: %(default)s]")
		parser.add_argument("bins", type=int,
						help="integer number of bins on one side of rack.")
		parser.add_argument('-V', '--version', action='version', version=program_version_message)
		parser.add_argument('-g', '--generations', action='store', dest='gens', type=int,
						help='integer number of generations of evolution. Default 1',
						default=1)
		parser.add_argument('-r', '--restore', action='store', dest='restore', type=str,
						help='Restore prior version of population from file',
						default='')

		# Process arguments
		args = parser.parse_args()

	except KeyboardInterrupt:
		### handle keyboard interrupt ###
		return 0
	except Exception as e:
		if DEBUG or TESTRUN:
			raise(e)
		indent = len(program_name) * " "
		sys.stderr.write(program_name + ": " + repr(e) + "\n")
		sys.stderr.write(indent + "  for help use --help")
		return 2
	
	
	########################################################################
	# this will be parallelized - TBD: create class MyGlobals and pickle it for 
	# multiprocesses
	
	class MyEnv:
		def __init__(self, args, CXPB=0.7):
			restore = args.restore
			if len(restore) > 0:
				if not os.path.isfile(restore):
					print('restore file {} does not exist'.format(restore))
					sys.exit(2)
				else:
					self.RESTORE=True
			else:
					self.RESTORE=False
	
			self.verbose = args.verbose
			racks = args.racks
			bins = args.bins
			
			self.NGENS = args.gens

			if self.verbose:
				print("Verbose mode on")
	
			if racks > 0:
				self.NUM_RACKS = racks
				if self.verbose:
					print("{} racks".format(racks))
			else:
				raise RuntimeError('must be int > 0 number of racks')
	
			if bins > 0:
				self.NUM_RACK_SIDE_BINS = bins
				if self.verbose:
					print("{} bins".format(bins))
			else:
				raise RuntimeError('must be int > 0 number of bins on each side of rack')
			
			self.NUM_BINS = self.NUM_RACKS * self.NUM_RACK_SIDE_BINS * 2 # two sides to a rack
			self.INDXS = np.arange(self.NUM_BINS)
			self.NUM_ORDERS = self.NUM_BINS * 10
			self.ORDER_LINES = 15
	
			self.CXPB=CXPB
			self.MUTPB=1.0 - CXPB

			self.wh = Warehouse(self.NUM_RACKS, self.NUM_RACK_SIDE_BINS)
	
			self.rsb = [(r, s, b) for r, s, b in product(range(self.NUM_RACKS), list('ab'),
														 range(1, self.NUM_RACK_SIDE_BINS + 1, 1))]
			self.idxs = np.arange(self.NUM_BINS)

			self.orders = []	
			seed(42)
			for _ in range(self.NUM_ORDERS):
				o = Order()
				o_items = choice(range(1, self.NUM_BINS + 1), size=self.ORDER_LINES, replace=False)
				for itm in o_items:
					o.add_line(item_no=int(itm), qty=10)
				self.orders.append(o)
	
			if self.RESTORE:
				with open(restore, 'rb') as infile:
					self.pop = pickle.load(infile)
				plen = len(self.pop[0])
				# reset pop_id and fitness = 0
				self.pop = [Individual(shape=(plen,), buffer=p) for p in self.pop]
				pass # for debugging	
			else:
				self.pop = list()
				for _ in range(1, self.NUM_BINS + 1):
					# individulas contain a shuffled list of item_no
					# bins contain a fixed qty of an item_no selected from a shuffled list
					# the fitness attribute will be set to number of steps required to fulfill orders from items when so distributed in wh
					self.pop.append(Individual(shape=(self.NUM_BINS,)))
	

	myenv = MyEnv(args)
	
	if myenv.verbose or RESULTS: 
		print('simulate warehouse with {} racks and {} bins on each side'.format(myenv.NUM_RACKS, myenv.NUM_BINS))
	
	##########################################################
	# support functions
	
	def evalFitness(individual):
		if individual.fitness != Individual.default_fitness():
			return individual.fitness
		
		myenv.wh.clear()
	
		for i, (r, s, bn) in zip(individual, myenv.rsb):
			if s == 'a':
				b = myenv.wh.racks[r].bins_a[bn]
			else: # s == 'b'
				b = myenv.wh.racks[r].bins_b[bn]
			myenv.wh.update_stock(int(i), 10, b.location)
			pass # for debugging

		tot_dist = sum(PickRoute(myenv.wh, o).route_distance
						for o in myenv.orders) 
		
		return tot_dist

	def mutSwap(individual, num):
		assert isinstance(individual, Iterable), 'mutSwap individual SBE iterable'
		assert isinstance(num, int) and num >=2 and num < len(individual),\
				'mutSwap 2nd arg SBE int in [2,len(ind)]'
		inda = individual.copy()
		f = choice(range(len(inda)), size=num, replace=False) # needed if num > 2
		orig = inda[f] # from
		t = roll(f, -1) # swap locations
		inda[t] = orig # to

		return Individual(shape=(myenv.NUM_BINS,), buffer=inda)


	def partMatched(mom, pop):
		dad = mom
		while dad is mom:
			dad = pop[randint(1, len(pop))]
		child_mom, child_dad = np.array(mom), np.array(dad)
		
		# TBD size SBE randint(4, 2 * (NUM_BINS // 4)), an even number
		
		# at 4, 2 for mom and 2 for dad
		dests = np.random.choice(myenv.idxs, size=6, replace=False)
		
		parents = (mom, dad)
		children = (child_dad, child_mom)
		for p, gene_loc in enumerate(dests):
			s = p + 1
			parent = parents[s % 1] # alternate parent
			child = children[s % 1] # if parent is mom, child SBE child_dad
			parent_gene = parent[gene_loc]
			child_gene_replaced = child[gene_loc]
			child_gene_replaced_loc = myenv.INDXS[np.isin(child, parent_gene)][0]
			child[[gene_loc, child_gene_replaced_loc]] = [parent_gene, child_gene_replaced]
			
		return (Individual((myenv.NUM_BINS,), buffer=child_mom),
				Individual((myenv.NUM_BINS,), buffer=child_dad))	

	
	def calcFitness(individual):
		individual.fitness = evalFitness(individual)
		
	
	######################################################
	# Simulation starts here
	######################################################
	

	for pop_no, ind in enumerate(myenv.pop):
		ind.fitness = evalFitness(ind)
		if myenv.verbose:
			msg = 'gen {:2d}: stock config {:4,d}, dist={:6,d}'.format(0, pop_no + 1, int(ind.fitness))
			print(msg)
		if TESTRUN and pop_no >= 1:
			break

	
	if RESULTS:
		d = nparray([x.fitness for x in myenv.pop])
		msg = 'gen {:2d} {:10s}: max: {:6,d}, min: {:6,d}, mean: {:.2f}, std: {:.2f}'\
				.format(0, 'pop', d.max(), d.min(), d.mean(), d.std())
		print(msg)

	for gen in range(myenv.NGENS):
		crossed_over = []

		for pop_no, ind in enumerate(myenv.pop):
			probCx = random()
			if probCx <= myenv.CXPB:
				c1, c2 = partMatched(ind, myenv.pop)
				c1.fitness = evalFitness(c1)
				c2.fitness = evalFitness(c2)
				crossed_over.append(c1)
				crossed_over.append(c2)
				if myenv.verbose:
					msg = 'gen {:2d}: crossover {:3,d}, dist1={:6,d}, dist2={:6,d}'.format(gen,pop_no + 1,
																						  int(c1.fitness),
																						  int(c2.fitness))
					print(msg)
				if TESTRUN and pop_no >= 2:
					break
				
		hof = myenv.pop + crossed_over
		heapq.heapify(hof)
		myenv.pop = heapq.nsmallest(myenv.NUM_BINS, hof)
		
		if RESULTS:
			d = nparray([x.fitness for x in myenv.pop])
			msg = 'gen {:2d} {:10s}: max: {:6,d}, min: {:6,d}, mean: {:.2f}, std: {:.2f}'\
					.format(gen, 'crossover', d.max(), d.min(), d.mean(), d.std())
			print(msg)
			
		# Done if no opportunity to evolve?
		if d.max() == d.min() and d.std() == 0.0:
			break

		mutated = []

		for pop_no, ind in enumerate(myenv.pop):
			probMut = random()
			if probMut <= myenv.MUTPB:
				c1 = mutSwap(nparray(ind), 2)
				c1.fitness = evalFitness(c1)
				if myenv.verbose:
					msg = 'gen {:2d}: {:10s} {:3,d}, dist={:6,d}'\
							.format(gen, 'mutate', pop_no + 1, int(c1.fitness))
					print(msg)
				mutated.append(c1)
				if TESTRUN and pop_no >= 2:
					break
		
		hof = myenv.pop + mutated
		heapq.heapify(hof)
		myenv.pop = heapq.nsmallest(myenv.NUM_BINS, hof)

		if RESULTS:
			d = nparray([x.fitness for x in myenv.pop])
			msg = 'gen {:2d} {:10s}: max: {:6,d}, min: {:6,d}, mean: {:.2f}, std: {:.2f}'\
					.format(gen, 'mutate', d.max(), d.min(), d.mean(), d.std())

			print(msg)
		
		# Done if no opportunity to evolve?
		if d.max() == d.min() and d.std() == 0.0:
			break

	if not DEBUG:
		_, m, d, t, y = ctime().split(' ')
		with open('pop_{}.pkl'.format(m+d+t+y), 'wb') as ofile:
			pickle.dump(myenv.pop, ofile)
	
	pass # for debugging
	
if __name__ == "__main__":
	if TESTRUN:
		import doctest
		doctest.testmod()
	if PROFILE:
		import cProfile
		import pstats
		profile_filename = 'runWhOpt_profile.txt'
		cProfile.run('main()', profile_filename)
		statsfile = open("profile_stats.txt", "w")
		p = pstats.Stats(profile_filename, stream=statsfile)
		stats = p.strip_dirs().sort_stats('cumulative')
		stats.print_stats()
		statsfile.close()
		sys.exit(0)
	sys.exit(main())