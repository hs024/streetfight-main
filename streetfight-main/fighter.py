import pygame



class fighter():
    def __init__(self,x,y,flip,data,sprite_sheet,animation_step,n,sound):
        self.rect=pygame.Rect((x,y,80,180))
        self.size=data[0]
        self.image_scale=data[1]
        self.offset=data[2]
        self.animation_list=self.load_image(sprite_sheet,animation_step)
        self.action=0#idle for run jump 
        self.frame_index=0
        self.image=self.animation_list[self.action][self.frame_index]
        self.update_time=pygame.time.get_ticks()
        self.vel_y=0
        self.running=False
        self.jump=False
        self.attack_type=0
        self.attaking=False
        self.health=100
        self.flip=flip
        self.attack_cooldown=0
        self.hit=False
        self.alive=True
        self.player=n
        self.sound=sound
        self.potion=3
        
    
    
    
    def load_image(self,sprite_sheet,animation_step):
        animation_list=[]
        for y,animation in enumerate(animation_step):
            temp_img_list=[]
            for x in range(animation):
                temp_img=sprite_sheet.subsurface(x*self.size,y*self.size,self.size,self.size)
                
                temp_img_list.append(pygame.transform.scale(temp_img,(self.size*self.image_scale,self.size*self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list   



    def draw(self,surface):
        img=pygame.transform.flip(self.image,self.flip,False)
        # pygame.draw.rect(surface,(255,0,0),self.rect)
        surface.blit(img,(self.rect.x-(self.offset[0]*self.image_scale),self.rect.y-(self.offset[1]*self.image_scale)))


    def move(self,surface,target):
        SPEED=10
        gravity=2
        dx=0
        dy=0
        self.running=False
        self.attack_type=0
        #getkeypress
        
        if self.player==1:
            key=pygame.key.get_pressed()
            if self.attaking==False and self.alive==True:
                if key[pygame.K_w] and self.jump==False:
                    self.vel_y=-30
                    self.jump=True
                if key[pygame.K_a]:
                    dx=-SPEED
                    self.running=True
                if key[pygame.K_d]:
                    dx=SPEED
                    self.running=True
                #attacks
                if key[pygame.K_r] or key[pygame.K_t]:
                    self.attack(surface,target)
                    # print(self.attack_cooldown)
                    if key[pygame.K_r]:
                        self.attack_type=1
                    if key[pygame.K_t]:
                        self.attack_type=2
                if key[pygame.K_q] :
                    self.potion-=1
                    self.health=100
                if key[pygame.K_1]:
                    target.health=10
                    self.sound.play()
        #########################3player2
        if self.player==2:
            key=pygame.key.get_pressed()
            if self.attaking==False and self.alive==True:
                if key[pygame.K_UP] and self.jump==False:
                    self.vel_y=-30
                    self.jump=True
                if key[pygame.K_LEFT]:
                    dx=-SPEED
                    self.running=True
                if key[pygame.K_RIGHT]:
                    dx=SPEED
                    self.running=True
                #attacks
                if key[pygame.K_k] or key[pygame.K_l]:
                    self.attack(surface,target)
                    # print(self.attack_cooldown)
                    if key[pygame.K_k]:
                        self.attack_type=1
                    if key[pygame.K_l]:
                        self.attack_type=2
        #gravity
        self.vel_y+=gravity
        dy+=self.vel_y
        if self.rect.left+dx<0:
            dx=0-self.rect.left+2
        if self.rect.right+dx>1000:
            dx=1000-self.rect.right-2
        if self.rect.bottom+dy>600-120:
            self.vel_y=0
            dy=600-120-self.rect.bottom
            self.jump=False
        #face each other
        if target.rect.center>self.rect.center:
            self.flip=False
        else:
            self.flip=True

        #attack cooldown
        if self.attack_cooldown>0:
            self.attack_cooldown-=2
        self.rect.x+=dx
        
        self.rect.y+=dy

    def update(self):
        #check action
        if self.health<=0:
            self.health=0
            self.alive=False
            self.update_action(6)
        elif self.hit==True:
            self.update_action(5)
        elif self.attaking==True:
            if self.attack_type==1:
                self.update_action(3)
            elif self.attack_type==2:
                self.update_action(4)
        elif self.jump==True:
            self.update_action(2)
        elif self.running==True:
            self.update_action(1)
        else:
            self.update_action(0)
        animation_cooldown=50
        
        self.image=self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks()-self.update_time>animation_cooldown:
            self.frame_index+=1
            self.update_time=pygame.time.get_ticks()
        if self.frame_index>=len(self.animation_list[self.action]):
            if self.alive==False:
                self.frame_index=len(self.animation_list[self.action])-1
            else:
                self.frame_index=0
                if self.action==3 or self.action==4:
                    self.attaking=False
                    self.attack_cooldown=50
                #check if hit
                if self.action==5:
                    self.hit=False
                    #if palyer middlw in attack
                    self.attaking=False
                    self.attack_cooldown=50



    def update_action(self,new_action):
        if new_action!=self.action:
            self.action=new_action
            self.frame_index=0
            self.update_time=pygame.time.get_ticks()

    def attack(self,surface,target):
        if self.attack_cooldown==0:
            self.sound.play()
            self.attaking=True
            attack_rect=pygame.Rect(self.rect.centerx-(2*self.rect.width*self.flip),self.rect.y,2*self.rect.width,self.rect.height)
            # pygame.draw.rect(surface,(0,255,0),attack_rect)
            if attack_rect.colliderect(target.rect):
                target.health-=10
                target.hit=True
            # print("hit")
        # self.attaking=False