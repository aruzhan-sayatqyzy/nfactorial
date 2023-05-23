import pygame
from constants import *
from utils import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Perfect Circle")
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2
        self.points = []
        self.drawing = False
        self.last_pos = None
        self.close_to_dot_error= False
        self.slow_eror = False
        self.not_complete_error = False
        self.wrong_way_error = False
        self.error_timer = 0
        self.drawing_color = GREEN
        self.target_color = GREEN
        self.transition_speed = 0.05
        self.perfectness = 100
        self.wrong_sound = pygame.mixer.Sound("wrong.mp3")
        self.good_job_sound = pygame.mixer.Sound("good_job.mp3")
        self.last_angle = None
        self.max_angle = None
        self.min_angle = None

    def reset_game(self):
        self.screen.fill(BLACK)
        self.points.clear()
        self.close_to_dot_error= False
        self.slow_eror = False
        self.not_complete_error = False
        self.error_timer = pygame.time.get_ticks()
        self.draw_center_dot()
        self.last_angle = None
        self.max_angle = None
        self.min_angle = None

    def draw_center_dot(self):
        pygame.draw.circle(self.screen, RED, (self.center_x, self.center_y), 5)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.drawing = True
                self.reset_game()
                self.last_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
          if event.button == 1:
              if self.drawing:
                  self.not_complete_error = True
                  self.error_timer = pygame.time.get_ticks()
                  self.wrong_sound.play()
              self.drawing = False
        elif event.type == pygame.MOUSEMOTION:
            if self.drawing:
                current_pos = event.pos

                wrong_direction, self.last_angle, self.max_angle, self.min_angle = \
                    check_wrong_direction((self.center_x, self.center_y), self.last_pos, current_pos, self.last_angle, self.max_angle, self.min_angle)

                if wrong_direction:
                    self.drawing = False
                    self.wrong_way_error = True
                    self.error_timer = pygame.time.get_ticks()
                    self.wrong_sound.play()

                if is_circle_closed(current_pos, self.points):
                    self.drawing = False
                    if self.perfectness > 90:
                      self.good_job_sound.play()

                self.points.append(current_pos)
                if is_close_to_center(current_pos, self.center_x, self.center_y):
                    self.draw = False; 
                    self.close_to_dot_error= True
                    self.error_timer = pygame.time.get_ticks()
                    pygame.draw.line(self.screen, BLACK, self.last_pos, current_pos, 3)
                    self.wrong_sound.play()
                elif is_too_slow(self.error_timer):
                    self.draw = False; 
                    self.slow_eror = True
                    self.error_timer = pygame.time.get_ticks()
                    pygame.draw.line(self.screen, BLACK, self.last_pos, current_pos, 3)
                    self.wrong_sound.play()
                elif self.perfectness < 5 and len(self.points) > 10:
                    self.drawing = False
                    self.wrong_sound.play()
                else: 
                    pygame.draw.line(self.screen, self.drawing_color, self.last_pos, current_pos, 3)
                    self.last_pos = current_pos
        return True

    def run(self):
        font = pygame.font.Font(None, 24)
        running = True
        while running:
            for event in pygame.event.get():
                running = self.handle_event(event)
            self.draw_center_dot()
            self.perfectness, self.drawing_color = calculate_perfectness(self.points, self.center_x, self.center_y, self.drawing_color, self.transition_speed)

            if pygame.time.get_ticks() - self.error_timer > ERROR_DISPLAY_TIME:
                self.close_to_dot_error= False
                self.slow_eror = False

            if self.close_to_dot_error_visible:
                error_text = font.render("TOO CLOSE TO DOT", True, RED)
                self.screen.blit(error_text, (10, 100))
            elif self.slow_eror:
                error_text = font.render("TOO SLOW", True, RED)
                self.screen.blit(error_text, (10, 100))
            elif self.not_complete_error: 
                error_text = font.render("INCOMPLETE CIRCLE", True, RED)
                self.screen.blit(error_text, (10, 100))
            elif self.wrong_way_error: 
                error_text = font.render("WRONG WAY", True, RED)
                self.screen.blit(error_text, (10, 100))

            perfectness_text = font.render(f"{self.perfectness:.2f}%", True, self.drawing_color)
            self.screen.fill(BLACK, (10, 70, 200, 30))  
            self.screen.blit(perfectness_text, (10, 70))

            if not self.drawing and len(self.points) > 0:
                score_text = font.render(f"Your score is: {self.perfectness:.2f}%", True, WHITE)
                self.screen.blit(score_text, (self.center_x + 10, self.center_y))

            pygame.display.flip()

        pygame.quit()
