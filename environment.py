import math
import pygame

BLACK = (0, 0, 0)	# color of the obstacles in the map
WHITE = (255, 255, 255)	# color of the free space in the map
RED = (255, 0, 0)	# color of the sensed obstacles in the map
GREEN = (0, 255, 0)	# color of the path in the map
BLUE = (0, 0, 255)	# color of the start and end points in the map

class build_environment:
	def __init__(self, path, width, height):
		print("Initializing the environment...")	# print a message to indicate the start of the environment initialization
		pygame.init()
		self.width = width	# width of the map
		self.height = height	# height of the map
		self.point_cloud = []
		self.external_map = pygame.image.load(path) # image path of the map
		self.map_window_name = "RRT path planning"	# name of the window

		pygame.display.set_caption(self.map_window_name)	# set the window name
		self.map = pygame.display.set_mode((self.width, self.height)) 	# create a window with the given width and height
		self.map.blit(self.external_map, (0, 0))	# draw the image on the window
  
  
	def polar2cartesian(self, distance, angle, position):
		"""
		Convert polar coordinates to cartesian coordinates.
		
		Parameters:
			distance (float): The distance from the origin.
			angle (float): The angle in radians.
			position (tuple): The position of the laser sensor (x, y). Output of the function is relative to this position.
		Returns:
			tuple: A tuple containing the x and y coordinates.
		"""
		x = distance * math.cos(angle) + position[0]
		y = distance * math.sin(angle) + position[1]
		return (int(x), int(y)) # return the x and y coordinates as integers


	def data_store(self, data):
		"""
		Store the data in the point cloud.
		
		Parameters:
			data (list): Polar coordinates of the obstacles received from the laser sensor.
		"""
		print("Storing the data...")	# print a message to indicate the start of the data storing
		print("Current point cloud length: ", len(self.point_cloud))	# print the current length of the point cloud
		for element in data:
			point = self.polar2cartesian(element[0], element[1], element[2])
			# check if the point is not already in the point cloud, if not add it
			if point not in self.point_cloud:
				self.point_cloud.append(point)
    
	
	def show_sensed_obstacles(self, color = BLUE):
		"""
		Show the sensed obstacles on the map.
		"""
		self.info_map = self.map.copy()	# create a copy of the map
		for point in self.point_cloud:
			self.info_map.set_at(point, color)	# set the color of the point to red