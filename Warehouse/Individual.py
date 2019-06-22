from collections.abc import Iterable
import numpy as np


class Individual(np.ndarray):
	'''
    from the numpy documentation, we subclass ndarray
to add a 'fitness' attribute
'''
	__last_pop_id = 1
	__default_fitness = 1e10
	
	def __new__(cls, shape, dtype=int, buffer=None, offset=0,
		        strides=None, order=None, pop_id=None, fitness=int(__default_fitness)):
		# Create the ndarray instance of our type, given the usual
		# ndarray input arguments.  This will call the standard
		# ndarray constructor, but return an object of our type.
		# It also triggers a call to Individual.__array_finalize__
		if buffer is None:
			buffer = np.array([x for x in range(1, 1 + shape[0])])
			np.random.shuffle(buffer)
		obj = super(Individual, cls).__new__(cls, shape, dtype,
		                                         buffer, offset, strides,
		                                         order)
		# set the new 'info' attribute to the value passed - default 0
		obj.fitness = fitness
		if pop_id is None:
			obj.pop_id = Individual.__last_pop_id
			Individual.__last_pop_id += 1
		else:
			obj.pop_id = pop_id
			
		# Finally, we must return the newly created object:
		return obj
	
	def __array_finalize__(self, obj):
		# ``self`` is a new object resulting from
		# ndarray.__new__(Individual, ...), therefore it only has
		# attributes that the ndarray.__new__ constructor gave it -
		# i.e. those of a standard ndarray.
		#
		# We could have got to the ndarray.__new__ call in 3 ways:
		# From an explicit constructor - e.g. Individual():
		#    obj is None
		#    (we're in the middle of the Individual.__new__
		#    constructor, and self.info will be set when we return to
		#    Individual.__new__)
		if obj is None:
			return
		# From view casting - e.g arr.view(Individual):
		#    obj is arr
		#     (type(obj) can be Individual)
		# From new-from-template - e.g infoarr[:3]
		#    type(obj) is Individual
		#
		# Note that it is here, rather than in the __new__ method,
		# that we set the default value for 'info', because this
		# method sees all creation of default objects - with the
		# Individual.__new__ constructor, but also with
		# arr.view(Individual).
		self.fitness = getattr(obj, 'fitness', None)
		# We do not need to return anything
		
	def __lt__(self, other):
		if self.fitness < other.fitness:
			return True
		else:
			return False
		
	def __eq__(self, other):
		if isinstance(other, type(self)) and self.fitness == other.fitness:
			return True
		elif isinstance(other, Iterable):
			return np.all(np.array(self) == other)
		else:
			return False
		
	def __getitem__(self, idx):
		return super(type(self), self).__getitem__(idx)
	
	def __setitem__(self, var):
		raise RuntimeError('Individual is immutable')

	@classmethod
	def default_fitness(cls):
		return cls.__default_fitness
	
	
