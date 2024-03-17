import pygame

class Player():
    #Initializes Player
    #player determines whether the user is player1 or player2
    #x and y is the location where the player is placed on the screen
    #data is a list that holds the player's variables like SIZE, SCALE, OFFSET, FLIP_OFFSET
    #sprite_sheet is the actual sprite sheet image that holds all the animations
    #animation_steps is the steps for each animation action
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
        self.player = player
        self.size = data[0] #size of the actual frame
        self.image_scale = data[1] #Scale the size of the player
        self.offset = data[2] #Set the player back into place
        self.flip_offset = data[3]
        self.animation_list = self.load_images(sprite_sheet, animation_steps) #A list with all the sets of animations
        self.action = 0 #0:idle, 1:run, 2:jump, 3:fall, 4:attack1 5:attack2 6:hit 7:death
        self.frame_index = 0 #The current frame of the animation set
        self.image = self.animation_list[self.action][self.frame_index] #ex. if animation_list[0][0] then it will use the idle set and the 1st frame of it
        self.update_time = pygame.time.get_ticks() #gets time when fighter was first created
        self.flip = flip #bool Flip the player or not
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0 #y velocity
        self.jump = False
        self.running = False
        self.attacking = False
        self.hit = False
        self.attack_type = 0 #Different ways to attack, 0:idle 1:attack1 2:attack2
        self.attack_cooldown = 0 #The time inbetween the nect attack
        self.attack_sound = sound
        self.health = 100 #Default health
        self.alive = True

    #Loads sets of animations in a list
    def load_images(self, sprite_sheet, animation_steps):
        #extracts the frames from the spritesheet
        animation_list = []
        step_counter = 0 #A counter for each frame, keeps going until the very last animation set frame
        for animation in animation_steps:
            temp_img_list = []

            for _ in range(animation):
                #Putting the animation frame in a temporary list set
                temp_img = sprite_sheet.subsurface(step_counter * self.size[0], 0, self.size[0], self.size[1]) #subsurface is used to take just a little square(frame) of the whole sprite sheet
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size[0] * self.image_scale, self.size[1] * self.image_scale))) #Scales the width and height of the image
                #print(str(step_counter * self.size[0]) + " ")
                step_counter += 1
            animation_list.append(temp_img_list)
        #print(animation_list)

        return animation_list


    #Moves the player left to right, jump
    #screen_width is width of the screen
    #screen_height is the height of the screen
    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 10 #Controls how fast they move
        GRAVITY = 2
        #change in x and y
        dx = 0
        dy = 0

        self.running = False #Initially starts at False, if no button pressed then false
        self.attack_type = 0 #No attack all the time unless action button is pressed

        #Gets the key presses
        key = pygame.key.get_pressed()

        #All actions can be performed if not attacking
        if self.attacking == False and self.alive == True and round_over == False:
            #Check if player 1
            if self.player == 1:
                #Movement
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True
                #jumping
                if key[pygame.K_w] and self.jump == False:
                    self.vel_y = -30 #negative in the y direction goes up, height of jump
                    self.jump = True
                #Attacks
                if key[pygame.K_r] or key[pygame.K_t]:
                    self.attack(surface, target)
                    if key[pygame.K_r]:
                        self.attack_type = 1
                    if key[pygame.K_t]:
                        self.attack_type = 2

            #Check if player 2
            if self.player == 2:
                #Movement
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True
                #jumping
                if key[pygame.K_UP] and self.jump == False:
                    self.vel_y = -30 #negative in the y direction goes up, height of jump
                    self.jump = True
                #Attacks
                if key[pygame.K_KP1] or key[pygame.K_KP2]:
                    self.attack(surface, target)
                    if key[pygame.K_KP1]:
                        self.attack_type = 1
                    if key[pygame.K_KP2]:
                        self.attack_type = 2

        # Implement Gravity
        self.vel_y += GRAVITY  # It will be brought down by gravity
        dy += self.vel_y

        #Player Doesn't goes off the screen, preventative measures if it does
        if self.rect.left + dx < 0:
            dx = -self.rect.left #just going to go as far as the edge and stop there
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110: #-110 because we don't want the player to go to very bottom
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom #Difference between the floor and the bottom of the rectangle

        #Makes sure that players face each other
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        #Attack Cooldown is activated
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1


        #Update Player Position
        self.rect.x += dx
        self.rect.y += dy

    #Allows the player to hit another target and decrease their health
    def attack(self, surface, target):
        if self.attack_cooldown == 0:
            #Attacks
            self.attacking = True
            attack_rect = pygame.Rect(self.rect.centerx - (3 * self.rect.width * self.flip), self.rect.y, 3 * self.rect.width, self.rect.height)
            self.attack_sound.play()
            if attack_rect.colliderect(target.rect):
                target.health -= 10
                target.hit = True
            #pygame.draw.rect(surface, (0, 255, 0), attack_rect) #Draws hit hitbox

    #animation update for the image
    def update(self):
        #Check which actions are happening
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.action = 7 #Death
        elif self.hit == True:
            self.update_action(6) #Hit
        elif self.attacking == True:
            if self.attack_type == 1: #Attack1
                self.update_action(4)
            elif self.attack_type == 2:
                self.update_action(5) #Attack2
        elif self.jump == True:
            self.update_action(2) #Jump
        elif self.running == True:
            #self.action = 1
            self.update_action(1) #Run
        else:
            #self.action = 0
            self.update_action(0) #Idle


        animation_cooldown = 50 #how long the animation cooldown for eachframe, in ms
        self.image = self.animation_list[self.action][self.frame_index]
        current_time = pygame.time.get_ticks()
        #updates the frame
        if current_time - self.update_time > animation_cooldown:  # if animation_cooldown time have passed between the last update and the current time then update the frame
            self.frame_index += 1
            self.update_time = current_time  # resets the cooldown
            #Checks to see if we reached the end of the animation sequence
            if self.frame_index >= len(self.animation_list[self.action]):
                #if the player dies then end all animation
                if self.alive == False:
                    self.frame_index = len(self.animation_list[self.action]) - 1 #stays at the last frame of death
                else:
                    self.frame_index = 0  # resets frame back to 0
                    #check if attack was executed, we want the attack animation to finish then go back to idle.
                    #I do it this way instead of making it false in the move function because the user needs to finish the animation before doing the next player action, unlike running where it doesn't need to finish the animation everytime
                    if self.action == 4 or self.action == 5:
                        self.attacking = False
                        self.attack_cooldown = 10 #The time between the next attack
                    #If player was hit, then run through the hit animation and set it to false
                    if self.action == 6:
                        self.hit = False
                        #If the player is attacked then they momentarily lose the ability to attack
                        self.attacking = False
                        self.attack_cooldown = 10

    #Updates the player action with a new action
    #If it is a new action then change the action, and reset the frame_index because orginally the frame_index would keep going to where it left off.
    #So setting the frame_index 0 allows the animation to reset back to the first frame
    def update_action(self, new_action):
        #checks to see whether the new action is different from the previous one
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    #Draws the player on the surface
    def draw(self, surface):
        #might need an if statement when we flip because the img offsets again
        img = pygame.transform.flip(self.image, self.flip, False) #The image, we can flip or not flip the image, might need a FLIP_OFFSET data in main
        #pygame.draw.rect(surface, (255, 0, 0), self.rect) #Draws hitbox

        #draws the image on the screen where the rectangle is
        #Have a flip offset depending on how the image looks when flipped
        if self.flip == False:
            surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale))) #Places the image on the surface, offset is to make sure the image is on the right place
        else:
            surface.blit(img, (self.rect.x - (self.flip_offset[0] * self.image_scale), self.rect.y - (self.flip_offset[1] * self.image_scale)))