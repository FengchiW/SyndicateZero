import pyray as pr
from ..SceneManager import SceneManager, Scene
from ..util import Unit, Tile, summonUnit, Button, distanceBetweenTiles
import random
from threading import Thread


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

        self.board:        list[Tile] = []
        self.screenWidth:  int = sw
        self.screenHeight: int = sh
        self.turn:         int = 0
        self.currentPhase: str = "Summon"
        self.units:        list[Unit] = []
        self.hand:         list[Tile] = []
        self.graveyard:    list[Unit] = []
        self.deck:         list[Unit] = []
        self.selectedUnit: Optional[Unit] = None
        self.gold:         int = 1
        self.bonusGold:    int = 0

        self.endTurnButton = Button(sw - 200, sh - 50, 150, 50, "Next Phase",
                                    lambda: self.triggerEndTurn())

        self.spawnUnit = 'warrior'
        self.spawnButton = Button(sw - 350, sh - 50, 150, 50, "Warrior",
                                  lambda: self.switchUnit())

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
                               self.board[0].rect.height, self.board[0], 0)
                          )
        self.board[0].occupant = self.units[0]
        self.board[0].isOccupied = True
        self.units.append(Unit(10, 4, 1, 1, "King",
                               pr.Vector2(
                                   self.board[BOARD_WIDTH - 1].rect.x,
                                   self.board[BOARD_WIDTH - 1].rect.y
                               ), self.board[BOARD_WIDTH - 1].rect.width,
                               self.board[BOARD_WIDTH - 1].rect.height,
                               self.board[BOARD_WIDTH - 1], 1)
                          )
        self.board[BOARD_WIDTH - 1].occupant = self.units[1]
        self.board[BOARD_WIDTH - 1].isOccupied = True

        self.playerKing = self.units[0]
        self.enemyKing = self.units[1]

    def triggerEndTurn(self):
        t = Thread(target=self.endTurn)
        t.start()

    def switchUnit(self):
        if self.spawnUnit == 'warrior':
            self.spawnUnit = 'tank'
            self.spawnButton.text = 'tank'
        elif self.spawnUnit == 'tank':
            self.spawnUnit = 'archer'
            self.spawnButton.text = 'archer'
        elif self.spawnUnit == 'archer':
            self.spawnUnit = 'cavalry'
            self.spawnButton.text = 'cavalry'
        elif self.spawnUnit == 'cavalry':
            self.spawnUnit = 'warrior'
            self.spawnButton.text = 'warrior'

    def endTurn(self):
        if self.currentPhase == "Summon":
            for unit in self.units:
                if unit.player == 0:
                    unit.update()
            self.currentPhase = "Move"
            self.endTurnButton.text = "End Turn"
        elif self.currentPhase == "Move":
            self.currentPhase = "Attack"
            for unit in self.units:
                if unit.player == 1:
                    unit.update()
            if self.enemyKing:
                pass
            self.endTurnButton.text = "Attack"
        elif self.currentPhase == "Attack":
            self.endTurnButton.text = "Waiting..."
            self.endTurnButton.isDisabled = True
            self.currentPhase = "Enemy Summon"
            summoningSquares = [self.board[9],
                                self.board[19], self.board[29], self.board[39]]
            canSpawn = self.turn
            for i in range(4):
                if canSpawn < 0:
                    break
                tile = summoningSquares[i]
                willSpawn = random.randint(0, 3)
                if self.turn > 3:
                    willSpawn = random.randint(1, 3)
                if self.turn > 6:
                    willSpawn = random.randint(2, 3)
                if willSpawn == 0:
                    self.units.append(Unit(2, 1, 1, 2, "warrior",
                                           pr.Vector2(
                                               tile.rect.x, tile.rect.y),
                                           tile.rect.width, tile.rect.height,
                                           tile,
                                           1))
                    if (not summonUnit(self.units[-1], tile)):
                        self.units.pop()
                        canSpawn += 1
                elif willSpawn == 1:
                    self.units.append(Unit(6, 1, 1, 1, "tank",
                                           pr.Vector2(
                                               tile.rect.x, tile.rect.y),
                                           tile.rect.width, tile.rect.height,
                                           tile,
                                           1))
                    if (not summonUnit(self.units[-1], tile)):
                        self.units.pop()
                        canSpawn += 1
                elif willSpawn == 2:
                    self.units.append(Unit(1, 3, 3, 2, "archer",
                                           pr.Vector2(
                                               tile.rect.x, tile.rect.y),
                                           tile.rect.width, tile.rect.height,
                                           tile,
                                           1))
                    if (not summonUnit(self.units[-1], tile)):
                        self.units.pop()
                        canSpawn += 1
                elif willSpawn == 4:
                    self.units.append(Unit(4, 2, 1, 4, "cavalry",
                                           pr.Vector2(
                                               tile.rect.x, tile.rect.y),
                                           tile.rect.width, tile.rect.height,
                                           tile,
                                           1))
                    if (not summonUnit(self.units[-1], tile)):
                        self.units.pop()
                        canSpawn += 1
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
            self.gold = self.turn
            self.endTurnButton.isDisabled = False

    def drawBoard(self):
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

    def drawUI(self):
        self.endTurnButton.draw()
        self.spawnButton.draw()

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
        pr.draw_rectangle(0, self.screenHeight - 20, 150, 20,
                          Color(0, 255, 0, 100))

        # draw cards in hand
        for i in range(len(self.hand)):
            self.hand[i].draw()

    def update(self, deltaTime: float) -> None:
        super().update(deltaTime)
        mouse = pr.get_mouse_position()
        for tile in self.board:
            tile.hovered = False
            if checkCollision(mouse, tile.rect):
                tile.hovered = True

        hasAllUnitsMoved = True
        if len(self.units) == 0:
            hasAllUnitsMoved = False
        for unit in self.units:
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

        if self.currentPhase == "Summon":
            summoningTiles = [self.board[0], self.board[10],
                              self.board[20], self.board[30]]
            for tile in summoningTiles:
                if tile.isOccupied:
                    hasAllUnitsMoved = False

        if hasAllUnitsMoved:
            self.triggerEndTurn()

    def draw(self) -> None:
        super().draw()
        self.drawBoard()
        self.drawUI()

    def handle_input(self) -> None:
        super().handle_input()
        if self.currentPhase == "Summon":
            mouse = pr.get_mouse_position()
            summoningTiles = [self.board[0], self.board[10],
                              self.board[20], self.board[30]]
            for tile in summoningTiles:
                if checkCollision(mouse, tile.rect):
                    if (pr.is_mouse_button_pressed(pr.MOUSE_LEFT_BUTTON)
                            and self.gold > 0):
                        if self.spawnUnit == "warrior":
                            self.gold -= 1
                            self.units.append(
                                Unit(2, 1, 1, 2, "warrior",
                                     pr.Vector2(tile.rect.x, tile.rect.y),
                                     tile.rect.width, tile.rect.height, tile, 0))
                            if (not summonUnit(self.units[-1], tile)):
                                self.gold += 1
                                self.units.pop()
                        elif self.spawnUnit == "tank":
                            if self.gold >= 2:
                                self.gold -= 2
                                self.units.append(
                                    Unit(6, 1, 1, 1, "tank",
                                         pr.Vector2(tile.rect.x, tile.rect.y),
                                         tile.rect.width, tile.rect.height, tile, 0))
                                if (not summonUnit(self.units[-1], tile)):
                                    self.gold += 1
                                    self.units.pop()
                        elif self.spawnUnit == "archer":
                            if self.gold >= 2:
                                self.gold -= 2
                                self.units.append(
                                    Unit(1, 3, 2, 2, "archer",
                                         pr.Vector2(tile.rect.x, tile.rect.y),
                                         tile.rect.width, tile.rect.height, tile, 0))
                                if (not summonUnit(self.units[-1], tile)):
                                    self.gold += 2
                                    self.units.pop()
                        elif self.spawnUnit == "cavalry":
                            if self.gold >= 3:
                                self.gold -= 3
                                self.units.append(
                                    Unit(4, 2, 1, 3, "cavalry",
                                         pr.Vector2(tile.rect.x, tile.rect.y),
                                         tile.rect.width, tile.rect.height, tile, 0))
                                if (not summonUnit(self.units[-1], tile)):
                                    self.gold += 3
                                    self.units.pop()
                        if self.gold == 0:
                            self.triggerEndTurn()
        elif self.currentPhase == "Move":
            for unit in self.units:
                if unit.player == 0:
                    if checkCollision(pr.get_mouse_position(), unit.rect):
                        if pr.is_mouse_button_pressed(pr.MOUSE_LEFT_BUTTON):
                            self.selectedUnit = unit
                            break
            if (self.selectedUnit):
                for tile in self.board:
                    if checkCollision(pr.get_mouse_position(), tile.rect):
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
            # Unknown phase
            pass

        self.endTurnButton.handle_input(pr.get_mouse_position())
        self.spawnButton.handle_input(pr.get_mouse_position())
