#!/usr/bin/env python
# coding=utf-8
import numpy as np
import matplotlib.pylab as plt
import matplotlib.image as mpimg


class Function:
    def __init__(self):
        self.__undo_stack = []
        self.__redo_stack = []

    def open(self, file_path):
        image = mpimg.imread(file_path)
        return image

    def undo(self):
        if len(self.__undo_stack) == 0:
            return

    def redo(self):
        if len(self.__redo_stack) == 0:
            return
