#!/usr/bin/env python

"""
Author : tharindra galahena (inf0_warri0r)
Project: generating images using genetic algorithms
Blog   : http://www.inf0warri0r.blogspot.com
Date   : 06/01/2013
License:

     Copyright 2012 Tharindra Galahena

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version. This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
details.

* You should have received a copy of the GNU General Public License along with
This program. If not, see http://www.gnu.org/licenses/.

"""

from Tkinter import *
import ga as ga
from PIL import Image, ImageTk

psize = 100
gnum = 100
width = 380
height = 200
k = 10
h = 10
w = 10


def fitness(a, dpix):

    mask = 0b00000000000000000000000011111111
    error = 0.0
    for y in range(0, h):
        for x in range(0, w):

            g = (a[y * w + x] & mask)
            d = 0
            for j in range(y * k, (y + 1) * k):
                for i in range(x * k, (x + 1) * k):
                    d = d + dpix[i, j][0]
                    d = d + dpix[i, j][1]
                    d = d + dpix[i, j][2]
            mean = float(d) / (3.0 * k * k)
            eg = (mean - float(g)) ** 2.0
            err = (1.0 / (1.0 + eg))
            error = error + err

    return error


def array2image(a, im_g):

    mask = 0b00000000000000000000000011111111
    pix = im_g.load()

    for y in range(0, h):
        for x in range(0, w):
            g = (a[y * w + x] & mask)
            for i in range(0, k):
                for j in range(0, k):
                    pix[x * k + i, y * k + j] = g, g, g


if __name__ == '__main__':

    pop = ga.population(psize, gnum, 100, 2)
    chro = pop.genarate()

    im_g = Image.new("RGB", (w * k, h * k))
    im_o = Image.open("test.png").resize((100, 100))

    root = Tk()
    root.title("image_generati0n")

    cnv = Canvas(root, width=width, height=height, background="black")
    cnv.grid(row=0, column=0)

    o_pix = im_o.load()
    array2image(chro[0], im_g)

    fit = list()

    for i in range(0, psize):
        fit.append(0.0)

    im1 = ImageTk.PhotoImage(im_g)
    im2 = ImageTk.PhotoImage(im_g)
    imd = ImageTk.PhotoImage(im_o)

    gen_count = 0
    b_fit = 0.0

    while 1:
        gen_count = gen_count + 1
        for i in range(0, psize):
            if i % 2 == 0:
                array2image(chro[i], im_g)
                cnv.delete(ALL)
                im1 = ImageTk.PhotoImage(im_g)
                cnv.create_image(20, 20, anchor=NW, image=im1)
                cnv.create_image(w * k + 40, 20, anchor=NW, image=im2)
                cnv.create_image(2 * w * k + 60, 20, anchor=NW, image=imd)
                cnv.create_text(20, h * k + 40, anchor=W, fill='white',
                    text="generation   : " + str(gen_count))
                cnv.create_text(20, h * k + 60, anchor=W, fill='white',
                    text="best fitness : " + str(b_fit))
                cnv.update()
            fit[i] = fitness(chro[i], o_pix)

        chro = pop.new_gen(fit)
        b_fit = fitness(chro[0], o_pix)
        array2image(chro[0], im_g)
        cnv.delete(ALL)
        im2 = ImageTk.PhotoImage(im_g)
        cnv.create_image(20, 20, anchor=NW, image=im1)
        cnv.create_image(140, 20, anchor=NW, image=im2)
        cnv.create_image(260, 20, anchor=NW, image=imd)
        cnv.create_text(20, h * k + 40, anchor=W, fill='white',
                    text="generation   : " + str(gen_count))
        cnv.create_text(20, h * k + 60, anchor=W, fill='white',
                    text="best fitness : " + str(b_fit))
        cnv.update()
    root.mainloop()
