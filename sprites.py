import pygame
import random
from os import path
from settings import *

class Selector(pygame.sprite.Sprite):
    def __init__(self,orientation,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.orientation=orientation
        if self.orientation=="vert":
            self.image=pygame.Surface((tile_dim+4,(BORDER_BTW+(tile_dim+BORDER_BTW)*tile_rows)))
            self.image.fill(GREEN)
            self.rect=self.image.get_rect()
            self.rect.topleft=(x,y)
        elif self.orientation=="horiz":
            self.image=pygame.Surface(((BORDER_BTW+(tile_dim+BORDER_BTW)*tile_rows),tile_dim+4))
            self.image.fill(GREEN)
            self.rect=self.image.get_rect()
            self.rect.topleft=(x,y)
            
class Player(pygame.sprite.Sprite):
    def __init__(self,color,game,name):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((tile_dim//3,tile_dim//3))
        self.image.fill(BLACK)
        self.rect=self.image.get_rect()
        self.color=color
        self.pos=["",""]
        self.game=game
        self.items=[]
        self.name=name
        
        self.collision_moved=False
        
        if self.color==RED:
            self.rect.center=(BORDER+tile_dim//2,BORDER+tile_dim//2)
        elif self.color==BLUE:
            self.rect.center=(BORDER+(tile_dim+BORDER_BTW)*6+tile_dim//2,BORDER+tile_dim//2)
        elif self.color==YELLOW:
            self.rect.center=(BORDER+tile_dim//2,BORDER+(tile_dim+BORDER_BTW)*6+tile_dim//2)
        elif self.color==GREEN:
            self.rect.center=(BORDER+(tile_dim+BORDER_BTW)*6+tile_dim//2,BORDER+(tile_dim+BORDER_BTW)*6+tile_dim//2)
        self.set_pos()
    
    def update(self):
        self.set_pos()
#         self.check_items()
        if self.items:
            self.current_item=self.items[0]
        pygame.draw.rect(self.image,self.color,(2,2,tile_dim//3-4,tile_dim//3-4))

#START HERE FOR COLLISION TESTING!
        
        if self.collision_moved:
            self.collision_unmove()
            self.collision_moved=False
        
        self.set_pos()
        
        for player in self.game.players:
            if player!=self:
                if player.pos==self.pos:
                    if not self.collision_moved:
                        self.collision_move()
                        self.collision_moved=True
                        break
                
#END HERE FOR COLLISION TESTING!
                    
    def collision_move(self):
        if self.color==RED:
#             print("red moving")
            self.rect.x-=tile_dim//8
            self.rect.y-=tile_dim//8
        elif self.color==BLUE:
#             print("blue moving")
            self.rect.x+=tile_dim//8
            self.rect.y-=tile_dim//8
        elif self.color==YELLOW:
#             print("yellow moving")
            self.rect.x-=tile_dim//8
            self.rect.y+=tile_dim//8
        elif self.color==GREEN:
#             print("green moving")
            self.rect.x+=tile_dim//8
            self.rect.y+=tile_dim//8
            
    def collision_unmove(self):
        if self.color==RED:
#             print("red moving back")
            self.rect.x+=tile_dim//8
            self.rect.y+=tile_dim//8
        elif self.color==BLUE:
#             print("blue moving back")
            self.rect.x-=tile_dim//8
            self.rect.y+=tile_dim//8
        elif self.color==YELLOW:
#             print("yellow moving back")
            self.rect.x+=tile_dim//8
            self.rect.y-=tile_dim//8
        elif self.color==GREEN:
#             print("green moving back")
            self.rect.x-=tile_dim//8
            self.rect.y-=tile_dim//8
    
    def set_pos(self):
        #set x pos
        if self.rect.centerx==BORDER+tile_dim//2:
            self.pos[0]="1"
        elif self.rect.centerx==BORDER+tile_dim+BORDER_BTW+tile_dim//2:
            self.pos[0]="2"
        elif self.rect.centerx==BORDER+(tile_dim+BORDER_BTW)*2+tile_dim//2:
            self.pos[0]="3"
        elif self.rect.centerx==BORDER+(tile_dim+BORDER_BTW)*3+tile_dim//2:
            self.pos[0]="4"
        elif self.rect.centerx==BORDER+(tile_dim+BORDER_BTW)*4+tile_dim//2:
            self.pos[0]="5"
        elif self.rect.centerx==BORDER+(tile_dim+BORDER_BTW)*5+tile_dim//2:
            self.pos[0]="6"
        elif self.rect.centerx==BORDER+(tile_dim+BORDER_BTW)*6+tile_dim//2:
            self.pos[0]="7"

        #set y pos
        if self.rect.centery==BORDER+tile_dim//2:
            self.pos[1]="A"
        elif self.rect.centery==BORDER+tile_dim+BORDER_BTW+tile_dim//2:
            self.pos[1]="B"
        elif self.rect.centery==BORDER+(tile_dim+BORDER_BTW)*2+tile_dim//2:
            self.pos[1]="C"
        elif self.rect.centery==BORDER+(tile_dim+BORDER_BTW)*3+tile_dim//2:
            self.pos[1]="D"
        elif self.rect.centery==BORDER+(tile_dim+BORDER_BTW)*4+tile_dim//2:
            self.pos[1]="E"
        elif self.rect.centery==BORDER+(tile_dim+BORDER_BTW)*5+tile_dim//2:
            self.pos[1]="F"
        elif self.rect.centery==BORDER+(tile_dim+BORDER_BTW)*6+tile_dim//2:
            self.pos[1]="G"
            
    def check_items(self):
        for tile in self.game.tiles:
            if tile.pos==self.pos:
                if tile.item==self.current_item:
                    self.items.remove(tile.item)
                    pygame.mixer.Sound(path.join(sound_dir,'ding.ogg')).play()

    def move(self,direct):
        for tile in self.game.tiles:
            if tile.pos==self.pos:
                if direct in tile.available_directions:
                    if direct=="right":
                        for tile2 in self.game.tiles:
                            if tile2.pos[1]==self.pos[1] and int(tile2.pos[0])==int(self.pos[0])+1:
                                if "left" in tile2.available_directions:
                                    self.rect.x+=(tile_dim+BORDER_BTW)
                                    pygame.mixer.Sound(path.join(sound_dir,'footstep.ogg')).play()
                    elif direct=="left":
                        for tile2 in self.game.tiles:
                            if tile2.pos[1]==self.pos[1] and int(tile2.pos[0])==int(self.pos[0])-1:
                                if "right" in tile2.available_directions:
                                    self.rect.x-=(tile_dim+BORDER_BTW)
                                    pygame.mixer.Sound(path.join(sound_dir,'footstep.ogg')).play()
                    elif direct=="down":
                        for tile2 in self.game.tiles:
                            if tile2.pos[0]==self.pos[0] and self.check_up_down(tile2,direct):
                                self.rect.y+=(tile_dim+BORDER_BTW)
                                pygame.mixer.Sound(path.join(sound_dir,'footstep.ogg')).play()
                    elif direct=="up":
                        for tile2 in self.game.tiles:
                            if tile2.pos[0]==self.pos[0] and self.check_up_down(tile2,direct):
                                self.rect.y-=(tile_dim+BORDER_BTW)
                                pygame.mixer.Sound(path.join(sound_dir,'footstep.ogg')).play()
                        
    def check_up_down(self,tile,direction):
        if direction=="down":
            if self.pos[1]=="A":
                if tile.pos[1]=="B" and "up" in tile.available_directions:
                    return True
                else:
                    return False
            elif self.pos[1]=="B":
                if tile.pos[1]=="C" and "up" in tile.available_directions:
                    return True
                else:
                    return False
            elif self.pos[1]=="C":
                if tile.pos[1]=="D" and "up" in tile.available_directions:
                    return True
                else:
                    return False
            elif self.pos[1]=="D":
                if tile.pos[1]=="E" and "up" in tile.available_directions:
                    return True
                else:
                    return False
            elif self.pos[1]=="E":
                if tile.pos[1]=="F" and "up" in tile.available_directions:
                    return True
                else:
                    return False
            elif self.pos[1]=="F":
                if tile.pos[1]=="G" and "up" in tile.available_directions:
                    return True
                else:
                    return False
        elif direction=="up":
            if self.pos[1]=="B":
                if tile.pos[1]=="A" and "down" in tile.available_directions:
                    return True
                else:
                    return False
            elif self.pos[1]=="C":
                if tile.pos[1]=="B" and "down" in tile.available_directions:
                    return True
                else:
                    return False
            elif self.pos[1]=="D":
                if tile.pos[1]=="C" and "down" in tile.available_directions:
                    return True
                else:
                    return False
            elif self.pos[1]=="E":
                if tile.pos[1]=="D" and "down" in tile.available_directions:
                    return True
                else:
                    return False
            elif self.pos[1]=="F":
                if tile.pos[1]=="E" and "down" in tile.available_directions:
                    return True
                else:
                    return False
            elif self.pos[1]=="G":
                if tile.pos[1]=="F" and "down" in tile.available_directions:
                    return True
                else:
                    return False
        return False
                
    def push(self,direction):
        if self.collision_moved:
            self.collision_unmove()
            self.collision_moved=False
        
        self.set_pos()
        
        if self.game.selected in self.pos:
            selector=self.game.selector
            
            if selector.orientation=="horiz":
                if direction=="right":
                    self.rect.x+=(tile_dim+BORDER_BTW)
                    if self.rect.x>=BOARD_WIDTH-BORDER-10:
                        self.rect.centerx=BORDER+tile_dim//2
                elif direction=="left":
                    self.rect.x-=(tile_dim+BORDER_BTW)
                    if self.rect.x<BORDER:
                        self.rect.centerx=BOARD_WIDTH-BORDER-tile_dim//2
            elif selector.orientation=="vert":
                if direction=="down":
                    self.rect.y+=(tile_dim+BORDER_BTW)
                    if self.rect.y>=BOARD_HEIGHT-BORDER:
                        self.rect.centery=BORDER+tile_dim//2
                elif direction=="up":
                    self.rect.y-=(tile_dim+BORDER_BTW)      
                    if self.rect.y<BORDER:
                        self.rect.centery=BOARD_HEIGHT-BORDER-tile_dim//2
                
                
class Card(pygame.sprite.Sprite):
    def __init__(self,item,x,y,player,game):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((tile_dim,tile_dim*3//2))
        self.image.fill(CARD_COLOR)
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
        self.item=item
        self.player=player
        self.game=game
        
    def update(self):
        
        if self.item==self.player.current_item and self.player.items:# and self.player==self.game.current_player:
            self.image.fill(CARD_COLOR)
            self.draw_item(self.item+".png",BLACK)
        elif not self.item in self.player.items:
#             self.show_item()
            self.draw_item("x.png",BLACK)
        else:
            self.image.fill(CARD_COLOR)
            self.draw_item("question.png",BLACK)
            
#         else:
#             self.image.fill(CARD_COLOR)
#             self.draw_item("question.png",BLACK)
        
    def draw_item(self,image_name,color_key):
        img=pygame.image.load(path.join(image_dir,image_name)).convert()
        img=pygame.transform.scale(img,(tile_dim*3//4,tile_dim*3//4))
        img.set_colorkey(color_key)
        img_rect=img.get_rect()
        img_rect.x+=tile_dim//8
        img_rect.y+=tile_dim//4
        self.image.blit(img,img_rect)


class Tile(pygame.sprite.Sprite):
    def __init__(self,game,path,x,y,rot):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((tile_dim,tile_dim))
        self.image.fill(BLUE)
        self.path=path
        self.pos=["",""]
        self.image_orig=self.image
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
        if self.rect.y>=BOARD_HEIGHT-BORDER:
            self.rect.topleft=EXTRA_COORDS
#         self.rot=random.choice([0,90,180,270])
        self.rot=rot
        self.item=""
        self.game=game
        self.available_directions=[]
        self.set_pos()
        self.set_item()
        self.update()
        
    def draw_tile(self):
        if self.path=="straight":
            pygame.draw.rect(self.image,PATH_COLOR,(tile_dim//4,0,tile_dim//2,tile_dim))
            #default orientation is vertical line like this: |
        if self.path=="corner":
            pygame.draw.rect(self.image,PATH_COLOR,(tile_dim//4,tile_dim//4,tile_dim//2,tile_dim*3//4))
            pygame.draw.rect(self.image,PATH_COLOR,(tile_dim//4,tile_dim//4,tile_dim*3//4,tile_dim//2))
            #default orientation is corner going down and right like this: r
        if self.path=="t shape":
            pygame.draw.rect(self.image,PATH_COLOR,(tile_dim//4,0,tile_dim//2,tile_dim*3//4))
            pygame.draw.rect(self.image,PATH_COLOR,(0,tile_dim//4,tile_dim,tile_dim//2))
#             pygame.draw.rect(self.image,RED,(tile_dim//4,0,tile_dim//2,tile_dim))
#             pygame.draw.rect(self.image,RED,(tile_dim//4,tile_dim//4,tile_dim*3//4,tile_dim//2))
            #default orientation is T upside down _|_
            
        if self.item=="red start":
            self.draw_circle(RED)
        elif self.item=="blue start":
            self.draw_circle(BLUE)
        elif self.item=="yellow start":
            self.draw_circle(YELLOW)
        elif self.item=="green start":
            self.draw_circle(GREEN)
        elif self.item!="":
#             print(self.item)
            self.draw_item(self.item+".png",BLACK)

    def update(self):
        self.set_pos()
        self.draw_tile()
        self.rotate()
        self.find_available_paths()
    
    def set_pos(self):
        #set x pos
        if self.rect.x==BORDER:
            self.pos[0]="1"
        elif self.rect.x==BORDER+tile_dim+BORDER_BTW:
            self.pos[0]="2"
        elif self.rect.x==BORDER+(tile_dim+BORDER_BTW)*2:
            self.pos[0]="3"
        elif self.rect.x==BORDER+(tile_dim+BORDER_BTW)*3:
            self.pos[0]="4"
        elif self.rect.x==BORDER+(tile_dim+BORDER_BTW)*4:
            self.pos[0]="5"
        elif self.rect.x==BORDER+(tile_dim+BORDER_BTW)*5:
            self.pos[0]="6"
        elif self.rect.x==BORDER+(tile_dim+BORDER_BTW)*6:
            self.pos[0]="7"

        #set y pos
        if self.rect.y==BORDER:
            self.pos[1]="A"
        elif self.rect.y==BORDER+tile_dim+BORDER_BTW:
            self.pos[1]="B"
        elif self.rect.y==BORDER+(tile_dim+BORDER_BTW)*2:
            self.pos[1]="C"
        elif self.rect.y==BORDER+(tile_dim+BORDER_BTW)*3:
            self.pos[1]="D"
        elif self.rect.y==BORDER+(tile_dim+BORDER_BTW)*4:
            self.pos[1]="E"
        elif self.rect.y==BORDER+(tile_dim+BORDER_BTW)*5:
            self.pos[1]="F"
        elif self.rect.y==BORDER+(tile_dim+BORDER_BTW)*6:
            self.pos[1]="G"
            
        if self.rect.topleft==EXTRA_COORDS:
            self.pos=["N","N"]
    
    def set_item(self):
        #set item
        if self.pos==["1","A"]:
            self.item="red start"
        elif self.pos==["3","A"]:
            self.item="skull"
        elif self.pos==["5","A"]:
            self.item="sword"
        elif self.pos==["7","A"]:
            self.item="blue start"
        elif self.pos==["1","C"]:
            self.item="coinbag"
        elif self.pos==["3","C"]:
            self.item="key"
        elif self.pos==["5","C"]:
            self.item="gem"
        elif self.pos==["7","C"]:
            self.item="helmet"
        elif self.pos==["1","E"]:
            self.item="book"
        elif self.pos==["3","E"]:
            self.item="crown"
        elif self.pos==["5","E"]:
            self.item="treasurechest"
        elif self.pos==["7","E"]:
            self.item="candlestick"
        elif self.pos==["1","G"]:
            self.item="yellow start"
        elif self.pos==["3","G"]:
            self.item="map"
        elif self.pos==["5","G"]:
            self.item="ring"
        elif self.pos==["7","G"]:
            self.item="green start"
        
        if self.item=="":
            if self.path=="corner" and self.game.other_items[0]: #and random.random()<0.25:
                self.item=self.game.other_items[0].pop(random.randrange((len(self.game.other_items[0]))))
            #t shape one can be kept as is b/c all t shapes have an item!
            if self.path=="t shape" and self.game.other_items[1]: #and random.random()<0.25:
                self.item=self.game.other_items[1].pop(random.randrange((len(self.game.other_items[1]))))
    
    def draw_circle(self,color):
        pygame.draw.circle(self.image,BLACK,(self.rect.width//2,self.rect.height//2),self.rect.width//4)
        pygame.draw.circle(self.image,color,(self.rect.width//2,self.rect.height//2),self.rect.width//4-BORDER_BTW)
    
    def draw_item(self,image_name,color_key):
        img=pygame.image.load(path.join(image_dir,image_name)).convert()
        img=pygame.transform.scale(img,(tile_dim//2,tile_dim//2))
        img.set_colorkey(color_key)
        img_rect=img.get_rect()
        img_rect.x+=tile_dim//4
        img_rect.y+=tile_dim//4
        self.image.blit(img,img_rect)
    
    def rotate(self):
        new_image=pygame.transform.rotate(self.image_orig,self.rot)
        old_center=self.rect.center
        self.image=new_image
        self.rect=self.image.get_rect()
        self.rect.center=old_center
        
#     def rotate_itself(self):
#         if self.rot==0:
#             self.rot=360
#         self.rot-=90
        
    def push(self,direction):
        if self.game.selected in self.pos or self.pos==["N","N"]:
            selector=self.game.selector
            
            if selector.orientation=="horiz":
                if direction=="right":
                    self.rect.x+=(tile_dim+BORDER_BTW)
                    if self.pos==["N","N"]:
                        self.rect.x=BORDER
                        if self.game.selected=="B":
                            self.rect.y=BORDER+tile_dim+BORDER_BTW
                        elif self.game.selected=="D":
                            self.rect.y=BORDER+(tile_dim+BORDER_BTW)*3
                        elif self.game.selected=="F":
                            self.rect.y=BORDER+(tile_dim+BORDER_BTW)*5
                    if self.rect.x>=BOARD_WIDTH-BORDER-10:
                        self.rect.topleft=EXTRA_COORDS
                        return True
                elif direction=="left":
                    self.rect.x-=(tile_dim+BORDER_BTW)
                    if self.pos==["N","N"]:
                        self.rect.x=BOARD_WIDTH-BORDER-tile_dim
                        if self.game.selected=="B":
                            self.rect.y=BORDER+tile_dim+BORDER_BTW
                        elif self.game.selected=="D":
                            self.rect.y=BORDER+(tile_dim+BORDER_BTW)*3
                        elif self.game.selected=="F":
                            self.rect.y=BORDER+(tile_dim+BORDER_BTW)*5
                    if self.rect.x<BORDER:
                        self.rect.topleft=EXTRA_COORDS
                        return True
            elif selector.orientation=="vert":
                if direction=="down":
                    self.rect.y+=(tile_dim+BORDER_BTW)
                    if self.pos==["N","N"]:
                        self.rect.y=BORDER
                        self.rect.x=BORDER+(tile_dim+BORDER_BTW)*(int(self.game.selected)-1)
                    if self.rect.y>=BOARD_HEIGHT-BORDER:
                        self.rect.topleft=EXTRA_COORDS
                        return True
                elif direction=="up":
                    self.rect.y-=(tile_dim+BORDER_BTW)      
                    if self.pos==["N","N"]:
                        self.rect.y=BOARD_HEIGHT-BORDER-tile_dim
                        self.rect.x=BORDER+(tile_dim+BORDER_BTW)*(int(self.game.selected)-1)
                    if self.rect.y<BORDER:
                        self.rect.topleft=EXTRA_COORDS
                        return True
        return None
                        
    def find_available_paths(self):
        for i in range(len(self.available_directions)-1,-1,-1):
            self.available_directions.pop(i)
        if self.path=="straight":
            if self.rot==0 or self.rot==180:
                self.available_directions.append("up")
                self.available_directions.append("down")
            elif self.rot==90 or self.rot==270:
                self.available_directions.append("left")
                self.available_directions.append("right")
        elif self.path=="corner":
            if self.rot==0:
                self.available_directions.append("down")
                self.available_directions.append("right")
            elif self.rot==90:
                self.available_directions.append("up")
                self.available_directions.append("right")
            elif self.rot==180:
                self.available_directions.append("up")
                self.available_directions.append("left")
            elif self.rot==270:
                self.available_directions.append("down")
                self.available_directions.append("left")
        elif self.path=="t shape":
            if self.rot==0:
                self.available_directions.append("left")
                self.available_directions.append("right")
                self.available_directions.append("up")
            elif self.rot==90:
                self.available_directions.append("up")
                self.available_directions.append("left")
                self.available_directions.append("down")
            elif self.rot==180:
                self.available_directions.append("down")
                self.available_directions.append("left")
                self.available_directions.append("right")
            elif self.rot==270:
                self.available_directions.append("down")
                self.available_directions.append("right")
                self.available_directions.append("up")
            
        if self.pos[0]=="1" and "left" in self.available_directions:
            self.available_directions.remove("left")
        if self.pos[0]=="7" and "right" in self.available_directions:
            self.available_directions.remove("right")
        if self.pos[1]=="A" and "up" in self.available_directions:
            self.available_directions.remove("up")
        elif self.pos[1]=="G" and "down" in self.available_directions:
            self.available_directions.remove("down")


#         if self.game.players and self.pos==self.game.p1.pos:
#             print(self.available_directions)
            
#         if self.pos==["N","N"]:
#             print(self.available_directions)
                        
# class Warn_Box(pygame.sprite.Sprite):
#     def __init__(self,text,x,y):
#         pygame.sprite.Sprite.__init__(self,x,y)
#         self.image=pygame.Surface((BOARD_WIDTH,tile_dim))
#         self.image.fill(BLACK)
#         self.rect=self.image.get_rect()
#         self.rect.topleft=(x,y)
#         self.text=text
#         self.font_name=pygame.font.match_font(FONT_NAME)
#     
#     def update(self):
#         font=pygame.font.Font(self.font_name,32)
#         text_surface=font.render(self.text,True,white)
#         text_rect=text_surface.get_rect()
#         text_rect.topleft=(0,0)
#         self.image.blit(text_surface,text_rect)
# 