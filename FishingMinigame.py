import pygame
import random

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((400, 900))
pygame.display.set_caption('Fishing Game')
clock = pygame.time.Clock()

class Upgrade:
    def __init__(self, name, cost, description):
        self.name = name
        self.cost = cost
        self.description = description

doExit = False
scrollY = 0
scrollYVel = 0
hookYPos = 500
hookYVel = 0
hookImage = pygame.image.load("Assets/Hook.png").convert_alpha()
boat1Image = pygame.image.load("Assets/Boat1.png").convert_alpha()
hookToggle = False
hookComplete = False
currentMoney = 0
minFishAmount = 50
maxFishAmount = 200
hookSize = 40

my_font = pygame.font.SysFont('Comic Sans MS', 20)

listOfFish = []

class Fish:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.speed = random.randrange(-4,5)
        self.color = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
        self.caught = False
        self.moving = False
        self.size = random.randrange(10,45)
        self.yposcatch = random.randrange(-40,40)
        self.xposcatch = random.randrange(150,250)

    def move(self, scrollY):
        global currentMoney
        if self.caught:
            self.ypos = scrollYVel + 500 + self.yposcatch
            if scrollY == 0:
                currentMoney += self.size/5
                return False
            return True  # Do nothing if the fish is caught
        
        self.xpos += self.speed
        if self.speed == 0:
            self.speed = 1
        if self.xpos < 0 or self.xpos > 800:
            return False
        
        # Check if the fish intersects with the hook
        hook_rect = pygame.Rect(175, scrollYVel + 500, hookSize, hookSize)
        fish_rect = pygame.Rect(self.xpos, self.ypos + scrollY, self.size, self.size - 8)
        
        if hook_rect.colliderect(fish_rect):
            print("Caught")
            self.xpos = self.xposcatch
            self.caught = True
            
        return True

    def draw(self, scrollY):
        if self.caught:
            pygame.draw.rect(screen, self.color, (self.xpos, self.ypos, self.size, self.size - 8))
        else:
            pygame.draw.rect(screen, self.color, (self.xpos, self.ypos + scrollY, self.size, self.size - 8))

# List of purchased upgrades
purchased_upgrades = []
# Function to handle mouse events
class BoatUpgrade(Upgrade):
    def __init__(self, name, cost, description, level):
        super().__init__(name, cost, description)
        self.level = level

    def apply_upgrade(self):
        global maxFishAmount
        maxFishAmount += 200 + (self.level - 1) * 50

class HookUpgrade(Upgrade):
    def __init__(self, name, cost, description, level):
        super().__init__(name, cost, description)
        self.level = level

    def apply_upgrade(self):
        global hookSize
        hookSize += 10 + (self.level - 1) * 10

# Initialize upgrade levels
boat_upgrade_levels = [
    BoatUpgrade("Boat Upgrade", 100, "Increases fish amount", 1),
    BoatUpgrade("Boat Upgrade", 200, "Increases fish amount", 2),
    BoatUpgrade("Boat Upgrade", 300, "Increases fish amount", 3),
    BoatUpgrade("Boat Upgrade", 400, "Increases fish amount", 4),
    BoatUpgrade("Boat Upgrade", 500, "Increases fish amount", 5)
]

hook_upgrade_levels = [
    HookUpgrade("Hook Upgrade", 150, "Increases hook size", 1),
    HookUpgrade("Hook Upgrade", 250, "Increases hook size", 2),
    HookUpgrade("Hook Upgrade", 350, "Increases hook size", 3),
    HookUpgrade("Hook Upgrade", 450, "Increases hook size", 4),
    HookUpgrade("Hook Upgrade", 550, "Increases hook size", 5)
]

# Function to apply purchased upgrades
def apply_upgrades():
    global maxFishAmount, hookSize
    maxFishAmount = 200  # Reset maxFishAmount
    hookSize = 40  # Reset hookSize
    for upgrade in purchased_upgrades:
        if isinstance(upgrade, BoatUpgrade):
            upgrade.apply_upgrade()
        elif isinstance(upgrade, HookUpgrade):
            upgrade.apply_upgrade()

# Function to check if an upgrade can be purchased
def can_purchase_upgrade(upgrade):
    return currentMoney >= upgrade.cost and upgrade not in purchased_upgrades

# Function to handle mouse events
def handle_mouse_event(event):
    global currentMoney
    global hookToggle
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        if 50 <= mouse_pos[0] <= 150 and 10 <= mouse_pos[1] <= 60:  # Check if mouse is within boat upgrade button area
            if not hookComplete:
                for upgrade in boat_upgrade_levels:
                    if can_purchase_upgrade(upgrade):
                        currentMoney -= upgrade.cost
                        purchased_upgrades.append(upgrade)
                        apply_upgrades()
                        break
        elif 250 <= mouse_pos[0] <= 350 and 10 <= mouse_pos[1] <= 60:  # Check if mouse is within hook upgrade button area
            if not hookComplete:
                for upgrade in hook_upgrade_levels:
                    if can_purchase_upgrade(upgrade):
                        currentMoney -= upgrade.cost
                        purchased_upgrades.append(upgrade)
                        apply_upgrades()
                        break
        else:
            if not hookToggle and not hookComplete:
                randomFishAmount = random.randrange(minFishAmount, maxFishAmount)
                for i in range(randomFishAmount):
                    listOfFish.append(Fish(random.randrange(100,200),random.randrange(800,8000)))
                
                hookToggle = True

# Initialize fish
randomFishAmount = random.randrange(minFishAmount, maxFishAmount)
for i in range(randomFishAmount):
    listOfFish.append(Fish(random.randrange(100,200),random.randrange(800,8000)))

while not doExit:
    screen.fill((0, 0, 0))
    clock.tick(60)
    
    pygame.draw.rect(screen, (0,157,196), (0, 500 + scrollY, 400, 7500))
    pygame.draw.rect(screen, (150,150,150), (0, 0 + scrollY, 400, 500))
    
    if hookToggle:
        scrollYVel -= 1
        if scrollYVel <= -80:
            hookComplete = True
            hookToggle = False

    elif not hookToggle and hookComplete:
        scrollYVel += 1
        if scrollYVel >= 80:
            hookComplete = False
            hookToggle = True

    if scrollY >= 0 and scrollYVel == 0:
        hookToggle = False
        hookComplete = False
        scrollYVel = 0
        scrollY = 0
    scrollY += scrollYVel

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            doExit = True
        handle_mouse_event(event)

    for f in listOfFish:
        fishAlive = f.move(scrollY)
        if fishAlive:
            f.draw(scrollY)
        else:
            listOfFish.remove(f)
        
    # Draw the hook line
    pygame.draw.line(screen, ((150,75,0)), ((207,scrollY + 450)),((207, scrollYVel + 500)),3)
    # Draw the hook image
    # Draw the hook image
    hook_scaled = pygame.transform.scale(hookImage, (hookSize, hookSize))
    hook_rect = hook_scaled.get_rect(center=(207, scrollYVel + 510 + hookSize/3))
    screen.blit(hook_scaled, hook_rect)
    # Draw the boat image
    screen.blit(boat1Image, (81,scrollY + 410))
    # Draw the upgrade buttons
    if not hookComplete:
        pygame.draw.rect(screen, (255, 255, 255), (50, 10, 100, 50))  # Boat upgrade button rectangle
        pygame.draw.rect(screen, (255, 255, 255), (250, 10, 100, 50))  # Hook upgrade button rectangle
        upgrade_text = my_font.render("Boat Upgrade", False, (0, 0, 0))
        screen.blit(upgrade_text, (60, 20))
        upgrade_text = my_font.render("Hook Upgrade", False, (0, 0, 0))
        screen.blit(upgrade_text, (260, 20))
        # Display current cash and upgrade levels
        cash_text = my_font.render("Current Cash: " + str(round(currentMoney)), False, (0, 255, 0))
        screen.blit(cash_text, (10, 70))
        level_text = my_font.render("Boat Upgrade Level: " + str(len([u for u in purchased_upgrades if isinstance(u, BoatUpgrade)])), False, (255, 255, 255))
        screen.blit(level_text, (10, 90))
        level_text = my_font.render("Hook Upgrade Level: " + str(len([u for u in purchased_upgrades if isinstance(u, HookUpgrade)])), False, (255, 255, 255))
        screen.blit(level_text, (10, 110))

    pygame.display.flip()

pygame.quit()
