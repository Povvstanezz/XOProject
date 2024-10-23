import pygame

class Button():
    def __init__(self, size=(200,50), text='button', bg_color=(120, 120, 120), text_color=(0,0,0)):
        pygame.font.init()
        self.button_surface = pygame.Surface(size)
        self.button_surface.fill(bg_color)
        
        self.cup_surface = pygame.Surface(size)
        # self.cup
        
                
        self.size = size
        self.button_text = pygame.font.Font('Arima.ttf', 34)
        self.text_surface = self.button_text.render(text, False, text_color)
        self.border_data = self.button_surface.get_rect()
        
        self.border = pygame.draw.rect(self.button_surface, (0,0,0), self.border_data, 1)

        self.btn_surface_size = self.button_surface.get_size()
        self.text_size = self.text_surface.get_size()

        self.text_pos = (self.btn_surface_size[0]/2 - self.text_size[0]/2, self.btn_surface_size[1]/2 - \
                         self.text_size[1]/2)
        
        # print(self.btn_surface_size)
        # print(self.text_size)
        # print(self.text_pos)

        self.button_surface.blit(self.text_surface, (self.text_pos))
    
    def button_surface(self):
            return self.button_surface
        
    def on_mouse_motion(self, btn_start_pos, mouse_pos):
        btn_end_pos = btn_start_pos[0] + self.size[0], btn_start_pos[1] + self.size[1]   
        if mouse_pos[0] > btn_start_pos[0] and mouse_pos[0] < btn_end_pos[0] and \
            mouse_pos[1] > btn_start_pos[1] and mouse_pos[1] < btn_end_pos[1]:
            self.cup_surface.fill((0, 0, 0))
            # btn_rect = pygame.draw.rect(self.button_surface, (100, 100, 100), (btn_start_pos, self.size))  
            self.button_surface.blit(self.cup_surface, (0, 0))
            return True
        
    def get_button_surface(self):
        return self.button_surface
    
    def click(self):
        pass

if __name__ == '__main__':
    btn = Button()