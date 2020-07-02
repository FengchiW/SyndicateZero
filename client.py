import pygame
from util.network import Network
from slack import Game
from math import sqrt
from entities import Player, Bullet
# from util.display import Display

version = "1.3.2"

width = 1280
height = 720

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, (1280, 720))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class SceneBase:
    def __init__(self):
        self.next = self
        self.width = 1280
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
    gameIcon = pygame.image.load('res/Icon.PNG')
    pygame.display.set_icon(gameIcon)
    pygame.display.set_caption('SyndicateZero V' + version)
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    frame = 0

    active_scene = starting_scene

    while active_scene is not None:
        if frame < 30:
            frame += 1
        else:
            frame = 0
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
        active_scene.Update(frame)
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
        self.bg = Background('res/background.PNG', [0,0])

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

    def Update(self, frame):
        pass

    def Render(self, screen):
        screen.fill((255, 255, 255))

        font = pygame.font.SysFont("comicsans", 60)

        screen.blit(self.bg.image, self.bg.rect)

        text = font.render(
            "Syndicate Zero",
            1,
            (255, 0, 0)
        )

        screen.blit(text, (0, 0))

        font = pygame.font.SysFont("comicsans", 20)

        text = font.render(
            "Client Version " + version,
            1,
            (0, 0, 0)
        )

        screen.blit(text, (0, 800 - text.get_height()))

        font = pygame.font.SysFont("comicsans", 30)

        text = font.render(
            "Connect to the slow server at 34.71.202.82 or the FAST server at 172.105.110.216",
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

    def Update(self, frame):
        print("Connecting to", self.n.addr[0], "on port", self.n.addr[1])
        self.connected = self.n.connect()
        if self.connected is False:
            self.msg = "Connection Failed Attempt ("+str(self.attempts)+"/5)"
            print(self.msg)
            self.attempts += 1
        else:
            self.SwitchToScene(GameScene(self.n, self.connected))
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
    def __init__(self, n, pid):
        SceneBase.__init__(self)
        self.projectiles = []
        self.Network = n
        self.playerData = self.Network.send("ready")
        self.shooting = False
        self.player = Player(pid)
        self.pid = int(pid)
        self.velocityY = 0
        self.velocityX = 0

    def move_to_pos(self, loc):
            spd = self.player.stats.MOVEMENT_SPEED / 25
            if abs(self.velocityY) < self.player.stats.MOVEMENT_SPEED:
                if loc == 1:
                    self.velocityY -= spd
                if loc == 2:
                    self.velocityY += spd
            if abs(self.velocityX) < self.player.stats.MOVEMENT_SPEED:
                if loc == 3:
                    self.velocityX -= spd
                if loc == 4:
                    self.velocityX += spd
    
    def move(self):
        if self.player.x < 0:
            self.velocityX = 5
        elif self.player.x > 1150:
            self.velocityX = -5
        if self.player.y < 0:
            self.velocityY = 5
        elif self.player.y > 700:
            self.velocityY = -5
        self.player.x += self.velocityX
        self.velocityX *= 0.8
        self.player.y += self.velocityY
        self.velocityY *= 0.8

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
                self.player.shooting = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.player.shooting = False

        if pressed_keys[pygame.K_w]:
            self.move_to_pos(1)
        if pressed_keys[pygame.K_s]:
            self.move_to_pos(2)
        if pressed_keys[pygame.K_a]:
            self.move_to_pos(3)
        if pressed_keys[pygame.K_d]:
            self.move_to_pos(4)
    
    def bullet_move(self, b):
        b.x += 5 * b.dir[0]
        b.y += 5 * b.dir[1]

    def Update(self, frame):
        try:
            self.playerData = self.Network.send("ready")
            self.player.stats.HITPOINTS = self.playerData[self.pid].stats.HITPOINTS
        except EOFError:
            print("Couldn't ready game")
            self.Network.disconect()
            self.SwitchToScene(MainMenu())
        except IndexError:
            self.player.id = self.playerData[int(self.player.id) - 1].id

        self.move()

        pos = pygame.mouse.get_pos()
        self.player.lookingAt = (pos[0],pos[1])

        dead = []
        for bullet in range(len(self.projectiles)):
            curr = self.projectiles[bullet]
            if sqrt((int(curr.x - curr.origin[0]) ** 2 + int(curr.y - curr.origin[1]) ** 2)) < 300:
                for player in self.playerData:
                    if player.id != curr.id:
                        if (player.x - 16) < curr.x and (player.x + 16) > curr.x:
                            if (player.y - 16) < curr.y and (player.y + 16) > curr.y:
                                self.Network.send("hit"+str(player.id))
                                dead.append(bullet)
                self.bullet_move(curr)
            else:
                dead.append(bullet)

        self.projectiles = [(self.projectiles[bullet]) for bullet in range(len(self.projectiles)) if bullet not in dead]

        heros = self.playerData

        for hero in heros:
            if hero.shooting and frame % int(600/hero.stats.DEXTARITY) == 0:
                self.projectiles.append(Bullet(hero.id, hero.x, hero.y, hero.lookingAt[0], hero.lookingAt[1]))


        try:
            self.Network.send(self.player)
            if self.player.stats.HITPOINTS < 0:
                self.Network.disconect()
                self.SwitchToScene(MainMenu())
        except EOFError:
            print("Couldn't ready game")
            self.Network.disconect()
            self.SwitchToScene(MainMenu())
        

    def Render(self, screen):
        screen.fill((200, 200, 200))
        font = pygame.font.SysFont("comicsans", 60)

        heros = self.playerData
        
        for hero in heros:
            loc = (int(hero.x), int(hero.y))
            text = font.render("X", 1, (int(255 * ((int(hero.id)+1)/(len(heros)+1))), 255 * ((int(hero.id)+1)/(len(heros)+1)), 0), True)
            screen.blit(text, loc)

            hp = pygame.Rect(loc[0] - 16, loc[1] + 42, 64, 10)
            pygame.draw.rect(screen, (0, 0, 0), hp)
            curhp = pygame.Rect(loc[0] - 16, loc[1] + 42, int(64 * hero.stats.HITPOINTS/hero.stats.MAX_HITPOINTS) , 10)
            pygame.draw.rect(screen, (255, 0, 0), curhp)


        for bullet in self.projectiles:
            pygame.draw.circle(screen, (255, 0, 0), (int(bullet.x), int(bullet.y)), 5)

        hp = pygame.Rect(0, 750, 1200, 50)
        pygame.draw.rect(screen, (0, 0, 0), hp)
        curhp = pygame.Rect(0, 750, int(1200 * self.player.stats.HITPOINTS/self.player.stats.MAX_HITPOINTS) , 50)
        pygame.draw.rect(screen, (255, 0, 0), curhp)

        font = pygame.font.SysFont("comicsans", 30)

        text = font.render(
            str(self.player.stats.MAX_HITPOINTS) + " / " + str(self.player.stats.HITPOINTS),
            1,
            (0, 0, 0)
        )


        screen.blit(text, (int(600 - text.get_width()/2), int(800 - text.get_height())))
    
