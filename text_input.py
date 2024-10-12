import pygame
import tkinter 
from tkinter import simpledialog


#these are input box inside the game(USED FOR LOGGING IN)
class text_input :
    def __init__ (self, font, max , min , x , y  , width, height  , screen) :
        self._text = ""
        self._font = font 
        self.__max_length = max
        self.__min_length = min
        self.__height = height
        self.__width = width
        self.__x =x
        self.__y = y
        #2 colour would be needed one for pasive input box the other for the active one
        self.__passive_color = (100,100,100)
        self.__active_color = (255,255,255)
        self._color = self.__passive_color
        self._rect = pygame.Rect(self.__x, self.__y,self.__width, self.__height)
        #input is nothing at first which is not valid
        self._valid = False 
        self._screen = screen
        self._selected = False

    def erasing (self):
        if self._selected:
            if len(self._text) > 0 :
                self._text = self._text[:-1]
                pygame.display.flip()
                if len(self._text) < self.__min_length  :
                    self._valid = False

    def typing (self , letter ):
        if self._selected:
            if len(self._text) <= self.__max_length:
                self._text += letter
                pygame.display.flip()
    #selecting the input box
    def select(self):
        self._color = self.__active_color
        self._selected = True
    def deselect(self):
        self._color = self.__passive_color
        self._selected = False

    def draw(self):
        pygame.draw.rect(self._screen, self._color, self._rect)
        self._screen.blit(self._font.render(self._text, True, (0,0,0)), (self._rect.x+5, self._rect.y+5))


#these are kind of input box which the written charackters are hidden (USED FOR PASSWORDS)
class hidden_text_input (text_input):
    def __init__(self, font, max, min, x, y, width, height, screen):
        super().__init__(font, max, min, x, y, width, height, screen)
    def draw(self):
        pygame.draw.rect(self._screen, self._color, self._rect)
        self._screen.blit(self._font.render("*"*len(self._text), True, (0,0,0)), (self._rect.x+5, self._rect.y+5))



#these are input box which pop out (USED FOR SIGNING UP)
class input_box :
    def __init__(self ,title,prompt  ):
        self._root = tkinter.Tk()
        self._prompt = prompt
        self._title = title

    def set_title_and_propt (self ,title,prompt ):
        self._prompt = prompt
        self._title = title
       
    def get_input (self):
        self._root.withdraw()
        return str(simpledialog.askstring(title=self._title,prompt=self._prompt))
    
#child of input box which make the input hidden aswell
class hidden_input_box(input_box):
    def __init__(self, title, prompt):
        input_box.__init__(self , title, prompt)
    def get_input(self):
        self._root.withdraw()
        return str(simpledialog.askstring(title=self._title,prompt=self._prompt , show= "*"))


