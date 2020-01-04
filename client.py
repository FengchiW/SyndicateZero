import pygame
from network import Network


pygame.font.init()

width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Syndicate Zero")


def redrawWindow(win, game, p):
    win.fill((128, 128, 128))

    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        msg = "Waiting for Players (1/2)..."
        text = font.render(msg, 1, (255, 0, 0), True)
        tw = width/2 - text.get_width()/2
        th = height/2 - text.get_height()/2
        win.blit(text, (tw, th))
    else:
        font = pygame.font.SysFont("comicsans", 60)

        hero1 = game.get_player_details(0)
        hero2 = game.get_player_details(1)

        loc_h1 = (hero1.stats.X_COORD, hero1.stats.Y_COORD)
        loc_h2 = (hero2.stats.X_COORD, hero2.stats.Y_COORD)

        text = font.render("P", 1, (255, 0, 0), True)
        win.blit(text, loc_h1)

        text = font.render("X", 1, (255, 0, 0), True)
        win.blit(text, loc_h2)

    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except EOFError:
            run = False
            print("Couldn't get game")
            break

        redrawWindow(win, game, player)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                n.send("1,0,"+str(pos[0])+","+str(pos[1]))

        redrawWindow(win, game, player)


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (255, 0, 0))
        win.blit(text, (100, 200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()


while True:
    menu_screen()
