import pygame as pg
import math
import random
import json
from itertools import islice

with open('pontuacoes.json','r') as file:
    pontuacoes = json.load(file)
pontuacoes = dict(sorted(pontuacoes.items(), key=lambda item: item[1],reverse=True))
pontuacoes = dict(islice(pontuacoes.copy().items(), 10))

while True:
    user = input('\nInforme seu username: ').lower().replace(' ','-')
    if len(user) > 10:
        print('Username com mais de 10 caracteres...')
        continue
    if user in pontuacoes.keys():
        match input('Já existe um com mesmo nome\nDeseja continuar? (s ou n): ').lower().replace(' ',''):
            case 'n':
                continue
            case _:
                break
    else:
        break

pg.init()

#Configurações
width,height = 1200,800
fps = 60
clock = pg.time.Clock()
window = pg.display.set_mode((width,height))
pg.display.set_caption("Space Shooter")

#Variáveis Globais
BLACK, WHITE = (0,0,0), (255,255,255)
FONT = pg.font.SysFont('cambria',15)

vmax_asteroide, vmin_asteroide = 6, .5
tempo_spawn_asteroides = 500 #500ms

highscore = pontuacoes[user]

#Definiçõa de classes
class Player():
    def __init__(self,x,y,life,ammo) -> None:
        self.x = self.initial_x = x
        self.y = self.initial_y = y
        self.life = self.initial_life = life
        self.ammo = ammo
        self.velocidade = 10
        self.nave = pg.transform.scale(pg.image.load('nave.png'), (110,110))
        self.rect = self.nave.get_rect()
    
    def draw(self,win):
        mouse_x, mouse_y = pg.mouse.get_pos()
        angulo = math.degrees(math.atan2(mouse_y - self.y, mouse_x - self.x))*-1
        nave_img_rotacionada = pg.transform.rotate(self.nave, angulo-90)
        self.rect = nave_img_rotacionada.get_rect()
        self.rect.center = (self.x, self.y)
        win.blit(nave_img_rotacionada, self.rect.topleft)

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
            length = math.sqrt(dx**2 + dy**2)
            dx /= length
            dy /= length
        self.x += dx * self.velocidade
        self.y += dy * self.velocidade

    def limites(self):
        offset = 30
        if self.x + self.rect.width > width + offset:
            self.x = width - self.rect.width + offset
        elif self.x - self.rect.width < -offset:
            self.x = self.rect.width - offset
        if self.y + self.rect.height > height + offset:
            self.y = height-self.rect.height + offset
        elif self.y - self.rect.height < -offset:
            self.y = self.rect.height - offset

    def verificar_vida(self):
        if self.life <= 0:
            return True
        elif self.life < 100:
            self.life +=.1
            return False

    def reset(self):
        self.x = self.initial_x
        self.y = self.initial_y
        self.life = self.initial_life

class Bullet():
    def __init__(self,pos,raio,velocidade,direcao,damage) -> None:
        self.x, self.y = pos[0],pos[1]
        self.raio = raio
        self.velocidade = velocidade
        self.damage = damage
        self.color = 'purple'
        self.dist = math.sqrt(((direcao[0]) - self.x)**2 + ((direcao[1]) - self.y)**2)
        self.dx,self.dy = ((direcao[0]) - self.x) / self.dist, ((direcao[1]) - self.y) / self.dist

    def draw(self,win):
        pg.draw.circle(win,self.color,(self.x,self.y),self.raio)
    
    def atualizar_pos(self):
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
        self.dx, self.dy = ((width//2) - self.x) / self.dist, ((height//2) - self.y) / self.dist
        self.asteroide = pg.transform.scale(pg.image.load('aste.png'), (150*self.size,150*self.size))
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
def spawn_asteroides(asteroides):
    pontos_spawn = [(0,0),(width,0),(width,height//2),(width,height),(width//2,height),(0,height),(0,height//2)]
    asteroides.append(
        Enemy(pos=random.choice(pontos_spawn),velocidade=random.uniform(vmin_asteroide,vmax_asteroide),life=100,size=random.uniform(.5,1.7))
    )

def draw(win,player,bullets,asteroides,tempo):
    #Background
    win.fill(BLACK)

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

def pre(pontuacoes):
    while True:
        clock.tick(fps)
        window.fill(BLACK)

        title = pg.font.SysFont('cambria',30).render('Melhores pontuações',True,WHITE)
        window.blit(title,(width//2-(title.get_width()//2),100))

        y = 200
        for i in pontuacoes.keys():
            pont1 = pg.font.SysFont('cambria',20).render(f'{i}. {pontuacoes[i]}min',True,WHITE)
            window.blit(pont1,(width//2-(pont1.get_width()//2),y))
            y+=30

        space = pg.font.SysFont('cambria',15).render('Pressione SPACE para continuar',True,WHITE)
        window.blit(space,(width//2-(space.get_width()//2),height-100))

        if pg.key.get_pressed()[pg.K_SPACE]:
            break
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
                
        pg.display.update()

def main():
    global vmax_asteroide, vmin_asteroide

    pre(pontuacoes)

    #Variáveis locais
    jogador = Player(x=width//2,y=height//2,life=100,ammo=1)
    dano_bullet = 30
    dano_asteroide = 50
    bullets = []
    asteroides = []
    t_i0 = pg.time.get_ticks()
    t_i1 = pg.time.get_ticks()
    t_i2 = pg.time.get_ticks()
    t_i3 = pg.time.get_ticks()

    #Início Game Loop
    while True:
        clock.tick(fps)
        draw(window,jogador,bullets,asteroides,t_i0)
        keys = pg.key.get_pressed()

        #Aumenta a velocidade max e min dos asteroides após 20seg
        if pg.time.get_ticks() - t_i2 > 20000:
            vmax_asteroide += 1 
            vmin_asteroide += .1
            t_i2 = pg.time.get_ticks()

        #Spawn asteroides
        if pg.time.get_ticks() - t_i1 > tempo_spawn_asteroides:
            spawn_asteroides(asteroides)
            t_i1 = pg.time.get_ticks()

        #Player
        jogador.limites()
        jogador.inputs(keys)
        if jogador.verificar_vida():
            if (pg.time.get_ticks() - t_i0)/60000 > highscore:
                pontuacoes[user] = round((pg.time.get_ticks() - t_i0)/60000,2)
                with open("pontuacoes.json", "w") as file:
                    json.dump(pontuacoes, file)
            asteroides = []
            bullets = []  
            vmax_asteroide = 6 
            vmin_asteroide = .5
            jogador.reset()
            perdeu = pg.font.SysFont('cambria',50).render('Você é ruim!!!',True,WHITE)    
            window.blit(perdeu,(width//2 - (perdeu.get_width()//2),height//2))
            pg.display.update()
            pg.time.delay(3000)
            t_i0 = pg.time.get_ticks()

        #Bullets
        for i,bullet in enumerate(bullets):
            if bullet.atualizar_pos():
                bullets.pop(i)
        
        #Asteroides
        for i,asteroide in enumerate(asteroides):
            asteroide.atualizar_pos()
            if asteroide.rect.collidepoint(jogador.x,jogador.y):
                jogador.life -= dano_asteroide
                asteroides.pop(i)
            for j,b in enumerate(bullets):
                if asteroide.rect.collidepoint(b.x,b.y):
                    asteroide.life -= bullet.damage
                    bullets.pop(j)
            if asteroide.life <= 0:
                asteroides.pop(i)

        if pg.mouse.get_pressed()[0] and pg.time.get_ticks()-t_i3 > 70:
            bullets.append(Bullet(pos=(jogador.x,jogador.y),raio=5,velocidade=30,damage=dano_bullet,direcao=pg.mouse.get_pos()))
            t_i3 = pg.time.get_ticks()

        #Eventos
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

#Execução
if __name__ == '__main__':
    main()