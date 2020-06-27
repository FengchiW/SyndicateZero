import pygame
from network import Network
from _thread import start_new_thread
from util.display import Display
# from util.camera import Camera

pygame.font.init()

win = pygame.display.set_mode(
    (1000, 800),
    pygame.DOUBLEBUF | pygame.RESIZABLE
)
pygame.display.set_caption("Syndicate Zero")

width = win.get_width()
height = win.get_height()


def connect(n, arg):
    print("Attempting to Connect to", n.addr[0], "on port", n.addr[1])
    n.try_connection()


def redrawWindow(win, game, p, disp):
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

        disp.draw_Hud(win)

    pygame.display.update()


def main(addr=None):
    print(addr)
    run = True
    clock = pygame.time.Clock()
    n = Network()
    n.set_server_address(addr)
    connected = False
    i = 1

    start_new_thread(connect, (n, None))

    while connected is False:
        if n.getP() is None:
            pygame.time.delay(1000)
            print("Connection Failed Trying again ("+str(i)+"/10)")
            i = i + 1
        else:
            connected = True
        if i >= 11:
            print("Connection Failed")
            menu_screen()

    player = int(n.getP())
    print("You are player", player)

    Disp = Display()

    while run:
        clock.tick(60)
        try:
            game = n.send("ready")
        except EOFError:
            run = False
            print("Couldn't ready game")
            break

        redrawWindow(win, game, player, Disp)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                n.send("1,0,"+str(pos[0])+","+str(pos[1]))

        redrawWindow(win, game, player, Disp)


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    addr = None

    input_box = pygame.Rect(100, 100, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    input_text = 'Different Server? Enter the IP Here and press the ENTER key'

    while run:
        clock.tick(60)
        win.fill((0, 0, 0))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render(
            "Syndicate Zero",
            1,
            (255, 0, 0)
        )
        win.blit(text, (0, 0))

        font = pygame.font.SysFont("comicsans", 30)
        text = font.render(
            "Click Anywhere To connect to the main Default Server",
            1,
            (100, 200, 100)
        )
        win.blit(text, (0, text.get_height()+20))
        font = pygame.font.SysFont("comicsans", 20)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                    input_text = ''
                else:
                    active = False
                color = color_active if active else color_inactive
                if not active:
                    run = False
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        addr = input_text
                        run = False
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        try:
                            if event.key == pygame.K_PERIOD:
                                input_text += event.unicode
                            else:
                                int(event.unicode)
                                input_text += event.unicode
                        except ValueError:
                            text = font.render(
                                "ERROR NUMEBRS ONLY",
                                1,
                                (100, 200, 100)
                            )
                            win.blit(text, (0, text.get_height()+50))
                            pygame.display.flip()
                            pygame.time.delay(300)

        txt_surface = font.render(input_text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        win.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(win, color, input_box, 2)

        pygame.display.flip()

    main(addr)


while True:
    menu_screen()
