#! /usr/bin/env python3

import numpy as np
import pandas as pd


def rough(hist):
    '''Determine the roughness of a histogram by calculating the 2nd order forward finite diff'''

    widths = np.diff(hist[1])
    cd = (widths[:-1]+widths[1:])/2
    cd2 = cd[:-1]+cd[1:]
    # f = np.log(hist[0]+1e-15)
    f = hist[0]
    fdp = (f[2:]-2*f[1:-1]+f[:-2])/(cd[:-1]*cd[1:])
    # fdp = (f[2:]-2*f[1:-1]+f[:-2])/(widths[:-2]*widths[2:])
    rough = np.sum(fdp**2*cd2)
    return rough


def err_nn(input_data, hist):
    cd = (hist[1][:-1]+hist[1][1:])/2
    counts = hist[0]
    nn_data = [[c]*int(n) for c, n in zip(cd, counts)]
    nn_data = [item for sublist in nn_data for item in sublist]
    # print(list(zip(np.asarray(nn_data), np.sort(input_data))))
    return np.sum(np.abs(np.asarray(nn_data)-np.sort(input_data)))


def err_li(input_data, hist):
    counts = hist[0]
    nn_data = []
    for i in range(len(hist[1])-1):
        if counts[i] == 1:
            nn_data.append(np.asarray([(hist[1][i]+hist[1][i+1])/2]))
        else:
            nn_data.append(np.linspace(hist[1][i], hist[1][i+1], counts[i]))
    nn_data = np.concatenate(nn_data)
    # print(list(zip(np.asarray(nn_data), np.sort(input_data))))
    return np.sum(np.abs(np.asarray(nn_data)-np.sort(input_data)))


def bep_optimizer(data):
    best_rough = np.inf
    best_bep = 0
    for nb in range(12, int(np.sqrt(len(data)))):
        _, bep = pd.qcut(data, nb, retbins=True)
        tmp_hist_ep = np.histogram(data, bins=bep)
        tmp_hist_ep_bw = tmp_hist_ep[0]/np.diff(tmp_hist_ep[1])
        tmp_rough = rough((tmp_hist_ep_bw, tmp_hist_ep[1]))
        if tmp_rough < best_rough:
            best_bep = bep
            best_rough = tmp_rough
    print(best_bep)
    return best_bep


def bb_optimizer(data):
    best_metric = np.inf
    best_p0 = 0
    p0s = [0.5, 0.4, 0.3, 0.2, 0.1, 0.05, 0.01, 0.001, 0.0001]
    for p0 in p0s:
        tmp_hist_ep = np.histogram(data, bins=bep)
        tmp_hist_ep_bw = tmp_hist_ep[0]/np.diff(tmp_hist_ep[1])
        tmp_rough = rough((tmp_hist_ep_bw, tmp_hist_ep[1]))
        if tmp_rough < best_rough:
            best_bep = bep
            best_rough = tmp_rough
    print(best_bep)
    return best_bep


def normalized(a):
    norm1 = (a - min(a))/(max(a)-min(a))
    print(norm1)
    return norm1
