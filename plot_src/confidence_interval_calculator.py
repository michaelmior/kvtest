#!/usr/bin/python -B

import sys
import math

# for MicroFuge the default T_TEST Value is set to the following
# df ==4 & 95% confidence interval
T_TEST = 2.776

# for now, suppose there is no missing value
# TODO Add missing value support like my java implementation
# return an array of size two
# the first value is the mean, the second value is the stderr
def get_conf_int(array, debug = False):
    rtn = []
    sum = 0.0
    for i in range(len(array)):
        sum += float(array[i])
    std_mean = sum / len(array)
    rtn.append(std_mean)
    std_derivation = 0.0
    for i in range(len(array)):
        std_derivation += ((std_mean - float(array[i])) * (std_mean - float(array[i])))
    std_derivation /= (len(array) - 1)
    std_derivation = math.sqrt(std_derivation)
    std_derivation = T_TEST * (std_derivation / math.sqrt(len(array)))
    rtn.append(std_derivation)
    return rtn

# for now, mannually verified with confident interval I wrote in java
def xcui_test():
    a=[45,55,67,45,68,79,98,87,84,82]
    rtn = get_conf_int(a)
    print rtn
