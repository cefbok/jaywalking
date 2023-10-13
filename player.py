import pygame, sys
from os import walk

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision):
        super().__init__(groups)

        # image
        self.import_player()
        self.frame_index = 0
        self.status = 'up'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        self.pos = pygame.math.Vector2(self.rect.center)

        # movement
        self.direction = pygame.math.Vector2()
        self.speed = 200

        # collision
        self.collision = collision
        self.hitbox = self.rect.inflate(0, -self.rect.height / 2)

    def collisions_sprite(self, direction):
        if direction == 'horizontal':
            for sprite in self.collision.sprites():
                if sprite.hitbox.colliderect(self.hitbox):
                    if hasattr(sprite, 'name') and sprite.name == 'car':
                        pygame.quit()
                        sys.exit()
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.rect.centerx
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
        else:
                for sprite in self.collision.sprites():
                    if sprite.hitbox.colliderect(self.hitbox):
                        if hasattr(sprite, 'name') and sprite.name == 'car':
                            pygame.quit()
                            sys.exit()
                        if self.direction.y > 0: # moving down
                            self.hitbox.bottom = sprite.hitbox.top
                            self.rect.centery = self.hitbox.centery
                            self.pos.y = self.rect.centery
                        if self.direction.y < 0: # moving up
                            self.hitbox.top = sprite.hitbox.bottom
                            self.rect.centery = self.hitbox.centery
                            self.pos.y = self.hitbox.centery
    
    def import_player(self):
        self.animations = {}
        for index, folder in enumerate(walk('./Frogger/graphics/player')):
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []
            else:
                for file_name in folder[2]:
                    path = folder[0].replace('\\','/') + '/' + file_name
                    surf = pygame.image.load(path).convert_alpha()
                    key = folder[0].split('\\')[1]
                    self.animations[key].append(surf)

    def animate(self, dt):
        current_animation = self.animations[self.status]
        if self.direction.magnitude() != 0:
            self.frame_index += 10 * dt
            if self.frame_index >= len(current_animation):
                self.frame_index = 0
        else:
            self.frame_index = 0
        self.image = current_animation[int(self.frame_index)]

    def move(self, dt):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # horizontal collision
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collisions_sprite('horizontal')

        # vertical collision
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collisions_sprite('vertical')

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0   

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0

    def restrict(self):
        if self.rect.left < 640:
            self.pos.x = 640 + self.rect.width / 2
            self.hitbox.left = 640
            self.rect.left = 640
        if self.rect.right > 2560:
            self.pos.x = 2560 + self.rect.width / 2
            self.hitbox.right = 2560
            self.rect.right = 2560
        if self.rect.bottom > 3500:
            self.pos.y = 3500 + self.rect.height / 2
            self.rect.bottom = 3500
            self.hitbox.centry = self.rect.centery

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
        self.restrict()