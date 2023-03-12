""" Platformer Game"""

import arcade

# constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer Game"

#Sprites scaling factors
CHARACTER_SCALING = 0.7
TILE_SCALING = 0.5

#Player move speed constant
PLAYER_MOVEMENT_SPEED = 5# No. of pixels per update our character travels
GRAVITY = 1 #represents acceleration for gravity
PLAYER_JUMP_SPEED = 20
COIN_SCALING = 0.5
CLOUD_SCALING = 0.09

class MyGame(arcade.Window):
    """ Main Application class"""

    def __init__(self): #contains variables initialized
        # calling the parent class and window setup
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # # lists that keep track of the sprites
        # self.wall_list = None
        # self.player_list = None

        # scene object-->manages a number of different SpriteLists
        self.scene = None

        self.player_sprite = None #variable that holds the player sprite

        self.physics_engine = None #physics engine

        #a camera used for scrolling the screen
        self.camera = None

        # Another camera used to draw GUI elements
        self.gui_camera = None

        # variable to keep track of score
        self.score = 0

        self.points_left = 24

        self.timer = 0.0

        # loading the sounds
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.collect_gem_sound = arcade.load_sound(":resources:sounds/coin4.wav")

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """Game set up is done here. Call this function to restart the game."""

        #initialize the camera, i.e. setup the game camera
        self.camera = arcade.Camera(self.width, self.height)

        # settting up the GUI camera
        self.gui_camera = arcade.Camera(self.width, self.height)

        #score set to 0 here because this fn. is intended to fully reset the game
        self.score = 0
        self.points_left = 24

        # initializing scene
        self.scene = arcade.Scene()

        #create sprite lists
        # self.player_list = arcade.SpriteList()
        # self.wall_list = arcade.SpriteList(use_spatial_hash=True)#Spatial hashing speeds the time it takes to find collisions
        
        #initializing the scene obj and adding SpriteLists instead of doing as above
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)

        # setting up the player
        image_source = ":resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 109
        # self.player_list.append(self.player_sprite)
        self.scene.add_sprite("Player", self.player_sprite)

        # creating the ground
        # using loop to iterate multiple sprites horizontally
        for x in range(0, 2250, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            # self.wall_list.append(wall)
            self.scene.add_sprite("Walls", wall)

        #putting some crates on the ground
        # for that coordinate list is used to place these sprites
        coordinate_list = [[320, 96], [512, 96], [704, 96],[768, 96], [768, 150], [967, 96], [1260, 96], [1520, 96]]

        for coordinate in coordinate_list:
            #adding crates on the ground
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", TILE_SCALING)
            wall.position = coordinate
            # self.wall_list.append(wall)
            self.scene.add_sprite("Walls", wall)

        #creating a physics engine for the player to move
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Walls"])

        #using loop to place coins
        for x in range(128, 2250, 256):
            coin = arcade.Sprite(":resources:images/items/coinGold.png", COIN_SCALING)
            coin.center_x = x
            coin.center_y = 96
            self.scene.add_sprite("Coins", coin)

        for x in range(550, 2250, 650):
            coin = arcade.Sprite(":resources:images/items/coinGold.png", COIN_SCALING)
            coin.center_x = x
            coin.center_y = 225
            self.scene.add_sprite("Coins", coin)

        for x in range(200, 2250, 530):
            gem = arcade.Sprite(":resources:images/items/gemBlue.png", COIN_SCALING)
            gem.center_x = x
            gem.center_y = 215
            self.scene.add_sprite("Gems", gem)

        # cloude coordinate list
        cloud_coordinate_list = [[-20, 490], [120, 550], [210, 510], [370, 450], [512, 590], [628, 570], 
                                 [767, 606], [830, 589], [950, 530], [1120, 560], [1285, 490], [1430, 520],
                                 [1487, 560], [1680, 550], [1810, 520], [1940, 567], [2055, 530], [2200, 549]]
        for cloud_coordinate in cloud_coordinate_list:
            cloud = arcade.Sprite("cloud.png", CLOUD_SCALING)
            cloud.position = cloud_coordinate
            self.scene.add_sprite("Clouds", cloud)

    def on_draw(self):
        """Render the screen"""

        # Clear the screen to the background color
        self.clear()

        #activating the camera so that we can use it. Always activate normal camera first then GUI camera
        self.camera.use()

        # code to draw the screen goes here
        # self.wall_list.draw()
        self.scene.draw() # drawing the scene instead of wall_list
        #draw the sprites
        self.player_sprite.draw()

        # activating the GUI camera before drawing GUI elements
        self.gui_camera.use()

        #drawing score on screen, moreover, scrolling it with viewpoint
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10, 10, arcade.csscolor.WHITE, 16)

        remaining_coins_text = f"Points Left: {self.points_left}"
        arcade.draw_text(remaining_coins_text, 120, 10, arcade.csscolor.WHITE, 16)

        # ********setting a on-screen timer********* 
        mins, secs = divmod(int(self.timer), 60)
        countdown = f"Time: {mins:02d}:{secs:02d}"
        arcade.draw_text(countdown, 280, 10, arcade.csscolor.WHITE, 16)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed"""
        #change_x, change_y-->holds the velocity that the sprite is moving with
        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED #due to gravity player will automatically come down
                arcade.play_sound(self.jump_sound)
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
    
    def on_key_release(self, key, modifiers):
        """Called whenever a key is released"""

        #not required for UP and DOWN since due to gravity change_y will be set to 0
        if key == arcade.key.LEFT:
            self.player_sprite.change_x =  0 
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def center_camera_to_palyer(self):
        """Function to keep the camera centered on the player"""

        #calculate the coordinates for the center of player relative to the screen, then move the camera to those
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width/2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height/2)

        # dont let the camera travel pass 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_update(self, delta_time): #is called about 60 times per second
        """Movement and game ligic goes here"""

        # moving the player with physics engine
        self.physics_engine.update()

        #positioning the camera --> function call
        self.center_camera_to_palyer()

        #collision detection
        #see if the player hit any coins
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene["Coins"])

        #loop through each coin we hit and accordingly remove it
        for coin in coin_hit_list:
            #remove the coin
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)#play the sound as we hit coin
            #add one to the score
            self.score += 1
            self.points_left -= 1

        # see if the player hit any gems
        gem_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene["Gems"])
        
        for gem in gem_hit_list:
            gem.remove_from_sprite_lists()
            arcade.play_sound(self.collect_gem_sound)
            self.score += 3
            self.points_left -= 3

        #updating timer
        self.timer += delta_time

def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
