# import pygame
# from environment import build_environment

# env = build_environment("map.png", 1200, 600)	# create an environment object with the given image path and width and height
# running = True	# flag to control the main loop

# while running:	# main loop
# 	for event in pygame.event.get():	# get all events
# 		if event.type == pygame.QUIT:	# if the event is quit
# 			print("Exiting the program...")	# print a message to indicate the exit
# 			running = False	# set the running flag to false

# 	pygame.display.update()	# update the display

import pygame
import environment
import sensor

env = environment.build_environment("map.png", 1200, 600)	# create an environment object with the given image path and width and height
env.original_map = env.map.copy()	# create a copy of the map
laser = sensor.laser_sensor(200, env.original_map, [0.5, 0.01])	# create a laser sensor object with the given range and map

env.map.fill(environment.BLACK)	# fill the map with black color
env.info_map = env.map.copy()	# create a copy of the map

running = True	# flag to control the main loop
while running:	# main loop
	sensor_on = False	# flag to control the laser sensor

	for event in pygame.event.get():    # get all events
		if event.type == pygame.QUIT:    # if the event is quit
			print("Exiting the program...")    # print a message to indicate the exit
			running = False    # set the running flag to false
		if pygame.mouse.get_focused():    # if the mouse is focused
			sensor_on = True
		else:
			sensor_on = False
	
		if sensor_on:	# if the laser sensor is on
			position = pygame.mouse.get_pos()	# get the position of the mouse
			laser.position = position
			sensor_data = laser.sense_obstcles()	# get the sensor data
			if sensor_data is not None:
				env.data_store(sensor_data)
			env.show_sensed_obstacles(environment.WHITE)
	env.map.blit(env.info_map, (0, 0))	# draw the image on the window
	pygame.display.update()    # update the display