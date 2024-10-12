import pygame
import setting
import images 
import heroes
import graphics
import os
import text_input
from cryptography.fernet import Fernet
import database
import ctypes 

#this is the  parent class for all the classes
class stage :
    def __init__ (self , background ):
        self.__height =  setting.SCREEN_HEIGHT
        self.__width =  setting.SCREEN_WIDTH
        self._background = pygame.transform.scale(images.background[background],(self.__width , self.__height ))

        #this is the what the current stage is 
        self.current_stage = "stages.start_stage()"


    def event_check (self,event):
        if event.type == pygame.QUIT:
         exit()

    def draw_screen (self ):
        setting.SCREEN.blit(self._background , (0 , 0))

    def Key_check (self):
        pass
    def update (self):
        pass
    def update_db (self):
        database.connection.commit()

#this is the stage for main menue
class start_stage(stage):
    def __init__ (self):
        stage.__init__(self , 0 )


    def event_check (self,event): 
        if event.type == pygame.MOUSEBUTTONUP :
            mouse_pos = pygame.mouse.get_pos()

            #checking that the exit buttom has been clicked
            if 512 > mouse_pos[0] > 286     and   422 > mouse_pos[1] > 355 :
                exit()

            #checking if the play buttom has been clicked
            elif 514 > mouse_pos[0] > 286 and 308 > mouse_pos[1] > 240 :
                self.current_stage= "stages.log_in()"

        if event.type == pygame.QUIT:
         exit()

class log_in (stage) :
    def __init__(self):
        stage.__init__(self , 5)

        #These are input box
        self._player1_username = text_input.text_input( pygame.font.Font(None, 24), setting.MAX_LETTERS_USERNAME , setting.MIN_LETTERS_USERNAME, 200 , 150  , 110, 30  , self._background)
        self.__player1_password = text_input.hidden_text_input( pygame.font.Font(None, 48), setting.MAX_LETTERS_PASSWORD , setting.MAX_LETTERS_PASSWORD , 200 , 300  , 110, 30  , self._background)
        self._player2_username = text_input.text_input( pygame.font.Font(None, 24), setting.MAX_LETTERS_USERNAME , setting.MIN_LETTERS_USERNAME, 550 , 150  , 110, 30  , self._background)
        self.__player2_password = text_input.hidden_text_input( pygame.font.Font(None, 48), setting.MAX_LETTERS_PASSWORD , setting.MAX_LETTERS_PASSWORD , 550 , 300 , 110, 30  , self._background)

        #these are buttoms in the window
        self.__OK_buttom = images.shade(" OK" , 1 , 100, 65 ,50)[0]
        self.__sign_up_buttom__OK_buttom = images.shade("Don't have an account? sign up!" , 1, 260, 40, 24)[0]

        #these are notes that will be shown in the window
        self.__player1_log_in_text = pygame.font.Font(None, 60).render('PLAYER 1', True,"WHITE")
        self.__player2_log_in_text = pygame.font.Font(None, 60).render('PLAYER 2', True, "WHITE")
        self.__log_in_text = pygame.font.Font(None, 24).render('USERNAME:', True, "WHITE")
        self.__password_text = pygame.font.Font(None, 24).render('PASSWORD:', True, "WHITE")
        self.__input_getter = text_input.input_box(None , None)

    #this is how users can sign up
    def sign_up (self):
        
        #poping out the username window
        self.__input_getter.set_title_and_propt("username" , "put a username")
        username = str(self.__input_getter.get_input())
        #checking the input is valid
        while not  setting.MIN_LETTERS_USERNAME < len(username) <setting.MAX_LETTERS_USERNAME+2 or  username == "None":
            if username == "None" :
                return([None , None])           
            #if not valid, pops out the window again
            self.__input_getter.set_title_and_propt("username" , "username has to have 4 up to 10 characters.")
            username = str(self.__input_getter.get_input())

        #poping out the password window
        self.__input_getter=text_input.hidden_input_box(None , None)
        self.__input_getter.set_title_and_propt("password" , "put a password")
        password = str(self.__input_getter.get_input())
        #checking that if the password is valid or not
        while not setting.MIN_LETTER_PASSWORD < len(password) <setting.MAX_LETTERS_PASSWORD+2 :
            if password == "None" :
                self.__input_getter = text_input.input_box(None , None)
                return [None , None]           
            #if password is not valid, pops out the window again
            self.__input_getter.set_title_and_propt("password" , "password has to have 6 to 8 characters.")
            password = str(self.__input_getter.get_input())

        #poping out the window for second password
        self.__input_getter.set_title_and_propt("password" , "repeat the password")
        repassword = str(self.__input_getter.get_input())
        #checking if the second password is as same as the first one
        while repassword != password :
            if repassword == "None" :
                self.__input_getter = text_input.input_box(None , None)
                return [None , None]
            #if passwords are not the same, pops the second password window again
            self.__input_getter.set_title_and_propt("password" , "Wrong! try again.")
            repassword = str(self.__input_getter.get_input())

        self.__input_getter = text_input.input_box(None , None)

        #this is how password will be crypted
        key = Fernet.generate_key()
        fernet = Fernet(key)
        encpassword = fernet.encrypt(password.encode())

        #entering data to the database
        id = database.cursor.execute('SELECT COUNT(*) from tblUserData').fetchone()[0] +1
        #id , username encrypted password and the key of cryption would be saved
        data = [(id ,username , encpassword , key , 0, 0, 0, 0)]  
        #here we check if the username is new or has been taken
        if data != [None , None]:
            #if try works, the username is unique and data would be entered the database
            try:
                database.cursor.executemany("INSERT INTO tblUserData VALUES (?,?,?,?,?,?,?,?)" , data)
                database.connection.commit()
                ctypes.windll.user32.MessageBoxW(0, "You signed up successfully!", "sign up", 1)
            #this is for the time the username was taken and data could not be added to database
            except :
                self.__input_getter = text_input.input_box(None , None)
                ctypes.windll.user32.MessageBoxW(0, "The username is taken.", "error", 1)
    

    #This is how usernames los in
    def log_in(self) :
        #getting passwords keys of passwords from database
        database.cursor.execute("SELECT Password , Key FROM tblUserData WHERE Username = (?)" ,[( self._player1_username._text)])
        Key_pad_player1 = database.cursor.fetchall()
        database.cursor.execute("SELECT Password , Key FROM tblUserData WHERE Username = (?)", [(self._player2_username._text)])
        Key_pad_player2 = database.cursor.fetchall()

        try:
            #checking if the first user input is as same as decrepted password in database
            if str(Fernet(Key_pad_player1[0][1]).decrypt(Key_pad_player1[0][0].decode()) , 'utf-8') == self.__player1_password._text :
                #checking if the second user input is as same as decrepted password in database
                if str(Fernet(Key_pad_player2[0][1]).decrypt(Key_pad_player2[0][0].decode()) , 'utf-8') == self.__player2_password._text :
                    #checking if two users are not useing tha same acount
                    if self._player1_username != self._player2_username :
                                self.current_stage = "stages.player_choosing_1( current_stage._player1_username._text , current_stage._player2_username._text )"
                    else:
                                ctypes.windll.user32.MessageBoxW(0, "You need 2 accounts! ", "error", 1)
                else:
                            ctypes.windll.user32.MessageBoxW(0, "Username or password of the player 2 is wrong! ", "error", 1)
            else :
                        ctypes.windll.user32.MessageBoxW(0, "Username or password of the player 1 is wrong!", "error", 1)
        except:
            ctypes.windll.user32.MessageBoxW(0, "please put your username and password", "error", 1)


    def draw_screen(self):
        setting.SCREEN.blit(self._background , (0 , 0))
        self._player1_username.draw()
        self._player2_username.draw()
        self.__player1_password.draw()
        self.__player2_password.draw()
        self._background.blit(self.__player1_log_in_text , (120 , 80))
        self._background.blit(self.__player2_log_in_text , (460 , 80))
        self._background.blit(self.__log_in_text, (100 , 155))
        self._background.blit(self.__log_in_text , (450 , 155))
        self._background.blit(self.__password_text, (100 , 305))
        self._background.blit(self.__password_text , (450 , 305))   
        self._background.blit(self.__OK_buttom , (340 , 370))
        self._background.blit(self.__sign_up_buttom__OK_buttom ,( 270,450))
     
       

    def event_check(self, event):

        if event.type == pygame.QUIT:
         exit()

         #these are fo activing and deactiving input boxes
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.__player1_password._rect.collidepoint(event.pos):
                self.__player1_password.select()
                self._player1_username.deselect()  
                self.__player2_password.deselect()
                self._player2_username.deselect()
            elif self._player1_username._rect.collidepoint(event.pos):
                self.__player1_password.deselect()
                self._player1_username.select()  
                self.__player2_password.deselect()
                self._player2_username.deselect()                  
        
            elif self.__player2_password._rect.collidepoint(event.pos):
                self.__player1_password.deselect()
                self._player1_username.deselect()  
                self.__player2_password.select()
                self._player2_username.deselect()
            elif self._player2_username._rect.collidepoint(event.pos):
                self.__player1_password.deselect()
                self._player1_username.deselect()  
                self.__player2_password.deselect()
                self._player2_username.select()  
            
            #checking of the OK butom has been clicked
            elif  340<pygame.mouse.get_pos()[0] <440 and 370 <pygame.mouse.get_pos()[1] < 430 :
                self.log_in()

            #checking if the sign up buttom is pressed
            elif  270<pygame.mouse.get_pos()[0] <530 and 450 <pygame.mouse.get_pos()[1] < 485 :
                self.sign_up()
     
        #getting keys as inputs
        if event.type  == pygame.KEYDOWN:
            #if input is backspace input should be ereased
            if event.key == pygame.K_BACKSPACE:
                self.__player1_password.erasing()
                self._player1_username.erasing()  
                self.__player2_password.erasing()
                self._player2_username.erasing()  

            else :
                self.__player1_password.typing(event.unicode)
                self._player1_username.typing(event.unicode)  
                self.__player2_password.typing(event.unicode)
                self._player2_username.typing(event.unicode)                               

  #this is the parent class for choosing sections (player 1, player2 and wallpaper)              
class choosing (stage ):

    def __init__ (self , player1 , player2 , wallpaper ,  player1_username , player2_username ):
        stage.__init__(self , 5)
        self._player1 = player1
        self._player2 = player2
        self._wallpaper = wallpaper
        self._player1_username = player1_username
        self._player2_username = player2_username


#this is where the first player chooses a hero
class player_choosing_1 (choosing) :

    def __init__(self , player1_username , player2_username):
        choosing.__init__(self, None , None , None , player1_username , player2_username )

    def draw_screen(self):
        setting.SCREEN.blit(self._background , (0 , 0))
        setting.SCREEN.blit(pygame.transform.scale(images.other_images["logo"] , (200,200) ), (300,0))
        #These are the drawn pictures for heroes
        setting.SCREEN.blit(pygame.transform.scale(images.hero["Behrad"]["choosing_section"][0] , (setting.PROFILE_WIDTH , setting.PROFILE_HEIGHT)) ,(0 , 130 ))
        setting.SCREEN.blit(pygame.transform.scale(images.hero["Reina"]["choosing_section"][0] , (setting.PROFILE_WIDTH , setting.PROFILE_HEIGHT)) ,(360 , 130 ))
        setting.SCREEN.blit(pygame.transform.scale(images.hero["Kenny"]["choosing_section"][0] , (setting.PROFILE_WIDTH , setting.PROFILE_HEIGHT)) ,(120, 130 ))

        m=0
        for a_hero in images.hero :   
            #here we sho bottoms to be clicked on incase of willind to choose a hero         
            setting.SCREEN.blit(pygame.transform.scale(images.other_images[a_hero + " profile"] , (2 * setting.PROFILE_REDIUS , 2 * setting.PROFILE_REDIUS)) , (120 + 200 * m,400))
            m += 1

    def event_check (self,event): 
        #checking which hero has beein chosen
        if event.type == pygame.MOUSEBUTTONUP :
            mouse_pos = pygame.mouse.get_pos()
            if setting.distance(mouse_pos , (160 , 440)) < 45 :
                self._player1 = "Behrad"
                self.current_stage= "stages.player_choosing_2('Behrad' , current_stage._player1_username ,current_stage._player2_username)"


            elif setting.distance(mouse_pos , (360 , 440)) < 45 :
                self._player1 = "Kenny"
                self.current_stage= "stages.player_choosing_2('Kenny', current_stage._player1_username ,current_stage._player2_username)"

            elif setting.distance(mouse_pos , (560 , 440)) < 45 :
                self._player1 = "Reina"
                self.current_stage= "stages.player_choosing_2('Reina', current_stage._player1_username ,current_stage._player2_username)"


        if event.type == pygame.QUIT:
         exit()

#here user 2 chooses a hero
class player_choosing_2 (choosing) :

    def __init__(self , player1 , player1_username , player2_username):
        choosing.__init__(self , player1, None , None , player1_username , player2_username)

    def draw_screen(self):
        setting.SCREEN.blit(self._background , (0 , 0))
        setting.SCREEN.blit(pygame.transform.scale(images.other_images["logo"] , (200,200) ), (300,0))
        if self._player1 != "Behrad":
            setting.SCREEN.blit(pygame.transform.scale(images.hero["Behrad"]["choosing_section"][0] , (setting.PROFILE_WIDTH , setting.PROFILE_HEIGHT)) ,(0 , 130 ))
        if self._player1 != "Reina":    
            setting.SCREEN.blit(pygame.transform.scale(images.hero["Reina"]["choosing_section"][0] , (setting.PROFILE_WIDTH , setting.PROFILE_HEIGHT)) ,(360 , 130 ))
        if self._player1 != "Kenny":
            setting.SCREEN.blit(pygame.transform.scale(images.hero["Kenny"]["choosing_section"][0] , (setting.PROFILE_WIDTH , setting.PROFILE_HEIGHT)) ,(120, 130 ))

        m=0
        for a_hero in images.hero :   
            if a_hero != self._player1:         
                setting.SCREEN.blit(pygame.transform.scale(images.other_images[a_hero + " profile"] , (2 * setting.PROFILE_REDIUS , 2 * setting.PROFILE_REDIUS)) , (120 + 200 * m,400))
            m += 1
    def event_check (self,event): 
        if event.type == pygame.MOUSEBUTTONUP :
            mouse_pos = pygame.mouse.get_pos()
            
            if setting.distance(mouse_pos , (160 , 440)) < 45 :
                if self._player1 != "Behrad":
                    self._player2 = "Behrad"
                    self.current_stage= "stages.wallpaper_choosing(current_stage._player1 , current_stage._player2, current_stage._player1_username ,current_stage._player2_username)"


            elif setting.distance(mouse_pos , (360 , 440)) < 45 :
                if self._player1 != "Kenny":
                    self._player2 = "Kenny"
                    self.current_stage= "stages.wallpaper_choosing(current_stage._player1 , current_stage._player2, current_stage._player1_username ,current_stage._player2_username)"

            elif setting.distance(mouse_pos , (560 , 440)) < 45 :
                if self._player1 != "Reina":
                    self._player2 = "Reina"
                    self.current_stage= "stages.wallpaper_choosing(current_stage._player1 , current_stage._player2, current_stage._player1_username ,current_stage._player2_username)"

        if event.type == pygame.QUIT:
         exit()

class wallpaper_choosing(choosing):
    def __init__(self, player1, player2 , player1_username , player2_username):
        choosing.__init__(self , player1, player2 , None, player1_username , player2_username)

    def draw_screen(self):
        setting.SCREEN.blit(self._background , (0 , 0))
        #Drawing a overview from all the wallpapers
        setting.SCREEN.blit(pygame.transform.scale(images.other_images["logo"] , (200,200) ), (300,0))
        setting.SCREEN.blit(pygame.transform.scale(images.background[1],(300,150)),(20,180))
        setting.SCREEN.blit(pygame.transform.scale(images.background[2],(300,150)),(20,350))
        setting.SCREEN.blit(pygame.transform.scale(images.background[3],(300,150)),(480,180))
        setting.SCREEN.blit(pygame.transform.scale(images.background[4],(300,150)),(480,350))

    def event_check (self,event): 
        #checking which wallpaper has been chosen
        if event.type == pygame.MOUSEBUTTONUP :
            mouse_pos = pygame.mouse.get_pos()
            if 320 > mouse_pos[0] > 20 and 330 > mouse_pos[1] > 180 :
                self._wallpaper = 1
                self.current_stage= "stages.game_stage(current_stage._player1 , current_stage._player2 , current_stage._wallpaper, current_stage._player1_username ,current_stage._player2_username)"

            elif 230 > mouse_pos[0] > 20 and 500 > mouse_pos[1] > 350 :
                self._wallpaper = 2
                self.current_stage= "stages.game_stage(current_stage._player1 , current_stage._player2 , current_stage._wallpaper, current_stage._player1_username ,current_stage._player2_username)"

            elif 780 > mouse_pos[0] > 480 and 330 > mouse_pos[1] > 180 :
                self._wallpaper = 3
                self.current_stage= "stages.game_stage(current_stage._player1 , current_stage._player2 , current_stage._wallpaper , current_stage._player1_username ,current_stage._player2_username)"

            elif 780 > mouse_pos[0] > 480 and 500 > mouse_pos[1] > 350 :
                self._wallpaper = 4
                self.current_stage= "stages.game_stage(current_stage._player1 , current_stage._player2 , current_stage._wallpaper , current_stage._player1_username ,current_stage._player2_username)"

                 
        
        if event.type == pygame.QUIT:
         exit()

#here is the where users start to play the actual game
class game_stage(stage) :

    def __init__(self , player1 , player2, background , player1_username , player2_username):

        stage.__init__(self, background)
        #this is the surface of that unique background the specific vertical scale for ground
        self.__level= setting.find_level(self._background) - setting.PLAYER_HEIGHT

        #heroes 
        self.__player1 = heroes.HERO (player1 , 120 ,self.__level , "False" )
        self.__player2 = heroes.HERO(player2 , 530 ,self.__level , "True")
        #this is the distance between two heroes
        self.__x_distance = setting.positive(self.__player1._x , self.__player2._x)
        self._winner = None
        self._player1_name = self.__player1._name
        self._player2_name = self.__player2._name
        #this is for the end of the game 
        self.__next_background = None
        self._player1_username = player1_username
        self._player2_username = player2_username
        #uploading datas in database for both players
        database.cursor.execute("SELECT Number_of_played_games , Won , Lost , Score FROM tblUserData WHERE Username = (?)", [(self._player1_username)])
        self.__player1_stats = database.cursor.fetchall()
        database.cursor.execute("SELECT Number_of_played_games , Won , Lost , Score FROM tblUserData WHERE Username = (?)", [(self._player2_username)])
        self.__player2_stats = database.cursor.fetchall()
                
    def update (self):
        
        self.__player1.update()
        self.__player2.update()

        #update distance
        self.__x_distance = setting.positive(self.__player1._x , self.__player2._x)

        #EndGame
        #when player two wins
        if self.__player1._current_state == "death" :
            self.__player2.win()
            if not self.__player2._animation._resume :
                #updating the database
                database.cursor.execute("UPDATE tblUserData SET Number_of_played_games =" + str(self.__player1_stats[0][0] + 1) + " WHERE Username = (?)", [(self._player1_username)])
                database.cursor.execute("UPDATE tblUserData SET Number_of_played_games =" + str(self.__player2_stats[0][0] + 1) + " WHERE Username = (?)", [(self._player2_username)])


                database.cursor.execute("UPDATE tblUserData SET Lost =" + str(self.__player1_stats[0][2] + 1) + " WHERE Username = (?)", [(self._player1_username)])
                database.cursor.execute("UPDATE tblUserData SET Won =" + str(self.__player2_stats[0][1] + 1) + " WHERE Username = (?)", [(self._player2_username)])

                database.cursor.execute("UPDATE tblUserData SET Score =" + str(self.__player1_stats[0][3] + setting.LOSING_SCORE) + " WHERE Username = (?)", [(self._player1_username)])
                database.cursor.execute("UPDATE tblUserData SET score =" + str(self.__player2_stats[0][3] + setting.WINNING_SCORE) + " WHERE Username = (?)", [(self._player2_username)])


                self._winner = self._player2_username
                #getting a screenshot to use for the next stage
                pygame.image.save(setting.SCREEN, os.path.join("assets/background/6.jpg"))
                images.background[6] =  pygame.image.load(os.path.join("assets/background/6.jpg"))
                self.current_stage = "stages.final_stage( current_stage._player1_username, current_stage._player2_username ,current_stage._winner )"
        
        #when the first player wins
        if self.__player2._current_state== "death" :
            self.__player1.win()
            if not self.__player1._animation._resume:

                database.cursor.execute("UPDATE tblUserData SET Number_of_played_games =" + str(self.__player1_stats[0][0] + 1) + " WHERE Username = (?)", [(self._player1_username)])
                database.cursor.execute("UPDATE tblUserData SET Number_of_played_games =" + str(self.__player2_stats[0][0] + 1) + " WHERE Username = (?)", [(self._player2_username)])

                database.cursor.execute("UPDATE tblUserData SET Won =" + str(self.__player1_stats[0][1] + 1) + " WHERE Username = (?)", [(self._player1_username)])
                database.cursor.execute("UPDATE tblUserData SET Lost =" + str(self.__player2_stats[0][2] + 1) + " WHERE Username = (?)", [(self._player2_username)])

                database.cursor.execute("UPDATE tblUserData SET Score =" + str(self.__player1_stats[0][3] + setting.WINNING_SCORE) + " WHERE Username = (?)", [(self._player1_username)])
                database.cursor.execute("UPDATE tblUserData SET score =" + str(self.__player2_stats[0][3] + setting.LOSING_SCORE) + " WHERE Username = (?)", [(self._player2_username)])
                self._winner = self._player1_username
                pygame.image.save(setting.SCREEN, os.path.join("assets/background/6.jpg"))
                images.background[6] =  pygame.image.load(os.path.join("assets/background/6.jpg"))
                self.current_stage = "stages.final_stage( current_stage._player1_username, current_stage._player2_username ,current_stage._winner )"



        #gravity
        if self.__player1._y < self.__level :
            self.__player1.gravity_effect()

        if self.__player2._y < self.__level :
            self.__player2.gravity_effect()       

    #jump
        #player1
            #getting ability yo go more up if the hero has been reached the max height
        if self.__player1._y < setting.MAX_HIGHT :
            self.__player1.upward_motion = False
        elif self.__player1._y >= self.__level :
            self.__player1._y >= self.__level
            if self.__player1._current_state == "jump" :
                self.__player1._current_state = "standing"
            #letting the hero jump again
            self.__player1.upward_motion = True
        #player2
        if self.__player2._y < setting.MAX_HIGHT :
            self.__player2.upward_motion = False
        elif self.__player2._y >= self.__level :
            self.__player2._y >= self.__level
            if self.__player2._current_state == "jump" :
                self.__player2._current_state = "walking"
            self.__player2.upward_motion = True



    def Key_check(self):
        self.__Key = pygame.key.get_pressed()
        #checking which key is pressed (not clicked)
        #player1
        if self.__player1._ready_for_new_action :
            if self.__Key [pygame.K_d] :
                if self.__player1._x < (setting.SCREEN_WIDTH - setting.PLAYER_WIDTH):
                    self.__player1.move_right()
            if self.__Key [pygame.K_a] :
                if self.__player1._x > 0:
                    self.__player1.move_left()

            if self.__Key [pygame.K_w] :
                self.__player1.jump()
        
        #checking if the hero has been stoped after walking
        if not self.__Key [pygame.K_d] and not self.__Key [pygame.K_a] and self.__player1._current_state == "walking" :
            self.__player1._current_state = "standing"

        #player2
        if self.__player2._ready_for_new_action :
            if self.__Key [pygame.K_RIGHT]:
                if self.__player2._x < (setting.SCREEN_WIDTH - setting.PLAYER_WIDTH):
                    self.__player2.move_right()
            if self.__Key [pygame.K_LEFT]:
                if self.__player2._x > 0:
                    self.__player2.move_left()

            if self.__Key[pygame.K_UP]:
                self.__player2.jump()

        if not self.__Key [pygame.K_RIGHT] and not self.__Key [pygame.K_LEFT] and self.__player2._current_state == "walking" :
            self.__player2._current_state = "standing"



    def event_check (self,event):
        if event.type == pygame.QUIT:
            exit()

        #checking if a key has been mover up
        if event.type == pygame.KEYUP:
            #player1
            if self.__player1._ready_for_new_action :
                #stop letting the hero go moreup after releasing the w key until it reaches the ground
                if event.key == pygame.K_w :
                    self.__player1.upward_motion = False
                if event.key == pygame.K_s :
                    self.__player1.uncrouch()


            #player2
            if self.__player2._ready_for_new_action :
                if event.key == pygame.K_UP:
                    self.__player2.upward_motion = False
                if event.key == pygame.K_DOWN :
                    self.__player2.uncrouch()
        #checking if the key is clicked(IT DOES NOT COUNT IF IS HAS BEEN KEPT PRESSED)
        if event.type == pygame.KEYDOWN :

            #player1
            if self.__player1._ready_for_new_action : 
                if event.key == pygame.K_x :
                    if self.__player1._current_state == "standing" or self.__player1._current_state == "walking":
                        self.__player1.Punch()
                        #checking distanece and if they are close enough, the punch can do an effect
                        if self.__x_distance < (setting.PLAYER_WIDTH + setting.PUNCH_DISTANCE) :
                            #checking if player one is facind the other player
                            if self.direction_check_player_1():
                                self.__player2.punched()
                if event.key == pygame.K_c:
                    if self.__player1._current_state == "standing" or self.__player1._current_state == "walking" :
                        self.__player1.kick()
                        if self.__x_distance < (setting.PLAYER_WIDTH + setting.KICK_DISTANCE)   :
                            if self.direction_check_player_1():
                                self.__player2.kicked()
            
                if event.key == pygame.K_s :
                    self.__player1.crouch()

              #player2 
            if self.__player2._ready_for_new_action :
                if event.key == pygame.K_l :
                    if self.__player2._current_state == "standing" or self.__player2._current_state == "walking" :
                        self.__player2.Punch()
                        if self.__x_distance < (setting.PLAYER_WIDTH + setting.PUNCH_DISTANCE)  :
                            if self.direction_check_player_2() :
                                self.__player1.punched()          
                if event.key == pygame.K_k:
                    if self.__player2._current_state == "standing" or self.__player2._current_state == "walking" :
                        self.__player2.kick()
                        if self.__x_distance < (setting.PLAYER_WIDTH + setting.KICK_DISTANCE)  :
                            if self.direction_check_player_2():
                                self.__player1.kicked()

                if event.key == pygame.K_DOWN :
                    self.__player2.crouch()     
    #here we check if players are facing each other
    def direction_check_player_1 (self):
        if (self.__player1._x > self.__player2._x and self.__player1._flipped == "True") or (self.__player1._x < self.__player2._x and self.__player1._flipped =="False"):
            return True
        else :
            return False

    def direction_check_player_2 (self):
        if (self.__player2._x > self.__player1._x and self.__player2._flipped == "True") or (self.__player2._x < self.__player1._x and self.__player2._flipped =="False"):
            return True
        else :
            return False           
                  
            
    def draw_screen(self):

        setting.SCREEN.blit(self._background , (0 , 0))
        setting.SCREEN.blit(pygame.transform.scale(images.other_images["healbars"] , (setting.SCREEN_WIDTH , 120) ), (0,0))
        self.__player1.draw(setting.SCREEN)
        self.__player2.draw(setting.SCREEN)
        setting.SCREEN.blit(self.__player1._healbar, (365*(1-self.__player1.health / self.__player1._max_health),0))
        setting.SCREEN.blit(self.__player2._healbar , (434 ,0))
        


class final_stage(stage) :
    def __init__(self , player1_username , player2_username , winner ):
        stage.__init__(self, 6)
        self.__winner = str(winner)
        self.__n_max = 8
        self._player1 = player1_username
        self._player2 = player2_username
        #these have been used to replace username of players in middle of their box
        self.__n1 = self.__n_max  - len(self._player1)
        self.__n2 = self.__n_max  - len(self._player2)
        #number od space for winner
        self.__nw = self.__n_max  - len(self.__winner)
        #making a shading picture ro shwo the winners
        self.__animation = graphics.shading_text_animation( " "*self.__nw + self.__winner + " Wins!" , setting.WINNER_NAME_BOX_HEIGHT , setting.WINNER_NAME_BOX_WIDTH , setting.WINNER_NAME_BOX_X , setting.WINNER_NAME_BOX_Y , setting.WINNER_SHADE_NUMBER, setting.WINNER_NAME_TEXT_SIZE , setting.WINNER_TIME)
        self.__play_again_buttom__OK_buttom = images.other_images["play_again"]
        self.__exit_buttom__OK_buttom = images.other_images["exit"] 
        #uploading data from database
        database.cursor.execute("SELECT  Score FROM tblUserData WHERE Username = (?)", [(self._player1 )])
        self.__player1_score = pygame.font.Font(None, 60).render(str(database.cursor.fetchall()[0][0]), True, "WHITE")
        database.cursor.execute("SELECT  Score FROM tblUserData WHERE Username = (?)", [(self._player2 )])
        self.__player2_score = pygame.font.Font(None, 60).render(str(database.cursor.fetchall()[0][0]), True, "WHITE")
        #these windows show the score of both players
        self.__player1_window = images.shade(" "*self.__n1 +self._player1 + " SCORE" ,1,200,200,34)[0]
        self.__player2_window = images.shade(" "*self.__n2 +self._player2 + " SCORE"  ,1,200,200,34) [0]   
     
    def draw_screen(self):
        setting.SCREEN.blit(self._background , (0 , 0))
        self.__animation.draw()
        setting.SCREEN.blit(self.__play_again_buttom__OK_buttom , setting.PLAY_AGAIN_BUTTOM_CORDINATES)  
        setting.SCREEN.blit(self.__exit_buttom__OK_buttom , setting.EXIT_BUTTOM_CORDINATE)
        setting.SCREEN.blit(self.__player1_window , (20,100))
        setting.SCREEN.blit(self.__player2_window , (570,100))    
        setting.SCREEN.blit(self.__player1_score , (100 , 180))     
        setting.SCREEN.blit(self.__player2_score , (660 , 180))  
    def update(self):
        self.__animation.update()

    def event_check (self,event): 
        if event.type == pygame.MOUSEBUTTONUP :
            mouse_pos = pygame.mouse.get_pos()
            #if PLAY AGAIN BUTTOM has been clicked
            if 315<mouse_pos[0] < 492 and 183<mouse_pos[1] < 228:
                self.current_stage= "stages.player_choosing_1( current_stage._player1 , current_stage._player2 )"
            #checking if EXIT buttom has been clicked
            elif   315<mouse_pos[0] < 492 and 300<mouse_pos[1] < 350 :
                exit() 
                            

        if event.type == pygame.QUIT:
         exit() 

