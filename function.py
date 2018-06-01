#!/usr/bin/env python
# coding=utf-8
import numpy as np
import matplotlib.pylab as plt
import matplotlib.image as mpimg
import cv2


class Function:
    def __init__(self):
        # float32
        self.current_image = None
        self.base_image = None
        self.__undo_stack = []
        self.__redo_stack = []

    def open(self, file_path):
        image = mpimg.imread(file_path)
        self.base_image = image
        self.current_image = image
        return image

    def undo(self):
        if len(self.__undo_stack) == 0:
            return
        self.current_image = self.__undo_stack[-1]
        self.__undo_stack.remove(self.current_image)
        return self.current_image

    def redo(self):
        if len(self.__redo_stack) == 0:
            return None
        self.current_image = self.__redo_stack[-1]
        self.__redo_stack.remove(self.current_image)
        return self.current_image

    def rollback(self):
        self.current_image = self.base_image

    def checkpoint(self):
        self.__undo_stack.append(self.base_image)
        self.base_image = self.current_image

    def motion_blur(self, length, theta):
        # theta = np.pi/4
        # len = 40
        row = int(np.floor(length*np.sin(theta*np.pi))+1)
        col = int(np.floor(length*np.cos(theta*np.pi))+1)
        motion = np.zeros(shape=(row, col))
        K = np.tan(theta)
        center_x = col/2
        center_y = row/2

        for i in range(0, row):
            for j in range(0, col):
                x = j-center_x
                y = center_y-i
                dis = abs(K*x-y)/np.sqrt(K*K+1)
                motion[i][j] = max(1-dis, 0)
        motion = motion/np.sum(motion)
        img = cv2.filter2D(self.base_image, -1, motion)
        self.current_image = img


def test_motion_blur():
    func = Function()
    func.open("2.jpg")
    func.motion_blur()
    plt.imshow(func.current_image)
    plt.show()


if __name__ == '__main__':
    test_motion_blur()
