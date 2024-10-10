import pygame
from fighter import fighter
from pygame import mixer
pygame.init()
mixer.init()
SCREEN_WIDTH=1000
SCREEN_HEIGHT=600
screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
#color
yellow=(255,255,0)
pygame.display.set_caption("brawler")
################
#game variable
intro_count=3
last_count_update=pygame.time.get_ticks()
score=[0,0]
round_over=False
ROUND_OVER_COOLDOWN=2000

##########################################WARRIOR DATA
warrior_size=162
warrior_scale=4
warrior_offset=[72,56]
warrior_data=[warrior_size,warrior_scale,warrior_offset]


wizard_size=250
wizard_scale=3
wizard_offset=[112,107]
wizard_data=[wizard_size,wizard_scale,wizard_offset]
clock=pygame.time.Clock()
fps=60
##################################################3
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1,0.0,5000)
sword_fx=pygame.mixer.Sound("sword.wav")
sword_fx.set_volume(0.6)
magic_fx=pygame.mixer.Sound("magic.wav")
magic_fx.set_volume(0.8)
#background
bg_image=pygame.image.load("background.jpg").convert_alpha()
scale_bg=pygame.transform.scale(bg_image,(SCREEN_WIDTH,SCREEN_HEIGHT))
victory_img=pygame.image.load("victory.png").convert_alpha()
#######################################################
#define font
count_font=pygame.font.Font("turok.ttf",100)
score_font=pygame.font.Font("turok.ttf",40)

#function for text
def draw_text(text,font,text_col,x,y):
    img=font.render(text,True,text_col)
    screen.blit(img,(x,y))
################################################################33
#load sprite sheet
warrior_sheet=pygame.image.load("warrior.png").convert_alpha()
wizard_sheet=pygame.image.load("wizard.png").convert_alpha()
#define step in animation
warrior_animation_steps=[10,8,1,7,7,3,7]
wizard_animation_steps=[8,8,1,8,8,3,7]

# function for background
def draw_bg():
    screen.blit(scale_bg,(0,0))
#healyh bar
def draw_health_bar(health,x,y):
    ratio=health/100
    pygame.draw.rect(screen,(0,0,0),(x-2,y-2,404,34))
    pygame.draw.rect(screen,(255,0,0),(x,y,400,30))
    pygame.draw.rect(screen,yellow,(x,y,400*ratio,30))
#create instance of fighter
fighter_1=fighter(200,310,False,warrior_data,warrior_sheet,warrior_animation_steps,1,sword_fx)
fighter_2=fighter(700,310,True,wizard_data,wizard_sheet,wizard_animation_steps,2,magic_fx)
#############################################################################################

#game loop
run=True
while run:
    clock.tick(fps)
    draw_bg()
    #update fighter
    fighter_1.update()
    fighter_2.update()
    #####33
    fighter_1.draw(screen)
    fighter_2.draw(screen)
    #haelthbar
    draw_health_bar(fighter_1.health,20,20)
    draw_health_bar(fighter_2.health,580,20)

    draw_text("P1: "+str(score[0]),score_font,(255,0,0),20,60)
    draw_text("P2: "+str(score[1]),score_font,(255,0,0),580,60)
    if intro_count<=0 and round_over==False:
        #move fighter
        fighter_1.move(screen,fighter_2)
        fighter_2.move(screen,fighter_1)
    else:
        draw_text(str(intro_count),count_font,(255,0,0),SCREEN_WIDTH//2,SCREEN_HEIGHT//3)
        if (pygame.time.get_ticks()-last_count_update)>=1000:
            intro_count-=1
            last_count_update=pygame.time.get_ticks()

    #check player defeat
    if round_over==False:
        if fighter_1.alive==False:
            score[1]+=1
            round_over=True
            round_over_time=pygame.time.get_ticks()
        if fighter_2.alive==False:
            score[0]+=1
            round_over=True
            round_over_time=pygame.time.get_ticks()
    else:
        screen.blit(victory_img,(360,150))
        if pygame.time.get_ticks()-round_over_time>ROUND_OVER_COOLDOWN:
            round_over=False
            intro_count=3
            fighter_1=fighter(200,310,False,warrior_data,warrior_sheet,warrior_animation_steps,1,sword_fx)
            fighter_2=fighter(700,310,True,wizard_data,wizard_sheet,wizard_animation_steps,2,magic_fx)
            ############################################################################################
        
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        key=pygame.key.get_pressed()
        if key[pygame.K_1]:
            draw_text("I AM IMMORTAL",count_font,(255,0,0),SCREEN_WIDTH//2,SCREEN_HEIGHT//3)







    pygame.display.update()




# exit
pygame.quit()


