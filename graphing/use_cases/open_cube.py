# This file started out in graphing, but migrated to pyray.

import numpy as np
import queue
from collections import defaultdict
from itertools import combinations
from PIL import Image, ImageDraw, ImageFont, ImageMath


def tst():
    survive = {3, 10, 11, 8, 5}
    gr = Graph_cube(survive)
    gr.dfs('00+')
    im = Image.new("RGB", (512, 512), (0,0,0))
    draw = ImageDraw.Draw(im,'RGBA')
    gr.draw = draw
    gr.reset_vert_col()
    gr.dfs_plot('00+')
    im.save("plots//im" + str(ix) + ".png")


def tst_all_combo():
    lst = np.arange(12)
    ix = 0
    for combo in combinations(lst, 5):
        survive = set(combo)
        gr = Graph_cube(survive)
        gr.dfs('00+')
        if len(gr.black_verts) == 6:
            if len(survive - {0,1,6,9}) == len(survive):
                im = Image.new("RGB", (512, 512), (0,0,0))
                draw = ImageDraw.Draw(im,'RGBA')
                gr.draw = draw
                gr.reset_vert_col()
                gr.dfs_plot('00+')
                im.save("plots//im" + str(ix) + ".png")
            ix += 1
    print(ix)


class Node():
    def __init__(self, val, color="white"):
        self.val = val
        self.color = color
        self.x = char2coord(val[0])
        self.y = char2coord(val[1])
        self.z = char2coord(val[2])
        # The flattened coordinates.
        self.x1 = 0
        self.y1 = 0


def char2coord(ch):
    if ch == '0':
        return 0
    elif ch == '+':
        return 1
    elif ch == '-':
        return -1


class Graph_cube():
    def __init__(self, survive_ros={}):
        self.white_verts = set()
        self.grey_verts = set()
        self.black_verts = set()
        self.adj = defaultdict(dict)
        self.vert_props = {}
        self.cov_p = set()
        self.cov_p.add((0,0))
        self.edges = [['-00','0+0'],#2
                      ['-00','0-0'],#1
                      ['-00','00-'],#5
                      ['-00','00+'],#8
                      ['0-0','00+'],
                      ['0-0','00-'],#12
                      ['0-0','+00'],
                      ['0+0','00+'],
                      ['0+0','00-'],#11
                      ['0+0','+00'],
                      ['+00','00+'],#7
                      ['+00','00-']]
        self.time = 0
        for ix in range(len(self.edges)):
            ed = self.edges[ix]
            vert_0 = ed[0]
            vert_1 = ed[1]
            self.vert_props[vert_0] = Node(vert_0)
            self.vert_props[vert_1] = Node(vert_1)
            if ix in survive_ros:
                self.white_verts.add(vert_0)
                self.white_verts.add(vert_1)
                # Save graph as an adjacency list.
                self.adj[vert_0][vert_1] = 0
                self.adj[vert_1][vert_0] = 0

    def reset_vert_col(self):
        for v in self.vert_props.keys():
            self.vert_props[v].color = "white"

    def print_vert_props(self):
        for k in self.vert_props.keys():
            print(str(self.vert_props[k].__dict__))

    def dfs(self, u):
        """This code does not work, we will have to rotate explicitly"""
        self.vert_props[u].color = "grey"
        for v in self.adj[u]:
            if self.vert_props[v].color == "white":
                if self.vert_props[v].x == self.vert_props[u].x:
                    sign = int(((self.vert_props[v].x > self.vert_props[u].x)-0.5)*2)
                    if (self.vert_props[u].x1+sign, self.vert_props[u].y1) not in self.cov_p:
                        self.vert_props[v].x1 = self.vert_props[u].x1+sign
                    else:
                        self.vert_props[v].x1 = self.vert_props[u].x1-sign
                    self.vert_props[v].y1 = self.vert_props[u].y1
                else:
                    sign = int(((self.vert_props[v].y > self.vert_props[u].y)-0.5)*2)
                    if (self.vert_props[u].x1, self.vert_props[u].y1+sign) not in self.cov_p:
                        self.vert_props[v].y1 = self.vert_props[u].y1+sign
                    else:
                        self.vert_props[v].y1 = self.vert_props[u].y1-sign
                    self.vert_props[v].x1 = self.vert_props[u].x1

                self.cov_p.add((self.vert_props[v].x1, self.vert_props[v].y1))
                self.dfs(v)
        self.vert_props[u].color = "black"
        self.black_verts.add(u)

    def dfs_plot(self, u):
        """Assumes a draw object attached to graph"""
        self.vert_props[u].color = "grey"
        w = 2
        x, y = map_to_plot(self.vert_props[u].x1, self.vert_props[u].y1)
        self.draw.ellipse((x-w,y-w,x+w,y+w), fill=(255,0,0), outline = (0,0,0))
        for v in self.adj[u]:
            if self.vert_props[v].color == "white":
                x1, y1 = map_to_plot(self.vert_props[v].x1, self.vert_props[v].y1)
                self.draw.line((x, y, x1, y1),
                                fill = (255,255,0), width = 1)
                self.dfs_plot(v)


def map_to_plot(x, y):
    scale = 40
    #shift = np.array([256,256])
    return 256 + x * scale, 256 + y * scale

