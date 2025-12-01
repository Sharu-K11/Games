import pygame
import sys
import random

WIDTH, HEIGHT = 400, 800

def draw_wrapped_text(surface, text, font, color, x, y, max_width):
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        test_surface = font.render(test_line, True, color)

        if test_surface.get_width() > max_width:
            lines.append(current_line)
            current_line = word + " "
        else:
            current_line = test_line

    lines.append(current_line)  # Add last line

    for i, line in enumerate(lines):
        line_surface = font.render(line, True, color)
        surface.blit(line_surface, (x, y + i * (font.get_height() + 5)))


def quiz(window, font):
    question_lyst = [
    "Sandy Hook is a barrier spit formed over thousands of years by longshore drift moving sand northward.",
    "The Sandy Hook Lighthouse was originally built about 1.5 miles inland from the shoreline.",
    "The Sandy Hook Lighthouse is the oldest operating lighthouse in the United States.",
    "During the American Revolution, the Sandy Hook Lighthouse was successfully destroyed by enemy forces.",
    "Fort Hancock played a major role in U.S. coastal defense, especially during World War I and the Cold War.",
    "Gunnison Beach is the only legal nude beach in New Jersey because it’s on federal land.",
    "Sandy Hook officially opened its public beaches in the 1970s after the National Park Service took over the land.",
    "There are officially ten designated beaches at Sandy Hook according to the National Park Service.",
    "Hurricane Sandy caused only minor damage to Sandy Hook and the park reopened within a few weeks.",
    "Parts of Sandy Hook still contain abandoned military structures like missile sites, gun batteries, and underground tunnels."
]

    answer_lyst = [1, 0, 1, 0, 1, 1, 1, 0, 0, 1]

    random_ques = random.randint(0, 1)
    question = question_lyst[random_ques]
    answer = answer_lyst[random_ques]
    question_surface = font.render(f"{question}", True, (255, 255, 255))
    pause = True
    cont = False
    yes_rect = pygame.Rect(60, 600, 100, 50)
    no_rect = pygame.Rect(200, 600, 100, 50)

    while pause:
        pygame.display.update()
        # window.blit(question_surface, (60, 300))
        draw_wrapped_text(window, question, font, (255,255,255), 20, 300, 360)  # 360 width so it fits inside 400 window

        pygame.draw.rect(window, "green", yes_rect)
        pygame.draw.rect(window, "red", no_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pause = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if yes_rect.collidepoint(event.pos):
                    pause = False
                    if answer == 1:
                        cont = True
                    break
                if no_rect.collidepoint(event.pos):
                    pause = False
                    if answer == 0:
                        cont = True
                    break

    return cont


def gen_rock(rock_count, curret_count, rock_lyst, rock_types):
    needed_rock = rock_count - curret_count
    if needed_rock > 0:
        for _ in range(0, needed_rock):
            rock_x = random.randint(20, WIDTH)
            rock_y = -random.randint(20, 100)
            rock_width = random.randint(20, 90)
            rock_height = random.randint(20, 90)
            rock = pygame.Rect(rock_x, rock_y, rock_width, rock_height)
            rock_lyst.append(rock)

    return rock_lyst


def main():
    pygame.init()
    pygame.mixer.init()
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Beach Rush")
    CLOCK = pygame.time.Clock()
    FPS = 60
    RUNNING = True

    PLAYER_VEL = 5
    PLAYER_RECT = pygame.Rect(WIDTH // 2 - 20, HEIGHT - 70, 40, 60)

    # player images loading for movements
    PLAYER_IMAGE_STRAIGHT = pygame.image.load(
        "resource/images/characters/boy.png"
    ).convert_alpha()
    PLAYER_IMAGE_STRAIGHT = pygame.transform.scale(PLAYER_IMAGE_STRAIGHT, (40, 60))

    PLAYER_IMAGE_LEFT = pygame.image.load("resource/images/characters/boyleft.png")
    PLAYER_IMAGE_LEFT = pygame.transform.scale(PLAYER_IMAGE_LEFT, (40, 60))

    PLAYER_IMAGE_RIGHT = pygame.image.load(
        "resource/images/characters/boyright.png"
    ).convert_alpha()
    PLAYER_IMAGE_RIGHT = pygame.transform.scale(PLAYER_IMAGE_RIGHT, (40, 60))

    # background image
    BG_IMAGE = pygame.image.load("resource/images/characters/ocean.png").convert_alpha()
    BG_IMAGE = pygame.transform.scale(BG_IMAGE, (WIDTH, HEIGHT))

    # SOUND AND MUSIC
    collison_sound = pygame.mixer.Sound("resource/audio/surfboard_rock_collision.wav")
    pygame.mixer.music.load("resource/audio/surfer_bg_loop_140bpm.wav")

    # FONT SETTINGS
    font = pygame.font.SysFont("Arial", 36)

    # TYPE OF ROCK LYST
    ROCK_TYPES = []
    for idx in range(0, 3):
        rock_name = f"rock_{idx}.png"
        path = "resource/images/characters/{rock_name}"

        print(rock_name, path)
        # ROCK = pygame.image.load(path).convert_alpha()
        # ROCK = pygame.transform.scale(ROCK,(((idx+1)*10),((idx+1)*10)))
        # ROCK_TYPES.append(ROCK)

    ROCK_IMAGE = pygame.image.load(
        "resource/images/characters/rock_2.png"
    ).convert_alpha()

    ROCK_COUNT = 5
    ROCK_LYST = []
    ROCK_VEL = 5

    # BG MUSIC
    pygame.mixer.music.play(-1)

    while RUNNING:
        CLOCK.tick(FPS)
        WINDOW.fill((255, 255, 255))
        WINDOW.blit(BG_IMAGE, (0, 0))

        ROCK_LYST = gen_rock(ROCK_COUNT, len(ROCK_LYST), ROCK_LYST, ROCK_TYPES)

        time_tick = (pygame.time.get_ticks()) // 1000

        text_surface = font.render(f" {time_tick}", True, (255, 255, 255))  # White text

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
        keys = pygame.key.get_pressed()
        PLAYER_IMAGE = PLAYER_IMAGE_STRAIGHT
        if keys[pygame.K_LEFT]:
            if PLAYER_RECT.x > 20:
                PLAYER_RECT.x -= PLAYER_VEL
                PLAYER_IMAGE = PLAYER_IMAGE_LEFT  # SMART MOTHERFUCKE
        if keys[pygame.K_RIGHT]:
            if PLAYER_RECT.x < WIDTH - 60:
                PLAYER_RECT.x += PLAYER_VEL
                PLAYER_IMAGE = PLAYER_IMAGE_RIGHT
        if keys[pygame.K_UP]:
            if PLAYER_RECT.y > 50:
                PLAYER_RECT.y -= PLAYER_VEL
        if keys[pygame.K_DOWN]:
            if PLAYER_RECT.y < HEIGHT - 50:
                PLAYER_RECT.y += PLAYER_VEL

        # Draw the player rectangle so it's visible
        #    pygame.draw.rect(WINDOW, (0, 0, 0), PLAYER_RECT)

        # DRAWING AREA
        WINDOW.blit(PLAYER_IMAGE, (PLAYER_RECT.x, PLAYER_RECT.y))

        for rock in ROCK_LYST[:]:
            rock.y = rock.y + ROCK_VEL
            # pygame.draw.rect(WINDOW,(255,44,22),rock)
            render_rock = pygame.transform.scale(ROCK_IMAGE, (rock.width, rock.height))
            WINDOW.blit(render_rock, (rock.x, rock.y))
            if rock.y > HEIGHT:
                ROCK_LYST.remove(rock)

            if PLAYER_RECT.colliderect(rock):
                collison_sound.play()
                ROCK_LYST.remove(rock)
                cont = quiz(WINDOW, font)
                if not cont:
                    RUNNING = False
                ROCK_LYST = []

        WINDOW.blit(text_surface, (0, 0))

        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
