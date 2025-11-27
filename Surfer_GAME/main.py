import pygame
import sys
import random

def create_ene(ene_count, ene_arr):
    l = len(ene_arr)
    if ene_count >  l: 
        #add more ene
        needed = ene_count - l 
        for i in range (0,needed):
            rock_width = random.randint(10,40) 
            rock_height = random.randint(10,40) 

            ene_rect = pygame.Rect(random.randint(20 ,400),-random.randint(10,30),rock_width,rock_height)
            ene_arr.append(ene_rect)


    return ene_arr

# def draw_ene(ene_arr , win):
#     for ene in ene_arr :
#         ene.y += 10 
#         pygame.draw.rect(win,(255,255,0),ene)


    

def main():
    pygame.init()


    CLOCK = pygame.time.Clock()
    FPS = 60
    WIDTH, HEIGHT = 400, 800
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Beach Game")

    ENEMEY_COUNT = 20



    RUN = True
    PLAYER_VEL = 5
    PLAYER_RECT = pygame.Rect(WIDTH // 2, HEIGHT // 2, 10, 30)
    ene_arr = []

    while RUN:
        ene_arr = create_ene(ENEMEY_COUNT ,ene_arr)
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            if (PLAYER_RECT.x > 20) :
                PLAYER_RECT.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT]:
            if (PLAYER_RECT.x < WIDTH-20) :
                PLAYER_RECT.x += PLAYER_VEL
        if keys[pygame.K_UP]:
            if (PLAYER_RECT.y > 50):
                PLAYER_RECT.y -= PLAYER_VEL
        if keys[pygame.K_DOWN]:
            if (PLAYER_RECT.y < HEIGHT-50):
                PLAYER_RECT.y += PLAYER_VEL

        WINDOW.fill("black")
        pygame.draw.rect(WINDOW, (255, 0, 0), PLAYER_RECT)

        for ene in ene_arr[:] :
            if ene.y > HEIGHT:
                ene_arr.remove(ene)
            else:
                ene.y += 10 
                pygame.draw.rect(WINDOW,(122,222,221), ene)


            if PLAYER_RECT.colliderect(ene):
                ene_arr.remove(ene)

        
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()