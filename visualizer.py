import turtle
from functions import *


class Stack():
    def __init__(self):
        self.stack = []

    def push(self, string):
        self.stack.append(string)

    def pop(self):
        return self.stack.pop(-1)


def visualize(string):
    t = turtle.Turtle()
    wn = turtle.Screen()
    turtle.tracer(False)
    wn.bgcolor('white')

    t.seth(90)
    t.shape('classic')
    t.color('black')
    t.pensize(1)
    t.penup()
    t.setpos(0, -250)
    t.pendown()
    t.speed(0)
    t.hideturtle()

    stack = Stack()

    for i in string:
        if i == 'F':
            t.forward(8)
        elif i == '-':
            t.right(30)
        elif i == '+':
            t.left(30)
        elif i == '[':
            x, y = t.pos()
            h = t.heading()
            stack.push((x, y, h))
        elif i == ']':
            x, y, h = stack.pop()
            t.penup()
            # print(x,y,h)
            t.setpos(x, y)
            t.seth(h)
            t.pendown()

    print("done")
    turtle.update()
    wn.exitonclick()


# s = lSysGenerate('F+F-[-F+F-F+F]', 4)
# visualize(s)
