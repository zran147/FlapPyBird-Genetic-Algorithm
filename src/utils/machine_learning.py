from itertools import cycle
import random
import sys

import pygame
from pygame.locals import *

import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import SGD
import os

total_models = 10
SCREENWIDTH  = 288.0
SCREENHEIGHT = 512.0

def save_pool():  # Fungsi untuk menyimpan bobot dari setiap model di dalam pool saat ini.
    for xi in range(total_models):  # Melakukan iterasi untuk setiap model di dalam pool.
        current_pool[xi].save_weights("Current_Model_Pool/model_new" + str(xi) + ".weights.h5")  # Menyimpan bobot dari model saat ini.
    print("Saved current pool!")  # Mencetak pesan yang menunjukkan bahwa pool saat ini telah disimpan.

def model_crossover(model_idx1, model_idx2):  # Fungsi untuk melakukan persilangan antara dua model.
    global current_pool  # Mendeklarasikan penggunaan variabel global 'current_pool'.
    weights1 = current_pool[model_idx1].get_weights()  # Mengambil bobot dari model pertama.
    weights2 = current_pool[model_idx2].get_weights()  # Mengambil bobot dari model kedua.
    weightsnew1 = weights1  # Membuat salinan bobot dari model pertama.
    weightsnew2 = weights2  # Membuat salinan bobot dari model kedua.
    weightsnew1[0] = weights2[0]  # Melakukan persilangan dengan menukar bobot lapisan pertama antara dua model.
    weightsnew2[0] = weights1[0]  # Melakukan persilangan dengan menukar bobot lapisan pertama antara dua model.
    print(weightsnew1)  # Mencetak bobot yang telah dimodifikasi dari model pertama setelah persilangan.
    print(weightsnew2)  # Mencetak bobot yang telah dimodifikasi dari model kedua setelah persilangan.
    return weightsnew1, weightsnew2  # Mengembalikan bobot yang telah dimodifikasi dari kedua model setelah persilangan.


def model_mutate(weights):  # Fungsi untuk melakukan mutasi pada bobot suatu model.
    for xi in range(len(weights)):  # Melakukan iterasi pada setiap lapisan dalam model.
        for yi in range(len(weights[xi])):  # Melakukan iterasi pada setiap bobot dalam lapisan.
            if random.uniform(0, 1) > 0.85:  # Memeriksa apakah bobot akan dimutasi berdasarkan probabilitas.
                change = random.uniform(-0.5,0.5)  # Menghasilkan nilai acak untuk perubahan bobot.
                weights[xi][yi] += change  # Melakukan mutasi pada bobot.
    return weights  # Mengembalikan bobot yang telah dimutasi.

def predict_action(height, dist, pipe_height, model_num):  # Fungsi untuk memprediksi tindakan berdasarkan input dan model yang diberikan.
    global current_pool  # Mendeklarasikan penggunaan variabel global 'current_pool'.
    # Tinggi, jarak, dan tinggi pipa harus dalam rentang 0 hingga 1 (Dikalaan oleh SCREENHEIGHT)
    height = min(SCREENHEIGHT, height) / SCREENHEIGHT - 0.5  # Skala tinggi ke dalam rentang -0.5 hingga 0.5.
    dist = dist / 450 - 0.5  # Skala jarak ke dalam rentang -0.5 hingga 0.5, maksimal jarak pipa dari pemain adalah 450.
    pipe_height = min(SCREENHEIGHT, pipe_height) / SCREENHEIGHT - 0.5  # Skala tinggi pipa ke dalam rentang -0.5 hingga 0.5.
    neural_input = np.asarray([height, dist, pipe_height])  # Membentuk input neural network sebagai array NumPy.
    neural_input = np.atleast_2d(neural_input)  # Memastikan input memiliki setidaknya 2 dimensi.
    output_prob = current_pool[model_num].predict(neural_input, 1, verbose=0)[0]  # Melakukan prediksi menggunakan model yang diberikan.
    if output_prob[0] <= 0.5:  # Jika probabilitas output kurang dari atau sama dengan 0.5.
        # Melakukan tindakan melompat
        return 1
    return 2