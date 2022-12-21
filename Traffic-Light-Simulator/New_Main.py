import pygame
import sys
from pygame import transform
import LightChecks as lightchecks

pygame.init()

WIDTH = 1200
HEIGHT = 600

BACKGROUND_COLOR = 0x002200
YELLOW = (255, 255, 0)
RED = (255,0,0)
GREEN = (0,255,0)

game_running = True
debug = True

screen = pygame.display.set_mode((WIDTH, HEIGHT))

trafficFont = pygame.font.SysFont("monospace", 35)

timingFont = pygame.font.SysFont("monospace", 20)

def build_street_light(screen, p_x, p_y, light):
	light_width = 80  # the width of the rectangle that the traffic light will be
	light_height = 20  # the height of the traffic light
	RADIUS = 6 # the radius of the light circles for each light
	Y_INSET = 10 # how low into the square each circle will be
	Y_ALIGN = p_y + Y_INSET # position in the square of where each light is
	X_COORDS = [15,40,65] # y coords of each of the three lights of green, yellow and red
	
	pygame.draw.rect(screen, (0,0,0), (p_x, p_y, light_width, light_height)) # builds the square backdrop for seeing lights
	pygame.draw.rect(screen, (255,255,255), (p_x, p_y, light_width, light_height), 1) # builds the square of each light structure section

	pygame.draw.circle(screen,    RED, (p_x + X_COORDS[0], Y_ALIGN), RADIUS, light_exchange(light[0])) # red light on a section
	pygame.draw.circle(screen, YELLOW, (p_x + X_COORDS[1], Y_ALIGN), RADIUS, light_exchange(light[1])) # yellow light on a section
	pygame.draw.circle(screen,  GREEN, (p_x + X_COORDS[2], Y_ALIGN), RADIUS, light_exchange(light[2])) # green light on a section

def light_exchange(light):
	if(light == 0):
		return 1
	elif(light == 1):
		return 0
	else:
		return -1

def build_street_light_direction(screen, p_x, p_y, lights):
	light_gap = 85              # gap between each light in each direction

	left   = p_x                 # left turn right
	middle = p_x + light_gap     # middle straight light
	right  = p_x + (light_gap * 2) # right straight or turn light

	build_street_light(screen,  right, p_y, lights[0]) # far right light
	build_street_light(screen, middle, p_y, lights[1]) # middle light
	build_street_light(screen,   left, p_y, lights[2]) # left turn light

def set_direction_label(screen, p_x, p_y, text):
	coords = [p_x + 100, p_y - 50]
	label = trafficFont.render(text, 1, YELLOW)
	pygame.draw.rect(screen, YELLOW, (coords[0] - 20,coords[1], 260, 40), 3)
	screen.blit(label, (coords[0], coords[1]))

def drawTimingInfo(p_x, p_y):
	timingScreen = pygame.Surface((300,200))
	timingScreen.fill(BACKGROUND_COLOR)

	label = timingFont.render("Start Time: " + str(lightchecks.getBeginningTime()), 0, 	YELLOW)
	timingScreen.blit(label, (5, 1))

	label = timingFont.render("Time Now  : " + str(lightchecks.getCurrentTime()), 0, YELLOW)
	timingScreen.blit(label, (5, 16))

	label = timingFont.render("Total Time: " + str(lightchecks.getTotalCurrentTime()), 0, YELLOW)
	timingScreen.blit(label, (5, 31))

	screen.blit(timingScreen, (p_x, p_y), (0, 0, 185, 60))
	
def set_direction_compass(screen, p_x, p_y, text):
	coords = [p_x, p_y]
	label = trafficFont.render(text, 1, YELLOW)
	#pygame.draw.rect(screen, YELLOW, (coords[0],coords[1], 260, 40), 3)
	screen.blit(label, (coords[0], coords[1]))
	
def build_roads(screen):
	road_color         = (10,10,10) # light black color
	road_line_color    = (100,100, 0)
	intersection_color = (60, 60, 60) # white intersection lines
	
	road_width = 200 # width of road for the intersection going north and west
	north_axis = ( HEIGHT / 2) - (road_width / 2) # alignment for where the north-bound road will start
	west_axis  = (  WIDTH / 2) - (road_width / 2) # alignment for where the west-bound road will start
	
	# draw north-bound road
	pygame.draw.rect(screen, road_color, (0, north_axis, WIDTH, road_width))
	
	# draw west-bound road
	pygame.draw.rect(screen, road_color, (west_axis, 0, road_width, HEIGHT))
	
	# intersecton center variables
	intersection_center_x = (WIDTH  / 2) - (road_width / 2) 
	intersection_center_y = (HEIGHT / 2) - (road_width / 2)
	
	# draw yellow middle lines
	pygame.draw.rect(screen, road_line_color, (WIDTH/2, 0, 10, HEIGHT))
	pygame.draw.rect(screen, road_line_color, (0, HEIGHT/2, WIDTH, 10))
	
		
	#draw intersection square
	pygame.draw.rect(screen, road_color, (intersection_center_x, intersection_center_y, road_width, road_width))
	pygame.draw.rect(screen, intersection_color, (intersection_center_x, intersection_center_y, road_width, road_width), 3)
	pygame.draw.rect(screen, road_color, (intersection_center_x + 3, intersection_center_y + 3, road_width - 10, road_width - 5))
	
def draw_compass(screen):
	x_pos         = WIDTH - 120
	y_pos         = 100
	compass_width = 100 #unused - was only used for east of compass but refactered code
	
	
	NORTH_COMPASS  = [  x_pos - 8,         10 ]
	EAST_COMPASS   = [ x_pos + 60, y_pos - 18 ]
	SOUTH_COMPASS  = [  x_pos - 8, y_pos + 50 ]
	WEST_COMPASS   = [ x_pos - 80, y_pos - 18 ]
	
	set_direction_compass(screen, NORTH_COMPASS[0], NORTH_COMPASS[1], "N")
	set_direction_compass(screen,  EAST_COMPASS[0],  EAST_COMPASS[1], "E")
	set_direction_compass(screen, SOUTH_COMPASS[0], SOUTH_COMPASS[1], "S")
	set_direction_compass(screen,  WEST_COMPASS[0],  WEST_COMPASS[1], "W")  
	
	pygame.draw.rect(screen, YELLOW, (x_pos - (compass_width/2), y_pos, compass_width, 1)) #draw horizontal axis of compass
	pygame.draw.rect(screen, YELLOW, (x_pos, y_pos - (compass_width/2), 1, compass_width) ) #draw vertical axis of compass
	pygame.draw.circle(screen, YELLOW, (x_pos, y_pos), compass_width/2, width=1)

def drawLights():
	north_screen = pygame.Surface((250, 250))
	east_screen  = pygame.Surface((250, 250))
	south_screen = pygame.Surface((250, 250))
	west_screen  = pygame.Surface((250, 250))

	HEIGHT_ALIGN = (WIDTH/2) - 120
	WIDTH_ALIGN = (HEIGHT/2) 
	NORTH_DIR = [ HEIGHT_ALIGN, (WIDTH_ALIGN - 140) ]         #North light placed at bottom of intersection for top incoming south bond traffic
	EAST_DIR  = [   HEIGHT_ALIGN - 30, WIDTH_ALIGN - 135 ]    #East light placed at left of intersection for right incoming west bond traffic
	SOUTH_DIR = [ HEIGHT_ALIGN, (WIDTH_ALIGN + 100) ]         #South light placed at top of intersection for bottom incoming north bond traffic
	WEST_DIR  = [   (WIDTH - 480 + 20), WIDTH_ALIGN - 135  ]  #West light placed at right of intersection for left incoming east bond traffic
	
	
	build_street_light_direction(north_screen, 0, 0, lightchecks.getLightList(0)) # NORTH light
	north_screen = pygame.transform.rotate(north_screen, 0.0)
	screen.blit(north_screen, ((NORTH_DIR[0],NORTH_DIR[1])), (0, 0, 250, 20))
				
	build_street_light_direction(east_screen, 0, 0, lightchecks.getLightList(1)) # EAST light
	east_screen = pygame.transform.rotate(east_screen, 90.0)
	screen.blit(east_screen, (EAST_DIR[0],EAST_DIR[1]), (0, 0, 20, 250))
	
	build_street_light_direction(south_screen, 0, 0, lightchecks.getLightList(2)) # SOUTH light
	south_screen = pygame.transform.rotate(south_screen, 180.0)
	screen.blit(south_screen, (SOUTH_DIR[0],SOUTH_DIR[1]), (0, 230, 250, 20))#y, x, width_size, height_size
	
	build_street_light_direction(west_screen,  0, 0, lightchecks.getLightList(3)) # WEST light
	west_screen = pygame.transform.rotate(west_screen, -90.0)
	screen.blit(west_screen, (WEST_DIR[0],WEST_DIR[1]), (230, 0, 20, 250))

def main():
	global game_running
	global debug

	game_running = True
	debug = True

	while game_running:
		if(lightchecks.isGameRunning() == False):
			lightchecks.startTrafficLights()
			lightchecks.onStartTime()

		for event in pygame.event.get():
			if(event.type == pygame.QUIT):
				sys.exit()
			if(event.type == pygame.KEYDOWN):
				if(event.key == pygame.K_d):
					debug = not debug


		screen.fill(BACKGROUND_COLOR)
		
		build_roads(screen)
		
		drawLights()

		#draws a compass to show what direction the cars are going and lights are facing
		draw_compass(screen)

		if(debug):
			drawTimingInfo(10,10)

		lightchecks.checkTrafficLights()
	   
		pygame.display.update()

#check if there is a main method and if there is then run it
if __name__ == "__main__":
	main() 