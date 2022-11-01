import gamebox
import pygame
import random

# important variables
status = False
gameover = False
speed = 5
clock = 0
player_width = 30
player_height = 30
current_health = 120
eaten_bitcoin = 0

# ------ SMALL ENOUGH WINDOW ------
# 800 by 600
camera = gamebox.Camera(800, 600)

# display variables
player = gamebox.from_color(400, 300, "tomato", player_width, player_height)
begin_message = gamebox.from_text(400, 370, "Press SPACE to begin", 40, "sienna", bold=False)
name_message = gamebox.from_text(400, 190, "Made by Ivory Tang (bjm7vv) and Chai Zhang (zdc4tp)", 25, "brown",
                                 bold=False)
begin_message4 = gamebox.from_text(400, 330, "Use the UP, DOWN, LEFT and RIGHT keys to navigate.", 25, "white")
begin_message3 = gamebox.from_text(400, 300,
                                   "Hitting the walls will get you eliminated. "
                                   "For every berry you eat, an obstacle will disappear.", 25, "White", bold=False)
begin_message2 = gamebox.from_text(400, 270, "For each coin you eat an obstacle will be generated, "
                                             "avoid them to maintain optimal health.", 25, "White", bold=False)
begin_message1 = gamebox.from_text(400, 240, "Eat as many Bitcoins as you can and stay alive!", 25, "White")
game_name = gamebox.from_text(400, 150, "Bits and Berries!", 70, "dark red")
game_over = gamebox.from_text(400, 300, "Game Over: Press Space to Play Again", 40, "Red", bold=True)
blockage = gamebox.from_color(random.randint(10, 790), random.randint(10, 590), "firebrick", 25, 25)
health_bar = gamebox.from_color((current_health * 1) + 20, 50, "red", current_health * 2, 30)
bit_counter = gamebox.from_text(600, 50, "Bitcoins Eaten: " + "0", 24, "dark orange", bold=True)
blockages = []

# ------ GRAPHICS/IMAGES
# Images will be used for bitcoins and berries
bitcoin = gamebox.from_image(random.randint(10, 790), random.randint(60, 590), 'bitcoin.png')
berry = gamebox.from_image(random.randint(10, 790), random.randint(60, 590), 'berry.png')

# ------ START SCREEN (REFERENCE DISPLAY VARIABLES ABOVE) ------
# Names and computing ID's above
# Game name: Bits and Berries!
# Game instructions in begin messages in display variables above
# Press space to start
camera.clear('light salmon')
camera.draw(begin_message)
camera.draw(begin_message1)
camera.draw(begin_message2)
camera.draw(begin_message3)
camera.draw(begin_message4)
camera.draw(name_message)
camera.draw(game_name)
camera.display()


def tick(keys):
    """
    This is the code for the game "Bits and Berries!". Each component is labelled
    with comments.
    :param keys: User's input as keys.
    :return: Game window with "Bits and Berries!"
    """
    global status, clock, gameover, player, blockages, current_health, health_bar, eaten_bitcoin, bit_counter

    # start game by pressing space
    if pygame.K_SPACE in keys:
        clock = 0
        status = True

    # game started
    if status:
        camera.clear("bisque")
        camera.draw(health_bar)
        camera.draw(bitcoin)
        camera.draw(bit_counter)

        # makes sure nothing touches the health_bar
        if bitcoin.touches(health_bar):
            bitcoin.move_to_stop_overlapping(health_bar)
        if berry.touches(health_bar):
            berry.move_to_stop_overlapping(health_bar)

        # make sure berries do not overlap bitcoins or blockages
        if berry.touches(bitcoin):
            berry.move_to_stop_overlapping(bitcoin)
        for block in blockages:
            if berry.touches(block):
                berry.move_to_stop_overlapping(block)

# ------ COLLECTIBLE: BITCOIN WILL PRODUCE MORE OBSTACLES, GOAL IS TO EAT BITCOIN ------
# Objective is to eat bitcoin
        if player.touches(bitcoin):
            # make new block
            new_block = gamebox.from_color(random.randint(13, 787), random.randint(60, 590), "firebrick", 25, 25)
            # make sure block doesn't overlap health bar, player, or other blocks
            new_block.move_to_stop_overlapping(health_bar)
            new_block.move_to_stop_overlapping(player)
            for block in blockages:
                if new_block.touches(block):
                    new_block.move_to_stop_overlapping(block)
            # add it to blockages list
            blockages.append(new_block)

            # "regenerate" bitcoin
            bitcoin.x = random.randint(10, 790)
            bitcoin.y = random.randint(60, 590)
            # make sure bitcoin don't overlap blocks
            for blocks in blockages:
                bitcoin.move_both_to_stop_overlapping(blocks)
            # display number of bitcoin player has eaten
            eaten_bitcoin += 1
            bit_counter = gamebox.from_text(600, 50, "Bitcoins Eaten: " + str(eaten_bitcoin), 24, "dark orange",
                                            bold=True)
            camera.draw(bit_counter)

        # draw obstacles and update health if player touches obstacles
        for new_blocks in blockages:
            camera.draw(new_blocks)
            if new_blocks.touches(player):
                player.move_to_stop_overlapping(new_blocks)
                current_health -= 1
                if current_health <= 0:
                    gameover = True

# ------ HEALTH BAR (UPDATE HEALTH ABOVE AND DISPLAY) ------
# Hitting and touching obstacles will deplete health bar
        health_bar = gamebox.from_color((current_health * 1) + 20, 50, "red", current_health * 2, 30)
        camera.draw(health_bar)

# ------ COLLECTIBLE: BERRIES WILL REMOVE OBSTACLES ------
# Eating berries will take away obstacles
        if player.touches(berry):
            berry.x = random.randint(10, 790)
            berry.y = random.randint(60, 590)
            if len(blockages) > 1:
                blockages.remove(blockages[len(blockages) - 1])
        # move berries every 5 seconds
        if clock % 150 == 0:
            berry.x = random.randint(10, 790)
            berry.y = random.randint(60, 590)
        camera.draw(berry)

# ------ USER CONTROLS ------
# Left/right and up/down keys will control where player goes
        if pygame.K_RIGHT in keys:
            player.speedx = speed
            player.speedy = 0
        if pygame.K_LEFT in keys:
            player.speedx = -1 * speed
            player.speedy = 0
        if pygame.K_UP in keys:
            player.speedy = -1 * speed
            player.speedx = 0
        if pygame.K_DOWN in keys:
            player.speedy = speed
            player.speedx = 0

# ------ GAME OVER ------
# Happens when player hits any of the sides of window, it will be an instant game over
        if player.y >= 585:
            player.y = 585
            gameover = True
        if player.y <= 15:
            player.y = 15
            gameover = True
        if player.x > 785:
            player.x = 785
            gameover = True
        if player.x < 15:
            player.x = 15
            gameover = True

# ------ TIMER (SCORE BOARD) ------
# Another objective is to survive for as long as possible (don't hit walls and avoid health bar running out)
        clock += 1
        score_board = gamebox.from_text(750, 50, "Score: " + str(clock // 30), 24, "dark orange", bold=True)
        camera.draw(score_board)

# ------ RESTART FROM GAME OVER (AND SHOW GAME OVER SCREEN) ------
# Press space to restart game
# This section also shows the game over screen
        if gameover:
            camera.draw(game_over)
            status = False
        # restart by pressing space
        if pygame.K_SPACE in keys:
            camera.clear("bisque")
            player.x = 400
            player.y = 300
            clock = 0
            blockages = []
            current_health = 120
            eaten_bitcoin = 0
            health_bar = gamebox.from_color((current_health * 1) + 20, 50, "red", current_health * 2, 30)
            bit_counter = gamebox.from_text(600, 50, "Bitcoins Eaten: " + str(eaten_bitcoin), 24, "dark orange",
                                            bold=True)
            camera.draw(player)
            camera.draw(health_bar)
            camera.draw(score_board)
            camera.draw(bit_counter)
            status = True
            gameover = False

        player.move_speed()
        camera.draw(player)
        camera.display()


gamebox.timer_loop(30, tick)