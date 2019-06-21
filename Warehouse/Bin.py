from _collections import defaultdict
from functools import total_ordering
import numpy

class Bin:
	
	bin_locations = defaultdict(lambda: None) # Bin.__bin_location[location] = Bin
	
	
	@classmethod
	def clear(cls):
		cls.bin_locations = defaultdict(lambda: None) # Bin.__bin_location[location] = Bin
		
		
	@classmethod
	def get_bin_by_location(cls, location):
		assert isinstance(location, Bin.Bin_Location), 'get_bin_by_location to be called with Bin.Bin_Location instance'
		return Bin.bin_locations[location]
	
	
	@classmethod
	def drop_bin(cls, location):
		assert isinstance(location, Bin.Bin_Location), 'drop_bin to be called with Bin.Bin_Location instance'
		try:
			del Bin.bin_locations[location]
		except:
			pass
	

	# start internal class Bin_location
	@total_ordering
	class Bin_Location:
		
		__name__ = 'Bin_Llocation'
		
		def __init__(self, rack_no, side, bin_no):
			self.__rack = rack_no
			self.__side = side
			self.__bin_no = bin_no
			self.__tuple = (rack_no, side, bin_no)
			
		
		def __lt__(self, other):
			return self.astuple < other.astuple
		
		
		def __eq__(self, other):
			return self.astuple == other.astuple
		
		
		def __hash__(self):
			return hash('{:02d}{:1s}{:02d}'.format(self.rack, self.side, self.bin_no))
		
		
		def __repr__(self):
			return 'rack: {}, side: {}, bin_no: {}'.format(self.rack, self.side, self.bin_no)


		@property
		def astuple(self):
			return self.__tuple
		
		@property
		def rack(self):
			return self.__rack
		
		@property
		def side(self):
			return self.__side
		
		@property
		def bin_no(self):
			return self.__bin_no

		# end of class Bin_Location
		

	# start methods for class Bin
	def __init__(self, rack_no, side, bin_no,
				 item=None, count=0):

		self.__rack_no = rack_no
		self.__bin_side = side # a or b
		self.__bin_no = bin_no
		self.__location = Bin.Bin_Location(rack_no, side, bin_no)
		lat = bin_no + 1 if bin_no > 0 else 0 # dock is bin_no 0 at lat 0
		long = (rack_no * 3) - 2 if side == 'a' else (rack_no * 3) - 1
		self.__lat_long = numpy.array([lat, long])
		self.__item = item
		self.__count = count
		self.__nearest_cap = None
		self.__nearest_cap_distance = None

		Bin.bin_locations[self.location] = self

	def stock_bin(self, item_no, item_count):
		'''
		add item_count of items in bin
		if item_no is != bin.item, replace bin.item, bin.count with item_no, item_count (not added to)
		SBE called from Inventory class where this bin instance lives
'''
		assert isinstance(item_no, int) and item_no > 0, 'item_no must be int > 0'
		assert isinstance(item_count, int), 'item_count must be int, can be +/-'
		self.__count = item_count if self.item != item_no else self.__count + item_count
		if self.__count < 0:
			self.__count = 0
		self.__item = item_no


	def __lt__(self, other):
		return self.location < other.location
	
	
	def __repr__(self):
		rtn =  'rack_no: {}, bin_no: {}, bin_side: {} '\
				.format(self.__rack_no, self.__bin_no, self.__bin_side)
		rtn += 'lat: {}, long: {}, item: {}, count: {} '\
				 .format(self.__lat_long[0], self.__lat_long[1],
						 self.__item, self.__count)

		return rtn

	
	@property
	def nearest_cap(self):
		return self.__nearest_cap
	
	@nearest_cap.setter
	def nearest_cap(self, cap):
		assert isinstance(cap, Bin), 'nearest_cap must be class Bin'
		self.__nearest_cap = cap
	
	@property
	def nearest_cap_distance(self):
		return self.__nearest_cap_distance
	
	@nearest_cap_distance.setter 
	def nearest_cap_distance(self, dist):
		assert isinstance(dist, int) and dist >= 0, 'distance must be int > 0'
		self.__nearest_cap_distance = int(dist)
	
	@property
	def rack_no(self):
		return self.__rack_no

	@property
	def bin_no(self):
		return self.__bin_no

	@property
	def bin_side(self):
		return self.__bin_side

	@property
	def bins(self):
		return Bin.bin_locations.values()

	@property
	def location(self):
		return self.__location

	@property
	def lat_long(self):
		return self.__lat_long

	@property
	def lat(self):
		return self.__lat_long[0]

	@property
	def long(self):
		return self.__lat_long[1]

	@property
	def item(self):
		return self.__item

	@property
	def count(self):
		return self.__count

