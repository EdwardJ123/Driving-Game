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
car_acceleration = 500
distance_between_wheels = 20
track_drag = 0.5
grass_drag = 1.5
sand_drag = 10
total_laps = 3


car_x = (window.get_width() - image.get_width()) / 2
car_y = (window.get_height() - image.get_height()) / 2
x = track_image.get_width() / 2
y = track_image.get_height() / 2
rotation = 0
speed = 0
steering_angle = 0
previous_terrain = 'track'
lap = 0
sector = 2

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
        steering_angle = -5
    if keys[pygame.K_RIGHT]:    
        steering_angle = 5
    if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
        steering_angle = 0
    if keys[pygame.K_UP]:    
        speed += car_acceleration * delta_time
    if keys[pygame.K_DOWN]:    
        speed -= car_acceleration * delta_time

    # Determine drag based on surface
    (r, g, b, a) = track_image.get_at((int(x), int(y)))
    terrain = 'track'
    drag = track_drag
    if g > r+10 and g > b+10:
        terrain = 'grass'
        drag = grass_drag
    elif r > b+10 and g > b+10:
        terrain = 'sand'
        drag = sand_drag
    elif r > b + g:
        terrain = 'start_finish'
        drag = track_drag
    elif b > r + g:
        terrain = 'checkpoint'
        drag = track_drag

    # Check if we need to start a new lap
    if sector == 2 and previous_terrain == 'track' and terrain == 'start_finish':
        lap += 1
        sector = 1

    # Check if we passed the checkpoint
    if previous_terrain == 'track' and terrain == 'checkpoint':
        sector = 2

    # Update previous terrain. Any comparisons must be done before this line
    previous_terrain = terrain
    
    # Apply drag
    speed -= drag * speed * delta_time

    #position of wheels at start of frame
    back_wheel_x = x - (0.5 * distance_between_wheels * math.sin(rotation * math.pi / 180))
    back_wheel_y = y + (0.5 * distance_between_wheels * math.cos(rotation * math.pi / 180))
    front_wheel_x = x + (0.5 * distance_between_wheels * math.sin(rotation * math.pi / 180))
    front_wheel_y = y - (0.5 * distance_between_wheels * math.cos(rotation * math.pi / 180))
    
    #positon of wheels at end of frame
    back_wheel_x += speed * delta_time * math.sin(rotation * math.pi / 180)
    back_wheel_y -= speed * delta_time * math.cos(rotation * math.pi / 180)
    front_wheel_x += speed * delta_time * math.sin((rotation + steering_angle) * math.pi / 180)
    front_wheel_y -= speed * delta_time * math.cos((rotation + steering_angle) * math.pi / 180)

    #new car position
    x = (back_wheel_x + front_wheel_x) / 2
    y = (back_wheel_y + front_wheel_y) / 2

    rotation = math.atan2(front_wheel_x - back_wheel_x, back_wheel_y - front_wheel_y) * 180 / math.pi


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
    fps_text = font.render("FPS:  " + str(round(clock.get_fps(), 2)), True, (255, 255, 255))
    window.blit( fps_text, (10, 10))

    # Show Speed
    speed_text = font.render("SPEED:  " + str(round(speed, 2)), True, (255, 255, 255))
    window.blit(speed_text, (10, 30))

    # Show Rotation
    rotation_text = font.render("ROTATION:  " + str(round(rotation, 2)), True, (255, 255, 255))
    window.blit(rotation_text, (10, 50))

    # Show Steering Angle
    steering_angle_text = font.render("STEERING ANGLE:  " + str(round(steering_angle, 2)), True, (255, 255, 255))
    window.blit(steering_angle_text, (10, 70))

    # Show Terrain 
    terrain_text = font.render("TERRAIN " + terrain, True, (255, 255, 255))
    window.blit(terrain_text, (10, 90))

    # Show Lap Count 
    lap_text = font.render("LAP " + str(lap) + '/' + str(total_laps), True, (255, 255, 255))
    window.blit(lap_text, (10, 110))

    # Show Sector
    sector_text = font.render("SECTOR " + str(sector), True, (255, 255, 255))
    window.blit(sector_text, (10, 130))

    # Update the screen
    pygame.display.update()

pygame.quit()
quit()





# Timer 
# Start and finish line 






 