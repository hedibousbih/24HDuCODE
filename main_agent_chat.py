import pygame
import sys
from agent_config import agent

# --- CONFIG ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TEXT_SPEED = 30

# --- INIT ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Camille - Chat IA")
clock = pygame.time.Clock()

# --- LOAD ASSETS ---
bg = pygame.image.load("bg_lobby.jpg").convert()
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

dialogue_box = pygame.Surface((SCREEN_WIDTH - 60, 200))
dialogue_box.fill((255, 255, 255))
pygame.draw.rect(dialogue_box, (0, 0, 0), dialogue_box.get_rect(), 4)

camille_img = pygame.image.load("hotel_agent_mouth_talking.gif")

font = pygame.font.SysFont("Courier", 20, bold=False)

# --- HISTORIQUE DE MESSAGES ---
history = []  # Chaque élément = (auteur, texte)
user_text = ""
input_active = True

def render_history(surface, messages, start_y, max_width):
    y = start_y
    for speaker, text in messages[-5:]:  # Affiche les 5 derniers messages
        prefix = "Camille: " if speaker == "ai" else "Vous: "
        full_text = prefix + text
        words = full_text.split(" ")
        x = 50
        line = ""
        for word in words:
            if font.size(line + word)[0] < max_width:
                line += word + " "
            else:
                rendered = font.render(line, True, (0, 0, 0))
                surface.blit(rendered, (x, y))
                y += 28
                line = word + " "
        rendered = font.render(line, True, (0, 0, 0))
        surface.blit(rendered, (x, y))
        y += 35

# --- MAIN LOOP ---
while True:
    screen.blit(bg, (0, 0))
    screen.blit(camille_img, (50, 80))
    screen.blit(dialogue_box, (30, SCREEN_HEIGHT - 220))

    render_history(screen, history, SCREEN_HEIGHT - 210, 700)

    # Zone de saisie
    input_display = font.render("> " + user_text, True, (0, 0, 0))
    screen.blit(input_display, (50, SCREEN_HEIGHT - 40))

    pygame.display.flip()
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if input_active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if user_text.strip() != "":
                    history.append(("user", user_text))
                    try:
                        response = agent.invoke(user_text)
                        reply = response["output"] if isinstance(response, dict) else str(response)
                        history.append(("ai", reply))
                    except Exception as e:
                        history.append(("ai", f"[Erreur] {e}"))
                    user_text = ""
            elif event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            else:
                user_text += event.unicode