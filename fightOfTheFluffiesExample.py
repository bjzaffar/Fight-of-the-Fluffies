import pygame
pygame.init()

#Setting name of the game
pygame.display.set_caption("Fight of the Fluffies")

#Setting window size
win = pygame.display.set_mode((2560, 1440))

#Loading Beebo animation walking frames
walk_right = [pygame.image.load("R1.png"), pygame.image.load("R2.png"), pygame.image.load("R3.png"), pygame.image.load("R4.png"), pygame.image.load("R5.png"), pygame.image.load("R6.png"), pygame.image.load("R7.png"), pygame.image.load("R8.png"), pygame.image.load("R9.png")]
walk_left = [pygame.image.load("L1.png"), pygame.image.load("L2.png"), pygame.image.load("L3.png"), pygame.image.load("L4.png"), pygame.image.load("L5.png"), pygame.image.load("L6.png"), pygame.image.load("L7.png"), pygame.image.load("L8.png"), pygame.image.load("L9.png")]

#Loading Gleek animation walking frames
g_walk_right = [pygame.image.load("GR1.png"), pygame.image.load("GR2.png"), pygame.image.load("GR3.png"), pygame.image.load("GR4.png"), pygame.image.load("GR5.png"), pygame.image.load("GR6.png"), pygame.image.load("GR7.png"), pygame.image.load("GR8.png"), pygame.image.load("GR9.png")]
g_walk_left = [pygame.image.load("GL1.png"), pygame.image.load("GL2.png"), pygame.image.load("GL3.png"), pygame.image.load("GL4.png"), pygame.image.load("GL5.png"), pygame.image.load("GL6.png"), pygame.image.load("GL7.png"), pygame.image.load("GL8.png"), pygame.image.load("GL9.png")]

#Loading projectile images
laser_img = pygame.image.load("Laser.png")
banana_img = pygame.image.load("Banana.png")
banana_peel_img = pygame.image.load("BananaPeel.png")

#Loading City Background
bg = pygame.image.load("City background.jpg")

#Making clock for frame rate
clock = pygame.time.Clock()

#Loading sound effects
bullet_sound = pygame.mixer.Sound("bullet.wav")
hit_sound = pygame.mixer.Sound("hit.wav")

#Loading music
music = pygame.mixer.music.load("Ode-to-Joy.wav")
#Playing the music
pygame.mixer.music.play(-1)

#Game restart variable
game_over = False


class Beebo(object):
    def __init__(self, x, y, width, height):
        #Making the variables
        self.x = int(x)
        self.y = int(y)
        self.width = width
        self.height = height
        self.vel = 5
        self.is_jump = False
        self.jump_count = 10
        self.left = False
        self.right = True
        self.walk_count = 0
        self.standing =True
        self.hitbox = (self.x + 80, self.y + 80, 90, 120)
        self.health = 19
        self.visible = True
        

    def draw(self, win):
        #Making the health bar, which is a green rect over a red rect, but each time the sprite gets hit, the width of the green rect is shortened
        pygame.draw.rect(win, (255, 0, 0), (70, 50, 1000, 50))
        #Restarting the animation when all the 9 images have appeared for 3 frames each
        if self.walk_count + 1 >= 27:
            self.walk_count = 0

        if self.visible:    
            if not (self.standing):
                if self.left:
                    #Scaling the images up, making them bigger
                    new_image = pygame.transform.scale(walk_left[self.walk_count // 3], (256, 256))
                    #Displaying the new, scaled image on to the screen
                    win.blit(new_image, (int(self.x), int(self.y)))
                    #Adding 1 to the walk_count each frame, so every 3 frames the next image in the animation shows up
                    self.walk_count += 1
                elif self.right:
                    #Scaling the images up, making them bigger
                    new_image = pygame.transform.scale(walk_right[self.walk_count // 3], (256, 256))
                    #Displaying the new, scaled image on to the screen
                    win.blit(new_image, (int(self.x), int(self.y)))
                    #Adding 1 to the walk_count each frame, so every 3 frames the next image in the animation shows up
                    self.walk_count += 1
            else:
                if self.right:
                    #Scaling the images up, making them bigger
                    new_image = pygame.transform.scale(walk_right[0], (256, 256))
                    #Displaying the new, scaled image on to the screen
                    win.blit(new_image, (round(self.x), round(self.y)))
                else:
                    #Scaling the images up, making them bigger
                    new_image = pygame.transform.scale(walk_left[0], (256, 256))
                    #Displaying the new, scaled image on to the screen
                    win.blit(new_image, (round(self.x), round(self.y)))
            #Making the hitbox, because the actual sprite is smaller than the image itself
            self.hitbox = (self.x + 80, self.y + 80, 90, 120)
            pygame.draw.rect(win, (0, 255, 0), (70, 50, 1000 - (50 * (19 - self.health)), 50))
        #pygame.draw.rect(win, (255,0,0), self.hitbox,2)
            
        
        

    #If the sprite gets hit
    def hit(self):
        self.walk_count = 0

        if self.health > 0:
            #If the health is more than 0, then take away 1
            self.health -= 1
        else:
            #If the health isn't more than 0, then the sprite isn't visible anymore
            self.visible = False
        

class Gleek(object):
    def __init__(self, x, y, width, height):
        #Making the variables
        self.x = int(x)
        self.y = int(y)
        self.width = width
        self.height = height
        self.vel = 5
        self.is_jump = False
        self.jump_count = 10
        self.left = True
        self.right = False
        self.walk_count = 0
        self.standing =True
        self.hitbox = (self.x + 95, self.y + 80, 75, 125)
        self.health = 19
        self.visible = True

    def draw(self, win):
        #Making the health bar, which is a green rect over a red rect, but each time the sprite gets hit, the width of the green rect is shortened
        pygame.draw.rect(win, (255, 0, 0), (1490, 50, 1000, 50))
        #Restarting the animation when all the 9 images have appeared for 3 frames each
        if self.walk_count + 1 >= 27:
            self.walk_count = 0
        if self.visible:    
            if not (self.standing):
                if self.left:
                    #Scaling the images up, making them bigger
                    new_image = pygame.transform.scale(g_walk_left[self.walk_count // 3], (256, 256))
                    #Displaying the new, scaled image on to the screen
                    win.blit(new_image, (int(self.x), int(self.y)))
                    #Adding 1 to the walk_count each frame, so every 3 frames the next image in the animation shows up
                    self.walk_count += 1
                elif self.right:
                    #Scaling the images up, making them bigger
                    new_image = pygame.transform.scale(g_walk_right[self.walk_count // 3], (256, 256))
                    #Displaying the new, scaled image on to the screen
                    win.blit(new_image, (int(self.x), int(self.y)))
                    #Adding 1 to the walk_count each frame, so every 3 frames the next image in the animation shows up
                    self.walk_count += 1
            else:
                if self.right:
                    #Scaling the images up, making them bigger
                    new_image = pygame.transform.scale(g_walk_right[0], (256, 256))
                    #Displaying the new, scaled image on to the screen
                    win.blit(new_image, (round(self.x), round(self.y)))
                else:
                    #Scaling the images up, making them bigger
                    new_image = pygame.transform.scale(g_walk_left[0], (256, 256))
                    #Displaying the new, scaled image on to the screen
                    win.blit(new_image, (round(self.x), round(self.y)))
            #Making the hitbox, because the actual sprite is smaller than the image itself
            self.hitbox = (self.x + 95, self.y + 80, 75, 125)
            pygame.draw.rect(win, (0, 255, 0), (1490, 50, 1000 - (50 * (19 - self.health)), 50))
            #pygame.draw.rect(win, (255,0,0), self.hitbox,2)
            
        
        

    #If the sprite gets hit
    def hit(self):
        self.walk_count = 0
        
        if self.health > 0:
            #If the health is more than 0, then take away 1
            self.health -= 1
        else:
            #If the health isn't more than 0, then the sprite isn't visible anymore
            self.visible = False
        

class Laser(object):
    def __init__(self, x, y, facing):
        #Making the variables
        self.x = x
        self.y = y
        self.facing = facing
        self.vel = 80 * facing
    
    def draw(self, win):
        #Scaling the image up, making it bigger
        new_laser_img = pygame.transform.scale(laser_img, (60, 15))
        #Displaying the new, scaled image on to the screen
        win.blit(new_laser_img, (self.x, self.y))

        
class Banana(object):
    def __init__(self, x, y, facing):
        #Making the variables
        self.x = x
        self.y = y
        self.facing = facing
        self.vel = 80 * facing
    
    def draw(self, win):
        #Scaling the image up, making it bigger
        new_banana_img = pygame.transform.scale(banana_img, (30, 45))
        #Displaying the new, scaled image on to the screen
        win.blit(new_banana_img, (self.x, self.y))


class BananaPeel(object):
    def __init__(self, x, y, facing):
        #Making the variables
        self.x = x
        self.y = y
        self.facing = facing
        self.vel = 60 * facing
        self.is_arch = False
        self.arch_count = 10

    def draw(self, win):
        #Scaling the image up, making it bigger
        new_banana_peel_img = pygame.transform.scale(banana_peel_img, (30, 45))
        #Displaying the new, scaled image on to the screen
        win.blit(new_banana_peel_img, (self.x, self.y))
        

def redrawGameWindow():
    #Displaying the background image on to the screen
    win.blit(bg, (0, 0))
    #Drawing player 1 and player 2 on to the screen
    player1.draw(win)
    player2.draw(win)

    #Setting the fonts and the font sizes for the texts that I want to blit on to the screen
    font = pygame.font.SysFont("comicsans", 200)
    font_p1 = pygame.font.SysFont("comicsans", 100)
    font_p2 = pygame.font.SysFont("comicsans", 100)
    font_vs = pygame.font.SysFont("comicsans", 100)

    #Rendering the fonts, also making the words and colour of the text
    victory_text = font.render("", 1, (0, 255, 0))
    p1_text = font_p1.render("Beebo", 1, (255, 165, 0))
    p2_text = font_p2.render("Gleek", 1, (255, 165, 0))
    vs_text = font_vs.render("VS", 1, (255, 165, 0))  

    if player1.visible and player2.visible:
        #Displaying the texts on to the screen
        win.blit(p1_text, (150, 200))
        win.blit(p2_text, (2160, 200))
        win.blit(vs_text, (1225, 50))

    #Displaying the victory text depending on which player won
    if player1.visible and not player2.visible and game_over:
        victory_text = font.render("Beebo wins! Press R to restart!", 1, (0, 255, 0))
        win.blit(victory_text, (300, 500))
        
    if player2.visible and not player1.visible and game_over:
        victory_text = font.render("Gleek wins! Press R to restart!", 1, (0, 255, 0))
        win.blit(victory_text, (300, 500))

    
    for laser in lasers:
        #Drawing the laser on to the screen
        laser.draw(win)

    for banana in bananas:
        #Drawing the laser on to the screen
        banana.draw(win)
    
    pygame.display.update()

#Assigning player 1 and player 2 to classes
player1 = Beebo(50,1050, 256, 256)
player2 = Gleek(2275, 1050, 256, 256)
#Projectile variables
lasers = []
laser_loop = 0
bananas = []
banana_loop = 0
banana_peels = []
banana_peel_loop = 0
#Making the program run by saying 'while run:' and saying 'run = True'
run = True

if game_over == False:
    #Main loop
    while run:
        #Setting the frame rate as 27 frames per second
        clock.tick(27)


        #Adding one to the laser_loop, so that there is a delay between each laser
        if laser_loop > 0:
            laser_loop += 1
        #Resetting the laser_loop back to 0 if it is 3, so it will allow the player to shoot another laser after the delay
        if laser_loop > 3:
            laser_loop = 0

        #Adding one to the banana_loop, so that there is a delay between each banana
        if banana_loop > 0:
            banana_loop += 1
        #Resetting the banana_loop back to 0 if it is 2, so it will allow the player to shoot another banana after the delay
        if banana_loop > 2:
            banana_loop = 0

        #So that if the person closes the game, it will close without an error
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


        for laser in lasers:
            #Checking if the laser is colliding with player 2's hitbox
            if laser.y < player2.hitbox[1] + player2.hitbox[3] and laser.y + 5 > player2.hitbox[1]:
                if laser.x + 60 > player2.hitbox[0] and laser.x < player2.hitbox[0] + player2.hitbox[2]:
                    #If both players are alive
                    if player1.visible and player2.visible:
                        #Play the sound effect, call the player 2 'hit' function and make the lasers disappear from the screen
                        hit_sound.play()
                        player2.hit()
                        lasers.pop(lasers.index(laser))
                    else:
                        #Else, just make the lasers disappear from the screen
                        lasers.pop(lasers.index(laser))
                            

            #If the laser is not at the edge of the screen
            if laser.x < 2560 and laser.x > 0:
                #Make the laser move by adding the velocity to the laser's x (keep in mind that it does this each frame)
                laser.x += laser.vel
            else:
                #Else, if the laser is at the edge of the screen and player 1 is visible
                if player1.visible:
                    #Make the lasers disappear from the screen
                    lasers.pop(lasers.index(laser))


        for banana in bananas:
            #Checking if the banana is colliding with player 1's hitbox
            if banana.y < player1.hitbox[1] + player1.hitbox[3] and banana.y + 5 > player1.hitbox[1]:
                if banana.x + 30 > player1.hitbox[0] and banana.x < player1.hitbox[0] + player1.hitbox[2]:
                    #If both players are alive
                    if player2.visible and player1.visible:
                        #Play the sound effect, call the player 1 'hit' function and make the bananas disappear from the screen
                        hit_sound.play()
                        player1.hit()
                        bananas.pop(bananas.index(banana))
                    else:
                        #Else, just make the bananas disappear from the screen
                        bananas.pop(bananas.index(banana))

            #If the banana is not at the edge of the screen
            if banana.x < 2560 and banana.x > 0:
                #Make the banana move by adding the velocity to the banana's x (keep in mind that it does this each frame)
                banana.x += banana.vel
            else:
                #Else, if the banana is at the edge of the screen and player 2 is visible
                if player2.visible:
                    #Make the bananas disappear from the screen
                    bananas.pop(bananas.index(banana))

        if player1.visible and not player2.visible:
            game_over = True

        elif player2.visible and not player1.visible:
            game_over = True




                

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and laser_loop == 0:
            if player1.visible and player2.visible:
                if player1.left:
                    facing = -1
                else:
                    facing = 1
                    
                if len(lasers) < 1:
                    lasers.append(Laser(round(player1.x + player1.width //2), round(player1.y + player1.height //2), facing))
                    bullet_sound.play()
                    
                laser_loop = 1

        if keys[pygame.K_r] and game_over:
            game_over = False
            player1 = Beebo(50,1050, 256, 256)
            player2 = Gleek(2275, 1050, 256, 256)
            lasers = []
            laser_loop = 0
            bananas = []
            banana_loop = 0
            banana_peels = []
            banana_peel_loop = 0
                
        if keys[pygame.K_RSHIFT] and banana_loop == 0:
            if player2.visible and player1.visible:
                if player2.left:
                    facing = -1
                else:
                    facing = 1
                    
                if len(bananas) < 1:
                    bananas.append(Banana(round(player2.x + player2.width //2), round(player2.y + player2.height //2), facing))
                    bullet_sound.play()
            
                banana_loop = 1
            

        if keys[pygame.K_a] and player1.x > 5:
            player1.x -= player1.vel
            player1.left = True
            player1.right = False
            player1.standing = False
        elif keys[pygame.K_d] and (player1.x + player1.width) < (2560 - 5):
            player1.x += player1.vel
            player1.right = True
            player1.left = False
            player1.standing = False
        else:
            player1.standing = True
            player1.walk_count = 0
        if not player1.is_jump:
            if keys[pygame.K_w]:
                player1.is_jump = True
                player1.walk_count = 0
        else:
            if player1.jump_count >= -10:
                neg = 1
                if player1.jump_count < 0:
                    neg = -1
                player1.y -=((player1.jump_count ** 2) * 0.5 * neg)
                player1.jump_count -=1
            else:
                player1.is_jump = False
                player1.jump_count = 10

        if keys[pygame.K_LEFT] and player2.x > 5:
            player2.x -= player2.vel
            player2.left = True
            player2.right = False
            player2.standing = False
        elif keys[pygame.K_RIGHT] and (player2.x + player2.width) < (2560 - 5):
            player2.x += player2.vel
            player2.right = True
            player2.left = False
            player2.standing = False
        else:
            player2.standing = True
            player2.walk_count = 0
            
        if not player2.is_jump:
            if keys[pygame.K_UP]:
                player2.is_jump = True
                player2.walk_count = 0
        else:
            if player2.jump_count >= -10:
                neg = 1
                if player2.jump_count < 0:
                    neg = -1
                player2.y -=((player2.jump_count ** 2) * 0.5 * neg)
                player2.jump_count -=1
            else:
                player2.is_jump = False
                player2.jump_count = 10
                
        redrawGameWindow()

pygame.quit()

