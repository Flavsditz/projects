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
            less.append(x)
        else:
            greater.append(x)
     
    return quickSort(less) + [pivot] + quickSort(greater)

def mergeSort(lis):
    """Mergesort is a algorithm which divides recursively a list until it is of length 1. Then it comes back the recursion stack by taking every two lists and organizing them into one. This is done until the list becomes whole again but in the right order.

    :param lis: A list of unordered values that the algorithm has to sort.
    :type lis: list of floats.
    :returns:  list -- organized list.

    """
    left = []
    right = []
    
    # Recursively break the list
    if len(lis) <= 1:
        return lis
    else:
        left = mergeSort(lis[:len(lis)/2])
        right = mergeSort(lis[len(lis)/2:])

    print "Left -"+str(left)
    print "Right -"+str(right)

    #Start to organize the list:
    ans = []
    i = j = 0
    while i < len(left) and j < len(right):
        # Add to final list
        if left[i] < right[j]:
            ans.append(left.pop(0))
            i += 1
        else:
            ans.append(right.pop(0))
            j += 1

    return ans

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
    randList = []
    for i in range(size):
        randList.append(random.randint(1,100))

    # Print array
    print "List:  "+str(randList)
    print '\n'

    # Quicksort Algorithm
    print "Quicksort Algorithm\n-------------------"
    l = randList[:]
    toc = time.time()
    print quickSort(l)
    tic = time.time()
    print 'Time - ' + str(tic - toc)

    print '\n\n'
    
    # Mergesort Algorithm
    print "Mergesort Algorithm\n-------------------"
    l = randList[:]
    toc = time.time()
    print mergeSort(l)
    tic = time.time()
    print 'Time - ' + str(tic - toc)

if __name__=="__main__":
    main(int(sys.argv[1]))
