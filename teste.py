import pygame
import pygame_gui as pgui
pygame.init()

# Defina as cores que você deseja usar
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Inicialize a janela
screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Campo de Texto no Pygame")
manager = pgui.UIManager((400,200))
text_input = pgui.elements.UITextEntryLine(relative_rect=pygame.Rect((30,50),(500,50)),manager=manager,object_id="#input")


clock = pygame.time.Clock()
fps = 60
running = True
texto = ''
while running:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pgui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#input":
            texto = event.text
        manager.process_events(event)
    
    print(texto)
    manager.update(clock.tick(fps)/1000)
    screen.fill(WHITE)
    manager.draw_ui(screen)
    pygame.display.update()

pygame.quit()
