import pyray as pr
from ..SceneManager import SceneManager, Scene
from ..util import Unit, Tile, Button, distanceBetweenTiles, Card
from threading import Thread
from . import MainMenu

from pyray import check_collision_point_rec as checkCollision
from pyray import Color
from typing import Optional


BOARD_WIDTH = 10
BOARD_HEIGHT = 4


class GameScene(Scene):
    def __init__(self, sm: SceneManager) -> None:
        super().__init__(sm, "Game")
        sw:           int = pr.get_screen_width()
        sh:           int = pr.get_screen_height()
        sm.rm.load_card('Data/Cards/Warrior.json', 'warrior')
        sm.rm.load_card('Data/Cards/Tank.json', 'tank')
        sm.rm.load_card('Data/Cards/Archer.json', 'archer')
        sm.rm.load_card('Data/Cards/Cavalry.json', 'cavalry')
        sm.rm.load_card('Data/Cards/King.json', 'king')

        self.camera: pr.Camera2D = pr.Camera2D(
            pr.Vector2(0, 0), pr.Vector2(0, 0), 0, 1
        )
        self.board:        list[Tile] = []
        self.screenWidth:  int = sw
        self.screenHeight: int = sh
        self.turn:         int = 0
        self.currentPhase: str = "Summon"
        self.units:        list[Unit] = []
        self.hand:         list[Card] = []
        self.opponentHand: list[Card] = []
        self.opponentDeck: list[Card] = [
            Card(sm.rm.fetch_card('warrior')) for _ in range(10)
        ]
        self.deck:         list[Card] = [
            Card(sm.rm.fetch_card('warrior')),
            Card(sm.rm.fetch_card('archer')),
            Card(sm.rm.fetch_card('warrior')),
            Card(sm.rm.fetch_card('warrior')),
            Card(sm.rm.fetch_card('archer')),
        ]
        self.selectedUnit: Optional[Unit] = None
        self.gold:         int = 1
        self.bonusGold:    int = 0
        self.selectedCard: Optional[Card] = None
        self.hoveredTile:  Optional[Tile] = None

        self.endTurnButton = Button(sw - 200, sh - 50, 150, 50, "Next Phase",
                                    lambda: self.triggerEndTurn())

        self.spawnUnit = 'warrior'

        # Create board
        boardViewPortSize: tuple[int, int] = (sw, (sh * 3) // 4)
        for i in range(BOARD_HEIGHT):
            for j in range(BOARD_WIDTH):
                self.board.append(Tile(
                    i, j,
                    boardViewPortSize[0] / BOARD_WIDTH,
                    boardViewPortSize[1] / BOARD_HEIGHT,
                    pr.Vector2(j * (boardViewPortSize[0] / BOARD_WIDTH),
                               i * (boardViewPortSize[1] / BOARD_HEIGHT))
                ))

        # kings
        self.units.append(Unit(10, 4, 1, 1, "King",
                               pr.Vector2(
                                   self.board[0].rect.x,
                                   self.board[0].rect.y
                               ), self.board[0].rect.width,
                               self.board[0].rect.height, self.board[0], 0,
                          Card(sm.rm.fetch_card('king')))
                          )
        self.board[0].occupant = self.units[0]
        self.board[0].isOccupied = True
        self.units.append(Unit(10, 4, 1, 1, "King",
                               pr.Vector2(
                                   self.board[BOARD_WIDTH - 1].rect.x,
                                   self.board[BOARD_WIDTH - 1].rect.y
                               ), self.board[BOARD_WIDTH - 1].rect.width,
                               self.board[BOARD_WIDTH - 1].rect.height,
                               self.board[BOARD_WIDTH - 1], 1,
                          Card(sm.rm.fetch_card('king')))
                          )
        self.board[BOARD_WIDTH - 1].occupant = self.units[1]
        self.board[BOARD_WIDTH - 1].isOccupied = True

        self.playerKing = self.units[0]
        self.enemyKing = self.units[1]

        # draw cards
        for i in range(3):
            self.drawCard()
            self.opponentHand.append(self.opponentDeck.pop())

    def triggerEndTurn(self):
        t = Thread(target=self.endTurn)
        t.start()

    def drawCard(self):
        if len(self.deck) > 0:
            deckAreaWidth = self.screenWidth * 2 / 3
            deckAreaX = self.screenWidth / 6
            self.hand.append(self.deck.pop())
            deckLength = len(self.deck)
            self.hand[-1].setPosition(deckAreaX + deckAreaWidth *
                                      (deckLength / 10),
                                      self.screenHeight * 5 / 7)
            self.hand[-1].setSizeForHand(self.screenWidth, self.screenHeight)
            self.hand[-1].isInHand = True
            self.hand[-1].isSelectable = True
        else:
            return

    def endTurn(self):
        if self.playerKing.health <= 0:
            self._sm.logMessage("You lost!")
            self._sm.changeScene(MainMenu.MainMenu(self._sm))
        if self.enemyKing.health <= 0:
            self._sm.logMessage("You won!")
            self._sm.changeScene(MainMenu.MainMenu(self._sm))

        if self.currentPhase == "Summon":
            for unit in self.units:
                unit.reset()
            self.currentPhase = "Move"
            self.endTurnButton.text = "End Turn"
        elif self.currentPhase == "Move":
            self.currentPhase = "Attack"
            for unit in self.units:
                if unit.player == 1:
                    unit.reset()
            if self.enemyKing:
                pass
            self.endTurnButton.text = "Attack"
        elif self.currentPhase == "Attack":
            self.endTurnButton.text = "Waiting..."
            self.endTurnButton.isDisabled = True
            self.currentPhase = "Enemy Summon"

            self.summoningTiles = [
                tile for tile in self.board if tile.isOccupied is False
            ]

            for card in self.opponentHand:
                self.units.append(card.summonCard(
                    self.summoningTiles.pop(), 1))
                self.opponentHand.remove(card)

            self.endTurn()
        elif self.currentPhase == "Enemy Summon":
            self.currentPhase = "Enemy Move"
            for unit in self.units:
                if unit.player == 1:
                    # find closest enemy unit
                    closestUnit = None
                    for u in self.units:
                        if u.player == 0:
                            if closestUnit is None:
                                closestUnit = u
                            elif (distanceBetweenTiles(unit.tile, u.tile) <
                                  distanceBetweenTiles(closestUnit.tile,
                                                       u.tile)):
                                closestUnit = u
                    if closestUnit is not None:
                        # make a legal move towards the closest enemy unit
                        bestMove = None
                        for tile in self.board:
                            if unit.canMoveToTile(tile):
                                if bestMove is None:
                                    bestMove = tile
                                elif (distanceBetweenTiles(tile, closestUnit.tile)
                                        < distanceBetweenTiles(bestMove, closestUnit.tile)):
                                    bestMove = tile

                        if bestMove is not None:
                            unit.move(bestMove)

            self.endTurn()
        elif self.currentPhase == "Enemy Move":
            self.currentPhase = "Enemy Attack"
            for unit in self.units:
                if unit.player == 1:
                    for tile in self.board:
                        if tile.isOccupied and tile.occupant.player == 0:
                            if unit.canAttackUnit(tile.occupant):
                                unit.attackUnit(tile.occupant)
            if self.playerKing.health <= 0:
                self._sm.logMessage("You lose!")
                pass
            self.turn += 1
            self.endTurn()
        else:
            self.currentPhase = "Summon"
            self.endTurnButton.text = "Next Phase"
            self.drawCard()
            self.gold = self.turn
            self.endTurnButton.isDisabled = False

    def drawBoard(self):
        pr.begin_mode_2d(self.camera)
        for tile in self.board:
            tile.draw()
        for unit in self.units:
            unit.draw()

            if (self.currentPhase == "Attack"
                and unit.player == 0
                    and unit.hasAttacked):
                pr.draw_rectangle_rec(unit.rect, Color(255, 0, 0, 100))

        if (self.selectedUnit):
            pr.draw_rectangle_lines(int(self.selectedUnit.rect.x),
                                    int(self.selectedUnit.rect.y),
                                    int(self.selectedUnit.rect.width),
                                    int(self.selectedUnit.rect.height),
                                    Color(255, 255, 255, 255))
            if (self.currentPhase == "Move"):
                for tile in self.board:
                    if self.selectedUnit.canMoveToTile(tile):
                        pr.draw_rectangle_lines_ex(tile.rect, 2,
                                                   Color(255, 255, 255, 255))
            elif (self.currentPhase == "Attack"):
                for unit in self.units:
                    if self.selectedUnit.canAttackUnit(unit):
                        pr.draw_rectangle_lines_ex(unit.rect, 2,
                                                   Color(255, 255, 255, 255))
            else:
                pass

        pr.end_mode_2d()

    def drawUI(self):
        self.endTurnButton.draw()

        # draw the current turn number and phase
        pr.draw_text(f"Turn: {self.turn}",
                     self.screenWidth - 200,
                     self.screenHeight - 90,
                     20, Color(0, 0, 0, 255))
        pr.draw_text(f"Phase: {self.currentPhase}",
                     self.screenWidth - 200,
                     self.screenHeight - 70,
                     20, Color(0, 0, 0, 255))

        # draw the current gold

        # center of screen
        x: float = self.screenWidth // 2
        for i in range(self.gold):
            pr.draw_circle(x + (i * 20),
                           50, 5, Color(255, 255, 0, 200))

        # draw a character portrait
        pr.draw_rectangle(0, self.screenHeight - 200,
                          200, 200, Color(50, 50, 50, 200))

        # draw a health bar
        pr.draw_rectangle(0, self.screenHeight - 20, 200, 20,
                          Color(255, 0, 0, 100))
        pr.draw_rectangle(0, self.screenHeight - 20,
                          int(200 * self.playerKing.health /
                              self.playerKing.maxHealth), 20,
                          Color(0, 255, 0, 100))

        # draw cards in hand
        for i in range(len(self.hand)):
            self.hand[i].draw()

        if self.selectedCard:
            self.selectedCard.draw()

    def update(self, deltaTime: float) -> None:
        super().update(deltaTime)
        for card in self.hand:
            card.update(deltaTime)

        mouse = pr.get_mouse_position()
        isATileHovered = False
        for tile in self.board:
            tile.hovered = False
            if checkCollision(pr.get_screen_to_world_2d(mouse, self.camera),
                              tile.rect):
                tile.hovered = True
                isATileHovered = True
                self.hoveredTile = tile
        if not isATileHovered:
            self.hoveredTile = None

        hasAllUnitsMoved = True
        if len(self.units) == 0:
            hasAllUnitsMoved = False
        for unit in self.units:
            unit.update(deltaTime)
            if unit.health <= 0:
                unit.tile.occupant = None
                unit.tile.isOccupied = False
                self.units.remove(unit)

            if unit.player == 0:
                if self.currentPhase == "Move":
                    if unit.moves == unit.speed:
                        hasAllUnitsMoved = False
                elif self.currentPhase == "Attack":
                    if unit.player == 0:
                        canAttack = False
                        for tile in self.board:
                            if tile.isOccupied and tile.occupant.player == 1:
                                if unit.canAttackUnit(tile.occupant):
                                    canAttack = True
                        if ((not unit.hasAttacked) and canAttack):
                            hasAllUnitsMoved = False
                else:
                    hasAllUnitsMoved = False

        if not (self.currentPhase in ["Summon", "Attack", "Move"]):
            hasAllUnitsMoved = False

        if hasAllUnitsMoved:
            self.triggerEndTurn()

        # Camera movements
        if pr.is_key_down(pr.KEY_W):
            self.camera.target.y = pr.lerp(self.camera.target.y,
                                           self.camera.target.y - 10,
                                           20 * deltaTime)
        if pr.is_key_down(pr.KEY_S):
            self.camera.target.y = pr.lerp(self.camera.target.y,
                                           self.camera.target.y + 10,
                                           20 * deltaTime)
        if pr.is_key_down(pr.KEY_A):
            self.camera.target.x = pr.lerp(self.camera.target.x,
                                           self.camera.target.x - 10,
                                           20 * deltaTime)
        if pr.is_key_down(pr.KEY_D):
            self.camera.target.x = pr.lerp(self.camera.target.x,
                                           self.camera.target.x + 10,
                                           10 * deltaTime)
        mouseWheel = pr.get_mouse_wheel_move()
        self.camera.zoom = pr.lerp(self.camera.zoom,
                                   self.camera.zoom + 0.1,
                                   mouseWheel * 20 * deltaTime)

    def draw(self) -> None:
        super().draw()
        pr.clear_background(Color(20, 100, 20, 255))
        self.drawBoard()
        self.drawUI()

    def handle_input(self) -> None:
        super().handle_input()

        mouse = pr.get_mouse_position()
        if (self.selectedCard is None):
            for card in self.hand:
                if (card.is_mouse_over(mouse)):
                    if (self.selectedCard is None):
                        self.selectedCard = card
                        self.selectedCard.isHovered = True
        else:
            if (not self.selectedCard.is_mouse_over(mouse)):
                self.selectedCard.isHovered = False
                self.selectedCard = None
            elif (pr.is_mouse_button_down(pr.MOUSE_LEFT_BUTTON)):
                self.selectedCard.isHeld = True
            elif (self.selectedCard.isHeld):
                if (not (self.hoveredTile is None)):
                    if (self.hoveredTile.isOccupied):
                        self.selectedCard.isHeld = False
                    else:
                        if (self.gold >= self.selectedCard.cost):
                            self.gold -= self.selectedCard.cost
                            self.selectedCard.isHeld = False
                            self.selectedCard.isHovered = False
                            self.selectedCard.isSelectable = False
                            self.units.append(
                                self.selectedCard.summonCard(
                                    self.hoveredTile, 0)
                            )
                            self.hand.remove(self.selectedCard)
                self.selectedCard.isHeld = False
                self.selectedCard.isHovered = False
                self.selectedCard = None
            else:
                self.selectedCard.isHeld = False

        if self.currentPhase == "Move":
            for unit in self.units:
                if unit.player == 0:
                    if checkCollision(
                            pr.get_screen_to_world_2d(mouse,
                                                      self.camera), unit.rect):
                        if pr.is_mouse_button_pressed(pr.MOUSE_LEFT_BUTTON):
                            self.selectedUnit = unit
                            break
            if (self.selectedUnit):
                for tile in self.board:
                    if checkCollision(
                        pr.get_screen_to_world_2d(mouse,
                                                  self.camera), tile.rect):
                        if pr.is_mouse_button_pressed(pr.MOUSE_LEFT_BUTTON):
                            if self.selectedUnit.canMoveToTile(tile):
                                self.selectedUnit.move(tile)
                                self.selectedUnit = None
                                break
        elif self.currentPhase == "Attack":
            for unit in self.units:
                if unit.player == 0:
                    if checkCollision(pr.get_mouse_position(), unit.rect):
                        if pr.is_mouse_button_pressed(pr.MOUSE_LEFT_BUTTON):
                            self.selectedUnit = unit
                            break
            if (self.selectedUnit):
                for unit in self.units:
                    if checkCollision(pr.get_mouse_position(), unit.rect):
                        if pr.is_mouse_button_pressed(pr.MOUSE_LEFT_BUTTON):
                            if self.selectedUnit.canAttackUnit(unit):
                                self.selectedUnit.attackUnit(unit)
                                self.selectedUnit = None
                                break
        else:
            pass

        self.endTurnButton.handle_input(pr.get_mouse_position())
