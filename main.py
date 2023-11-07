import pygame as pg
import math
import random
pg.init()

#Configurações
width,height = 1200,800
fps = 60
clock = pg.time.Clock()
window = pg.display.set_mode((width,height))
pg.display.set_caption("Space Shooter")
BLACK = (0,0,0)
WHITE = (255,255,255)
FONT = pg.font.SysFont('cambria',15)

nave = pg.image.load('nave.png')
nave = pg.transform.scale(nave, (150,150))
background = pg.image.load("background.jpg")
background = pg.transform.scale(background,(1200,800))
background.set_alpha(128)
vmax_asteroide = 6
vmin_asteroide = .5

t_spwan_ast = 500 # 1segundo


#Definiçõa de classes
class Player():
    def __init__(self,x,y,life,ammo) -> None:
        self.x = self.initial_x = x
        self.y = self.initial_y = y
        self.life = life
        self.ammo = ammo
        self.velocidade = 10
    
    def draw(self,win):
        mouse_x, mouse_y = pg.mouse.get_pos()
        angle = math.degrees(math.atan2(mouse_y - self.y, mouse_x - self.x))*-1
        rotated_image = pg.transform.rotate(nave, angle-90)
        rotated_rect = rotated_image.get_rect()
        rotated_rect.center = (self.x, self.y)
        win.blit(rotated_image, rotated_rect.topleft)

    def inputs(self,keys):
        dx, dy = 0, 0
        if keys[pg.K_w]:
            dy -= 1
        if keys[pg.K_s]:
            dy += 1
        if keys[pg.K_a]:
            dx -= 1
        if keys[pg.K_d]:
            dx += 1

        # Verifica se o jogador está se movendo diagonalmente
        if dx != 0 and dy != 0:
            # Normaliza o vetor diagonal
            length = math.sqrt(dx**2 + dy**2)
            dx /= length
            dy /= length
        self.x += dx * self.velocidade
        self.y += dy * self.velocidade
        
    def atualizar_pos(self):
        if self.life <= 0:
            return True
        elif self.life < 100:
            self.life +=.1
            return False

    def reset(self):
        self.x = self.initial_x
        self.y = self.initial_y
        self.life = 100
class Bullet():
    def __init__(self,x,y,raio,velocidade,direcao,damage) -> None:
        self.x = x
        self.y = y
        self.raio = raio
        self.velocidade = velocidade
        self.damage = damage
        self.dist = math.sqrt(((direcao[0]) - self.x)**2 + ((direcao[1]) - self.y)**2)
        self.dx,self.dy = ((direcao[0]) - self.x) / self.dist, ((direcao[1]) - self.y) / self.dist
    def draw(self,win):
        pg.draw.circle(win,'yellow',(self.x,self.y),self.raio)
    
    def atualizar_pos(self):
        # Atualiza a posição do círculo
        self.x += self.dx * self.velocidade
        self.y += self.dy * self.velocidade
        collide = True if self.y + self.raio > height or self.y - self.raio < 0 or self.x +self.raio>width or self.x - self.raio < 0 else False
        return collide
class Enemy():
    angle = 0
    def __init__(self,pos,velocidade,life,size) -> None:
        self.x, self.y = pos[0],pos[1]
        self.velocidade = velocidade
        self.life = life
        self.size = size
        self.dist = math.sqrt(((width//2) - self.x)**2 + ((height//2) - self.y)**2)
        self.dx,self.dy = ((width//2) - self.x) / self.dist, ((height//2) - self.y) / self.dist
        self.asteroide = pg.image.load('aste.png')
        self.asteroide = pg.transform.scale(self.asteroide, (150*self.size,150*self.size))
        self.rect = self.asteroide.get_rect()
    
    def draw(self,win):        
        self.angle += self.velocidade/4
        image = pg.transform.rotate(self.asteroide, self.angle)
        self.rect = image.get_rect()
        self.rect.center = (self.x, self.y)
        win.blit(image,self.rect.topleft)
    
    def atualizar_pos(self):
        self.x += self.dx * self.velocidade
        self.y += self.dy * self.velocidade

#Definição de funções
def spawn_aste(asteroides):
    spawn_points = [(0,0),(width,0),(width,height//2),(width,height),(width//2,height),(0,height)]
    
    asteroides.append(
        Enemy(pos=random.choice(spawn_points),velocidade=random.uniform(vmin_asteroide,vmax_asteroide),life=100,size=random.uniform(.5,1.7))
    )

def draw(win,player,bullets,asteroides,tempo):
    #Background
    win.blit(background,(0,0))

    #Textos
    vida = FONT.render(f'Vida do jogador: {player.life:.0f}',True,WHITE)
    tempo_ = FONT.render(f'Tempo vivo: {((pg.time.get_ticks()-tempo)/60000):.2f}minutos',True,WHITE)
    win.blit(vida,(width//2 - (vida.get_width()//2),50))
    win.blit(tempo_,(width//2 - (tempo_.get_width()//2),100))
    #Bullets
    for bullet in bullets:
        bullet.draw(win)
        
    #Jogador
    player.draw(win)

    #Asteroides
    for each in asteroides:
        each.draw(win)

    #Atualizar
    pg.display.update()

def main():
    global vmax_asteroide, vmin_asteroide
    #Variáveis locais
    jogador = Player(x=width//2,y=height//2,life=100,ammo=1)
    dano = 30
    bullets = []
    asteroides = []
    t_i = pg.time.get_ticks()
    t_i2 = pg.time.get_ticks()
    t_i3 = pg.time.get_ticks()
    tempo_inicial = pg.time.get_ticks()
    while True:
        clock.tick(fps)
        draw(window,jogador,bullets,asteroides,tempo_inicial)
        keys = pg.key.get_pressed()

        #Aumenta a velocidade max e min dos asteroides após 30seg
        if pg.time.get_ticks() - t_i2 > 20000:
            vmax_asteroide += 1 
            vmin_asteroide += .1
            t_i2 = pg.time.get_ticks()

        #Spawn asteroides
        if pg.time.get_ticks() - t_i > t_spwan_ast:
            spawn_aste(asteroides)
            t_i = pg.time.get_ticks()

        #Player
        jogador.inputs(keys)
        if jogador.atualizar_pos():
            asteroides = []
            bullets = []  
            vmax_asteroide = 6 
            vmin_asteroide = .5
            jogador.reset()
            perdeu = pg.font.SysFont('cambria',50).render('Você é ruim...',True,WHITE)    
            window.blit(perdeu,(width//2 - (perdeu.get_width()//2),height//2))
            pg.display.update()
            pg.time.delay(3000)
            tempo_inicial = pg.time.get_ticks()

        #Bullets
        for i,bullet in enumerate(bullets):
            if bullet.atualizar_pos():
                bullets.pop(i)
        
        #Asteroides
        for i,asteroide in enumerate(asteroides):
            asteroide.atualizar_pos()
            if asteroide.rect.collidepoint(jogador.x,jogador.y):
                jogador.life -=50
                asteroides.pop(i)
            for j,b in enumerate(bullets):
                if asteroide.rect.collidepoint(b.x,b.y):
                    asteroide.life -= bullet.damage
                    bullets.pop(j)
            if asteroide.life <= 0:
                asteroides.pop(i)

        if pg.mouse.get_pressed()[0] and pg.time.get_ticks()-t_i3 > 70:
            t_i3 = pg.time.get_ticks()
            bullet = Bullet(x=jogador.x,y=jogador.y,raio=5,velocidade=30,damage=dano,direcao=pg.mouse.get_pos())
            bullets.append(bullet)

        #Eventos
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

#Execução
if __name__ == '__main__':
    main()