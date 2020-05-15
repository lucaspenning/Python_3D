import pygame
from pygame.locals import *
import numpy as np

#Tamanho da janela
SCR_HEIGHT	= 700
SCR_WIDTH	= 1000
#Taxa de atualizaçõa
FPS			= 120
#Cores da linha		
COLOR		= (255,255,255)

#Classe que faz todo o processo de girar e definir posicionamento da figura
class Point:
	def __init__(self,x=0,y=0,z=0):
		self.x = x
		self.y = y
		self.z = z

	def xyz(self):
		return self.x,self.y,self.z

	#Girar em torno do eixo X pelo ângulo especificado em graus.
	def rotateX(self,angle=1):		
		theta=angle*np.pi/180
		sintht = np.sin(theta)
		costht = np.cos(theta)
		self.y=self.y*costht - self.z*sintht
		self.z=self.y*sintht + self.z*costht

	#Girar em torno do eixo Y pelo ângulo especificado em graus.
	def rotateY(self,angle=1):
		theta=angle*np.pi/180
		sintht = np.sin(theta)
		costht = np.cos(theta)
		self.z=self.z*costht - self.x*sintht
		self.x=self.z*sintht + self.x*costht

	#Girar em torno do eixo Z pelo ângulo especificado em graus.
	def rotateZ(self,angle=1):
		theta=angle*np.pi/180
		sintht = np.sin(theta)
		costht = np.cos(theta)
		self.x=self.x*costht - self.y*sintht
		self.y=self.x*sintht + self.y*costht

	#Definindo posicionamento da forma geométrica na tela
	def project(self):
		factor = 2000/(15+self.z)
		x = self.x*factor + SCR_WIDTH/3
		y = self.y*factor + SCR_HEIGHT/4
		return x,y

#Classe onde eu defino a forma da figura 3D
class Cube:
	def __init__(self):
		#Definindo as vertices que compões cada uma das 6 faces
		self.length = 200
		self.points = [	Point(-1,1,1),
						Point(1,1,1),
						Point(1,-1,1),
						Point(-1,-1,1),
						Point(-1,1,-1),
						Point(1,1,-1),
						Point(1,-1,-1),
						Point(-1,-1,-1)]
		self.ver1 = (0,2,5,7)
		self.ver2 = ((1,3,4),(1,3,6),(1,4,6),(3,4,6))

	#Atualizo os pontos conforme rotacionar a figura
	def update(self,x,y,z):
		for p in self.points:
			if x:
				p.rotateX(x)
			if y:
				p.rotateY(y)
			if z:
				p.rotateZ(z)

	#Juntando todas as informações da figura e colocando dentro da janela
	def drawlines(self,screen):
		p=self.points
		for i,b in zip(self.ver1,self.ver2):
			for j in b:
				pygame.draw.aaline(screen,COLOR,p[i].project(),p[j].project())

#Classe de inicialização
class Render:
	def __init__(self):
		#Criar a Janela
		self.screen = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
		#Desenhar o cubo dentro da janela
		self.cu1 = Cube()
		#Definir o angulo de rotação
		self.angle = 1

	#Atualização da figura dentro da Janela
	def draw(self,x,y,z):
		self.cu1.update(x,y,z)
		self.cu1.drawlines(self.screen)

	#Atualizando as informação
	def run(self):
		clock = pygame.time.Clock()
		n_exit_game = True
		while n_exit_game:
			clock.tick(FPS)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					n_exit_game=False
			keys=pygame.key.get_pressed()
			x=y=z=0
			#Girando em torno do eixo X
			if keys[K_s]:
				x=1
			if keys[K_w]:
				x=-1
			#Girando em torno do eixo Y			
			if keys[K_a]:
				y=1
			if keys[K_d]:
				y=-1
			#Girando em torno do eixo Z
			if keys[K_x]:
				z=1
			if keys[K_z]:
				z=-1
			self.screen.fill((0, 0, 0))
			self.draw(x,y,z)
			pygame.display.update()

if __name__ == "__main__":
	Render().run()