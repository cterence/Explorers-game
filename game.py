#!/usr/bin/python3

# Auteur : Térence Chateigné

from tkinter import *
import random, math


it, itMax = 0, 100000 # Nombre d'itérations
height, width = 300, 200
goal = (width/2, height/2)
refreshRate = 50

class Dot: # Objet point
	def __init__(self) :
		global width, height 
		self.x = width/2
		self.y = 3*height/4
		self.alive = True
		self.score = 0
		self.moves = []
	
	def __str__(self) :
		return "x : "+str(self.x)+", y : "+str(self.y)+", alive : "+str(self.alive)+", score : "+str(self.score)
		
	def isAlive(self) :
		if self.x <= 0 or self.x >= width-5 or self.y <= 0 or self.y >= height-5 or (self.x < goal[0]+10 and self.x > goal[0]-10 and self.y < goal[1]+10 and self.y > goal[1]-10) :
			self.alive = False
			
	def move(self) :
		self.isAlive()
		if (self.alive == True) :
			newX, newY = self.x, self.y
			rand = random.random()
			
			if (rand <= 0.25) :
				newX+=5
			elif (rand <= 0.5) :
				newX-=5
			elif (rand <= 0.75) :
				newY+=5
			else :
				newY-=5
			
			self.moves.append((newX,newY))
			self.x, self.y = newX, newY
			self.fitness()
		
		
	def fitness(self) :
		global goal
		self.score = len(self.moves)*math.sqrt((self.x-goal[0])**2+(self.y-goal[1])**2)
	

class Board:
	def __init__(self) :
		global height, width
		self.canvas = Canvas(root, width=width, height=height, background='white')
		self.dots = []
		self.createPopulation()

	def addDot(self, dot) :
		self.dots.append(dot)
		self.canvas.create_oval(dot.x, dot.y, dot.x+5, dot.y+5, fill='black')	
	
	def createPopulation(self) :
		for i in range(50) :
			self.dots.append(Dot())
	
	def play(self) :
		global goal, it
		self.canvas.delete("all")
		self.canvas.create_oval(goal[0], goal[1], goal[0]+5, goal[1]+5, fill='green')	
		self.update()
		self.canvas.after(refreshRate, self.play)
	
	def update(self) :
		for dot in self.dots :
			dot.move()
			self.canvas.create_oval(dot.x, dot.y, dot.x+5, dot.y+5, fill='black')
	
	def selectFittest(self) :
		minFitness = sys.maxsize
		for dot in self.dots :
			if dot.score < minFitness :
				fittest = dot
				minFitness = dot.score
		return fittest

if __name__ == '__main__' :

	generation = 0
	root = Tk()
	board = Board()
	board.canvas.pack()
	while generation <= 0 :
		root.title("Generation "+str(generation))
		board.play()
		root.after(5000, root.quit)
		root.mainloop()
		fittest = board.selectFittest()
		print("Fittest : "+str(fittest))
		print(len(fittest.moves))
		generation += 1
		
