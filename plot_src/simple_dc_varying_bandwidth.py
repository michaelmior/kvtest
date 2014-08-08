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
base_dir = '/mininet/src/result/various_link_bandwidth/'
data_dirs = [base_dir + '0_8mbps/',
             base_dir + '0_9mbps/',
             base_dir + '1_0mbps/',
             base_dir + '1_1mbps/',
             base_dir + '1_2mbps/'
         ]


base_mean = []
base_err = []

# return values will be filled into rtn_mean, rtn_std
def get_results(key_word):
    for i in range(len(data_dirs)):
        overall_arr = get_overall_arr(key_word, data_dirs[i])
        stdmean_stderr = CI.get_conf_int(overall_arr)
        base_mean.append(int(stdmean_stderr[0] / 100) / 10.0)
        base_err.append(int(stdmean_stderr[1] / 100) / 10.0)


get_results('Total time')

comp_mean = []
comp_err = []

base_dir = '/mininet/src/result/various_link_bandwidth_scheduling/'
data_dirs = [base_dir + '0_8mbps/',
             base_dir + '0_9mbps/',
             base_dir + '1_0mbps/',
             base_dir + '1_1mbps/',
             base_dir + '1_2mbps/'
         ]
# return values will be filled into rtn_mean, rtn_std
def get_results_new(key_word):
    for i in range(len(data_dirs)):
        overall_arr = get_overall_arr(key_word, data_dirs[i])
        stdmean_stderr = CI.get_conf_int(overall_arr)
        comp_mean.append(int(stdmean_stderr[0] / 100) / 10.0)
        comp_err.append(int(stdmean_stderr[1] / 100) / 10.0)

get_results_new('Total time')


### plotting now
# this clears the current figure

plt.clf()
plt.figure(None, figsize=(8,5), dpi = 300)

print(base_mean)
print(base_err)
print(comp_mean)

base = plt.plot(range(5), base_mean, marker='o', color='r', linestyle='--', label='Without scheduling')
plt.errorbar(range(5), base_mean, yerr = base_err, zorder=2, fmt='ko', color ='r')
comp_line = plt.plot(range(5), comp_mean, marker='o', color='b', linestyle='-', label='With scheduling')
# check out what fmt & zorder means && xcuiTODO
plt.errorbar(range(5), comp_mean, yerr = comp_err, zorder=2, fmt='ko', color = 'b')

# this line sets the x axis max value
# plt.xlim(xmax=3.3)
# plt.xlim(xmax=1.95)
plt.xlim(xmin=-0.5)
plt.xlim(xmax=4.5)
plt.ylim(ymin=0)
plt.ylabel('Query completion time in seconds')
plt.xlabel('Link capacity in Mbps')
plt.xticks((0,1,2,3,4), ('0.8', '0.9', '1.0', '1.1', '1.2') )
plt.legend(loc='upper right')
# plt.legend([base, comp_line], ['Without Scheduling', 'With Scheduling'])

# plt.yticks(np.arange(0,46,5))
# plt.legend((p0[0], p1[0]),
           # ('Without Scheduling',
            # 'With Scheduling'))
           # loc = 'upper left', prop={'size':12},
           # ncol is # of columns for the legend
           # ncol=2)
saver.save(plt, 'plots/simple_topo_varying_bd')
