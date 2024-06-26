import os
import random
import sys
import pygame as pg
import time


WIDTH, HEIGHT = 1600, 900
DELTA={  # 移動量辞書
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(+5,0),
}
KOUKATON=pg.image.load("ex2/fig/3.png")

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct: pg.rect) -> tuple[bool,bool]:
    """
    引数：こうかとんRectかばくだんRect
    戻り値；　タプル（横方向判定結果、縦方向判定結果）
    画面内ならTrue、画面外ならFalce
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate

def return_KOUKAITEN():
    return {  #こうかとん回転の辞書
    (0,-5):pg.transform.rotozoom(pg.transform.flip(KOUKATON,True,False),90,2.0),
    (+5,-5):pg.transform.rotozoom(pg.transform.flip(KOUKATON,True,False),45,2.0),
    (+5,0):pg.transform.rotozoom(pg.transform.flip(KOUKATON,True,False),0,2.0),
    (+5,+5):pg.transform.rotozoom(pg.transform.flip(KOUKATON,True,False),315,2.0),
    (0,+5):pg.transform.rotozoom(pg.transform.flip(KOUKATON,True,False),270,2.0),
    (-5,+5):pg.transform.rotozoom(KOUKATON,90,2.0),
    (-5,0):pg.transform.rotozoom(KOUKATON,0,2.0),
    (-5,-5):pg.transform.rotozoom(KOUKATON,270,2.0),
    (0,0):pg.transform.rotozoom(pg.transform.flip(KOUKATON,True,False),0,2.0),
    }

def bonb_time():
    bb_accs= [a for a in range(1,11)]
    up_bb=[]
    for r in range(1,11):
        bb_img = pg.Surface((20*r,20*r))
        pg.draw.circle(bb_img, (255,0,0),(10*r,10*r),10*r)
        bb_img.set_colorkey((0,0,0))
        up_bb.append(bb_img)
    return tuple(bb_accs),tuple(up_bb)

def gameover():
    screen = pg.display.set_mode((WIDTH,HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    screen.blit(bg_img,[0,0])
    go_img=pg.Surface((WIDTH,HEIGHT))
    pg.draw.rect(go_img,(0,0,0),pg.Rect(0,0,WIDTH,HEIGHT))
    go_img.set_alpha(127)
    screen.blit(go_img,[0,0])
    fonto=pg.font.Font(None,80)
    txt=fonto.render("Game Over",True,(255,255,255))
    screen.blit(txt,[650,450])
    kk2_img=pg.transform.rotozoom(pg.image.load("fig/8.png"),0,2.0)
    screen.blit(kk2_img,[550,400])
    screen.blit(kk2_img,[975,400])
    pg.display.update()
    time.sleep(5)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bb_img = pg.Surface((20,20))
    bb_img.set_colorkey((0,0,0))
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)
    vx, vy =+5, +5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bb_rct):
            gameover()
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] +=v[0]
                sum_mv[1] +=v[1]

        kk_rct.move_ip(sum_mv)
        kk_img=return_KOUKAITEN()[tuple(sum_mv)]
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)


        bb_accs,up_bb =bonb_time()
        avx =vx*bb_accs[min(tmr//500,9)]
        avy =vy*bb_accs[min(tmr//500,9)]
        bb_img = up_bb[min(tmr//500,9)]
        bb_rct.move_ip(avx,avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *=-1
        if not tate:
            vy *=-1
        screen.blit(bb_img,bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)





if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
