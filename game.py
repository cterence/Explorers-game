#!/usr/bin/python3

# Auteur : Térence Chateigné

from tkinter import *
import random, math, time, copy

### Variables globales ###

height, width = 300, 100
goal = (width/4, 5*height/6)
start = (3*width/4, height/6)
refreshRate = 1
population = 100
generations = 100
firstGen = True
goalReached = False
won = False
allDead = False

### Classe point ###

class Dot:  # Objet point
	def __init__(self):
		global width, height
		self.x = start[0]
		self.y = start[1]
		self.alive = True
		self.score = 0
		self.moves = []
		self.fittest = False

	def __str__(self):
		return "x : "+str(self.x)+", y : "+str(self.y)+", alive : "+str(self.alive)+", score : "+str(self.score)+", fittest ="+str(self.fittest)+", move number :"+str(len(self.moves))

	def isAlive(self):
		if self.x <= 0 or self.x >= width-5 or self.y <= 0 or self.y >= height-5 or (self.x < goal[0]+10 and self.x > goal[0]-10 and self.y < goal[1]+10 and self.y > goal[1]-10):
			self.alive = False
	
	def hasWon(self):
		if self.x < goal[0]+10 and self.x > goal[0]-10 and self.y < goal[1]+10 and self.y > goal[1]-10 :
			return True
		return False

	def move(self):
		self.isAlive()
		if (self.alive == True):
			newX, newY = self.x, self.y
			rand = random.random()
			if (rand <= 0.25):
				newX += 5
			elif (rand <= 0.5):
				newX -= 5
			elif (rand <= 0.75):
				newY += 5
			else:
				newY -= 5
			self.moves.append((newX-self.x, newY-self.y))
			self.x, self.y = newX, newY
			self.fitness()

	def fitness(self):
		global goal
		if goalReached == True:
			if abs(self.x-goal[0]) == 5 and abs(self.y-goal[1]) == 5 :# Cas où le point arrive en diag du but
				print("diag")
				self.score = len(self.moves)*(self.y-goal[1]) # Mise à zéro de la différence entre le x du point et du goal
			else :
				self.score = len(self.moves)*math.sqrt((self.x-goal[0])**2+(self.y-goal[1])**2)
		else :
			self.score = math.sqrt((self.x-goal[0])**2+(self.y-goal[1])**2)

	def moveMutated(self, fittest):
		self.isAlive()
		if (self.alive == True):
			newX, newY = self.x, self.y
			if (random.random() <= 0.1 or len(self.moves) >= len(fittest.moves)) and self.fittest == False:
				rand = random.random()
				if (rand <= 0.25):
					newX += 5
				elif (rand <= 0.5):
					newX -= 5
				elif (rand <= 0.75):
					newY += 5
				else:
					newY -= 5
			else:
				
				newX += fittest.moves[len(self.moves)][0]
				newY += fittest.moves[len(self.moves)][1]

			self.moves.append((newX-self.x, newY-self.y))
			self.x, self.y = newX, newY
		self.fitness()

### Classe plateau ###

class Board:
	def __init__(self):
		global height, width
		self.canvas = Canvas(root, width=width, height=height, background='white')
		self.dots = []
		self.fittest = None
		self.job = None
		self.createPopulation()

	def addDot(self, dot):
		self.dots.append(dot)
		self.canvas.create_oval(dot.x, dot.y, dot.x+5, dot.y+5, fill='black')

	def createPopulation(self):
		for i in range(population):
			self.dots.append(Dot())

	def update(self, firstGen):
		global won, allDead
		allDead = True
		for dot in self.dots:
			if firstGen == True:
				dot.move()
			else:
				dot.moveMutated(self.fittest)
			if dot.fittest == True:
				self.canvas.create_oval(dot.x, dot.y, dot.x+5, dot.y+5, fill='red')
			else :
				self.canvas.create_oval(dot.x, dot.y, dot.x+5, dot.y+5, fill='black')
			if dot.hasWon():
				won = True
				break
			if dot.alive :
				allDead = False

	def play(self):
		global goal, won, firstGen, goalReached
		self.canvas.delete("all")
		self.canvas.create_oval(goal[0], goal[1], goal[0]+5, goal[1]+5, fill='green')
		self.update(firstGen)
		if won == False and allDead == False:
			self.job = self.canvas.after(refreshRate, self.play)
		else :
			if allDead == False :
				self.killAll()
				firstGen = False
				goalReached = True
			root.after(1000, root.quit)

	def cancel(self):
		if self.job is not None:
			self.canvas.after_cancel(self.job)
			self.job = None

	def selectFittest(self):
		minFitness = sys.maxsize
		for dot in self.dots:
			if dot.score < minFitness:
				self.fittest = dot
				minFitness = dot.score
		self.fittest.fittest = True
		print("Score du fittest :"+str(self.fittest.score), self.fittest.x-goal[0], self.fittest.y-goal[1])

	def heritage(self):
		self.dots = []
		fitDot = copy.deepcopy(self.fittest)
		fitDot.alive, fitDot.x, fitDot.y, fitDot.moves, fitDot.win = True, start[0], start[1], [], False
		
		normalDot = copy.deepcopy(fitDot)
		normalDot.fittest = False
		for i in range(population-1):
			self.dots.append(copy.deepcopy(normalDot))
		self.dots.append(fitDot)

	def killAll(self):
		global root
		for dot in self.dots :
			dot.alive = False
		

### Main ###

if __name__ == '__main__':

	generation = 0
	root = Tk()
	board = Board()
	board.canvas.pack()
	root.title("Gen "+str(generation))
	board.play()
	root.mainloop()
	firstGen = False
	board.cancel()
	board.selectFittest()
	generation += 1

	while generation <= generations:
		won = False
		root.title("Gen "+str(generation))
		board.heritage()
		board.play()
		root.mainloop()
		board.cancel()
		board.selectFittest()
		generation += 1

#voir écart entre ancien et nouveau fittest, afficher le nombre de mouvements du fittest dans la fenêtre
#fontion calcul score privilégie trop le peu de mouvements (si le point meurt rapidement = bien)