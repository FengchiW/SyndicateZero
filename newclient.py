import pygame
from util.network import Network
import game
# from util.display import Display


class SceneBase:
    def __init__(self):
        self.next = self
        self.width = 1200
        self.height = 800

    def ProcessInput(self, events, pressed_keys):
        print("This function should be overwritten")

    def Update(self):
        print("This function should be overwritten")

    def Render(self, screen):
        print("This function should be overwritten")

    def SwitchToScene(self, next_scene):
        self.next = next_scene

    def Terminate(self):
        self.SwitchToScene(None)


def run_game(width, height, fps, starting_scene):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    active_scene = starting_scene

    while active_scene is not None:
        pressed_keys = pygame.key.get_pressed()

        # Event filtering
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            if event.type == pygame.QUIT:
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressed_keys[pygame.K_LALT] or \
                              pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_ESCAPE:
                    quit_attempt = True
                elif event.key == pygame.K_F4 and alt_pressed:
                    quit_attempt = True

            if quit_attempt:
                active_scene.Terminate()
            else:
                filtered_events.append(event)

        active_scene.ProcessInput(filtered_events, pressed_keys)
        active_scene.Update()
        active_scene.Render(screen)

        active_scene = active_scene.next

        pygame.display.flip()
        clock.tick(fps)


class MainMenu(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.addr = None
        self.active = False
        self.input_box = pygame.Rect(100, 100, 140, 32)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.input_text = None
        self.color = self.color_inactive

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_box.collidepoint(event.pos):
                    self.active = not self.active
                    self.input_text = ''
                else:
                    self.active = False
                self.color = self.color_active if self.active else self.color_inactive

            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        self.addr = self.input_text
                        self.SwitchToScene(GameLobby(self.input_text))
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.SwitchToScene(GameLobby(self.input_text))
                    else:
                        try:
                            if event.key == pygame.K_PERIOD:
                                self.input_text += event.unicode
                            else:
                                int(event.unicode)
                                self.input_text += event.unicode
                        except ValueError:  # TODO: Add error catch
                            pass
                else:
                    pass

    def Update(self):
        pass

    def Render(self, screen):
        screen.fill((255, 255, 255))

        font = pygame.font.SysFont("comicsans", 60)

        text = font.render(
            "Syndicate Zero",
            1,
            (255, 0, 0)
        )

        screen.blit(text, (0, 0))

        font = pygame.font.SysFont("comicsans", 30)

        text = font.render(
            "Click Anywhere To connect to the main Default Server",
            1,
            (100, 200, 100)
        )
        screen.blit(text, (0, text.get_height()+20))
        font = pygame.font.SysFont("comicsans", 20)

        txt_surface = font.render(self.input_text, True, self.color)
        width = max(200, txt_surface.get_width()+10)
        self.input_box.w = width
        screen.blit(txt_surface, (self.input_box.x+5, self.input_box.y+5))
        pygame.draw.rect(screen, self.color, self.input_box, 2)


class GameLobby(SceneBase):
    def __init__(self, addr):
        SceneBase.__init__(self)
        self.n = Network()
        self.addr = addr
        self.n.set_server_address(addr)
        self.attempts = 0
        self.connected = False
        self.msg = ""

    def ProcessInput(self, events, pressed_keys):
        pass

    def Update(self):
        print("Connecting to", self.n.addr[0], "on port", self.n.addr[1])
        self.connected = self.n.connect()
        if self.connected is False:
            self.msg = "Connection Failed Attempt ("+str(self.attempts)+"/5)"
            print(self.msg)
            self.attempts += 1
        else:
            self.SwitchToScene(GameScene(self.n))
        if self.attempts >= 6:
            print("Connection Failed")
            self.SwitchToScene(MainMenu())

    def Render(self, screen):
        screen.fill((128, 128, 128))
        tw = self.width/2
        th = self.height/2
        if self.connected:
            font = pygame.font.SysFont("comicsans", 80)
            msg = "Waiting for Players (1/2)..."
            text = font.render(msg, 1, (255, 0, 0), True)
            screen.blit(text, (int(tw - text.get_width()/2), int(th - text.get_height()/2)))
        else:
            font = pygame.font.SysFont("comicsans", 50)
            msg = "Connecting to " + str(self.addr) + " On port 5555..."
            text = font.render(msg, 1, (255, 0, 0), True)
            screen.blit(text, (int(tw - text.get_width()/2), int(th - text.get_height()/2)))
            text = font.render(self.msg, 1, (255, 0, 0), True)
            screen.blit(text, (int(tw - text.get_width()/2), int(th - text.get_height()*2)))


class GameScene(SceneBase):
    def __init__(self, n):
        SceneBase.__init__(self)
        self.Network = n
        self.shooting = False

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
                self.shooting = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.shooting = False
        if self.shooting:
            pos = pygame.mouse.get_pos()
            self.Network.send("2,"+str(pos[0])+","+str(pos[1]))
        w, d, a, s = "0", "0", "0", "0"
        if pressed_keys[pygame.K_w]:
            w = "1"
        if pressed_keys[pygame.K_s]:
            s = "1"
        if pressed_keys[pygame.K_a]:
            a = "1"
        if pressed_keys[pygame.K_d]:
            d = "1"
        self.Network.send("1,"+w+","+s+","+a+","+d)

    def Update(self):
        try:
            self.game = self.Network.send("ready")
        except EOFError:
            print("Couldn't ready game")
            self.SwitchToScene(MainMenu)

    def Render(self, screen):
        screen.fill((200, 200, 200))
        font = pygame.font.SysFont("comicsans", 60)

        hero1 = self.game.get_player_details(0)
        hero2 = self.game.get_player_details(1)

        projectiles = self.game.get_projectiles()

        for bullet in projectiles:
            pygame.draw.circle(screen, (255, 0, 0), (int(bullet.x), int(bullet.y)), 5)

        loc_h1 = (int(hero1.x), int(hero1.y))
        loc_h2 = (int(hero2.x), int(hero2.y))

        text = font.render("P", 1, (255, 0, 0), True)
        screen.blit(text, loc_h1)

        text = font.render("X", 1, (255, 0, 0), True)
        screen.blit(text, loc_h2)


run_game(1200, 800, 60, MainMenu())
