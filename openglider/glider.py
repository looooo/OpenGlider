#! /usr/bin/python2
# -*- coding: utf-8; -*-
#
# (c) 2013 booya (http://booya.at)
#
# This file is part of the OpenGlider project.
#
# OpenGlider is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# OpenGlider is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with OpenGlider.  If not, see <http://www.gnu.org/licenses/>.


__author__ = 'simon'
import numpy
import copy

from openglider.Import import IMPORT_GEOMETRY, EXPORT_3D


class Glider(object):
    def __init__(self):
        self.cells = []
        self.data = {}

    def import_geometry(self, path, filetype=None):
        if not filetype:
            filetype = path.split(".")[-1]
        IMPORT_GEOMETRY[filetype](path, self)

    def export_geometry(self, path="", filetype=None):
        if not filetype:
            filetype = path.split(".")[-1]
        #EXPORT_NAMES[filetype](self, path)

    def export_3d(self, path="", filetype=None, midribs=0, numpoints=None, floatnum=6):
        if not filetype:
            filetype = path.split(".")[-1]
        EXPORT_3D[filetype](self, path, midribs, numpoints, floatnum)

    def return_ribs(self, num=0):
        if not self.cells:
            return numpy.array([])
        num += 1
        #will hold all the points
        ribs = []
        #print(len(self.cells))
        for cell in self.cells:
            for y in range(num):
                ribs.append(cell.midrib(y * 1. / num).data)
        ribs.append(self.cells[-1].midrib(1.).data)
        return ribs

    def return_polygons(self, num=0):
        if not self.cells:
            return numpy.array([]), numpy.array([])
        ribs = self.return_ribs(num)
        #points per rib
        numpoints = len(ribs[0])
        # ribs is [[point1[x,y,z],[point2[x,y,z]],[point1[x,y,z],point2[x,y,z]]]
        ribs = numpy.concatenate(ribs)
        #now ribs is flat
        polygons = []
        for i in range(len(self.cells) * num):  # without +1, because we use i+1 below
            for k in range(numpoints - 1):  # same reason as above
                polygons.append(
                    [i * numpoints + k, i * numpoints + k + 1, (i + 1) * numpoints + k + 1, (i + 1) * numpoints + k])
        return polygons, ribs

    def close_rib(self, rib=-1):
        self.ribs[rib].profile_2d *= 0.
        self.ribs[rib].recalc()

    def get_midrib(self, y=0):
        k = y % 1
        i = y - k
        if i == len(self.cells) and k == 0:  # Stabi-rib
            i -= 1
            k = 1
        return self.cells[i].midrib_basic_cell(k)

    def mirror(self, cutmidrib=True):
        if not self.cells:
            return
        if self.cells[0].rib1.pos[1] != 0 and cutmidrib:  # Cut midrib
            self.cells = self.cells[1:]
        for rib in self.ribs:
            rib.mirror()
        for cell in self.cells:
            first = cell.rib1
            cell.rib1 = cell.rib2
            cell.rib2 = first
        self.cells = self.cells[::-1]

    def recalc(self):
        for rib in self.ribs:
            rib.recalc()
        for cell in self.cells:
            cell.recalc()

    def copy(self):
        return copy.deepcopy(self)

    def _get_ribs_(self):
        if not self.cells:
            return []
        return [self.cells[0].rib1] + [cell.rib2 for cell in self.cells]

    def _get_numpoints(self):
        return self.ribs[0].profile_2d.Numpoints

    def _set_numpoints(self, numpoints):
        self.ribs[0].profile_2d.Numpoints = numpoints
        xvalues = self.ribs[0].profile_2d.XValues
        for rib in self.ribs:
            rib.profile_2d.XValues = xvalues

    ribs = property(fget=_get_ribs_)
    numpoints = property(_get_numpoints, _set_numpoints)





