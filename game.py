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
car_scale = 1
image = pygame.transform.scale(image, (image.get_width() * car_scale, image.get_height() * car_scale))
car_acceleration = 400
rotation_speed = 10
distance_between_wheels = 20
drag = 0.01

car_x = (window.get_width() - image.get_width()) / 2
car_y = (window.get_height() - image.get_height()) / 2
x = track_image.get_width() / 2
y = track_image.get_height() / 2
speed = 0
rotation = 0
steering_angle = 0

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

    # Account for drag
    speed -= drag * speed

    # Wheel positions at start of frame
    front_wheel_x = x + (distance_between_wheels / 2) * math.sin(rotation * math.pi / 180)
    front_wheel_y = y + (distance_between_wheels / 2) * -1 * math.cos(rotation * math.pi / 180)
    back_wheel_x = x - (distance_between_wheels / 2) * math.sin(rotation * math.pi / 180)
    back_wheel_y = y - (distance_between_wheels / 2) * -1 * math.cos(rotation * math.pi / 180)

    # Update wheel positions
    back_wheel_x += speed * delta_time * math.sin(rotation * math.pi / 180)
    back_wheel_y -= speed * delta_time * math.cos(rotation * math.pi / 180)
    front_wheel_x += speed * delta_time * math.sin((rotation + steering_angle) * math.pi / 180)
    front_wheel_y -= speed * delta_time * math.cos((rotation + steering_angle) * math.pi / 180)

    # Calculate new position and rotation
    x = (back_wheel_x + front_wheel_x) / 2
    y = (back_wheel_y + front_wheel_y) / 2
    rotation = math.atan2((front_wheel_x - back_wheel_x), (back_wheel_y - front_wheel_y)) * 180 / math.pi

    # Clamp position to ensure we stay on the track
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
    fps_text = font.render("FPS: " + str(round(clock.get_fps(), 2)), True, (255, 255, 255))
    window.blit(fps_text, (10, 10))

    # Show Speed
    speed_text = font.render("Speed: " + str(round(speed, 2)), True, (255, 255, 255))
    window.blit(speed_text, (10, 30))

    # Show Rotation
    rotation_text = font.render("Rotation: " + str(round(rotation, 2)), True, (255, 255, 255))
    window.blit(rotation_text, (10, 50))

    # Show Steering Angle
    steering_text = font.render("Steering angle: " + str(round(steering_angle, 2)), True, (255, 255, 255))
    window.blit(steering_text, (10, 70))

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





 