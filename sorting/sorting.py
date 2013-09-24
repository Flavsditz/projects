#!/usr/bin/python

############################
#
#  Author: Flavio Diez
# Version: 0.1
#
#    Info: This program implements different sorting algorithms in order to test the times of sorting of each implementation.
#          Each function returns its run time.
#
############################

import sys
import time
import random

def quickSort(lis):
    """Quicksort is a divide and conquer algorithm that divides a large list into two smaller sub-lists. These lists are recursively sorted by the algorithm.

    :param lis: A list of unordered values that the algorithm has to sort.
    :type lis: list of floats.
    :returns:  list -- organized list.
    
    This version is implemented with the pivot element beeing the middle element of the array

    """

    if len(lis) <= 1:
        return lis

    #Select pivot element
    pivot = lis.pop(len(lis)/2)

    less = []
    greater = []

    for x in lis:
        if x <= pivot:
            less.append(less)
        else:
            greater.append
    return quickSort(less) + [pivot] + quickSort(greater)

def mergeSort():
    pass

def inplaceMergeSort():
    pass

def heapSort():
    pass

def insertionSort():
    pass

def introSort():
    pass

def selectionSort():
    pass

def timSort():
    pass

def shellSort():
    pass

def bubbleSort():
    pass

def binaryTreeSort():
    pass

def cycleSort():
    pass

def librarySort():
    pass

def patienceSort():
    pass

def smoothSort():
    pass

def strandSort():
    pass

def tournamentSort():
    pass

def cocktailSort():
    pass

def combSort():
    pass

def gnomeSort():
    pass

def main(size):
    l = []
    for i in range(size):
        l.append(random.random())

    # Quicksort Algorithm
    toc = time.time()
    quickSort(l)
    tic = time.time()
    print 'Quicksort - ' + str(tic - toc)

if __name__=="__main__":
    main(int(sys.argv[1]))
