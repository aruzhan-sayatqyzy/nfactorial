import math
import pygame
from math import atan2, pi
from constants import *

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def calculate_perfectness(points, center_x, center_y, drawing_color, transition_speed):
    if len(points) < 2:
        return 0, drawing_color

    selected_pnts = points[::POINTS_TO_SKIP]
    est_radius = sum(distance(center_x, center_y, x, y) 
    for x, y in selected_pnts) / len(selected_pnts)
    diff = [abs(distance(center_x, center_y, x, y) - est_radius) for x, y in selected_pnts]
    avg_diff = sum(diff) / len(diff)

    perfectness = max(0, (ACCEPTABLE_DIFFERENCE - avg_diff) / ACCEPTABLE_DIFFERENCE) * 100

    if perfectness == 0: 
        return perfectness, RED

    if perfectness >= 90:
        target_color = GREEN
    elif perfectness >= 80:
        interpolation = (perfectness - 80) / 10
        target_color = get_color(interpolation, GREEN, YELLOW)
    elif perfectness >= 70:
        interpolation = (perfectness - 70) / 10
        target_color = get_color(interpolation, YELLOW, RED)
    else:
        target_color = RED

    drawing_color = tuple(int(drawing_color[i] + (target_color[i] - drawing_color[i]) * transition_speed) for i in range(3))
    return [perfectness, drawing_color]

def get_color(interpolation, color1, color2):
    return (
        int((1 - interpolation) * color1[0] + interpolation * color2[0]),
        int((1 - interpolation) * color1[1] + interpolation * color2[1]),
        int((1 - interpolation) * color1[2] + interpolation * color2[2])
    )

def is_circle_closed(current_pos, points):
    return len(points) > 50 and distance(current_pos[0], current_pos[1], points[0][0], points[0][1]) <= 6

def is_close_to_center(current_pos, center_x, center_y):
    return distance(current_pos[0], current_pos[1], center_x, center_y) <= RADIUS

def is_too_slow(error_timer):
    return pygame.time.get_ticks() - error_timer > ERROR_DELAY

def check_wrong_direction(center, last_pos, current_pos, last_angle, max_angle, min_angle):
    dx, dy = current_pos[0] - center[0], center[1] - current_pos[1]
    angle = atan2(dy, dx) % (2 * pi)

    wrong_direction = False
    if last_angle is not None:
      angle_diff = (angle - last_angle + pi) % (2 * pi) - pi 
      if angle_diff > 0: 
          max_angle = max(max_angle, angle) if max_angle is not None else angle
      elif angle_diff < 0: 
          min_angle = min(min_angle, angle) if min_angle is not None else angle

      # if (max_angle is not None and angle < max_angle) or (min_angle is not None and angle > min_angle):
      #     wrong_direction = True

    last_angle = angle

    return wrong_direction, last_angle, max_angle, min_angle