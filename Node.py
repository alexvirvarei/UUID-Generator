import ctypes
import time

class Node:
	NODE_ID_BITS = 10 # up to 1023
	TIMESTAMP_BITS = 44 # around 278 years
	COURSE_BITS = 10 # up to 1023 requests / ms
	
	def __init__(self,node_id):
		self.node_id = node_id 
		self.last_reponse_time = None
		self.course = 0
		# sleeping as little as possible to ensure uniqueness after a node failure and immediate reboot 
		time.sleep(1/1000)
	

	def get_id(self):
		# getting current time of the get_id request
		current_time = time.time_ns()

		# checking if a request has already been made this millisecond
		if current_time == self.last_reponse_time:
			self.course += 1

			# checking if course maximum has been reached for this millisecond
			if self.course > (2 ** self.COURSE_BITS) - 1:
		
				# waiting for the next millisecond (time.sleep(1/1000) would actually sleep for at least 10ms)
				while(current_time == self.last_reponse_time):
					current_time = time.time_ns()
			
				self.course = 0
		
		# else it is the first request done in the course of this millisecond
		else:
			self.course = 0

		self.last_reponse_time = current_time
		

		# limiting current_time variable to 44 bits
		current_time &= (2 ** self.TIMESTAMP_BITS) - 1

		# first 10 bits are the node's id bits
		uuid = self.node_id << (self.TIMESTAMP_BITS + self.COURSE_BITS)
		# next 44 are the timestamp bits
		uuid |= current_time << self.COURSE_BITS
		# last 10 are the course bits
		uuid |= self.course

		return uuid

