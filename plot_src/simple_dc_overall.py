#!/usr/bin/env python
# a stacked bar plot with errorbars
import sys
import numpy as np
import matplotlib.pyplot as plt
import re
from os.path import expanduser
import confidence_interval_calculator as CI
import save_fig as saver


def get_overall_arr(key_word, data_dir):
    rtn = []
    for i in range(1,6):
        data = open(data_dir + 'client_' + (str(i)) + '.out' , "r")
        for line in data:
            if(re.search(key_word, line)):
                tokens = line.split(" ")
                rtn.append(float(tokens[len(tokens) - 3]))
    return rtn

PATTERN = [ "/" , "\\" ,"o", "*", "O", "x", ".", '-', "|" , "+"]
base_dir = '/mininet/src/result/1mbps/'
data_dirs = [base_dir + 'norm/',
             base_dir + 'scheduling_queue_5_for_h1/',
             base_dir + 'scheduling_queue_6_for_h1/',
             base_dir + 'scheduling_queue_7_for_h1/',
             base_dir + 'scheduling_queue_8_for_h1/',
             base_dir + 'scheduling_queue_9_for_h1/',
             base_dir + 'scheduling_queue_10_for_h1/']


rtn_mean = []
rtn_std = []

# return values will be filled into rtn_mean, rtn_std
def get_results():
    for i in range(len(data_dirs)):
        overall_arr = get_overall_arr('Total time', data_dirs[i])
        stdmean_stderr = CI.get_conf_int(overall_arr)
        rtn_mean.append(int(stdmean_stderr[0] / 100) / 10.0)
        rtn_std.append(int(stdmean_stderr[1] / 100) / 10.0)



get_results()
print rtn_mean

base_mean = [rtn_mean[0], rtn_mean[0], rtn_mean[0], rtn_mean[0], rtn_mean[0], rtn_mean[0]]
base_err = [rtn_std[0], rtn_std[0], rtn_std[0], rtn_std[0], rtn_std[0], rtn_std[0]]
compare_mean = rtn_mean[1:]
compare_err = rtn_std[1:]

N = 6
ind = np.arange(N)    # the x locations for the groups
width = 0.22      # the width of the bars

### plotting now
# this clears the current figure

plt.clf()
plt.figure(None, figsize=(8,5), dpi = 300)

ind = ind + 0.3

p0 = plt.bar(ind + width * 0,  base_mean, width, color='r',
             yerr=base_err, ecolor='b',
             edgecolor='black', hatch=PATTERN[0])


p1 = plt.bar(ind + width * 1,  compare_mean,width, color='y',
             yerr=compare_err, ecolor='b',
             edgecolor='black', hatch=PATTERN[1])





# this line sets the x axis max value
# plt.xlim(xmax=3.3)
# plt.xlim(xmax=1.95)
plt.ylim(ymax=240)
plt.ylabel('Query completion time in seconds')
plt.xlabel('Minimum bandwidth guarantee for the largest flow in Mbps')
plt.xticks(ind+width, ('0.5', '0.6', '0.7', '0.8', '0.9', '1.0') )
# plt.yticks(np.arange(0,46,5))
plt.legend((p0[0], p1[0]),
           ('Without Scheduling',
            'With Scheduling'))
           # loc = 'upper left', prop={'size':12},
           # ncol is # of columns for the legend
           # ncol=2)
saver.save(plt, 'plots/simple_topo_overall')
