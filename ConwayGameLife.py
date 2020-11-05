import random as rn
import numpy as np
import pygame
import threading
from datetime import datetime


class procesor(threading.Thread):
    def __init__(self, downlength, toplength, downwidth, topwidth, table, newState, length, width):
        threading.Thread.__init__(self)
        self.downlength = downlength
        self.downwidth = downwidth
        self.toplength = toplength
        self.topwidth = topwidth
        self.length = length
        self.width = width
        self.table = table
        self.newState = newState

    def run(self):
        self.update()

    def update(self):
        for i in range(self.downlength, self.toplength):
            for k in range(self.downwidth, self.topwidth):
                a = (self.table[(i - 1 + self.length) % self.length][(k - 1 + self.width) % self.width] +
                     self.table[(i - 1 + self.length) % self.length][(k + self.width) % self.width] +
                     self.table[(i + self.length) % self.length][(k - 1 + self.width) % self.width] +
                     self.table[(i + 1 + self.length) % self.length][(k + 1 + self.width) % self.width] +
                     self.table[(i + 1 + self.length) % self.length][(k + self.width) % self.width] +
                     self.table[(i + self.length) % self.length][(k + 1 + self.width) % self.width] +
                     self.table[(i + 1 + self.length) % self.length][(k - 1 + self.width) % self.width] +
                     self.table[(i - 1 + self.length) % self.length][(k + 1 + self.width) % self.width])

                if self.table[i][k] == 0:
                    if a == 765:
                        self.newState[i][k] = 255
                    else:
                        self.newState[i][k] = 0
                else:
                    if 510 > a or a > 765:
                        self.newState[i][k] = 0
                    else:
                        self.newState[i][k] = 255


class visor:

    def __init__(self, length, width):
        self.table = np.zeros((length, width))
        self.newState = np.zeros((length, width))
        self.length = length
        self.width = width
        self.lengthRange = range(length)
        self.widthRange = range(width)

        for i in range(length):
            for k in range(width):
                self.table[i][k] = rn.choice([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255])


    def update(self):
        threads = []


        # Create new threads
        thread1 = procesor(0, 333, 0, 333, self.table, self.newState, self.length,
                           self.width)
        thread2 = procesor(333, 666, 0, 333, self.table, self.newState, self.length,
                           self.width)
        thread4 = procesor(0, 333, 333, 666, self.table, self.newState, self.length,
                           self.width)
        thread5 = procesor(333, 666, 333, 666, self.table, self.newState, self.length,
                           self.width)

        # Start new Threads
        thread1.start()
        thread2.start()
        thread4.start()
        thread5.start()

        # Add threads to thread list
        threads.append(thread1)
        threads.append(thread2)
        threads.append(thread4)
        threads.append(thread5)

        # Wait for all threads to complete
        for t in threads:
            t.join()

        # change the state
        w = self.table
        self.table = self.newState
        self.newState = w

    def updateU(self):
        for i in self.lengthRange:
            for k in self.widthRange:
                a = (self.table[(i - 1 + self.length) % self.length][(k - 1 + self.width) % self.width] +
                     self.table[(i - 1 + self.length) % self.length][(k + self.width) % self.width] +
                     self.table[(i + self.length) % self.length][(k - 1 + self.width) % self.width] +
                     self.table[(i + 1 + self.length) % self.length][(k + 1 + self.width) % self.width] +
                     self.table[(i + 1 + self.length) % self.length][(k + self.width) % self.width] +
                     self.table[(i + self.length) % self.length][(k + 1 + self.width) % self.width] +
                     self.table[(i + 1 + self.length) % self.length][(k - 1 + self.width) % self.width] +
                     self.table[(i - 1 + self.length) % self.length][(k + 1 + self.width) % self.width])

                if self.table[i][k] == 0:
                    if a == 765:
                        self.newState[i][k] = 255
                    else:
                        if a == 0 and rn.randint(1, 1000) >= 999:
                            self.newState[i][k] = 255
                            break

                        self.newState[i][k] = 0
                else:
                    if 510 > a or a > 765:
                        self.newState[i][k] = 0
                    else:
                        self.newState[i][k] = 255

        # change the state
        w = self.table
        self.table = self.newState
        self.newState = w

    def reset(self):
        for i in range(self.length):
            for k in range(self.width):
                self.table[i][k] = rn.choice([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255])


h, w = 1000, 1000
border = 5

v = visor(200, 200)
pygame.init()
screen = pygame.display.set_mode((w + (2 * border), h + (2 * border)))
pygame.display.set_caption("Serious Work - not games")
done = False
clock = pygame.time.Clock()

# Get a font for rendering the frame number
basicfont = pygame.font.SysFont(None, 32)

# Clear screen to white before drawing
screen.fill((255, 255, 255))

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # Convert to a surface and splat onto screen offset by border width and height
    surface = pygame.surfarray.make_surface(v.table)

    surface = pygame.transform.scale(surface, (1000, 1000))
    screen.blit(surface, (border, border))


    pygame.display.flip()
    clock.tick(60)

    # current date and time
    now = datetime.now()

    v.updateU()

    print((datetime.now() - now), "------------------")
