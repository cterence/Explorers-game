#!/usr/bin/python3

from tkinter import *
import random

class Dot:
	def __init__(self) :
		self.x = 300
		self.y = 550
		self.alive = True
		self.score = 0
		self.moves = []
		
	def isAlive(self) :
		if self.x < 0 or self.x > 600 or self.y < 0 or self.y > 600 :
			self.alive = False
			
	def move(self) :
		newX, newY = 0, 0
		if (random.random() <= 0.5) :
			newX = self.x+5
		else :
			newX = self.x-5
		if (random.random() <= 0.5) :
			newY = self.y+5
		else :
			newY = self.y-5
		
		self.moves.append((newX,newY))
		print(newX, newY)
		self.x, self.y = newX, newY
		self.isAlive()

class Board:
	def __init__(self) :
		self.canvas = Canvas(fenetre, width=600, height=600, background='white')
		self.dots = []

	def addDot(self, dot) :
		self.dots.append(dot)
		self.canvas.create_oval(dot.x, dot.y, dot.x+5, dot.y+5, fill='black')	
	
	def displayDots(self) :
		self.canvas.delete("all")
		self.canvas.create_oval(300, 50, 305, 55, fill='green')	
		self.update()
		self.canvas.after(5, self.displayDots)
	
	def update(self) :
		for dot in self.dots :
			if dot.alive == True :
				dot.move()	
				self.canvas.create_oval(dot.x, dot.y, dot.x+5, dot.y+5, fill='black')
			print(dot.x, dot.y)
		
if __name__ == '__main__' :

	
	fenetre = Tk()
	dot = Dot()
	
	board = Board()
	board.addDot(dot)
	board.addDot(dot)
	board.addDot(dot)
	board.canvas.pack()
	
	board.displayDots()

	fenetre.mainloop()
