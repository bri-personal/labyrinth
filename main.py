import pygame
import random
from os import path
from settings import *
from sprites import *

class Game:
    def __init__(self):
    #initialize pygame and create window
        pygame.init()
        pygame.mixer.init()
        self.screen=pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Labyrinth")
        self.clock=pygame.time.Clock()
        self.font_name=pygame.font.match_font(FONT_NAME)
        self.running=True
        self.player_count=4
        
        pygame.mixer.music.load(path.join(sound_dir,'Unfolding_Revelation_-_David_Fesliyan.mp3'))
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)
    
    def new(self):
        self.all_sprites=pygame.sprite.Group()
        self.tiles=pygame.sprite.Group()
        self.selectors=pygame.sprite.Group()
        self.players=pygame.sprite.Group()
        self.cards=pygame.sprite.Group()
        self.selected=""
        
        self.last_selected=""
        self.last_dir=""
        
        self.stage="push"
        
        self.other_items=[["owl","beetle","lizard","spiderweb","moth","mouse","","","","","",""],["ghost","dragon","genie","troll","bat","wand"]]
        self.all_items=["skull","sword","coinbag","key","gem","helmet","book","crown","treasurechest","candlestick","map","ring"]
        
        for i in range(len(self.other_items)):
            for item in self.other_items[i]:
                if item!="":
                    self.all_items.append(item)
#         print(self.all_items)

#         path_list=[]
#         for i in range(tile_rows):
#             path_list.append([])
#             for _ in range(tile_columns):
#                 path_list[i].append(random.choice(["straight","corner","t shape"])) 
                    
#         print(PATHS_ORS)
#         print(PATHS_LIST)

        self.tile_list=[]
        count=0
        y_count=-1
        for row in range(len(PATHS_LIST)):
            for path in PATHS_LIST[row]:
                x=BORDER+((tile_dim+BORDER_BTW)*count)%((tile_dim+BORDER_BTW)*tile_columns)
                if x==BORDER:
                    y_count+=1
                y=BORDER+(tile_dim+BORDER_BTW)*y_count

                tile=Tile(self,path,x,y,PATHS_ORS[row][count%tile_columns])
                    
                self.tile_list.append(tile)
                self.all_sprites.add(self.tile_list[count])
                self.tiles.add(self.tile_list[count])
                count+=1
        
        self.p1=Player(RED,self,"Player 1")
        self.all_sprites.add(self.p1)
        self.players.add(self.p1)
        
        self.p2=Player(BLUE,self,"Player 2")
        self.all_sprites.add(self.p2)
        self.players.add(self.p2)
        
        if self.player_count>2:
            self.p3=Player(YELLOW,self,"Player 3")
            self.all_sprites.add(self.p3)
            self.players.add(self.p3)
            
            if self.player_count>3:
                self.p4=Player(GREEN,self,"Player 4")
                self.all_sprites.add(self.p4)
                self.players.add(self.p4)
        
        while self.all_items:
            for player in self.players:
                n=random.choice(self.all_items)
                player.items.append(n)
                self.all_items.remove(n)
        
#         for player in self.players:
#             print(player.items)
        
        y=BORDER
        for player in self.players:
            x=BOARD_WIDTH+tile_dim*3+BORDER_BTW*2
            for item in player.items:
                card=Card(item,x,y,player,self)
                self.all_sprites.add(card)
                self.cards.add(card)
                x+=tile_dim+BORDER_BTW
                if self.player_count==2 and x>=BOARD_WIDTH+tile_dim*3+BORDER_BTW*2+(tile_dim+BORDER_BTW)*6:
                    x=BOARD_WIDTH+tile_dim*3+BORDER_BTW*2
                    y+=(tile_dim*3//2+BORDER_BTW)
            if self.player_count==2:
                y+=tile_dim-BORDER_BTW
            else:
                y+=tile_dim*2+BORDER_BTW
        
        self.current_player=self.p1
         
        self.run()
        
    def run(self):
        self.playing=True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    
    def events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
#                     self.current_player.items=[]
                    if not self.selectors and self.stage=="move":
                        if not self.current_player.items:
                            player=self.current_player
                            if player.color==RED and player.pos==["1","A"]:
                                self.win(player)
                            elif player.color==BLUE and player.pos==["7","A"]:
                                self.win(player)
                            elif player.color==YELLOW and player.pos==["1","G"]:
                                self.win(player)
                            elif player.color==GREEN and player.pos==["7","G"]:
                                self.win(player)
        
                        self.current_player.check_items()
                        self.stage="push"
                        if self.current_player==self.p1:
                            self.current_player=self.p2
                        elif self.current_player==self.p2:
                            if self.player_count>2:
                                self.current_player=self.p3
                            else:
                                self.current_player=self.p1
                        elif self.current_player==self.p3:
                            if self.player_count>3:
                                self.current_player=self.p4
                            else:
                                self.current_player=self.p1
                        elif self.current_player==self.p4:
                            self.current_player=self.p1
                if event.key==pygame.K_RIGHT:
                    if self.selectors and self.stage=="push":
                        if not(self.last_dir=="left" and self.last_selected==self.selected):
#                             pygame.mixer.Sound(path.join(sound_dir,'rumble.ogg')).play()
                            for tile in self.tile_list:
                                if tile.push("right"):
                                    for player in self.players:
                                        player.push("right")
                                    self.stage="move"
                                    self.last_selected=self.selected
                                    self.last_dir="right"
                                    for selector in self.selectors:
                                        selector.kill()
                                        pygame.mixer.Sound(path.join(sound_dir,'rumble.ogg')).play()
#                         else:
#                             self.warning=Warn_Box("You can't push it that way!",BORDER,BOARD_HEIGHT)
#                             self.all_sprites.add(self.warning) 
                    elif not self.selectors and self.stage=="move":
#                         pygame.mixer.Sound(path.join(sound_dir,'footstep.ogg')).play()
                        self.current_player.move("right")
#                         self.stage="push"
                if event.key==pygame.K_LEFT:
                    if self.selectors and self.stage=="push":
                        if not(self.last_dir=="right" and self.last_selected==self.selected):
#                             pygame.mixer.Sound(path.join(sound_dir,'rumble.ogg')).play()
                            for tile in self.tile_list:
                                if tile.push("left"):
                                    for player in self.players:
                                        player.push("left")
                                    self.stage="move"
                                    self.last_selected=self.selected
                                    self.last_dir="left"
                                    for selector in self.selectors:
                                        selector.kill()
                                        pygame.mixer.Sound(path.join(sound_dir,'rumble.ogg')).play()
                    elif not self.selectors and self.stage=="move":
#                         pygame.mixer.Sound(path.join(sound_dir,'footstep.ogg')).play()
                        self.current_player.move("left")
#                         self.stage="push"
                if event.key==pygame.K_DOWN:
                    if self.selectors and self.stage=="push":
                        if not(self.last_dir=="up" and self.last_selected==self.selected):
#                             pygame.mixer.Sound(path.join(sound_dir,'rumble.ogg')).play()
                            for tile in self.tile_list:
                                if tile.push("down"):
                                    for player in self.players:
                                        player.push("down")
                                    self.stage="move"
                                    self.last_selected=self.selected
                                    self.last_dir="down"
                                    for selector in self.selectors:
                                        selector.kill()
                                        pygame.mixer.Sound(path.join(sound_dir,'rumble.ogg')).play()
                    elif not self.selectors and self.stage=="move":
#                         pygame.mixer.Sound(path.join(sound_dir,'footstep.ogg')).play()
                        self.current_player.move("down")
#                         self.stage="push"
                if event.key==pygame.K_UP:
                    if self.selectors and self.stage=="push":
                        if not(self.last_dir=="down" and self.last_selected==self.selected):
#                             pygame.mixer.Sound(path.join(sound_dir,'rumble.ogg')).play()
                            for tile in self.tile_list:
                                if tile.push("up"):
                                    for player in self.players:
                                        player.push("up")
                                    self.stage="move"
                                    self.last_selected=self.selected
                                    self.last_dir="up"
                                    for selector in self.selectors:
                                        selector.kill()
                                        pygame.mixer.Sound(path.join(sound_dir,'rumble.ogg')).play()
                    elif not self.selectors and self.stage=="move":
#                         pygame.mixer.Sound(path.join(sound_dir,'footstep.ogg')).play()
                        self.current_player.move("up")
#                         self.stage="push"
                        
                if event.key==pygame.K_r:
                    if self.stage=="push":
                        for tile in self.tile_list:
                            if tile.pos==["N","N"]:
                                if tile.rot==0:
                                    tile.rot=360
                                tile.rot-=90
                        
                if event.key==pygame.K_2:
                    if self.selectors:
                        if self.selected=="2":
                            for selector in self.selectors:
                                selector.kill()
                            self.selected=""
                        elif self.stage=="push":
                            for selector in self.selectors:
                                selector.kill()
                            self.spawn_selector("vert",BORDER+tile_dim,BORDER-BORDER_BTW)
                            self.selected="2"
                    elif self.stage=="push":
                        self.spawn_selector("vert",BORDER+tile_dim,BORDER-BORDER_BTW)
                        self.selected="2"
                if event.key==pygame.K_4:
                    if self.selectors:
                        if self.selected=="4":
                            for selector in self.selectors:
                                selector.kill()
                            self.selected=""
                        elif self.stage=="push":
                            for selector in self.selectors:
                                selector.kill()
                            self.spawn_selector("vert",BORDER+tile_dim*3+BORDER_BTW*2,BORDER-BORDER_BTW)
                            self.selected="4"
                    elif self.stage=="push":
                        self.spawn_selector("vert",BORDER+tile_dim*3+BORDER_BTW*2,BORDER-BORDER_BTW)
                        self.selected="4"
                if event.key==pygame.K_6:
                    if self.selectors:
                        if self.selected=="6":
                            for selector in self.selectors:
                                selector.kill()
                            self.selected=""
                        elif self.stage=="push":
                            for selector in self.selectors:
                                selector.kill()
                            self.spawn_selector("vert",BORDER+tile_dim*5+BORDER_BTW*4,BORDER-BORDER_BTW)
                            self.selected="6"
                    elif self.stage=="push":
                        self.spawn_selector("vert",BORDER+tile_dim*5+BORDER_BTW*4,BORDER-BORDER_BTW)
                        self.selected="6"
                if event.key==pygame.K_b:
                    if self.selectors:
                        if self.selected=="B":
                            for selector in self.selectors:
                                selector.kill()
                            self.selected=""
                        elif self.stage=="push":
                            for selector in self.selectors:
                                selector.kill()
                            self.spawn_selector("horiz",BORDER-BORDER_BTW,BORDER+tile_dim)
                            self.selected="B"
                    elif self.stage=="push":
                        self.spawn_selector("horiz",BORDER-BORDER_BTW,BORDER+tile_dim)
                        self.selected="B"
                if event.key==pygame.K_d:
                    if self.selectors:
                        if self.selected=="D":
                            for selector in self.selectors:
                                selector.kill()
                            self.selected=""
                        elif self.stage=="push":
                            for selector in self.selectors:
                                selector.kill()
                            self.spawn_selector("horiz",BORDER-BORDER_BTW,BORDER+tile_dim*3+BORDER_BTW*2)
                            self.selected="D"
                    elif self.stage=="push":
                        self.spawn_selector("horiz",BORDER-BORDER_BTW,BORDER+tile_dim*3+BORDER_BTW*2)
                        self.selected="D"
                if event.key==pygame.K_f:
                    if self.selectors:
                        if self.selected=="F":
                            for selector in self.selectors:
                                selector.kill()
                            self.selected=""
                        elif self.stage=="push":
                            for selector in self.selectors:
                                selector.kill()
                            self.spawn_selector("horiz",BORDER-BORDER_BTW,BORDER+tile_dim*5+BORDER_BTW*4)
                            self.selected="F"
                    elif self.stage=="push":
                        self.spawn_selector("horiz",BORDER-BORDER_BTW,BORDER+tile_dim*5+BORDER_BTW*4)
                        self.selected="F"
                        
    def update(self):
        self.all_sprites.update()
        
#         for player in self.players:
#             if not player.items:
#                 if player.color==RED and player.pos==["1","A"]:
#                     self.win(player)
#                 elif player.color==BLUE and player.pos==["7","A"]:
#                     self.win(player)
#                 elif player.color==YELLOW and player.pos==["1","G"]:
#                     self.win(player)
#                 elif player.color==GREEN and player.pos==["7","G"]:
#                     self.win(player)
        
#         if self.last_dir:
#             print(self.last_dir,self.last_selected)
                
    def win(self,player):
        pygame.mixer.Sound(path.join(sound_dir,'victory.ogg')).play()
        self.winner=player
        self.playing=False
        
    def draw(self):
        self.screen.fill(BLACK)
        for i in range(1,6,2):
            pygame.draw.polygon(self.screen,YELLOW,[(BORDER+i*(tile_dim+BORDER_BTW)+tile_dim/4,BORDER/4),(BORDER+i*(tile_dim+BORDER_BTW)+tile_dim*3/4,BORDER/4),(BORDER+i*(tile_dim+BORDER_BTW)+tile_dim/2,BORDER*3/4)])
            pygame.draw.polygon(self.screen,YELLOW,[(BORDER+i*(tile_dim+BORDER_BTW)+tile_dim/4,BOARD_HEIGHT-BORDER/4),(BORDER+i*(tile_dim+BORDER_BTW)+tile_dim*3/4,BOARD_HEIGHT-BORDER/4),(BORDER+i*(tile_dim+BORDER_BTW)+tile_dim/2,BOARD_HEIGHT-BORDER*3/4)])
            pygame.draw.polygon(self.screen,YELLOW,[(BORDER/4,BORDER+i*(tile_dim+BORDER_BTW)+tile_dim/4),(BORDER/4,BORDER+i*(tile_dim+BORDER_BTW)+tile_dim*3/4),(BORDER*3/4,BORDER+i*(tile_dim+BORDER_BTW)+tile_dim/2)])
            pygame.draw.polygon(self.screen,YELLOW,[(BOARD_HEIGHT-BORDER/4,BORDER+i*(tile_dim+BORDER_BTW)+tile_dim/4),(BOARD_HEIGHT-BORDER/4,BORDER+i*(tile_dim+BORDER_BTW)+tile_dim*3/4),(BOARD_HEIGHT-BORDER*3/4,BORDER+i*(tile_dim+BORDER_BTW)+tile_dim/2)])

#         background=pygame.image.load(path.join(image_dir,"background.png")).convert()
#         background=pygame.transform.scale(background,(WIDTH,HEIGHT))
#         background_rect=background.get_rect()
#         self.screen.blit(background,background_rect)
        if self.stage=="push":
            self.draw_text("Push a tile to move the maze!",32,self.current_player.color,BOARD_WIDTH//2,BOARD_HEIGHT+BORDER_BTW)
        else:
            self.draw_text("Move through the maze!",32,self.current_player.color,BOARD_WIDTH//2,BOARD_HEIGHT+BORDER_BTW)
        
        y=BORDER-BORDER_BTW
        if self.player_count>2:
            for player in self.players:
                pygame.draw.rect(self.screen,player.color,(BOARD_WIDTH+tile_dim*2+BORDER_BTW,y,(tile_dim+BORDER_BTW)*(24//self.player_count+1)+BORDER_BTW,tile_dim*3//2+BORDER_BTW*2))
                y+=tile_dim*2+BORDER_BTW
        else:
            for player in self.players:
                pygame.draw.rect(self.screen,player.color,(BOARD_WIDTH+tile_dim*2+BORDER_BTW,y,(tile_dim+BORDER_BTW)*(24//(2*self.player_count)+1)+BORDER_BTW,(tile_dim*3//2)*2+BORDER_BTW*3))
                y+=tile_dim*4+BORDER_BTW
        
        self.all_sprites.draw(self.screen)
        self.tiles.draw(self.screen)
        self.players.draw(self.screen)
        pygame.display.flip()
        
    def spawn_selector(self,orientation,x,y):
        self.selector=Selector(orientation,x,y)
        self.all_sprites.add(self.selector)
        self.selectors.add(self.selector)
        
    def draw_text(self,text,size,color,x,y):
        font=pygame.font.Font(self.font_name,size)
        text_surface=font.render(text,True,color)
        text_rect=text_surface.get_rect()
        text_rect.midtop=(x,y)
        self.screen.blit(text_surface,text_rect)
        
    def show_start_screen(self):
        self.screen.fill(BLACK)
        background=pygame.image.load(path.join(image_dir,"background.png")).convert()
        background=pygame.transform.scale(background,(WIDTH,HEIGHT))
        background_rect=background.get_rect()
        self.screen.blit(background,background_rect)
        self.draw_text("LABYRINTH",48,WHITE,WIDTH//2,10)
        self.draw_text("Press number of players to start",22,WHITE,WIDTH//2,HEIGHT*3//4)
        pygame.display.flip()
        self.wait_for_key()
        
    def show_end_screen(self):
        if not self.running:
            return
        self.screen.fill(BLACK)
        background=pygame.image.load(path.join(image_dir,"background.png")).convert()
        background=pygame.transform.scale(background,(WIDTH,HEIGHT))
        background_rect=background.get_rect()
        self.screen.blit(background,background_rect)
        self.draw_text(self.winner.name+" wins!",48,self.winner.color,WIDTH//2,10)
        self.draw_text("Press number of players to start",22,WHITE,WIDTH//2,HEIGHT*3//4)
        pygame.display.flip()
        self.wait_for_key()
        
    def wait_for_key(self):
        waiting=True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    waiting=False
                    self.running=False
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_2:
                        g.player_count=2
                        waiting=False
                    elif event.key==pygame.K_3:
                        g.player_count=3
                        waiting=False
                    elif event.key==pygame.K_4:
                        g.player_count=4
                        waiting=False

g=Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_end_screen()
    
pygame.quit()

# print("done")