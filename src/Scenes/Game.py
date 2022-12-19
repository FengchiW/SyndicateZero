import pyray as pr
from ..SceneManager import SceneManager, Scene
from ..util import Unit, Tile, Button, Card
from ..util import Map
from threading import Thread
from . import MainMenu

from pyray import check_collision_point_rec as checkCollision
from pyray import Color
from typing import Optional


class GameScene(Scene):
    def __init__(self, sm: SceneManager) -> None:
        super().__init__(sm, "Game")

    def onLoad(self):
        self.isLoaded = True
        self._sm.logMessage("Welcome to the game!")
        sw:           int = pr.get_screen_width()
        sh:           int = pr.get_screen_height()

        self.board:        Map = self._sm.rm.fetch_map('map1')
        self.screenWidth:  int = sw
        self.screenHeight: int = sh
        self.turn:         int = 0
        self.currentPhase: str = "Summon"
        self.units:        list[Unit] = []
        self.hand:         list[Card] = []
        self.opponentHand: list[Card] = []
        self.opponentDeck: list[Card] = [
            self._sm.rm.fetch_card('warrior') for _ in range(10)
        ]
        self.deck:         list[Card] = [
            self._sm.rm.fetch_card('warrior'),
            self._sm.rm.fetch_card('archer'),
            self._sm.rm.fetch_card('cavalry'),
            self._sm.rm.fetch_card('cavalry'),
            self._sm.rm.fetch_card('warrior'),
            self._sm.rm.fetch_card('warrior'),
            self._sm.rm.fetch_card('archer'),
        ]
        self.selectedUnit: Optional[Unit] = None
        self.gold:         int = 1
        self.bonusGold:    int = 0
        self.selectedCard: Optional[Card] = None
        self.hoveredTile:  Optional[Tile] = None

        self.endTurnButton = Button(sw - 200, sh - 50, 150, 50, "Next Phase",
                                    lambda: self.triggerEndTurn())

        self.spawnUnit = 'warrior'
        self.tileSize:          float = 50

        # Camera
        self.camera: pr.Camera2D = pr.Camera2D(
            pr.Vector2(0, 0),
            pr.Vector2(0, 0),
            0,
            1
        )

        self.cameraTarget = pr.Vector2(-self.tileSize * 2, -self.tileSize * 2)
        self.cameraZoom = 1

        # kings
        KingLoc1 = self.board[0, 0]

        if KingLoc1 is not None:
            self.playerKing = self._sm.rm.fetch_card('king').summonCard(KingLoc1, 0)
            self.units.append(
                self.playerKing
            )
            KingLoc1.occupant = self.units[0]

        KingLoc2 = self.board[0, 9]
        if KingLoc2 is not None:
            self.enemyKing = self._sm.rm.fetch_card('king').summonCard(KingLoc2, 1)
            self.units.append(
                self.enemyKing
            )
            KingLoc2.occupant = self.units[0]

        # draw cards
        for _ in range(3):
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
            self.endTurnButton.text = "Attack"
        elif self.currentPhase == "Attack":
            self.endTurnButton.text = "Waiting..."
            self.endTurnButton.isDisabled = True
            self.currentPhase = "Enemy Summon"

            self.summoningTiles = [
                tile for tile in self.board if tile.occupant is False
            ]

            for card in self.opponentHand:
                if self.summoningTiles:
                    self.units.append(card.summonCard(
                        self.summoningTiles.pop(), 1))
                    self.opponentHand.remove(card)

            self.endTurn()
        elif self.currentPhase == "Enemy Summon":
            self.currentPhase = "Enemy Move"
            enemyUnits = [unit for unit in self.units if unit.player == 1]

            for unit in enemyUnits:
                # find closest enemy unit
                closestUnit = None
                playerUnits = [u for u in self.units if u.player == 0]
                for u in playerUnits:
                    if closestUnit is None:
                        closestUnit = u
                    elif (self.board.getDistanceBetweenTiles(unit.tile, u.tile)
                            < self.board.getDistanceBetweenTiles(unit.tile, closestUnit.tile)):
                        closestUnit = u
                if closestUnit is not None:
                    # make a legal move closest to the closest enemy unit
                    bestMove: Optional[tuple[Tile, int]] = None
                    for move, dist in unit.getLegalMoves(self.board):
                        if bestMove is None:
                            bestMove = (move, dist)
                        elif dist < self.board.getDistanceBetweenTiles(move, closestUnit.tile):
                            bestMove = (move, dist)

                    if bestMove is not None:
                        unit.move(bestMove[0], bestMove[1])

            self.endTurn()
        elif self.currentPhase == "Enemy Move":
            self.currentPhase = "Enemy Attack"
            for unit in self.units:
                if unit.player == 1:
                    for tile in self.board:
                        if tile.occupant and tile.occupant.player == 0:
                            if unit.canAttackUnit(tile.occupant, self.board):
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
        mouseWorld = pr.get_screen_to_world_2d(mouse, self.camera)
        isATileHovered = False
        for tile in self.board:
            tile.hovered = False
            if tile.collisionShape.checkCollisionPoint(mouseWorld):
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
                self.units.remove(unit)

            if unit.player == 0:
                if self.currentPhase == "Move":
                    if unit.moves == unit.speed:
                        hasAllUnitsMoved = False
                elif self.currentPhase == "Attack":
                    if unit.player == 0:
                        canAttack = False
                        for tile in self.board:
                            if tile.occupant and tile.occupant.player == 1:
                                if unit.canAttackUnit(tile.occupant, self.board):
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
        if self.camera.zoom < self.cameraZoom:
            self.camera.zoom = pr.lerp(self.camera.zoom,
                                       self.cameraZoom, 10 * deltaTime)
        elif self.camera.zoom > self.cameraZoom:
            self.camera.zoom = pr.lerp(self.camera.zoom,
                                       self.cameraZoom, 10 * deltaTime)

        if self.cameraTarget.x < self.camera.target.x:
            self.camera.target.x = pr.lerp(self.camera.target.x,
                                           self.cameraTarget.x, 10 * deltaTime)
        elif self.cameraTarget.x > self.camera.target.x:
            self.camera.target.x = pr.lerp(self.camera.target.x,
                                           self.cameraTarget.x, 10 * deltaTime)

        if self.cameraTarget.y < self.camera.target.y:
            self.camera.target.y = pr.lerp(self.camera.target.y,
                                           self.cameraTarget.y, 10 * deltaTime)
        elif self.cameraTarget.y > self.camera.target.y:
            self.camera.target.y = pr.lerp(self.camera.target.y,
                                           self.cameraTarget.y, 10 * deltaTime)

    def draw(self) -> None:
        super().draw()
        pr.clear_background(Color(20, 100, 20, 255))
        self.drawBoard()
        self.drawUI()

    def handle_input(self) -> None:
        super().handle_input()

        if pr.is_key_down(pr.KEY_W) or pr.is_key_down(pr.KEY_UP):
            self.cameraTarget.y -= 5
        if pr.is_key_down(pr.KEY_S) or pr.is_key_down(pr.KEY_DOWN):
            self.cameraTarget.y += 5
        if pr.is_key_down(pr.KEY_A) or pr.is_key_down(pr.KEY_LEFT):
            self.cameraTarget.x -= 5
        if pr.is_key_down(pr.KEY_D) or pr.is_key_down(pr.KEY_RIGHT):
            self.cameraTarget.x += 5

        if pr.get_mouse_wheel_move() > 0:
            self.cameraZoom += 0.1
            self.cameraZoom = pr.clamp(self.cameraZoom, 0.1, 3)
        elif pr.get_mouse_wheel_move() < 0:
            self.cameraZoom -= 0.1
            self.cameraZoom = pr.clamp(self.cameraZoom, 0.1, 3)

        mouse = pr.get_mouse_position()
        mouseWorldPos = pr.get_screen_to_world_2d(mouse, self.camera)
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
                    if (self.hoveredTile.occupant):
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
                    if checkCollision(mouseWorldPos, unit.rect):
                        if pr.is_mouse_button_pressed(pr.MOUSE_LEFT_BUTTON):
                            self.selectedUnit = unit
                            for tile in self.board:
                                tile.highlighted = False
                            for tile, _ in self.selectedUnit.getLegalMoves(self.board):
                                tile.highlighted = True
                            break
            if (self.selectedUnit):
                legalMoves = self.selectedUnit.getLegalMoves(self.board)
                for tile, dist in legalMoves:
                    if tile.collisionShape.checkCollisionPoint(mouseWorldPos):
                        if pr.is_mouse_button_pressed(pr.MOUSE_LEFT_BUTTON):
                            if (not self.selectedUnit):
                                break
                            self.selectedUnit.move(tile, dist)
                            self.selectedUnit = None
                            for tile, _ in legalMoves:
                                tile.highlighted = False
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
                            if self.selectedUnit.canAttackUnit(unit, self.board):
                                self.selectedUnit.attackUnit(unit)
                                self.selectedUnit = None
                                break

        self.endTurnButton.handle_input(pr.get_mouse_position())
