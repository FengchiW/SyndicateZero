const inputMessage = document.getElementById('inputMessage');
const messages = document.getElementById('messages');

class BootScene extends Phaser.Scene {
  constructor() {
    super({
      key: 'BootScene',
      active: true
    });
  }

  preload() {
    // map tiles
    this.load.image('tiles', 'assets/map/spritesheet-extruded.png');
    // map in json format
    this.load.tilemapTiledJSON('map', 'assets/map/map.json');
    // our two characters
    this.load.spritesheet('player', 'assets/RPG_assets.png', {
      frameWidth: 16,
      frameHeight: 16
    });
  }

  create() {
    this.scene.start('WorldScene');
  }
}

class WorldScene extends Phaser.Scene {
  constructor() {
    super({
      key: 'WorldScene'
    });
  }

  create() {
    this.socket = io();
    this.otherPlayers = this.physics.add.group();

    // create map
    this.createMap();

    // create player animations
    this.createAnimations();

    // user input
    this.cursors = this.input.keyboard.addKeys(
        {up:Phaser.Input.Keyboard.KeyCodes.W,
        down:Phaser.Input.Keyboard.KeyCodes.S,
        left:Phaser.Input.Keyboard.KeyCodes.A,
        right:Phaser.Input.Keyboard.KeyCodes.D});

    // listen for web socket events
    this.socket.on('currentPlayers', function (players) {
      Object.keys(players).forEach(function (id) {
        if (players[id].playerId === this.socket.id) {
          this.createPlayer(players[id]);
        } else {
          this.addOtherPlayers(players[id]);
        }
      }.bind(this));
    }.bind(this));

    this.socket.on('newPlayer', function (playerInfo) {
      this.addOtherPlayers(playerInfo);
    }.bind(this));

    this.socket.on('playerdisconnected', function (playerId) {
      this.otherPlayers.getChildren().forEach(function (player) {
        if (playerId === player.playerId) {
          console.log("[Info] Player Disconnected")
        }
      }.bind(this));
    }.bind(this));

    this.socket.on('playerMoved', function (playerInfo) {
      this.otherPlayers.getChildren().forEach(function (player) {
        if (playerInfo.playerId === player.playerId) {
          player.flipX = playerInfo.flipX;
          player.setPosition(playerInfo.x, playerInfo.y);
        }
      }.bind(this));
    }.bind(this));
  }

  createMap() {
    // create the map
    this.map = this.make.tilemap({
      key: 'map'
    });

    // first parameter is the name of the tilemap in tiled
    var tiles = this.map.addTilesetImage('spritesheet', 'tiles', 16, 16, 1, 2);

    // creating the layers
    var grass = this.map.createStaticLayer('Grass', tiles, 0, 0);
    var obstacles = this.map.createStaticLayer('Obstacles', tiles, 0, 0);

    obstacles.setCollisionByExclusion([-1]);

    // don't go out of the map
    this.physics.world.bounds.width = this.map.widthInPixels;
    this.physics.world.bounds.height = this.map.heightInPixels;
  }

  createAnimations() {
    //  animation with key 'left', we don't need left and right as we will use one and flip the sprite
    this.anims.create({
      key: 'left',
      frames: this.anims.generateFrameNumbers('player', {
        frames: [1, 7, 1, 13]
      }),
      frameRate: 10,
      repeat: -1
    });

    // animation with key 'right'
    this.anims.create({
      key: 'right',
      frames: this.anims.generateFrameNumbers('player', {
        frames: [1, 7, 1, 13]
      }),
      frameRate: 10,
      repeat: -1
    });

    this.anims.create({
      key: 'up',
      frames: this.anims.generateFrameNumbers('player', {
        frames: [2, 8, 2, 14]
      }),
      frameRate: 10,
      repeat: -1
    });

    this.anims.create({
      key: 'down',
      frames: this.anims.generateFrameNumbers('player', {
        frames: [0, 6, 0, 12]
      }),
      frameRate: 10,
      repeat: -1
    });
  }

  createPlayer(playerInfo) {
    // our player sprite created through the physics system
    this.player = this.add.sprite(0, 0, 'player', 6);

    this.container = this.add.container(playerInfo.x, playerInfo.y);
    this.container.setSize(16, 16);
    this.physics.world.enable(this.container);
    this.container.add(this.player);

    // update camera
    this.updateCamera();

    // don't go out of the map
    this.container.body.setCollideWorldBounds(true);

    this.container.body.setOnCollideWith(t)
  }

  addOtherPlayers(playerInfo) {
    const otherPlayer = this.add.sprite(playerInfo.x, playerInfo.y, 'player', 6);
    otherPlayer.setTint(Math.random() * 0xffffff);
    otherPlayer.playerId = playerInfo.playerId;
    this.otherPlayers.add(otherPlayer);
  }

  updateCamera() {
    // limit camera to map
    this.cameras.main.setBounds(0, 0, this.map.widthInPixels, this.map.heightInPixels);
    this.cameras.main.startFollow(this.container);
    this.cameras.main.roundPixels = true; // avoid tile bleed
  }

  update() {
    if (this.container) {
      this.container.body.setVelocity(0);

      // Horizontal movement
      if (this.cursors.left.isDown) {
        this.container.body.setVelocityX(-80);
      } else if (this.cursors.right.isDown) {
        this.container.body.setVelocityX(80);
      }

      // Vertical movement
      if (this.cursors.up.isDown) {
        this.container.body.setVelocityY(-80);
      } else if (this.cursors.down.isDown) {
        this.container.body.setVelocityY(80);
      }

      // Update the animation last and give left/right animations precedence over up/down animations
      if (this.cursors.left.isDown) {
        this.player.anims.play('left', true);
        this.player.flipX = true;
      } else if (this.cursors.right.isDown) {
        this.player.anims.play('right', true);
        this.player.flipX = false;
      } else if (this.cursors.up.isDown) {
        this.player.anims.play('up', true);
      } else if (this.cursors.down.isDown) {
        this.player.anims.play('down', true);
      } else {
        this.player.anims.stop();
      }

      // emit player movement
      var x = this.container.x;
      var y = this.container.y;
      var flipX = this.player.flipX;
      if (this.container.oldPosition && (x !== this.container.oldPosition.x || y !== this.container.oldPosition.y || flipX !== this.container.oldPosition.flipX)) {
        this.socket.emit('playerMovement', { x, y, flipX });
      }
      // save old position data
      this.container.oldPosition = {
        x: this.container.x,
        y: this.container.y,
        flipX: this.player.flipX
      };
    }
  }
}

var config = {
  type: Phaser.AUTO,
  parent: 'content',
  width: 320,
  height: 240,
  zoom: 3,
  pixelArt: true,
  physics: {
    default: 'arcade',
    arcade: {
      gravity: {
        y: 0
      },
      debug: false // set to true to view zones
    }
  },
  scene: [
    BootScene,
    WorldScene
  ]
};
var game = new Phaser.Game(config);

