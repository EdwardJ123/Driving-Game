import pygame
import math

TARGET_FPS = 60
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.init()
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Loading image')
image = pygame.image.load('red_car_small.png')
track_image = pygame.image.load('race_track.png')
car_scale = 3
image = pygame.transform.scale(image, (image.get_width() * car_scale, image.get_height() * car_scale))
car_speed = 1000
rotation_speed = 360

car_x = (window.get_width() - image.get_width()) / 2
car_y = (window.get_height() - image.get_height()) / 2
x = track_image.get_width() / 2
y = track_image.get_height() / 2
rotation = 0

# temp variables for debugging
prev_track_x = ''
prev_track_x = ''
distance = 0
clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 20)

running = True
while running:
    delta_time = clock.tick(TARGET_FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                break

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:    
        rotation -= rotation_speed * delta_time
    if keys[pygame.K_RIGHT]:    
        rotation += rotation_speed * delta_time
    if keys[pygame.K_UP]:    
        x += car_speed * delta_time * math.sin(rotation * math.pi / 180)
        y -= car_speed * delta_time * math.cos(rotation * math.pi / 180)
    if keys[pygame.K_DOWN]:    
        x -= car_speed * delta_time * math.sin(rotation * math.pi / 180)
        y += car_speed * delta_time * math.cos(rotation * math.pi / 180)

    x = max(min(x, track_image.get_width() - SCREEN_WIDTH), SCREEN_WIDTH)
    y = max(min(y, track_image.get_height() - SCREEN_HEIGHT), SCREEN_HEIGHT)


    # Get relevant part of map, rotate it and draw it to the screen
    center = (x, y)
    dimensions = (SCREEN_WIDTH * 2, SCREEN_HEIGHT * 2)
    smaller_rect = pygame.Rect(center, dimensions)
    smaller_rect.center = center
    smaller_track_image = track_image.subsurface(smaller_rect)
    rotated_smaller_track_image = pygame.transform.rotate(smaller_track_image, rotation)
    rotated_smaller_track_rect = rotated_smaller_track_image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    window.fill((0, 0, 0))
    window.blit(rotated_smaller_track_image, rotated_smaller_track_rect)

    # Draw the car
    car_rect = image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    window.blit(image, car_rect)

    # Show FPS
    fps_text = font.render(str(round(clock.get_fps(), 2)), True, (255, 255, 255))
    window.blit(fps_text, (10, 10))

    # Update the screen
    pygame.display.update()

    







pygame.quit()
quit()




# Background image(s)
# Timer 
#Basic Physics
# Collision detection + obstacles and walls
# Other cars
#Stopping/slowing car leaving track





 