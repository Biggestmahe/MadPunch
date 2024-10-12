import pygame 
import setting
import stages
import database

#making database
database.make_database()
pygame.display.set_caption('MAD PUNCH')
pygame.init()
current_stage = stages.start_stage()
stcurrent = " stages.start_stage()"



while setting.RUN :
    for event in pygame.event.get():
        current_stage.event_check(event)


    #checking if the current stage has been changed
    if stcurrent != current_stage.current_stage:
        current_stage = eval(current_stage.current_stage)
        stcurrent = current_stage.current_stage

    current_stage.Key_check()
    current_stage.update()
    current_stage.update_db()
    current_stage.draw_screen()
    setting.clock.tick(setting.FPS)
    pygame.display.update()


















