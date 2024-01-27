import pygame

class Timer:
    def __init__(self, duration, repeated = False, function = None):    
        self.duration = duration
        self.repeated = repeated
        self.function = function

        self.start_time = 0
        self.is_active = False

    def activate(self):
        self.is_active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        self.is_active = False
        self.start_time = 0
        
    def update(self):
        curr_time = pygame.time.get_ticks()

        if curr_time - self.start_time >= self.duration and self.is_active:
            if self.function and self.start_time != 0:
                self.function()

            self.deactivate()

            if self.repeated:
                self.activate()