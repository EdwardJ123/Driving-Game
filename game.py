import pygame
import math

TARGET_FPS = 60
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

DEBUG = False

pygame.init()
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Speed!')

title_screen_image = pygame.image.load('Title Screen.png')
finish_screen_image = pygame.image.load('finish_screen.png')
car_image = pygame.image.load('red_car_small.png')
track_image = pygame.image.load('race_track.png')
car_acceleration = 500
distance_between_wheels = 20
track_drag = 0.5
grass_drag = 1.5
sand_drag = 10
max_laps = 3

def init_game_state():
    global car_x, car_y, x, y, rotation, speed, steering_angle, laps, sector, previous_terrain, lap_times, running_time
    car_x = (window.get_width() - car_image.get_width()) / 2
    car_y = (window.get_height() - car_image.get_height()) / 2
    x = track_image.get_width() / 2
    y = track_image.get_height() / 2
    rotation = 0
    speed = 0
    steering_angle = 0
    laps = 0
    sector = 2
    previous_terrain = 'track'
    lap_times = []
    running_time = 0

def format_time(time):
    minutes = math.floor(time/60)
    seconds = math.floor(time%60)
    milliseconds = round((time - math.floor(time)) * 1000)
    return str(minutes).zfill(2) + ':' + str(seconds).zfill(2) + '.' + str(milliseconds).zfill(3)

init_game_state()

state = 'title screen'

clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 20)

while state != 'quit':
    # Time elapsed since the previous frame
    delta_time = clock.tick(TARGET_FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state = 'quit' 
            break
        elif event.type == pygame.KEYDOWN:
            if state == 'running' or state == 'finish_screen':
                if event.key == pygame.K_ESCAPE:
                    state = 'title screen'
                    break
            elif state == 'title screen':
                init_game_state()
                state = 'running'
    

    keys = pygame.key.get_pressed()
    if state == 'running':
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
    elif r > g + 10 and r > b + 10:
        terrain = 'start_line'
        drag = track_drag
    elif b > r + g:
        terrain = 'checkpoint'
        drag = track_drag
    
    # Apply drag
    speed -= drag * speed * delta_time

    # position of wheels at start of frame
    back_wheel_x = x - (0.5 * distance_between_wheels * math.sin(rotation * math.pi / 180))
    back_wheel_y = y + (0.5 * distance_between_wheels * math.cos(rotation * math.pi / 180))
    front_wheel_x = x + (0.5 * distance_between_wheels * math.sin(rotation * math.pi / 180))
    front_wheel_y = y - (0.5 * distance_between_wheels * math.cos(rotation * math.pi / 180))
    
    # positon of wheels at end of frame
    back_wheel_x += speed * delta_time * math.sin(rotation * math.pi / 180)
    back_wheel_y -= speed * delta_time * math.cos(rotation * math.pi / 180)
    front_wheel_x += speed * delta_time * math.sin((rotation + steering_angle) * math.pi / 180)
    front_wheel_y -= speed * delta_time * math.cos((rotation + steering_angle) * math.pi / 180)

    # new car position
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

    # Check for lap completion
    if previous_terrain == 'start_line' and terrain == 'track' and sector == 2:
        laps += 1
        sector = 1
        if laps > max_laps:
            state = 'finish_screen'
        else:
            lap_times.append(0)

    if previous_terrain == 'checkpoint' and terrain == 'track':
        sector = 2

    previous_terrain = terrain

    if len(lap_times) > 0 and state == 'running':
        lap_times[-1] += delta_time
        running_time += delta_time

    # Draw the car
    car_rect = car_image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    window.blit(car_image, car_rect)

    # Show Laps
    laps_text = font.render("LAPS " + str(laps) + "/" + str(max_laps), True, (255, 255, 255))
    window.blit(laps_text, (10, 10))

    # Show Sector
    sector_text = font.render("SECTOR " + str(sector), True, (255, 255, 255))
    window.blit(sector_text, (10, 30))

    if DEBUG:
        # Show FPS
        fps_text = font.render("FPS:  " + str(round(clock.get_fps(), 2)), True, (255, 255, 255))
        window.blit( fps_text, (10, 130))

        # Show Speed
        speed_text = font.render("SPEED:  " + str(round(speed, 2)), True, (255, 255, 255))
        window.blit(speed_text, (10, 150))

        # Show Rotation
        rotation_text = font.render("ROTATION:  " + str(round(rotation, 2)), True, (255, 255, 255))
        window.blit(rotation_text, (10, 170))

        # Show Steering Angle
        steering_angle_text = font.render("STEERING ANGLE:  " + str(round(steering_angle, 2)), True, (255, 255, 255))
        window.blit(steering_angle_text, (10, 190))

        # Show Terrain 
        terrain_text = font.render("TERRAIN " + terrain, True, (255, 255, 255))
        window.blit(terrain_text, (10, 230))

    # Show Lap Times
    for i, time in enumerate(lap_times):
        lap_time_text = font.render(str(i+1) + ' - ' + format_time(time), True , (255, 255, 255))
        window.blit(lap_time_text, (10,70 + i * 20))
    
    # Show Running Time
    running_time_text = font.render("RUNNING TIME: " + format_time(running_time), True, (255, 255, 255))
    window.blit(running_time_text, (10, 50))

    if state == 'title screen':
        title_screen_rect = title_screen_image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        window.blit(title_screen_image, title_screen_rect)
    
    if state == 'finish_screen':
        finish_screen_rect = finish_screen_image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        running_time_text = font.render("RUNNING TIME: " + format_time(running_time), True, (242, 13, 13))
        window.blit(finish_screen_image, finish_screen_rect)
        window.blit(running_time_text, (250, 270))
        for i, time in enumerate(lap_times):
            lap_time_text = font.render(str(i+1) + ' - ' + format_time(time), True , (242, 13, 13))
            window.blit(lap_time_text, (320,290 + i * 20))
        instructions_text = font.render("Press ESC to return to title screen", True, (242, 13, 13))
        window.blit(instructions_text, (235, 370))

    # Update the screen
    pygame.display.update()
    
pygame.quit()
quit()








 