const inputMessage = document.getElementById('inputMessage');
const messages = document.getElementById('messages');

class Bullet extends Phaser.Physics.Arcade.Sprite
{
    constructor (scene, x, y)
    {
        super(scene, x, y, 'bullet');
        this.startX = 0
        this.startY = 0
    }

    reset(x, y) 
    {
        this.startX = x
        this.startY = y
        this.body.reset(x ,y)
    }

    fire (x, y, dirx, diry)
    {
        this.reset(x, y);

        this.setActive(true);
        this.setVisible(true);

        this.setVelocityX(dirx * 100);
        this.setVelocityY(diry * 100);
    }

    preUpdate (time, delta)
    {
        super.preUpdate(time, delta);

        if (Math.sqrt(Math.pow((this.x - this.startX), 2) + Math.pow((this.y - this.startY), 2) ) > 100)
        {
            console.log(this.startX, this.startY, this.x, this.y)
            this.reset(0, 0)
            this.setActive(false);
            this.setVisible(false);
        }
    }

    bullethit (obj)
    {
        console.log("hit")
        this.reset(0, 0)
        this.setActive(false);
        this.setVisible(false);
    }
}

class Bullets extends Phaser.Physics.Arcade.Group
{
    constructor (scene)
    {
        super(scene.physics.world, scene);

        this.createMultiple({
            frameQuantity: 50,
            key: 'bullet',
            active: false,
            visible: false,
            classType: Bullet
        });
    }

    fireBullet (x, y, dirx, diry)
    {
        let bullet = this.getFirstDead(false);

        if (bullet)
        {
            bullet.fire(x, y, dirx, diry);
        }
    }
}