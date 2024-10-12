import pygame
import setting
import images
import graphics


# Class that make diffrent heroes
class HERO :
    def __init__(self , Name , x , y , flipped) :
        self._x = x
        self._y = y 

        #This rectangle is the real objects and 
        self._rect = pygame.Rect((self._x , self._y , 80 ,180))
        self._name = Name

        #The pictures are always to the right orginally. For pictures to reprresent by facing to the left the picture should be flipped
        self._flipped = flipped
        self.__speed_x = eval("setting."+self._name.upper()+"_SPEED") 
        self.__speed_y = 0

        #Every max health depend on the hero 
        self._max_health = setting.HEALTH * eval("setting."+self._name.upper()+"_HEALTH")

        self.health = self._max_health
        self._healbar = pygame.transform.scale(images.other_images["healbar"],(setting.HEALBAR_WIDTH * self.health / self._max_health, setting.HEALBAR_HEGHT ))
        self._current_state = "standing" 

        #This is a stack for recording all states the hero has been in it 
        self._state = ["standing"] 

        self._animation = eval("graphics."+self._state[-1]+"_animation(self._name , [self._x , self._y] )" )

        #This shows the ability of hero to move upward.If false, it cannot
        self.upward_motion = True 

        #these to are atributes for animation. if resume is True the animation would not change 
        self._resume = True
        self._ready_for_new_action = self._animation._resume





    def update (self):

        #changing the lenght of the healbar
        self._healbar = pygame.transform.scale(images.other_images["healbar"],(setting.HEALBAR_WIDTH * self.health / self._max_health , setting.HEALBAR_HEGHT ))

        # updates state stack of state has been updated
        if (self._current_state != self._state[-1]) and not self.gameover_check() :
            self._state.append(self._current_state)
            self._animation = eval("graphics."+self._state[-1]+"_animation(self._name , [self._x , self._y] )")

        self._ready_for_new_action = self._animation._resume

        #this is for when that a animation has been done so charackter should do another thing
        if  not self._ready_for_new_action :
            self._current_state = self._state [-2] 

        if self.health == 0 :
            self.die()
        self._animation.update()
        self._animation.flip_update(eval(self._flipped))
        self._animation._position = [self._x , self._y]
    
    #checking that if the game is over or not
    def gameover_check(self):
        if "win" in self._state or "death" in self._state :
            return True
        else:
            return False

        #This is how gravity effects on the object
    def gravity_effect(self):
            self.__speed_y += setting.GRAVITY
            self._y += self.__speed_y


    def move_right (self):

        if self._current_state == "standing" or self._current_state == "walking" or self._current_state == "jump" :
            self._x += self.__speed_x
            self._flipped = "False"
            if self._current_state != "jump" :
                self._current_state =  "walking"
              
    
    def move_left (self):
        if self._current_state == "standing" or self._current_state == "walking" or self._current_state == "jump" or self._current_state == "crouch":
            self._flipped = "True"
            if   self._current_state == "standing" or self._current_state == "walking" or self._current_state == "jump"  :     
                self._x -= self.__speed_x
                if self._current_state != "jump" :
                    self._current_state = "walking"


    def jump (self) :

        if self._current_state == "standing" or self._current_state == "walking" or self._current_state == "jump":
            self._current_state = "jump"
            if self.upward_motion :
                self.__speed_y = -setting.V0_JUMP
                self._y += self.__speed_y 
        
    
    def Punch (self) :
        self._current_state = "punch"


    #if the other players has punched succsessfully 
    def punched (self) :
        if self._current_state != "crouch":
            if self.health > 5 :
                self.health -= setting.PUNCH_POWER
                self._current_state = "hitted"

            else :
                self.health =0

    def kick (self) :
        self._current_state = "kick"

    #if the other player has kicked successfully
    def kicked (self) :
        if self._current_state != "crouch":
            if self.health > 5 :
                self.health -= setting.PUNCH_POWER
                self._current_state = "hitted"

            else :
                self.health =0

    def crouch (self) :
        if self._current_state != "dead" and self._current_state != "jump":
            self._current_state = "crouch"
   
    def uncrouch (self) :
        self._current_state = "standing"

    def die (self):
        self._current_state = "death"

     
    def win (self):
        self._current_state = "win"



    def draw(self , surface ) :
        self._animation.draw()

