import pygame
import math

TARGET_FPS = 60
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.init()
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('Loading image')
image = pygame.image.load('red_car_small.png')
track_image = pygame.image.load('race_track.png')
car_scale = 3
image = pygame.transform.scale(image, (image.get_width() * car_scale, image.get_height() * car_scale))
car_speed = 1000
rotation_speed = 360

car_x = (window.get_width() - image.get_width()) / 2
car_y = (window.get_height() - image.get_height()) / 2
x = car_x
y = car_y
rotation = 0

# temp variables for debugging
prev_track_x = ''
prev_track_x = ''
distance = 0

running = True
while running:
    delta_time = pygame.time.Clock().tick(TARGET_FPS) / 1000.0

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
        x -= car_speed * delta_time * math.sin(rotation * math.pi / 180)
        y += car_speed * delta_time * math.cos(rotation * math.pi / 180)
    #if keys[pygame.K_DOWN]:    
    #    x += car_speed * delta_time * math.sin(rotation * math.pi / 180)
    #    y -= car_speed * delta_time * math.cos(rotation * math.pi / 180)

    # Move the track so that the same point is still under the car after the rotation
    # Find the position of the car relative to the track centre
    car_rel_track_x = car_x - x
    car_rel_track_y = car_y - y

    # Avoid divide by zero
    if car_rel_track_x == 0:
        car_rel_track_x = 0.0001

    # Calculate the distance from the track centre to the car
    previous_distance = distance
    distance = math.sqrt(car_rel_track_x ** 2 + car_rel_track_y ** 2)

    # Calculate the angle of the car relative to the track centre before rotation
    #angle_before_rotation_rad = math.atan(car_rel_track_y / car_rel_track_x)
    angle_before_rotation_rad = math.acos(car_rel_track_x / distance)
    angle_after_rotation_rad = angle_before_rotation_rad - (rotation * math.pi / 180 ) 

    # Calculate the new position of the car relative to the track centre after rotation
    new_car_rel_track_x = math.cos(angle_after_rotation_rad) * distance
    new_car_rel_track_y = math.sin(angle_after_rotation_rad) * distance

    # Calculate the new position of the track centre
    new_track_x = car_x - new_car_rel_track_x
    new_track_y = car_y - new_car_rel_track_y

    if prev_track_x != '' and ((new_track_x - prev_track_x) ** 2 + (new_track_y - prev_track_y) ** 2) > 5000:
        print(f"rotation: {rotation}")
        print(f"prev_distance: {previous_distance}")
        print(f"distance: {distance}")
        print(f"car_rel_track_x: {car_rel_track_x}")
        print(f"car_rel_track_y: {car_rel_track_y}")
        print(f"angle_before_rotation_rad: {angle_before_rotation_rad}")
        print(f"angle_after_rotation_rad: {angle_after_rotation_rad}")
        print(f"new_car_rel_track_x: {new_car_rel_track_x}")
        print(f"new_car_rel_track_y: {new_car_rel_track_y}")
        pygame.quit()
        quit()

    
    prev_track_x = new_track_x
    prev_track_y = new_track_y

    # Drawing the track with the newly calculated postion and rotation
    rotated_track_image = pygame.transform.rotate(track_image, rotation)
    rotated_track_rect = rotated_track_image.get_rect(center=(new_track_x, new_track_y))
    window.blit(rotated_track_image, rotated_track_rect)

    # Draw the car
    car_rect = image.get_rect(center=(car_x, car_y))
    window.blit(image, car_rect)

    # Update the screen
    pygame.display.update()

    







pygame.quit()
quit()




# Rotating the car
# Background image(s)
# Timer 
# Collision detection + obstacles and walls
# Other cars






 