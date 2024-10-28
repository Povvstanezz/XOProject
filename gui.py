import pygame

class Button():
    def __init__(self, size=(200,50), text='button', bg_color=(120, 120, 120), text_color=(0,0,0)):

        self.button_surface = pygame.Surface(size)                
        self.size = size
        self.btn_surface_size = self.button_surface.get_size()
        self.border = self.button_surface.get_rect()
        pygame.draw.rect(self.button_surface, (180,180,180), (0,0,200,50))

        pygame.font.init()
        
        self.button_font = pygame.font.FontType('Arima.ttf', 32)
        self.text_surface = self.button_font.render('Start GAME!', False,(0,0,0))
        self.text_size = self.text_surface.get_size()
        self.text_pos = (self.btn_surface_size[0]/2 - self.text_size[0]/2, self.btn_surface_size[1]/2 - \
                self.text_size[1]/2)
        self.button_surface.blit(self.text_surface, self.text_pos)
        self.button_norm()


    def button_hover(self):
        pygame.draw.rect(self.button_surface, (180,180,180), (0,0,200,50))
        pygame.draw.rect(self.button_surface,(0,0,0), self.border, 1)
        self.update()
    
    def button_norm(self):
        pygame.draw.rect(self.button_surface, (150,150,150), (0,0,200,50))
        self.update()
        return False


    def on_mouse_over(self, btn_start_pos, mouse_pos):
        btn_end_pos = btn_start_pos[0] + self.size[0], btn_start_pos[1] + self.size[1]

        if mouse_pos[0] > btn_start_pos[0] and mouse_pos[0] < btn_end_pos[0] and \
            mouse_pos[1] > btn_start_pos[1] and mouse_pos[1] < btn_end_pos[1]:
            self.button_hover()
            return True
        else:
            self.button_norm()
            return False
        
        
    def get_button_surface(self):
        return self.button_surface
    
    def click(self, btn_start_pos, mouse_pos):
        if self.on_mouse_over(btn_start_pos, mouse_pos):
            print('Click!')
            return True

    def update(self):
        self.button_surface.blit(self.text_surface, self.text_pos)
    

if __name__ == '__main__':
    btn = Button()