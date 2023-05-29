import json
import math

import pygame
import pygame.freetype
import random

import numpy as np
import scipy.constants


import Grehem
import Djarvis
import LargestTriangle
import LTBinary
from Edge import Edge, Segment
from colors import colors


pygame.font.init()

class Game:

    def __init__(self):
        self.settings = {}
        self.edges = []
        self.segments_lin = []
        self.segments_tri = []
        self.buttons = []

        self.upload_settings()
        self.upload_buttons()

        self.screen = pygame.display.set_mode((self.settings["screen"]["width"], self.settings["screen"]["heights"]))
        self.screen.fill(colors[self.settings["screen"]["color"]])

        pygame.display.set_caption('Laba OGKG')
        self.clock = pygame.time.Clock()
        self.fps = 100
        self.functions = (self.clear, self.edges.clear, self.clear_segments, self.add_some_points,
                          self.add_many_points, self.grehem, self.djarvis, self.largest_triangle, self.largest_triangle_improved)
        self.is_moving = False
        self.angels = []

        self.distance = 5
        self.rad_edges = 10
        self.menu_width = 220

    def upload_settings(self):
        with open('settings.json') as file:
            file_content = file.read()
            self.settings = json.loads(file_content)
        file.close()

    def upload_buttons(self):
        my_font = pygame.font.SysFont('Comic Sans MS', 25)
        texts = ['Clear all', 'Clear points', 'Clear segments', 'Add points', 'Add more points', 'Grehem', 'Djarvis', 'Overrun', 'Divide Conquer']
        for text in texts:
            self.buttons.append(my_font.render(text, False, (0, 0, 0)))

    def check_edge(self, cords):
        cords = np.array(cords)

        for edge1 in self.edges:
            if edge1.distance(cords) < 2 * self.rad_edges:
                return True

        if cords[0] < self.rad_edges + self.distance or \
                cords[0] > self.settings["screen"]["width"] - self.menu_width - self.distance - self.rad_edges or \
                cords[1] < self.rad_edges + self.distance or \
                cords[1] > self.settings["screen"]["heights"] - self.rad_edges - + self.distance:
            return True

        return False

    def new_edge(self, cords):

        if self.check_edge(cords):
            return

        self.edges.append(Edge(cords))

        if self.is_moving:
            self.angels.append(random.random() * 2 * scipy.constants.pi)

    def clear(self):
        self.screen.fill(colors[self.settings["screen"]["color"]])
        self.edges.clear()
        self.clear_segments()
        self.angels.clear()

    def clear_segments(self):
        self.screen.fill(colors[self.settings["screen"]["color"]])
        self.segments_lin.clear()
        self.segments_tri.clear()

    def add_points(self, k):
        for i in range(k):
            self.new_edge((
                int((self.settings["screen"]["width"] - self.menu_width -
                     self.distance - self.rad_edges) * random.random()),
                int((self.settings["screen"]["heights"] - self.rad_edges - + self.distance) * random.random())))

    def add_some_points(self):
        self.add_points(10)

    def add_many_points(self):
        self.add_points(100)



    def renew_segments(self, result):
        self.segments_lin.clear()
        for i in range(len(result) - 1):
            self.segments_lin.append(Segment((result[i][0], result[i][1], result[i + 1][0], result[i + 1][1])))

    def renew_segments_tri(self, result):
        self.segments_tri.clear()
        for i in range(len(result)-1):
            self.segments_tri.append(Segment((result[i][0], result[i][1], result[i + 1][0], result[i + 1][1])))
        self.segments_tri.append(Segment((result[len(result)-1][0], result[len(result)-1][1], result[0][0], result[0][1])))

    def grehem(self):
        if len(self.edges) < 2:
            return
        result = Grehem.grehem(self.edges)
        self.renew_segments(result)

    def djarvis(self):
        if len(self.edges) < 2:
            return
        result = Djarvis.djarvis(self.edges)
        self.renew_segments(result)

    def largest_triangle(self):
        vertices = Djarvis.djarvis(self.edges)
        max_triangle = LargestTriangle.largestTriangle(vertices)
        self.renew_segments_tri(max_triangle)

    def largest_triangle_improved(self):
        vertices = Djarvis.djarvis(self.edges)
        max_triangle = LTBinary.find_max_triangle(vertices)
        self.renew_segments_tri(max_triangle)



    def update_segments(self):
        for segment in self.segments_lin:
            pygame.draw.line(self.screen, colors[self.settings["segment"]["lin_color"]], segment.x, segment.y, width=4)
        for segment in self.segments_tri:
            pygame.draw.line(self.screen, colors[self.settings["segment"]["tri_color"]], segment.x, segment.y, width=4)

    def update_edges(self):
        for edge in self.edges:
            pygame.draw.circle(surface=self.screen, color=colors[self.settings["edge"]["color"]],
                               center=(int(edge.cords[0]), int(edge.cords[1])), radius=self.rad_edges, width=0)

    def update_frames(self):

        pygame.draw.rect(self.screen, colors['white'], (self.settings["screen"]["width"] - self.menu_width, 3,
                                                        self.menu_width - 3, self.settings["screen"]["heights"] - 6), 0)

        pygame.draw.rect(self.screen, colors['black'], (self.settings["screen"]["width"] - self.menu_width, 3,
                                                        self.menu_width - 3, self.settings["screen"]["heights"] - 6),
                         width=6)

        pygame.draw.rect(self.screen, colors['black'], (3, 3, self.settings["screen"]["width"] - self.menu_width,
                                                        self.settings["screen"]["heights"] - 8), width=6)

    def update_buttons(self):
        for i, button in enumerate(self.buttons):
            self.screen.blit(button, (self.settings["screen"]["width"] - self.menu_width * 9 / 10, 40 * i + 6))
            pygame.draw.rect(self.screen, colors['black'], (self.settings["screen"]["width"] - self.menu_width, 40 * i,
                                                            self.settings["screen"]["width"] - 6, 40), width=2)

    def update(self):
        self.screen.fill(colors[self.settings["screen"]["color"]])
        self.update_segments()
        self.update_edges()
        self.update_frames()
        self.update_buttons()
        pygame.display.update()
    def start(self):

        self.update()

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        if event.pos[0] < self.settings["screen"]["width"] - self.menu_width:
                            self.new_edge(event.pos)
                        else:
                            try:
                                self.functions[event.pos[1] // 40]()
                            except Exception:
                                pass
                        self.update()

            self.clock.tick(self.fps)


if __name__ == '__main__':
    game = Game()
    game.start()
