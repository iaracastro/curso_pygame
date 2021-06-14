import pygame

from pygame import mixer
import os
from pygame.locals import (DOUBLEBUF,
                           FULLSCREEN,
                           KEYDOWN, KEYUP,
                           K_DOWN, K_s,
                           K_UP, K_w,
                           K_LEFT, K_a,
                           K_RIGHT, K_d,
                           QUIT,
                           K_ESCAPE, K_RCTRL, K_LCTRL, K_SPACE,
                           K_1, K_2, K_3, K_4,
                           K_x
                           )

from fundo import Fundo
from elementos import ElementoSprite
from sons import Sons

import random

class Jogo:
    def __init__(self, size=(850, 800), fullscreen=False, icon="virus_orange.png"):
        self.elementos = {}
        pygame.init()
        flags = pygame.DOUBLEBUF
        if fullscreen:
            flags |= FULLSCREEN
        self.tela = pygame.display.set_mode(size, flags=flags, depth=16)
        self.fundo = Fundo()
        self.jogador = None
        self.interval = 0
        self.nivel = 0
        self.fonte = pygame.font.SysFont("monospace", 32)
        self.over_font = pygame.font.Font('freesansbold.ttf', 64)
        self.menu_font = pygame.font.SysFont("freesansbold.ttf", 32)
        self.opc_font = pygame.font.SysFont("freesansbold.ttf", 28)

        self.screen_size = self.tela.get_size()
        pygame.mouse.set_visible(0)
        pygame.display.set_caption('Corona Shooter')
        icon = os.path.join('imagens', icon)
        icon = pygame.image.load(icon).convert()
        pygame.display.set_icon(icon)
        self.run = True


    def escreve_placar(self):
        vidas = self.fonte.render(f'Vidas: {self.jogador.get_lives()*"❤"}', 1, (255, 255, 0), (0, 0, 0))
        fase = self.fonte.render(f'Fase: {self.nivel}', 1, (255, 255, 0), (0, 0, 0))
        score = self.fonte.render(f'Score: {self.jogador.pontos}', 1, (255, 255, 0), (0, 0, 0))
        self.tela.blit(vidas, (25, 20))
        self.tela.blit(fase, (self.screen_size[0] - self.screen_size[0]/2.5, 20))
        self.tela.blit(score, (self.screen_size[0] - 180, 20))


    def jogo_text(self):
        over_text = self.over_font.render("CORONA SHOOTER", 1, (255, 255, 255))
        self.tela.blit(over_text, (self.screen_size[0]/2 - self.screen_size[0]/2.7,self.screen_size[1]/3.25))

    def menu(self):
        replay = self.menu_font.render("Jogar  (1)", 1, (255, 255, 255))
        tutorial = self.menu_font.render("Tutorial  (2)", 1, (255, 255, 255))
        personalizar = self.menu_font.render("Personalizar  (3)", 1, (255, 255, 255))
        quit = self.menu_font.render("Sair  (4)", 1, (255, 255, 255))
        self.tela.blit(replay, (self.screen_size[0]/2 - self.screen_size[0]/4,self.screen_size[1]/2))
        self.tela.blit(tutorial, (self.screen_size[0]/2 - self.screen_size[0]/4, (self.screen_size[1]/2)+40))
        self.tela.blit(personalizar, (self.screen_size[0]/2 - self.screen_size[0]/4, (self.screen_size[1]/2)+80))
        self.tela.blit(quit, (self.screen_size[0]/2 - self.screen_size[0]/4, (self.screen_size[1] / 2) + 120))

    def tutorial_text(self):
        tutorial_title = self.over_font.render("TUTORIAL", 1, (255, 255, 255))
        tutorial_desc = self.menu_font.render("Finge que tem um texto explicativo aqui.", 1, (255, 255, 255))
        tutorial_opc1 = self.menu_font.render("<-- Voltar  (x)", 1, (255, 255, 255))
        self.tela.blit(tutorial_title, (self.screen_size[0]/2 - self.screen_size[0]/2.7, self.screen_size[1]/5))
        self.tela.blit(tutorial_desc, (self.screen_size[0] / 2 - self.screen_size[0] / 2.7, self.screen_size[1] / 3.5))
        self.tela.blit(tutorial_opc1, ((self.screen_size[0] / 2 - self.screen_size[0] / 2.5), self.screen_size[1] / 1.5))

    def personalizar_text(self):
        personalizar = self.over_font.render("PERSONALIZAR", 1, (255, 255, 255))
        personalizar_desc = self.menu_font.render("Escolha a cor da sua seringa:", 1, (255, 255, 255))
        personalizar_opc1 = self.opc_font.render("Roxo Padrão  (1)", 1, (255, 255, 255))
        personalizar_opc2 = self.opc_font.render("Vermelho  (2)" , 1, (255, 255, 255))
        personalizar_opc3 = self.opc_font.render("Rosa  (3)", 1, (255, 255, 255))
        personalizar_voltar = self.opc_font.render("Voltar  (x)", 1, (255, 255, 255))
        self.tela.blit(personalizar, (self.screen_size[0]/2 - self.screen_size[0]/2.7, self.screen_size[1]/5))
        self.tela.blit(personalizar_desc, (self.screen_size[0]/2 - self.screen_size[0]/2.7, (self.screen_size[1]/3.5)+60))
        self.tela.blit(personalizar_opc1, (self.screen_size[0]/2 - self.screen_size[0]/2.7, (self.screen_size[1]/3.5)+140))
        self.tela.blit(personalizar_opc2, (self.screen_size[0]/2 - self.screen_size[0]/2.7, (self.screen_size[1]/3.5)+180))
        self.tela.blit(personalizar_opc3, (self.screen_size[0]/2 - self.screen_size[0]/2.7, (self.screen_size[1]/3.5)+220))
        self.tela.blit(personalizar_voltar, ((self.screen_size[0]/2 - self.screen_size[0]/2.7), (self.screen_size[1]/3.5)+260))

    def game_over_text(self):
        over_text = self.over_font.render("GAME OVER!", 1, (255, 255, 255))
        self.tela.blit(over_text, (self.screen_size[0]/2 - self.screen_size[0]/4,self.screen_size[1]/3.25))


    def manutenção(self):
        r = random.randint(0, 100)
        x = random.randint(1, self.screen_size[0])
        virii = self.elementos["virii"]
        if r > (10 * len(virii)):
            enemy = Virus([0, 0])
            size = enemy.get_size()
            enemy.set_pos([min(max(x, size[0] / 2), self.screen_size[0] - size[0] / 2), size[1] / 2])
            colisores = pygame.sprite.spritecollide(enemy, virii, False)
            if colisores:
                return
            self.elementos["virii"].add(enemy)

    def muda_nivel(self):
        xp = self.jogador.get_pontos()
        if xp > 10 and self.level == 0:
            self.fundo = Fundo("tile2.png")
            self.nivel = 1
            self.jogador.set_lives(self.jogador.get_lives() + 3)
        elif xp > 50 and self.level == 1:
            self.fundo = Fundo("tile3.png")
            self.nivel = 2
            self.jogador.set_lives(self.player.get_lives() + 6)

    def atualiza_elementos(self, dt):
        self.fundo.update(dt)
        for v in self.elementos.values():
            v.update(dt)

    def desenha_elementos(self):
        self.fundo.draw(self.tela)
        for v in self.elementos.values():
            v.draw(self.tela)

    def verifica_impactos(self, elemento, list, action):
        """
        Verifica ocorrência de colisões.
        :param elemento: Instância de RenderPlain ou seja um grupo de sprites
        :param list: lista ou grupo de sprites
        :param action: função a ser chamada no evento de colisão
        :return: lista de sprites envolvidos na colisão
        """
        if isinstance(elemento, pygame.sprite.RenderPlain):
            hitted = pygame.sprite.groupcollide(elemento, list, 1, 0)
            for v in hitted.values():
                for o in v:
                    action(o)
            return hitted

        elif isinstance(elemento, pygame.sprite.Sprite):
            if pygame.sprite.spritecollide(elemento, list, 1):
                action()
            return elemento.morto

    def ação_elemento(self, explosionSound="short_explosion.wav", game_over="game_over.wav"):
        """
        Executa as ações dos elementos do jogo.
        :return:
        """
        self.verifica_impactos(self.jogador, self.elementos["tiros_inimigo"],
                               self.jogador.alvejado)
        if self.jogador.morto:
            game_over = os.path.join('sons', game_over)
            game_over = pygame.mixer.Sound(game_over)
            game_over.set_volume(0.08)
            game_over.play()
            J.loop_morto()
            #self.run = False
            return

        # Verifica se o personagem trombou em algum inimigo
        self.verifica_impactos(self.jogador, self.elementos["virii"],
                               self.jogador.colisão)
        if self.jogador.morto:
            game_over = os.path.join('sons', game_over)
            game_over = pygame.mixer.Sound(game_over)
            game_over.set_volume(0.08)
            game_over.play()
            J.loop_morto()
            #self.run = False
            return

        # Verifica se o personagem atingiu algum alvo.
        hitted = self.verifica_impactos(self.elementos["tiros"],
                                        self.elementos["virii"],
                                        Virus.alvejado)
        if hitted:
            explosionSound = os.path.join('sons', explosionSound)
            explosionSound = pygame.mixer.Sound(explosionSound)
            explosionSound.set_volume(0.07)
            explosionSound.play()

        # Aumenta a pontos baseado no número de acertos:
        self.jogador.set_pontos(self.jogador.get_pontos() + len(hitted))

    def trata_eventos(self):
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            self.run = False
        # serve para quebrar o loop, fechar a janela.
        if event.type in (KEYDOWN, KEYUP):
            key = event.key
            if key == K_ESCAPE:
                self.run = False
            elif key == K_SPACE:
                self.interval = 0
                self.jogador.atira(self.elementos["tiros"])
            elif key in (K_UP, K_w):
                self.jogador.accel_top()
            elif key in (K_DOWN, K_s):
                self.jogador.accel_bottom()
            elif key in (K_RIGHT, K_d):
                self.jogador.accel_right()
            elif key in (K_LEFT, K_a):
                self.jogador.accel_left()
            elif key in (K_ESCAPE, K_2):
                self.run = False

        keys = pygame.key.get_pressed()
        if self.interval > 10:
            self.interval = 0
            if keys[K_RCTRL] or keys[K_LCTRL]:
                self.jogador.atira(self.elementos["tiros"])

    def menu_eventos(self):
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            self.run = False
        # serve para quebrar o loop, fechar a janela.
        if event.type in (KEYDOWN, KEYUP):
            key = event.key
            if key == K_1:
                J.loop_vivo()
            elif key == K_2:
                J.loop_tutorial()
            elif key == K_3:
                J.loop_personalizar()
            elif key in (K_ESCAPE, K_4):
                self.run = False

    def tutorial_eventos(self):
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            self.run = False
        # serve para quebrar o loop, fechar a janela.
        if event.type in (KEYDOWN, KEYUP):
            key = event.key
            if key == K_x:
                J.loop_menu()
            elif key == K_ESCAPE:
                self.run = False

    def personalizar_eventos(self):
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            self.run = False
        # serve para quebrar o loop, fechar a janela.
        if event.type in (KEYDOWN, KEYUP):
            key = event.key
            #if key == K_1:
                #J.loop_menu()
            #elif key == K_2:
                #J.loop_menu()
            #elif key == K_3:
                #J.loop_menu()
            if key == K_x:
                J.loop_menu()
            elif key == K_ESCAPE:
                self.run = False


    def loop_vivo(self, soundtrack="corona_soundtrack.mp3"):
        clock = pygame.time.Clock()
        dt = 16
        self.elementos['virii'] = pygame.sprite.RenderPlain(Virus([120, 50]))
        self.jogador = Jogador([self.screen_size[0]/6, self.screen_size[1]-150], 5)
        self.elementos['jogador'] = pygame.sprite.RenderPlain(self.jogador)
        self.elementos['tiros'] = pygame.sprite.RenderPlain()
        self.elementos['tiros_inimigo'] = pygame.sprite.RenderPlain()
        soundtrack = os.path.join('sons', soundtrack)
        mixer.music.load(soundtrack)
        mixer.music.set_volume(0.05)
        pygame.mixer.music.play(-1)

        while self.run:
            clock.tick(1000 / dt)

            self.trata_eventos()
            self.ação_elemento()
            self.manutenção()
            # Atualiza Elementos
            self.atualiza_elementos(dt)

            # Desenhe no back buffer
            self.desenha_elementos()
            self.escreve_placar()
            # texto = self.fonte.render(f"Vidas: {self.jogador.get_lives()}", True, (255, 255, 255), (0, 0, 0))

            pygame.display.flip()

    def loop_morto(self, menu_soundtrack="menu_soundtrack.mp3"):
        clock = pygame.time.Clock()
        dt = 16
        self.elementos['virii'] = pygame.sprite.RenderPlain(Virus([120, 50]))
        self.jogador = Jogador([self.screen_size[0]/6, self.screen_size[1]-150], 5)
        self.elementos['jogador'] = pygame.sprite.RenderPlain(self.jogador)
        self.elementos['tiros'] = pygame.sprite.RenderPlain()
        self.elementos['tiros_inimigo'] = pygame.sprite.RenderPlain()
        menu_soundtrack = os.path.join('sons', menu_soundtrack)
        mixer.music.load(menu_soundtrack)
        mixer.music.set_volume(0.025)
        pygame.mixer.music.play(-1)
        while self.run:
            clock.tick(1000 / dt)
            #self.ação_elemento()
            self.manutenção()
            self.atualiza_elementos(dt)
            self.desenha_elementos()
            self.escreve_placar()
            self.game_over_text()
            self.menu()
            self.menu_eventos()
            pygame.display.flip()


    def loop_menu(self, menu_soundtrack="menu_soundtrack.mp3"):
        clock = pygame.time.Clock()
        dt = 16
        self.elementos['virii'] = pygame.sprite.RenderPlain(Virus([120, 50]))
        self.jogador = Jogador([self.screen_size[0]/6, self.screen_size[1]-150], 5) #Jogador (Posição, Vidas)
        #self.elementos['jogador'] = pygame.sprite.RenderPlain(self.jogador)
        self.elementos['tiros'] = pygame.sprite.RenderPlain()
        self.elementos['tiros_inimigo'] = pygame.sprite.RenderPlain()
        menu_soundtrack = os.path.join('sons', menu_soundtrack)
        mixer.music.load(menu_soundtrack)
        mixer.music.set_volume(0.025)
        pygame.mixer.music.play(-1)
        while self.run:
            clock.tick(1000 / dt)
            #self.ação_elemento()
            self.manutenção()
            self.atualiza_elementos(dt)
            self.desenha_elementos()
            self.escreve_placar()
            self.jogo_text()
            self.menu()
            self.menu_eventos()
            pygame.display.flip()

    def loop_tutorial(self, menu_soundtrack="menu_soundtrack.mp3"):
        clock = pygame.time.Clock()
        dt = 16
        self.elementos['virii'] = pygame.sprite.RenderPlain(Virus([120, 50]))
        self.jogador = Jogador([self.screen_size[0]/6, self.screen_size[1]-150], 5)
        #self.elementos['jogador'] = pygame.sprite.RenderPlain(self.jogador)
        menu_soundtrack = os.path.join('sons', menu_soundtrack)
        mixer.music.load(menu_soundtrack)
        mixer.music.set_volume(0.03)
        pygame.mixer.music.play(-1)
        while self.run:
            clock.tick(1000 / dt)
            #self.ação_elemento()
            self.manutenção()
            self.atualiza_elementos(dt)
            self.desenha_elementos()
            self.tutorial_text()
            #self.menu_eventos()
            self.tutorial_eventos()
            pygame.display.flip()

    def loop_personalizar(self, menu_soundtrack="menu_soundtrack.mp3"):
        clock = pygame.time.Clock()
        dt = 16
        menu_soundtrack = os.path.join('sons', menu_soundtrack)
        mixer.music.load(menu_soundtrack)
        mixer.music.set_volume(0.03)
        pygame.mixer.music.play(-1)
        while self.run:
            clock.tick(1000 / dt)
            #self.ação_elemento()
            self.jogador = Jogador([self.screen_size[0] / 6, self.screen_size[1] - 150], 5)
            self.elementos['jogador'] = pygame.sprite.RenderPlain(self.jogador)
            self.manutenção()
            self.atualiza_elementos(dt)
            self.desenha_elementos()
            self.personalizar_text()
            #self.menu_eventos()
            self.personalizar_eventos()
            pygame.display.flip()

class Nave(ElementoSprite):
    def __init__(self, position, lives=0, speed=[0, 0], image=None, new_size=[100, 248]):
        self.acceleration = [3, 3]
        if not image:
            image = "seringa.png"
        super().__init__(image, position, speed, new_size)
        self.set_lives(lives)

    def get_lives(self):
        return self.lives

    def set_lives(self, lives):
        self.lives = lives

    def colisão(self):
        if self.get_lives() <= 0:
            #crash = pygame.mixer.Sound("crash.wav")
            #crash.play()
            self.kill()
        else:
            self.set_lives(self.get_lives() - 1)

    def atira(self, lista_de_tiros, image=None):
        s = list(self.get_speed())
        s[1] *= 2
        Tiro(self.get_pos(), s, image, lista_de_tiros)

    def alvejado(self):
        if self.get_lives() <= 0:
            self.kill()
        else:
            self.set_lives(self.get_lives() - 1)

    @property
    def morto(self):
        return self.get_lives() == 0

    def accel_top(self):
        speed = self.get_speed()
        self.set_speed((speed[0], speed[1] - self.acceleration[1]))

    def accel_bottom(self):
        speed = self.get_speed()
        self.set_speed((speed[0], speed[1] + self.acceleration[1]))

    def accel_left(self):
        speed = self.get_speed()
        self.set_speed((speed[0] - self.acceleration[0], speed[1]))

    def accel_right(self):
        speed = self.get_speed()
        self.set_speed((speed[0] + self.acceleration[0], speed[1]))


class Virus(Nave):
    def __init__(self, position, lives=1, speed=None, image=None, size=(80,80)):
        if not image:
            image = "virus_verm.png"
        super().__init__(position, lives, speed, image, size)


class Jogador(Nave):
    """
    A classe Player é uma classe derivada da classe GameObject.
       No entanto, o personagem não morre quando passa da borda, este só
    interrompe o seu movimento (vide update()).
       E possui experiência, que o fará mudar de nivel e melhorar seu tiro.
       A função get_pos() só foi redefinida para que os tiros não saissem da
    parte da frente da nave do personagem, por esta estar virada ao contrário
    das outras.
    """

    def __init__(self, position, lives=10, image=None, new_size=[50,140]):
        if not image:
            image = "seringa.png"
        super().__init__(position, lives, [0, 0], image, new_size)
        self.pontos = 0

    def update(self, dt):
        move_speed = (self.speed[0] * dt / 16,
                      self.speed[1] * dt / 16)
        self.rect = self.rect.move(move_speed)

        if (self.rect.right > self.area.right):
            self.rect.right = self.area.right

        elif (self.rect.left < 0):
            self.rect.left = 0

        if (self.rect.bottom > self.area.bottom):
            self.rect.bottom = self.area.bottom

        elif (self.rect.top < 0):
            self.rect.top = 0

    def get_pos(self):
        return (self.rect.center[0], self.rect.top)

    def get_pontos(self):
        return self.pontos

    def set_pontos(self, pontos):
        self.pontos = pontos

    def atira(self, lista_de_tiros, image=None):
        l = 1
        if self.pontos > 25:
            l = 3
        if self.pontos > 100:
            l = 5

        p = self.get_pos()
        speeds = self.get_fire_speed(l)
        for s in speeds:
            Tiro(p, s, image, lista_de_tiros)

    def get_fire_speed(self, shots):
        speeds = []

        if shots <= 0:
            return speeds

        if shots == 1:
            speeds += [(0, -5)]

        if shots > 1 and shots <= 3:
            speeds += [(0, -5)]
            speeds += [(-2, -3)]
            speeds += [(2, -3)]

        if shots > 3 and shots <= 5:
            speeds += [(0, -5)]
            speeds += [(-2, -3)]
            speeds += [(2, -3)]
            speeds += [(-4, -2)]
            speeds += [(4, -2)]

        return speeds


class Tiro(ElementoSprite):
    def __init__(self, position, speed=None, image=None, list=None, size=[60,60]):
        if not image:
            image = "tiro.png"
        super().__init__(image, position, speed, size)
        if list is not None:
            self.add(list)


if __name__ == '__main__':
    J = Jogo()
    J.loop_menu()
