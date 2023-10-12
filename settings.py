import random
from os import path

tile_rows=7
tile_columns=7

tile_dim=100

BORDER=20
BORDER_BTW=2

BOARD_WIDTH=BORDER*2+(tile_dim+BORDER_BTW)*tile_columns-BORDER_BTW
BOARD_HEIGHT=BORDER*2+(tile_dim+BORDER_BTW)*tile_rows-BORDER_BTW
WIDTH= BORDER*2+(tile_dim+BORDER_BTW)*(tile_columns+11)-BORDER_BTW+BORDER
HEIGHT=BORDER*2+(tile_dim+BORDER_BTW)*(tile_rows+2)-BORDER_BTW
FPS=120

image_dir=path.join(path.dirname(__file__),'images')
sound_dir=path.join(path.dirname(__file__),'sounds')

FONT_NAME='arial'

BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
YELLOW=(255,255,0)
CYAN=(0,255,255)

PATH_COLOR=(255,128,0)
CARD_COLOR=(0,128,255)

PATHS_LIST=[["corner","","t shape","","t shape","","corner"],["","","","","","",""],["t shape","","t shape","","t shape","","t shape"],["","","","","","",""],["t shape","","t shape","","t shape","","t shape"],["","","","","","",""],["corner","","t shape","","t shape","","corner"],[""]]
PATHS_ORS=[[0,-1,180,-1,180,-1,270],[-1,-1,-1,-1,-1,-1,-1],[270,-1,270,-1,180,-1,90],[-1,-1,-1,-1,-1,-1,-1],[270,-1,0,-1,90,-1,90],[-1,-1,-1,-1,-1,-1,-1],[90,-1,0,-1,0,-1,180],[0]]
# PATHS_ORS=[[0,-1,270,-1,270,-1,270],[-1,-1,-1,-1,-1,-1,-1],[0,-1,0,-1,270,-1,180],[-1,-1,-1,-1,-1,-1,-1],[0,-1,90,-1,180,-1,180],[-1,-1,-1,-1,-1,-1,-1],[90,-1,90,-1,90,-1,180],[0]]

other_paths=[]
for _ in range(12):
    other_paths.append("straight")
for _ in range(16):
    other_paths.append("corner")
for _ in range(6):
    other_paths.append("t shape")

for i in range(tile_rows):
    for j in range(tile_columns):
        if PATHS_LIST[i][j]=="":
            PATHS_LIST[i][j]=(random.choice(other_paths))
            other_paths.remove(PATHS_LIST[i][j])
PATHS_LIST[tile_rows][0]=other_paths.pop(0)
        
for i in range(tile_rows):
    for j in range(tile_columns):
        if PATHS_ORS[i][j]==-1:
            PATHS_ORS[i][j]=(random.choice([0,90,180,270]))


EXTRA_COORDS=(BORDER+(tile_dim+BORDER_BTW)*(tile_rows+1)-tile_dim//2,BORDER+(tile_dim+BORDER_BTW)*(tile_columns//2))

# for _ in range(4):
#     PATHS_LIST.append("corner")
# for _ in range(tile_rows*tile_columns-4):
#     PATHS_LIST.append(random.choice(["straight","corner","t shape"]))

