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
                rtn.append(float(tokens[len(tokens) - 2]))
    return rtn

PATTERN = [ "/" , "\\" ,"o", "*", "O", "x", ".", '-', "|" , "+"]
base_dir = '/mininet/src/result/1mbps/'
data_dirs = [base_dir + 'norm/',
             base_dir + 'scheduling_queue_8_for_h1/']



base_mean = []
base_err = []

# return values will be filled into rtn_mean, rtn_std
def get_results(key_word):
    for i in range(len(data_dirs)):
        overall_arr = get_overall_arr(key_word, data_dirs[i])
        stdmean_stderr = CI.get_conf_int(overall_arr)
        base_mean.append(int(stdmean_stderr[0] / 100) / 10.0)
        base_err.append(int(stdmean_stderr[1] / 100) / 10.0)

N = 4
ind = np.arange(N)    # the x locations for the groups
width = 0.22      # the width of the bars

### plotting now
# this clears the current figure

plt.clf()
plt.figure(None, figsize=(8,5), dpi = 300)

ind = ind + 0.3

final_base = []
final_base_err = []
final_comp = []
final_comp_err = []

for i in reversed(range(4)):
    base_mean = []
    base_err = []
    get_results('10.0.0.' + str(i+1))
    final_base.append(base_mean[0])
    final_base_err.append(base_err[0])
    final_comp.append(base_mean[1])
    final_comp_err.append(base_err[1])


p0 = plt.bar(ind + width * 0,  final_base, width, color='w',
             yerr=final_base_err, ecolor='b',
             edgecolor='black', hatch=PATTERN[0])

p1 = plt.bar(ind + width * 1,  final_comp,width, color='r',
             yerr=final_comp_err, ecolor='b',
             edgecolor='black', hatch=PATTERN[1])


# this line sets the x axis max value
# plt.xlim(xmax=3.3)
# plt.xlim(xmax=1.95)
plt.ylim(ymax=240)
plt.ylabel('Sub-query completion time in seconds')
plt.xlabel('Server hosts')
plt.xticks(ind+width, ('h4', 'h3', 'h2', 'h1') )
# plt.yticks(np.arange(0,46,5))
plt.legend((p0[0], p1[0]),
           ('Without Scheduling',
            'With Scheduling'))
           # loc = 'upper left', prop={'size':12},
           # ncol is # of columns for the legend
           # ncol=2)
saver.save(plt, 'plots/simple_topo_closer_8')
