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
	
	def __str__(self) :
		return "x : "+str(self.x)+", y : "+str(self.y)+", alive : "+str(self.alive)+", score : "+str(self.score)
		
	def isAlive(self) :
		if self.x < 0 or self.x > 600 or self.y < 0 or self.y > 600 :
			self.alive = False
			
	def move(self) :
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
		self.canvas.after(50, self.displayDots)
	
	def update(self) :
		for dot in self.dots :
			print("Before :"+str(dot))
			if dot.alive == True :
				dot.move()
				self.canvas.create_oval(dot.x, dot.y, dot.x+5, dot.y+5, fill='black')
				print("After :"+str(dot))
		print('end')
		
if __name__ == '__main__' :

	
	fenetre = Tk()
	dot1 = Dot()
	dot2 = Dot()
	
	board = Board()
	board.addDot(dot1)
	board.addDot(dot2)
	
	board.canvas.pack()
	
	board.displayDots()

	fenetre.mainloop()
