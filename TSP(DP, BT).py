#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 17 11:36:40 2021

@author: xuan
"""
import random

def Graph(n):
    matrix = [([0] * n) for i in range(n)] 
    for i in range(n):
        for j in range(n):
            if i == j:
                matrix[i][j] = 0
            else:
                matrix[i][j] = random.randrange(1, 30)
    return matrix

#dynamic programming
import copy
def TSP_DP(matrix, n):
    g = {}
    p = []

    for x in range(1, n):
        g[x + 1, ()] = matrix[x][0]

    weight = get_minimum(1, (range(2, n + 1)), g, p)

    return weight


def get_minimum(k, a, g, p):
    if (k, a) in g:
        # Already calculated Set g[%d, (%s)]=%d' % (k, str(a), g[k, a]))
        return g[k, a]

    values = []
    all_min = []
    for j in a:
        set_a = copy.deepcopy(list(a))
        set_a.remove(j)
        all_min.append([j, tuple(set_a)])
        result = get_minimum(j, tuple(set_a), g, p)
        values.append(matrix[k - 1][j - 1] + result)

    # get minimun value from set as optimal solution for
    g[k, a] = min(values)
    p.append(((k, a), all_min[values.index(g[k, a])]))

    return g[k, a]

#Backtracing
#https://www.geeksforgeeks.org/travelling-salesman-problem-implementation-using-backtracking/
answer = []

def TSP_BT(graph, v, currPos, n, count, cost):
	if (count == n and graph[currPos][0]):
		answer.append(cost + graph[currPos][0])
		return

	# BACKTRACKING STEP
	for i in range(n):
		if (v[i] == False and graph[currPos][i]):
			
			# Mark as visited
			v[i] = True
			TSP_BT(graph, v, i, n, count + 1, cost + graph[currPos][i])
			
			# Mark ith node as unvisited
			v[i] = False

#main function
import time
import csv

g = {}
p = []
l = []
a = ()
for V in range(4, 21): 
    print("vertex number: ", V)
    matrix = Graph(V)
                     
    #run TSP_DP
    start = time.time()
    r1 = TSP_DP(matrix, V)
    end = time.time()
    time1 = end-start
    print("DP_weight:", r1, "; DP_time:", time1)
            
    #run TSP_BT
    start = time.time()
    v = [False for i in range(V)]
    v[0] = True # Mark 0th node as visited
    TSP_BT(matrix, v, 0, V, 1, 0) # Find the minimum weight Hamiltonian Cycle
    r2 = min(answer) # ans is the minimum weight Hamiltonian Cycle
    end = time.time()
    time2 = end-start
    print("BT_weight:", r2, "; BT_time:", time2)
                    
                    
    #calculate error
    error = (r2 - r1)/r1
    print("error:", error)
    
    print("-------------------------------------------------")
    
    with open('TSP_data(DP, BT).csv', 'a+', newline='')as csvFile:        
        csvWriter = csv.writer(csvFile)
        #csvWriter.writerow(['vertex number', 'dp weight','na weight','dp time', 'na time', 'error'])
        csvWriter.writerow([str(V), str(r1), str(r2), str(time1), str(time2), str(error)])    
    csvFile.close()
    