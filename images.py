import pygame
import  os
from PIL import Image, ImageDraw, ImageFont

#backround images
background = {}
for i in range (7) :
    background[i] = pygame.image.load(os.path.join("assets/background",str(i)+".jpg"))



#hero images
hero = {"Behrad": {} , "Kenny" : {} , "Reina" :{}}

for a_hero  in hero :
    #each hero has several picture for each action
    hero[a_hero] = {"crouch" :{} , "death" :{} ,  "hitted" : {} , "jump" :{} , "kick" :{} ,"punch":{} , "standing" : {} , "walking": {} ,"win":{} ,"choosing_section":{}} 
    for activity in hero[a_hero] :
        n = 0 
        for path in os.listdir(os.path.realpath("assets/characters/"+ a_hero +"/"+activity)):
            hero[a_hero][activity][n] = pygame.image.load(os.path.join("assets/characters/"+a_hero+"/"+activity , path))
            n +=1



#other useful images
other_images = {}
other_images["logo"]  = pygame.image.load(os.path.join("assets/choosing_sectoin/logo.png"))

    #this is where pictures from heros for choosing section has been uploaded
for a_hero in hero :
    other_images[a_hero + " profile"] = pygame.image.load(os.path.join("assets/choosing_sectoin/" + a_hero+ ".png"))

other_images["healbars"] = pygame.image.load(os.path.join("assets/play_stage/healbars.png"))
other_images["healbar"] = pygame.image.load(os.path.join("assets/play_stage/healbar.png"))
other_images["winner_of_the_game"] = pygame.image.load(os.path.join("assets/final_stage/winner.png"))
other_images["play_again"] = pygame.image.load(os.path.join("assets/final_stage/play_again.png"))
other_images["exit"] = pygame.image.load(os.path.join("assets/final_stage/exit.png"))

# generating text of the winner
def shade (text , time , width , height ,text_size):
    image_list=[]
    out = Image.new("RGB", (width , height), (0,0,0))

    fnt = ImageFont.truetype(os.path.join("assets/font/font.ttf") , text_size)
    d = ImageDraw.Draw(out)
    #infact a lost of pictures would be save which all of them are shades
    for i in range (1, time+1):
        d.multiline_text((10, 10), text , font=fnt, fill=(255-i, 255-i, 255-i))
        out.save(os.path.join("assets/final_stage/winner.png"))
        image_list.append(pygame.image.load(os.path.join("assets/final_stage/winner.png")))
    
    return image_list




