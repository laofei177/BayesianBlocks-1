#! /usr/bin/env python

from __future__ import division
import numpy as np
from scipy import stats
from bayesian_blocks_modified import bayesian_blocks
from matplotlib import pyplot as plt
import cPickle as pkl
import scipy.stats as st
import cPickle as pkl
from bb_plotter import make_hist_ratio_blackhole

def do_bh_analysis():

    plt.close('all')
    normed = True
    log = True
    ST_low = 2300
    samples = 5000
    seed = 2
    p0=0.005
    data_driven = True
    signal = True
    inject = True
    if signal: signal_num = 10
    else: signal_num = 0

    df_mc = pkl.load(open('files/BHTree_mc.p','rb'))
    df_signal = pkl.load(open('files/BHTree_signal.p','rb'))
    df_data = pkl.load(open('files/BHTree_data.p','rb'))

    weights = df_mc.weightTree.unique()#[0.27436519,0.0401976,0.01657276]
    df_mc_list = []
    for weight in weights:
        df_mc_list.append(df_mc[np.isclose(df_mc.weightTree,weight)])

    all_edges = {}
    #for ST in range(2,11):
    for ST in [10]:
        my_ST_data = df_data[df_data['ST_mul'+str(ST)]>ST_low]['ST_mul'+str(ST)].values
        nentries = len(my_ST_data)
        df_mc_st_list = [df[df['ST_mul'+str(ST)]>ST_low]['ST_mul'+str(ST)] for df in df_mc_list]
        if signal:
            my_ST_signal = df_signal[df_signal['ST_mul'+str(ST)]>ST_low]['ST_mul'+str(ST)].values
        my_ST_mc = []

        samples,rel_weights = find_sample_number(df_mc_st_list,weights)
        for i,mc in enumerate(df_mc_st_list):
            my_ST_mc = np.append(my_ST_mc, mc.sample(int(samples*rel_weights[i]),random_state=seed).values)

        print 'n_data',nentries
        print 'n_mc',len(my_ST_mc)

#get the edges from bb, and the normalized bin values (integral of all hists is 1)
        normed_counts_data, bb_edges = np.histogram(my_ST_data,bayesian_blocks(my_ST_data,p0=p0), density=True)
        normed_counts_data_nobb, nobb_edges = np.histogram(my_ST_data,20, density=True)
        normed_counts_mc, _= np.histogram(my_ST_mc,bb_edges, density=True)
        normed_counts_mc_nobb, _= np.histogram(my_ST_mc,nobb_edges, density=True)
        if signal:
            normed_counts_signal, _= np.histogram(my_ST_signal,bb_edges, density=True)
            normed_counts_signal_nobb, _= np.histogram(my_ST_signal,nobb_edges, density=True)

#rescale the values so that the integral of the data hist is = num of entries
        rescaled_counts_data = normed_counts_data*nentries
        rescaled_counts_data_nobb = normed_counts_data_nobb*nentries
        rescaled_counts_mc = normed_counts_mc*(nentries-signal_num)
        rescaled_counts_mc_nobb = normed_counts_mc_nobb*(nentries-signal_num)
        if signal:
            rescaled_counts_signal = normed_counts_signal*signal_num
            rescaled_counts_signal_nobb = normed_counts_signal_nobb*signal_num

#properly calculate the error bars on the data
        counts_data, _= np.histogram(my_ST_data,bb_edges)
        counts_data_nobb, _= np.histogram(my_ST_data,nobb_edges)
        rescaled_err = np.sqrt(counts_data)/(bb_edges[1:]-bb_edges[:-1])
        rescaled_err_nobb = np.sqrt(counts_data_nobb)/(nobb_edges[1:]-nobb_edges[:-1])
        err = np.sqrt(counts_data)

        make_hist_ratio_blackhole(bb_edges, rescaled_counts_data, rescaled_counts_mc, rescaled_err, str(ST), suffix = None, data_driven=data_driven, signal = rescaled_counts_signal, inject = inject)
        make_hist_ratio_blackhole(nobb_edges, rescaled_counts_data_nobb, rescaled_counts_mc_nobb, rescaled_err_nobb, str(ST), suffix = 'nobb', data_driven=data_driven, signal = rescaled_counts_signal_nobb, inject = inject)

        plt.show()

        all_edges[ST]=bb_edges

    for key in all_edges:
        print 'ST'+str(key), all_edges[key]
    return all_edges


def find_sample_number(df_list,weights):
    props = [len(df_list[i])*weights[i] for i in range(len(df_list))]
    props = [i/min(props) for i in props]
    props = [i/sum(props) for i in props]
    for sample in range(min(map(len,df_list)), max(map(len,df_list))):
        for j in range(len(props)):
            if int(sample*props[j])>len(df_list[j]):
                return (sample-1,props)
    return (sample, props)

if __name__ =="__main__":
    do_bh_analysis()

