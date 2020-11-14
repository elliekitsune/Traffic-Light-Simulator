import pygame
import sys

pygame.init()

WIDTH =1200
HEIGHT = 600

RGB_COLOR = 65
YELLOW = (255, 255, 0)
RED = (255,0,0)
GREEN = (0,255,0)
BACKGROUND_COLOR = (RGB_COLOR, RGB_COLOR, RGB_COLOR)

lightlist = [#   red,  yellow,    green
[[1,0,1], [1,1,0], [1,1,0]], #pole west
[[0,1,1], [0,1,1], [0,1,1]], #pole north
[[1,0,1], [1,1,0], [1,1,0]], #pole east
[[0,1,1], [0,1,1], [0,1,1]]  #pole south
]

screen = pygame.display.set_mode((WIDTH, HEIGHT))

myfont = pygame.font.SysFont("monospace", 35)

game_over = False

def build_street_light(screen, p_x, p_y, light):
    light_width = 140  # the width of the rectangle that the traffic light will be
    light_height = 40  # the height of the traffic light
    RADIUS = 10 # the radius of the light circles for each light
    Y_INSET = 20 # how low into the square each circle will be
    Y_ALIGN = p_y + Y_INSET # position in the square of where each light is
    X_COORDS = [30, 70, 110] # y coords of each of the three lights of green, yellow and red
    
    pygame.draw.rect(screen, (0,0,0), (p_x, p_y, light_width, light_height)) # builds the square backdrop for seeing lights
    pygame.draw.rect(screen, (255,255,255), (p_x, p_y, light_width, light_height), 1) # builds the square of each light structure section

    pygame.draw.circle(screen,    RED, (p_x + X_COORDS[0], Y_ALIGN), RADIUS, light[0]) # red light on a section
    pygame.draw.circle(screen, YELLOW, (p_x + X_COORDS[1], Y_ALIGN), RADIUS, light[1]) # yellow light on a section
    pygame.draw.circle(screen,  GREEN, (p_x + X_COORDS[2], Y_ALIGN), RADIUS, light[2]) # green light on a section

def build_street_light_direction(screen, p_x, p_y, lights):
    light_gap = 150              # gap between each light in each direction

    left   = p_x                 # left turn right
    middle = p_x + light_gap     # middle straight light
    right  = p_x + (light_gap * 2) # right straight or turn light

    build_street_light(screen,  right, p_y, lights[2][:]) # far right light
    build_street_light(screen, middle, p_y, lights[1][:]) # middle light
    build_street_light(screen,   left, p_y, lights[0][:]) # left turn light

def set_direction_label(screen, p_x, p_y, text):
    coords = [p_x + 100, p_y - 50]
    label = myfont.render(text, 1, YELLOW)
    pygame.draw.rect(screen, YELLOW, (coords[0] - 20,coords[1], 260, 40), 3)
    screen.blit(label, (coords[0], coords[1]))
    
def build_roads(screen):
    road_color = (10,10,10) # light black color
    intersection_color = (255, 255, 255) # white intersection lines
    
    road_width = 200 # width of road for the intersection going north and west
    north_axis = (HEIGHT / 2) - (road_width / 2) # alignment for where the north-bound road will start
    west_axis  = (WIDTH / 2) - (road_width / 2) # alignment for where the west-bound road will start
    
    # draw north-bound road
    pygame.draw.rect(screen, road_color, (0, north_axis, WIDTH, road_width))
    
    # draw west-bound road
    pygame.draw.rect(screen, road_color, (west_axis, 0, road_width, HEIGHT))
    
    # intersecton center variables
    intersection_center_x = (WIDTH  / 2) - (road_width / 2) 
    intersection_center_y = (HEIGHT / 2) - (road_width / 2)
    
    # draw yellow middle lines
    pygame.draw.rect(screen, YELLOW, (WIDTH/2, 0, 10, HEIGHT))
    pygame.draw.rect(screen, YELLOW, (0, HEIGHT/2, WIDTH, 10))
    
        
    #draw intersection square
    pygame.draw.rect(screen, road_color, (intersection_center_x, intersection_center_y, road_width, road_width))
    pygame.draw.rect(screen, intersection_color, (intersection_center_x, intersection_center_y, road_width, road_width), 3)
    pygame.draw.rect(screen, road_color, (intersection_center_x + 3, intersection_center_y + 3, road_width - 10, road_width - 5))

while not game_over:
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            sys.exit()

    screen.fill(BACKGROUND_COLOR)
    
    build_roads(screen)

    HEIGHT_ALIGN = (WIDTH/2) - 220
    WIDTH_ALIGN = (HEIGHT/2) 

    WEST_DIR  = [              20, WIDTH_ALIGN  ]
    SOUTH_DIR = [ HEIGHT_ALIGN, (HEIGHT - 60) ]
    EAST_DIR  = [   (WIDTH - 480), WIDTH_ALIGN  ]
    NORTH_DIR = [ HEIGHT_ALIGN,            60 ]

    set_direction_label(screen, WEST_DIR[0], WEST_DIR[1], "West Light")
    set_direction_label(screen, SOUTH_DIR[0], SOUTH_DIR[1], "South Light")
    set_direction_label(screen, EAST_DIR[0], EAST_DIR[1], "East Light")
    set_direction_label(screen, NORTH_DIR[0], NORTH_DIR[1], "North Light")

    build_street_light_direction(screen,  WEST_DIR[0],  WEST_DIR[1], lightlist[:][0][:]) # WEST light
    build_street_light_direction(screen, SOUTH_DIR[0], SOUTH_DIR[1], lightlist[:][1][:]) # SOUTH light
    build_street_light_direction(screen,  EAST_DIR[0],  EAST_DIR[1], lightlist[:][2][:]) # EAST light
    build_street_light_direction(screen, NORTH_DIR[0], NORTH_DIR[1], lightlist[:][3][:]) # NORTH light
    pygame.display.update()