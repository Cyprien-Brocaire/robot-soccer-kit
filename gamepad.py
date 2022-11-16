import pygame
from pygame.locals import *
import time
import numpy as np
from rsk import *
from rsk.client import ClientError


pygame.init()


joystick = list()
for i in range(pygame.joystick.get_count()):
    joystick.append(pygame.joystick.Joystick(i))
    joystick[i].init()
print(f"Joystick connected : {len(joystick)}")

with Client(host="localhost", key="", wait_ready=False) as client:

    mode = int(input("1 - Duel \n2 - Coop\n"))
    if mode == 1:
        robots = [(client.robots[team][num], [0, 0, 0]) for num in (1, 2) for team in ("blue", "green")][: len(joystick)]
    elif mode == 2:
        robots = [(client.robots[team][num], [0, 0, 0]) for team in ("blue", "green") for num in (1, 2)][: len(joystick)]
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                print("Exit")
                exit()
            elif ev.type == pygame.JOYAXISMOTION:
                if ev.axis in (0, 1):
                    robots[ev.instance_id][1][ev.axis] = -1 * ev.value if (-0.1 > ev.value or ev.value > 0.1) else 0
                if ev.axis == 2:
                    robots[ev.instance_id][1][ev.axis] = -10 * ev.value if (-0.1 > ev.value or ev.value > 0.1) else 0
            elif ev.type == pygame.JOYBUTTONDOWN:
                if ev.button in (0, 7):
                    robots[ev.instance_id][0].kick()

        for robot, acc in robots:
            print(acc)
            robot.control(acc[1], acc[0], acc[2])
