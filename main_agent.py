import pygame
import sys
import pyttsx3
from PIL import Image
from agent_config import agent

# --- CONFIG ---
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 650
FPS = 60

# --- INIT ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Camille - Chat IA")
clock = pygame.time.Clock()

# --- TTS ENGINE ---
engine = pyttsx3.init()
engine.setProperty('rate', 170)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Change index if needed

# --- LOAD ASSETS ---
bg = pygame.image.load("bg_lobby.jpg").convert()
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

dialogue_rect = pygame.Rect(30, SCREEN_HEIGHT - 260, SCREEN_WIDTH - 60, 240)
dialogue_box = pygame.Surface(dialogue_rect.size, pygame.SRCALPHA)
dialogue_box.fill((255, 255, 255, 230))
pygame.draw.rect(dialogue_box, (0, 0, 0), dialogue_box.get_rect(), 4)

font = pygame.font.SysFont("Segoe UI", 24, bold=True)

# --- LOAD GIF FRAMES ---
def load_gif_frames(path):
    pil_img = Image.open(path)
    frames = []
    try:
        while True:
            pil_img_rgba = pil_img.convert("RGBA")
            mode = pil_img_rgba.mode
            size = pil_img_rgba.size
            data = pil_img_rgba.tobytes()
            py_image = pygame.image.fromstring(data, size, mode)
            py_image = pygame.transform.scale(py_image, (360, 360))
            frames.append(py_image)
            pil_img.seek(pil_img.tell() + 1)
    except EOFError:
        pass
    return frames

camille_frames = load_gif_frames("hotel_agent_mouth_talking.gif")
camille_idle = camille_frames[0]
frame_index = 0
frame_timer = 0
frame_delay = 120
is_talking = False

# --- HISTORY ---
history = []
user_text = ""
scroll_y = 0

def render_history_clipped(surface, messages, max_width, scroll_offset):
    dialogue_surface = pygame.Surface(dialogue_box.get_size(), pygame.SRCALPHA)
    y = 10 - scroll_offset
    for speaker, text in messages:
        prefix = "Camille: " if speaker == "ai" else "Vous: "
        full_text = prefix + text
        words = full_text.split(" ")
        x = 20
        line = ""
        for word in words:
            if font.size(line + word)[0] < max_width:
                line += word + " "
            else:
                rendered = font.render(line, True, (0, 0, 0))
                dialogue_surface.blit(rendered, (x, y))
                y += 30
                line = word + " "
        rendered = font.render(line, True, (0, 0, 0))
        dialogue_surface.blit(rendered, (x, y))
        y += 35
    surface.blit(dialogue_surface, dialogue_rect.topleft)

def typewriter_response(text):
    global is_talking, frame_index, frame_timer
    is_talking = True
    typed = ""

    # TTS in a non-blocking way using engine.iterate()
    engine.stop()
    engine.say(text)
    engine.runAndWait()

    for char in text:
        typed += char
        if history and history[-1][0] == "ai":
            history[-1] = ("ai", typed)
        else:
            history.append(("ai", typed))
        now = pygame.time.get_ticks()
        if now - frame_timer > frame_delay:
            frame_timer = now
            frame_index = (frame_index + 1) % len(camille_frames)
        current_frame = camille_frames[frame_index]
        screen.blit(bg, (0, 0))
        screen.blit(current_frame, (SCREEN_WIDTH // 2 - 180, 150))
        screen.blit(dialogue_box, dialogue_rect.topleft)
        render_history_clipped(screen, history, 760, scroll_y)
        input_display = font.render("> " + user_text, True, (0, 0, 0))
        screen.blit(input_display, (50, SCREEN_HEIGHT - 55))
        pygame.display.flip()
        pygame.time.delay(20)

    is_talking = False

# --- MAIN LOOP ---
while True:
    now = pygame.time.get_ticks()
    screen.blit(bg, (0, 0))

    current_frame = camille_frames[frame_index] if is_talking else camille_idle
    screen.blit(current_frame, (SCREEN_WIDTH // 2 - 180, 150))

    screen.blit(dialogue_box, dialogue_rect.topleft)
    render_history_clipped(screen, history, 760, scroll_y)

    user_input_display = font.render("> " + user_text, True, (0, 0, 0))
    screen.blit(user_input_display, (50, SCREEN_HEIGHT - 55))

    pygame.display.flip()
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                scroll_y = max(0, scroll_y - 30)
            elif event.button == 5:
                scroll_y += 30
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if user_text.strip():
                    history.append(("user", user_text))
                    try:
                        response = agent.invoke(user_text)
                        reply = response["output"] if isinstance(response, dict) else str(response)
                        typewriter_response(reply)
                    except Exception as e:
                        history.append(("ai", f"[Erreur] {e}"))
                    user_text = ""
            elif event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            elif event.key == pygame.K_UP:
                scroll_y = max(0, scroll_y - 30)
            elif event.key == pygame.K_DOWN:
                scroll_y += 30
            else:
                if event.unicode.isprintable():
                    user_text += event.unicode