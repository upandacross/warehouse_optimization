from Warehouse.Inventory import Inventory
from builtins import property

class Order:
	"""
	Order contains order_lines which contain order_items
	
	Assumptions:
		It is permissable to add items to order that are not in Inventory
"""

	class OrderItem:
		'''
		OrderItem is class for contents of order line item
'''
		def __init__(self, line_no, item_no, qty, status='ordered'):
			self.__line_no = line_no 
			self.__item_no = item_no 
			self.__qty = qty 
			self.__status = status 
		
		def __repr__(self):
			return 'line_no: {}, item_no: {}, qty: {}, line status: {}'.format(self.line_no,
																				self.item_no,
																				self.qty,
																				self.status)
			
		@property
		def line_no(self):
			return self.__line_no
		
		@property
		def item_no(self):
			return self.__item_no
		
		@property
		def qty(self):
			return self.__qty
		
		@property
		def status(self):
			return self.__status
		
		@status.setter 
		def status(self, stat):
			self.__status = stat
			

	##############################
	# Order class variabiles
	
	__last_order_no = 0
	
	__inventory = Inventory()
	
	
	@classmethod
	def clear(cls):
		'''
		clear needed to keep unit tests independent
'''
		cls.__last_order_no = 0
		pass # for debugging
	
	@classmethod
	def last_order_no(cls):
		return cls.__last_order_no


	def __init__(self):
		Order.__last_order_no += 1
		self.__order_no__ = 0 + Order.__last_order_no
		self.__lines = []
		self.__last_line_no = 0


	def add_line(self, item_no=None, qty=None):
		assert item_no is not None,\
			'Order Line SBE instantiated with item_no and qty'
		assert isinstance(item_no, int) and item_no > 0,\
			'item_no must be int > 0, is {}'.format(item_no)
		assert isinstance(qty, int) and qty > 0,\
			'qty must be int > 0, is {}'.format(qty)
		
		# not sure I'm ready for this assert:
		# assert item_no in Order.__inventory, 'attemted to add item not in inventory: {}'.format(item_no)
		
		self.__last_line_no += 1
		line = Order.OrderItem(0 + self.__last_line_no, item_no, qty, 'ordered')
		self.__lines.append((line))
		

	def __repr__(self):
		return('order_no: {}, {} lines'.format(self.__order_no__,
												len(self.__lines)))

	@property
	def order_no(self):
		return self.__order_no__

	@property
	def lines(self):
		return self.__lines

