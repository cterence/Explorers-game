#!/usr/bin/python3

# Auteur : Térence Chateigné

from tkinter import *
import random
import math
import time
import copy


it, itMax = 0, 100000  # Nombre d'itérations
height, width = 600, 200
goal = (width/2, height/6)
refreshRate = 2
genTime = 5000
population = 1000
generations = 10
firstGen = True


class Dot:  # Objet point
	def __init__(self):
		global width, height
		self.x = width/2
		self.y = 3*height/4
		self.alive = True
		self.score = 0
		self.moves = []
		self.fittest = False

	def __str__(self):
		return "x : "+str(self.x)+", y : "+str(self.y)+", alive : "+str(self.alive)+", score : "+str(self.score)+", fittest ="+str(self.fittest)+", move number :"+str(len(self.moves))

	def isAlive(self):
		if self.x <= 0 or self.x >= width-5 or self.y <= 0 or self.y >= height-5 or (self.x < goal[0]+10 and self.x > goal[0]-10 and self.y < goal[1]+10 and self.y > goal[1]-10):
			self.alive = False

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
		self.score = len(self.moves)*((self.x-goal[0])**2+(self.y-goal[1])**2)**2

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
		for dot in self.dots:
			if firstGen == True:
				dot.move()
			else:
				dot.moveMutated(self.fittest)
			if dot.fittest == True:
				self.canvas.create_oval(dot.x, dot.y, dot.x+5, dot.y+5, fill='red')
			else :
				self.canvas.create_oval(dot.x, dot.y, dot.x+5, dot.y+5, fill='black')

	def play(self):
		global goal
		self.canvas.delete("all")
		self.canvas.create_oval(goal[0], goal[1], goal[0]+5, goal[1]+5, fill='green')
		self.update(firstGen)
		self.job = self.canvas.after(refreshRate, self.play)

	def cancel(self):
		if self.job is not None:
			self.canvas.after_cancel(self.job)
			self.job = None

	def selectFittest(self):
		minFitness = sys.maxsize
		for dot in self.dots:
			print(dot)
			if dot.score < minFitness:
				self.fittest = dot
				minFitness = dot.score
		self.fittest.fittest = True

	def heritage(self):
		self.dots = []
		fitDot = copy.deepcopy(self.fittest)
		fitDot.alive, fitDot.x, fitDot.y, fitDot.moves = True, width/2, 3*height/4, []
		self.dots.append(fitDot)
		normalDot = copy.deepcopy(fitDot)
		normalDot.fittest = False
		for i in range(population-1):
			self.dots.append(copy.deepcopy(normalDot))


if __name__ == '__main__':

	generation = 0
	root = Tk()
	board = Board()
	board.canvas.pack()
	root.title("Generation "+str(generation))
	board.play()
	root.after(genTime, root.quit)
	root.mainloop()
	board.cancel()
	board.selectFittest()
	firstGen = False
	generation += 1

	while generation <= generations:
		root.title("Generation "+str(generation))
		board.heritage()
		board.play()
		root.after(genTime, root.quit)
		root.mainloop()
		board.cancel()
		board.selectFittest()
		generation += 1
