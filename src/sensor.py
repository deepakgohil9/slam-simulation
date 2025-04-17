import pygame
import numpy as np
import math

def add_uncertainty(distance, angle, sigma):
	"""
	Add uncertainty to the distance and angle using a multivariate normal distribution.

	Parameters:
		distance (float): The distance to add uncertainty to.
		angle (float): The angle to add uncertainty to.
		sigma (list): A list of standard deviations for distance and angle.
	
	Returns:
		list: A list containing the distance and angle with added uncertainty.
	"""
	mean = np.array([distance, angle])	# mean of the distance and angle
	covariance = np.diag(sigma ** 2)	# covariance matrix of the distance and angle, i.e. diagonal matrix with the variances, mathematically [sigma[0]^2, 0; 0, sigma[1]^2]
	distance, angle = np.random.multivariate_normal(mean, covariance)	# sample from the multivariate normal distribution with the given mean and covariance
	distance = max(0, distance)	# set the distance to 0 if it is negative
	angle = max(0, angle)	# set the angle to 0 if it is negative
	return [distance, angle]	# return the distance and angle with uncertainty


class laser_sensor:
	def __init__(self, Range, map, uncertainty):
		self.Range = Range	# range of the laser sensor
		self.speed = 4 	# speed of the laser sensor in rounds per second
		self.sigma = np.array([uncertainty[0], uncertainty[1]])	# standard deviation of the laser sensor
		self.position = (0, 0)	# position of the laser sensor
		self.map = map	# map of the environment
		self.width, self.height = pygame.display.get_surface().get_size()	# get the width and height of the window
		self.sensed_obstacles = []	# list of sensed obstacles point cloud

	def distance(self, p1, p2 = None):
		"""
		Calculate the distance between two points in 2D space.
		
		Parameters:
			p1 (tuple): The first point (x, y).
			p2 (tuple, optional): The second point (x, y). If not provided, defaults to the position of the laser sensor.

		Returns:
			float: The Euclidean distance between the two points.
		"""
		if p2 is None:	# if the second point is not given
			p2 = self.position	# set the second point to the position of the laser sensor
		return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)	# calculate the euclidean distance between the two points
	
	def sense_obstcles(self):
		data = []
		x1, y1 = self.position	# get the position of the laser sensor
		for angle in np.linspace(0, 2 * np.pi, 60, False):
			x2 = x1 + self.Range * math.cos(angle)	# calculate x coordinate farest point in the line of sight
			y2 = y1 + self.Range * math.sin(angle)	# calculate y coordinate farest point in the line of sight
			# sampling some points in the line of sight & check if they are in black color on the map as black color represents obstacles
			for i in np.linspace(0, 1, 100, False):
				x = int(x1 + i * (x2 - x1)) 	# calculate x coordinate of the point in the line of sight
				y = int(y1 + i * (y2 - y1))		# calculate y coordinate of the point in the line of sight
				if 0 < x < self.width and 0 < y < self.height:
					color = self.map.get_at((x, y))
					if color == (0, 0, 0):
						distance = self.distance((x, y))
						output = add_uncertainty(distance, angle, self.sigma)	# add uncertainty to the distance and angle
						output.append(self.position)	# add the position of the laser sensor to the output
						data.append(output)
						break
		
		if len(data) > 0:
			return data	# return the list of sensed obstacles
		else:
			return None