# coding=utf-8
# !/usr/bin/env python
import numpy as np
import numpy.matlib
import time
import matplotlib.pylab as plt
import matplotlib.image as mpimg
from scipy import ndimage

import cv2
import math
import random


class Function:
    def __init__(self):
        # float32
        self.current_image = None
        self.base_image = None
        self.__undo_stack = []
        self.__redo_stack = []
        self.current_image_path = None

    def save(self, path=None):
        if not path:
            path = self.current_image_path
        cv2.imwrite(path, self.base_image)

    def open(self, file_path):
        image = mpimg.imread(file_path)
        self.base_image = image
        self.current_image = image
        self.current_image_path = file_path
        return image

    def undo(self):
        if len(self.__undo_stack) == 0:
            return
        self.__redo_stack.append(self.base_image)
        self.current_image = self.__undo_stack[-1]
        self.base_image = self.current_image
        self.__undo_stack.remove(self.current_image)
        return self.current_image

    def redo(self):
        if len(self.__redo_stack) == 0:
            return None
        self.__undo_stack.append(self.base_image)
        self.current_image = self.__redo_stack[-1]
        self.base_image = self.current_image
        self.__redo_stack.remove(self.current_image)
        return self.current_image

    def rollback(self):
        self.current_image = self.base_image

    def checkpoint(self):
        self.__undo_stack.append(self.base_image)
        self.base_image = self.current_image

    def median_blur(self, sz):
        """
        中值滤波
        """
        img_out = self.base_image.copy()
        img_out = ndimage.median_filter(img_out, size=sz)
        self.current_image = img_out

    def gaussian_blur(self, sigma):
        """
        高斯滤波
        """
        img_out = self.base_image.copy()
        img_out = ndimage.gaussian_filter(img_out, sigma=sigma)
        self.current_image = img_out

    def average_blur(self, sz):
        """
        均值滤波
        """
        img_out = self.base_image.copy()
        img_out = ndimage.uniform_filter(img_out, size=sz)
        self.current_image = img_out

    def radial_blur(self):
        """
        径向模糊
        """
        img_out = self.base_image.copy()
        img = self.base_image.astype(float)
        row, col, channel = self.base_image.shape
        xx = np.arange(col)
        yy = np.arange(row)
        x_mask = numpy.matlib.repmat(xx, row, 1)  # xx重复row次
        y_mask = numpy.matlib.repmat(yy, col, 1)  # yy重复col次
        y_mask = np.transpose(y_mask)
        center_y = (row - 1) / 2.0
        center_x = (col - 1) / 2.0
        r = np.sqrt((x_mask - center_x) ** 2 +
                    (y_mask - center_y) ** 2)  # 到中心的距离
        angle = np.arctan2(y_mask - center_y, x_mask - center_x)  # 到中心的角度
        num = 30
        arr = np.arange(num)
        part_1_time = 0
        part_2_time = 0
        for i in range(row):
            for j in range(col):
                t1 = time.time()
                r_arr = r[i, j] - arr
                r_arr[r_arr < 0] = 0
                new_x = r_arr * np.cos(angle[i, j]) + center_x
                new_y = r_arr * np.sin(angle[i, j]) + center_y
                int_x = new_x.astype(int)
                int_y = new_y.astype(int)
                int_x[int_x > col - 1] = col - 1
                int_x[int_x < 0] = 0
                int_y[int_y > row - 1] = row - 1
                int_y[int_y < 0] = 0
                part_1_time += (time.time() - t1)

                t1 = time.time()
                img_out[i, j, 0] = img[int_y, int_x, 0].mean()
                img_out[i, j, 1] = img[int_y, int_x, 1].mean()
                img_out[i, j, 2] = img[int_y, int_x, 2].mean()
                part_2_time += (time.time() - t1)
        print(part_1_time)
        print(part_2_time)
        self.current_image = img_out

    def surface_blur(self, r, threshold):
        """
        表面模糊
        """
        img_out = self.current_image.copy()

        def channel_surface_blur(img, radi, thre):
            """
            对单通道做表面模糊
            """
            w, h = img.shape
            img_out_out = img.copy()
            for i in range(radi, w - radi):
                for j in range(radi, h - radi):
                    patch = img_out_out[i - radi:i +
                                                 radi + 1, j - radi:j + radi + 1:]
                    p0 = img_out_out[i, j]
                    mask1 = np.tile(p0, [2 * radi + 1, 2 * radi + 1])
                    mask2 = 1 - np.abs(patch - mask1) / (2.5 * thre)
                    mask3 = np.max(mask2, 0)
                    img_out_out[i, j] = np.sum(
                        np.sum(patch * mask3)) / np.sum(mask3)
            return img_out_out

        img_out[:, :, 0] = channel_surface_blur(
            img_out[:, :, 0], r, threshold)
        img_out[:, :, 1] = channel_surface_blur(
            img_out[:, :, 1], r, threshold)
        img_out[:, :, 2] = channel_surface_blur(
            img_out[:, :, 2], r, threshold)
        self.current_image = img_out

    def wave(self, degree):
        """
        波浪扭曲
        :param degree:
        :return:
        """
        alpha = 70.0
        beta = 30.0
        img = self.base_image.astype(float)
        img_out = self.base_image.copy()
        row, col, shape = img_out.shape
        center_x = (col - 1) / 2
        center_y = (row - 1) / 2
        xx = np.arange(col)
        yy = np.arange(row)
        x_mask = np.matlib.repmat(xx, row, 1)
        y_mask = np.matlib.repmat(yy, col, 1)
        y_mask = np.transpose(y_mask)
        xx_dif = x_mask - center_x
        yy_dif = center_y - y_mask

        x = degree * np.sin(2 * math.pi * yy_dif / alpha) + xx_dif
        y = degree * np.cos(2 * math.pi * xx_dif / beta) + yy_dif

        x_new = x + center_x
        y_new = center_y - y

        int_x = np.floor(x_new)
        int_x = int_x.astype(int)
        int_y = np.floor(y_new)
        int_y = int_y.astype(int)

        for ii in range(row):
            for jj in range(col):
                new_xx = int_x[ii, jj]
                new_yy = int_y[ii, jj]

                if x_new[ii, jj] < 0 or x_new[ii, jj] > col - 1:
                    continue
                if y_new[ii, jj] < 0 or y_new[ii, jj] > row - 1:
                    continue

                img_out[ii, jj, :] = img[new_yy, new_xx, :]
        self.current_image = img_out

    def guided_filter(self, r, eps):
        """
        导向滤波
        """

        def average(i):
            return ndimage.uniform_filter(i, size=r)

        def channel_guided_filter(p, r, eps):
            I = p.copy()
            r = 2 * r + 1
            mean_I = average(I)
            mean_p = average(p)
            mean_ip = average(I * p)
            conv_ip = mean_ip - mean_I * mean_p
            mean_II = average(I * I)
            var_I = mean_II - mean_I * mean_I
            a = conv_ip / (var_I + eps)
            b = mean_p - a * mean_I
            mean_a = average(a)
            mean_b = average(b)
            q = mean_a * I + mean_b
            return q

        img_out[:, :, 0] = channel_guided_filter(img_out[:, :, 0], r, eps)
        img_out[:, :, 1] = channel_guided_filter(img_out[:, :, 1], r, eps)
        img_out[:, :, 2] = channel_guided_filter(img_out[:, :, 2], r, eps)
        self.current_image = img_out

    def motion_blur(self, length, theta):
        """
        运动模糊
        """
        # theta = np.pi/4
        # len = 40
        theta = np.pi / 200 * theta
        row = int(np.floor(length * np.sin(theta)) + 1)
        col = int(np.floor(length * np.cos(theta)) + 1)
        motion = np.zeros(shape=(row, col))
        K = np.tan(theta)
        center_x = col / 2
        center_y = row / 2

        for i in range(0, row):
            for j in range(0, col):
                x = j - center_x
                y = center_y - i
                dis = abs(K * x - y) / np.sqrt(K * K + 1)
                motion[i][j] = max(1 - dis, 0)
        motion = motion / np.sum(motion)
        img = cv2.filter2D(self.base_image, -1, motion)
        self.current_image = img

    def high_pass(self, half):
        """
        高反差保留
        :param half:
        :return:
        """
        half /= 10.0
        img_out = self.base_image.copy()
        f_size = 2 * half + 1
        img_filter = ndimage.gaussian_filter(img_out, sigma=int(f_size))
        img_diff = img_out - img_filter
        img_out = (img_diff + 128)
        self.current_image = img_out

    def lighten_edge(self, alpha):
        """
        照亮边缘
        :param alpha:
        :return:
        """
        alpha = alpha / 100.0
        img_out = self.base_image.copy()
        r = img_out[:, :, 0]
        g = img_out[:, :, 1]
        b = img_out[:, :, 2]

        def find_gradient(c):
            gy = np.array([[-1, -3, -1], [0, 0, 0], [1, 3, 1]])
            gx = np.array([[-1, 0, 1], [-3, 0, 3], [-1, 0, 1]])
            iy = cv2.filter2D(c, -1, gy)
            ix = cv2.filter2D(c, -1, gx)
            return np.abs(ix) * alpha + np.abs(iy) * (1 - alpha)

        img_out[:, :, 0] = find_gradient(r)
        img_out[:, :, 1] = find_gradient(g)
        img_out[:, :, 2] = find_gradient(b)
        self.current_image = img_out

    def blur_glass(self, fine):
        """
        模糊玻璃
        :return:
        """
        img = self.base_image
        img_out = ndimage.gaussian_filter(img, sigma=2)
        rows, cols, depth = img_out.shape
        for i in range(fine, rows - fine):
            for j in range(fine, cols - fine):
                k1 = random.random() - 0.5
                k2 = random.random() - 0.5
                m = int(k1 * (2 * fine - 1))
                n = int(k2 * (2 * fine - 1))
                h = (i + m) % rows
                w = (j + n) % cols
                img_out[i, j, :] = img[h, w, :]
        self.current_image = img_out


def t_wave(func):
    func.blur_glass(0.01, 5)
    plt.imshow(func.current_image)
    plt.show()


if __name__ == '__main__':
    func = Function()
    func.open("5.jpg")
    # test_radial_blur(func)
    # test_motion_blur(func)
    t_wave(func)
