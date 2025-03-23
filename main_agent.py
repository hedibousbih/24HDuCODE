import pygame
import sys
import time
from itertools import cycle
from agent_config import agent  # Assure-toi que ce fichier est dans le même dossier ou accessible

# --- CONFIG ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TEXT_SPEED = 30

# --- INIT ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Camille - Assistant IA")
clock = pygame.time.Clock()

# --- LOAD ASSETS ---
bg = pygame.image.load("bg_lobby.jpg").convert()
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

dialogue_box = pygame.Surface((SCREEN_WIDTH - 60, 130))
dialogue_box.fill((255, 255, 255))
pygame.draw.rect(dialogue_box, (0, 0, 0), dialogue_box.get_rect(), 5)

# Load talking GIF (static version or loop through frames)
camille_img = pygame.image.load("hotel_agent_mouth_talking.gif")

font = pygame.font.SysFont("Courier", 22, bold=True)

# --- TYPEWRITER TEXT ---
def typewriter(text, pos, max_width):
    displayed = ""
    start_time = time.time()
    while True:
        elapsed = time.time() - start_time
        chars = min(int(elapsed * TEXT_SPEED), len(text))
        displayed = text[:chars]

        screen.blit(bg, (0, 0))
        screen.blit(camille_img, (50, 100))
        screen.blit(dialogue_box, (30, SCREEN_HEIGHT - 150))

        words = displayed.split(" ")
        x, y = pos
        line = ""
        for word in words:
            if font.size(line + word)[0] < max_width:
                line += word + " "
            else:
                rendered = font.render(line, True, (0, 0, 0))
                screen.blit(rendered, (x, y))
                y += 30
                line = word + " "
        rendered = font.render(line, True, (0, 0, 0))
        screen.blit(rendered, (x, y))

        pygame.display.flip()
        clock.tick(FPS)

        if chars >= len(text):
            break

# --- MAIN LOOP ---
user_text = ""
response_text = ""
input_active = True

while True:
    screen.blit(bg, (0, 0))
    screen.blit(camille_img, (50, 100))
    screen.blit(dialogue_box, (30, SCREEN_HEIGHT - 150))

    # Draw user input
    txt_surface = font.render("> " + user_text, True, (0, 0, 0))
    screen.blit(txt_surface, (50, SCREEN_HEIGHT - 120))

    pygame.display.flip()
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if input_active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Appel à l'agent LangChain
                try:
                    response = agent.invoke(user_text)
                    response_text = response["output"] if isinstance(response, dict) else str(response)
                except Exception as e:
                    response_text = f"[Erreur] {e}"

                user_text = ""
                input_active = False
                typewriter(response_text, (50, SCREEN_HEIGHT - 130), 700)
                input_active = True
            elif event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            else:
                user_text += event.unicode