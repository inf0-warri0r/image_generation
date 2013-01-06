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

import random
import sys
import thread
import threading


class population:

    def __init__(self, s, n, cross, mutation):

        self.crossover_rate = cross
        self.mutation_rate = mutation
        self.size = s
        self.gnum = n
        self.b_fit = 0
        self.avg_fitness = 0.0
        self.chromosoms = list()
        self.chromosoms_new = list()
        self.thread_count = 0
        self.cut = 0.0
        self.lock = threading.Lock()

        for i in range(0, self.size):
            self.chromosoms.append(list())
            self.chromosoms_new.append(list())

    def genarate(self):
        for i in range(0, self.size):
            for j in range(0, self.gnum):
                self.chromosoms[i].append(random.randrange(sys.maxint))
                self.chromosoms_new[i].append(random.randrange(sys.maxint))
        return self.chromosoms

    def get_total(self, fit):
        s = 0.0
        for i in range(0, self.size):
            if fit[i] >= self.cut:
                s = s + fit[i]
        return s

    def choose(self, fit, m):
        ind = 0
        ft = self.get_total(fit)
        rd = random.randrange(0, 100)
        count = 0.0
        for i in range(0, self.size):
            f = fit[i]
            if f >= self.cut - m:
                f = (f / ft) * 100.0
                count = count + f
                if count >= rd:
                    ind = i
                    break

        if ind <= 0:
            ind = 0
        return ind

    def mutate(self, i1):

        for i in range(0, self.gnum):
            if random.randrange(0, 100) < self.mutation_rate:
                shift = random.randrange(-1 * sys.maxint, sys.maxint)
                self.chromosoms_new[i1][i] = self.chromosoms_new[i1][i] + shift

    def cross_over(self, i1, i2, i):

        if random.randrange(0, 100) < self.crossover_rate:
            cross_point1 = random.randrange(0, self.gnum)
            cross_point2 = random.randrange(cross_point1, self.gnum)
            for j in range(0, cross_point1):
                self.chromosoms_new[i][j] = self.chromosoms[i1][j]
                self.chromosoms_new[i + 1][j] = self.chromosoms[i2][j]
            for j in range(cross_point1, cross_point2):
                self.chromosoms_new[i][j] = self.chromosoms[i2][j]
                self.chromosoms_new[i + 1][j] = self.chromosoms[i1][j]
            for j in range(cross_point1, self.gnum):
                self.chromosoms_new[i][j] = self.chromosoms[i1][j]
                self.chromosoms_new[i + 1][j] = self.chromosoms[i2][j]
        else:
            for j in range(0, self.gnum):
                self.chromosoms_new[i] = self.chromosoms[i1]
                self.chromosoms_new[i + 1] = self.chromosoms[i2]

    def copy(self, new, old):
        for i in range(0, self.gnum):
            self.chromosoms_new[new][i] = self.chromosoms[old][i]

    def copy2(self, new, old):
        for i in range(0, self.gnum):
            self.chromosoms[old][i] = self.chromosoms_new[new][i]

    def new_gen(self, fit):
        i = 0

        self.fitness = fit
        self.cal_b_fit(fit)

        self.copy(0, 0)
        self.copy(1, 1)

        max1 = -1.0
        max2 = -1.0
        i1 = 0
        i2 = 1

        for i in range(i, self.size):
            if max1 < fit[i]:
                max1 = fit[i]
                i1 = i
        for i in range(i, self.size):
            if max1 > fit[i] and max2 < fit[i]:
                max2 = fit[i]
                i2 = i

        self.copy(0, i1)
        self.copy(1, i2)

        newfit = sorted(fit)
        ind = 3 * self.size / 4
        self.cut = newfit[ind]
        i = 2

        self.thread_count = 0
        while i < self.size:
            thread.start_new_thread(self.operation, (fit, i))
            i += 2

        while self.thread_count < (i - 2) / 2:
            pass

        for l in range(0, self.size):
            self.copy2(l, l)
        return self.chromosoms

    def cal_b_fit(self, fit):
        mx = -1.0
        for i in range(0, self.size):
            if mx < fit[i]:
                mx = fit[i]
                self.b_fit = i

        return self.b_fit

    def cal_w_fit(self, fit):
        mn = 1000
        for i in range(0, self.size):
            if mn > fit[i]:
                mn = fit[i]
            self.w_fit = i

    def cal_avg_fit(self, fit):
        self.fitness = fit
        self.avg_fit = self.get_total(fit) / self.size
        return self.avg_fit

    def operation(self, fit, i):

        nfit = fit[:]
        i1 = self.choose(nfit, 0.0)
        i2 = i1
        tmp = nfit[i1]
        nfit[i1] = 0.0
        for j in range(0, self.size):
            i2 = self.choose(nfit, tmp)
            if i1 != i2:
                break

        if i1 == i2:
            i2 = (i1 + 1) % self.size

        self.cross_over(i1, i2, i)
        self.mutate(i)
        self.mutate(i + 1)
        self.lock.acquire()
        self.thread_count = self.thread_count + 1
        self.lock.release()
