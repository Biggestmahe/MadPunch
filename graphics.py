import setting
import pygame
import images


#parent class for all animations
class animation :
    def __init__(self , hero , act, time , position ):
        self.__hero = hero
        self._list = images.hero[self.__hero][act]
        #every hero has it own speed
        self._time = time* eval("setting."+self.__hero.upper()+"_SPEED")
        #counting the time that has been passed 
        self._update_time = pygame.time.get_ticks()
        self._frame_index = 0
        self._position = position
        #pictures should be fit on squers of players so their posision should always be shifted with a constant amount every time
        self._hero_first_position =eval("setting."+self.__hero.upper()+"_FIRST_POSITION")
        #pictures of heroes should be scaled
        self._scale =eval("setting."+self.__hero.upper()+"_SCALE")
        self._image =  self._list[self._frame_index]
        self._resume = True
        #the same flip as the one in stages file
        self.__flipped = False
        self.n=0


    def update (self):
        pass

    #flippinf the picture if needed 
    def flip_update (self , flip):
        self.__flipped = flip
        self._image = pygame.transform.flip(self._image, self.__flipped , False)
        if self.__flipped :
            #the amount of shifting pictures to fit the square if pictures are flipped
            self._hero_first_position =eval("setting."+self.__hero.upper()+"_FIRST_POSITION_FLIPPED")

        else :
            self._hero_first_position =eval("setting."+self.__hero.upper()+"_FIRST_POSITION") 
        
        
    def draw (self):
        setting.SCREEN.blit(pygame.transform.scale(self._image , self._scale) ,( self._position[0] + self._hero_first_position[0]  ,self._position[1] + self._hero_first_position[1] ))


#some animations should be repeated when all the pictures in the list has been used
class repeating_animation (animation):
    def __init__(self, hero, act , time, position):
        super().__init__(hero, act, time , position)

    def update(self):
        self._image =  self._list[self._frame_index]
        if pygame.time.get_ticks()-self._update_time > self._time :
            self._frame_index += 1
            self._frame_index = self._frame_index % (len(self._list) - 1)
            self._update_time = pygame.time.get_ticks()
    
#some animation should stay in their final index after reaching it
class unrepeating_animation (animation):
    def __init__(self, hero, act, time, position):
        super().__init__(hero, act, time, position )

    def update(self):
        self._image =  self._list[self._frame_index]
        if (pygame.time.get_ticks()-self._update_time >self._time) and (self._frame_index != (len(self._list) - 1)):
            self._frame_index += 1  
            self._update_time = pygame.time.get_ticks()  

            

                               
#after some list has bean reached the end, the action has to be change 
class acting_animation(animation) :
    def __init__(self, hero, act, time, position):
        super().__init__(hero, act, time, position )

    def update(self):
        self._image =  self._list[self._frame_index]
        if (self._frame_index != (len(self._list) - 1)) :
            if (pygame.time.get_ticks()-self._update_time > self._time) :
                self._frame_index += 1  
                self._update_time = pygame.time.get_ticks()  
        else:
            self._resume = False

class walking_animation(repeating_animation):
    def __init__(self, hero, position ):
        super().__init__(hero, "walking", setting.WALKING_SPEED, position )

class standing_animation(repeating_animation):
    def __init__(self, hero,  position ):
        super().__init__(hero, "standing", setting.STANDING_SPEED, position )



class jump_animation(unrepeating_animation) :
    def __init__(self, hero, position ):
        super().__init__(hero, "jump", setting.JUMP_SPEED, position )

class crouch_animation(unrepeating_animation) :
    def __init__(self, hero,  position):
        super().__init__(hero, "crouch", setting.CROUCH_SPEED, position)

class death_animation(unrepeating_animation) :
    def __init__(self, hero,  position ):
        super().__init__(hero, "death", setting.DEAD_SPEED, position) 

class win_animation(unrepeating_animation) :
    def __init__(self, hero,  position):
        super().__init__(hero, "win", setting.WIN_SPEED, position) 

    def update(self):
        self._image =  self._list[self._frame_index]
        if (self._frame_index == (len(self._list) - 1)):
            if pygame.time.get_ticks()-self._update_time > setting.END_DELAY :
                self._resume = False
    
        elif (pygame.time.get_ticks()-self._update_time >self._time) and (self._frame_index <= (len(self._list) -1 )):
            self._frame_index += 1  
            self._update_time = pygame.time.get_ticks()  


class punch_animation (acting_animation):
    def __init__(self, hero, position ):
        super().__init__(hero,"punch", setting.PUNCH_SPEED, position )

class kick_animation (acting_animation):
    def __init__(self, hero,  position):
        super().__init__(hero,"kick", setting.KICK_SPEED, position )

class hitted_animation (acting_animation):
    def __init__(self, hero, position ):
        super().__init__(hero,"hitted", setting.HITTED_SPEED, position)


#this is the animation for shading texts
class shading_text_animation :
    def __init__ (self, text , height , width , x , y , shade_number , text_size , time):
        self._time = time
        self._update_time = pygame.time.get_ticks()
        self.__height = height
        self.__width = width
        self.__x = x
        self.__y = y
        self.__text = text
        self.__shade_number = shade_number
        self.__text_size = text_size
        self.__list = images.shade(self.__text  , self.__shade_number  , self.__width ,self.__height , self.__text_size)
        self.__frame_index = 0
        self.__image = self.__list[self.__frame_index]

    #updating the current index after a amount of time
    def update (self):
        self._image =  self.__list[self.__frame_index]
        if self.__frame_index != self.__shade_number-1 and (pygame.time.get_ticks()-self._update_time >self._time) :
            self.__frame_index += 1
            self._update_time = pygame.time.get_ticks()  

    def draw (self):
        setting.SCREEN.blit(self._image  ,( self.__x  ,self.__y))



