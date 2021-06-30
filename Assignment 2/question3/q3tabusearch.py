import numpy as np
import random
import matplotlib.pyplot as plt

distancefile = open("distance.csv")
distance_array = np.loadtxt(distancefile, delimiter=",")

flowfile = open("flow.csv")
flow_array = np.loadtxt(flowfile, delimiter=",")

def tabusearch(initiallayout, distancearray, flowarray, tabu_matrix, tabu_tenure, typeof):
    layout = initiallayout
    cost = search_cost(layout)
    tabu_list = []
    iterations = 0
    
    while cost > 2570 and iterations < 1000:
        iterations += 1
        if typeof == "DYNAMIC" and iterations % 45 == 0:
            tabu_tenure = random.randint(1, 300)

        if typeof == "ASPIRATION/FREQUENCY" and iterations > 250 == 0 and len(tabu_list) > 0:
            layout = tabu_list[0]

        cost,layout = swap_and_test(layout, cost, tabu_matrix, tabu_tenure, typeof)
        
    print("BEST SOLUTION COST : ", cost)
    print("BEST SOLUTION LAYOUT: ", layout)
    return cost
    

    
def search_cost(layout):
    
    searchcost= 0
    layout = list(layout.flatten())
    for x in range(20):
        for y in range(20):
            searchcost +=  flow_array[int(layout[x])][int(layout[y])] * distance_array[x][y]
    return searchcost


def swap_and_test(layout, initcost, tabu_list, tabu_tenure, typeof):
    bestfoundcost = initcost
    bestlayout = layout.copy()
    haschanged = False
    for x in range(4):
        for y in range(3):
            #Can change range of neighbourhood below by changing value of i and j
            for i in range(3): # normally 4 for whole neighbourhood, 3 in this case
                for j in range(3):
                    if j > y or (y == j and i > x): 
                        newlayout = layout.copy()
                        swap = newlayout[i][j]
                        newlayout[i][j] = newlayout[x][y]
                        newlayout[x][y] = swap
                        newcost = search_cost(newlayout)
                        repeated = False
                        for item in tabu_list:
                            if (item[1] == newlayout).all() and repeated == False:
                                repeated = True
                                break
                        
                        if len(tabu_list) == 0 or repeated == False:  
                            if newcost < bestfoundcost:
                                bestfoundcost = newcost
                                bestlayout = newlayout
                                haschanged = True
        if haschanged == True: 
            add_to_tabu_list(bestlayout, bestfoundcost, tabu_list, tabu_tenure, typeof)
    return bestfoundcost, bestlayout 


def add_to_tabu_list(newlayout, newcost, tabu_list, tabu_tenure, typeof):
    
    tabu_list.append((newcost,newlayout))
    if typeof == "ASPIRATION":
        tabu_list = sorted(tabu_list, key=lambda x: x[0], reverse=True)
    if typeof == "ASPIRATION/FREQUENCY":
        tabu_list = sorted(tabu_list, key=lambda x: x[0], reverse=True)
    
    if len(tabu_list) >= tabu_tenure:
        while len(tabu_list) != tabu_tenure:
            tabu_list.pop(0)
        
        

def create_random_matrix():
    import random
    initiallayout = np.zeros(shape=(4,5))

    locations = list(range(0, 20))

    random.shuffle(locations)

    for i, row in enumerate(initiallayout):
        random = locations[:5] 
        del locations[:5]
        initiallayout[i] = random
    return initiallayout
        
        
        
        
def select_experiment(distance_array, flow_array, tabu_list, tabu_tenure):
    experiment = input("Please put number of experiment: ")
    if experiment == '0':
        initialayout = create_random_matrix()
        cost = tabusearch(initialayout, distance_array, flow_array, tabu_list, tabu_tenure, "NORMAL")


    elif experiment == '1':


        runcosts = []
        for i in range(20):
            print ("RUN NUMBER: ", i)
            initialayout = create_random_matrix()
            cost = tabusearch(initialayout, distance_array, flow_array, tabu_list, tabu_tenure, "20RUNS")
            runcosts.append(cost)
        print("AVERAGE of 20 RUNS: ", sum(runcosts)/len(runcosts))
        plt.title("BASIC TABU SEARCH ")
        plt.xticks([x for x in range(20)])   
        plt.xlabel('RUN NUMBER')
        plt.ylabel('COST')
        plt.scatter([x for x in range(20)], runcosts)
        plt.show()


    elif experiment == '2':
        tabu_sizes = []
        best_cost = []
        initialayout = create_random_matrix()
        print("CHANGING TABU BY +- 10")



        print("TABU SIZE: ", tabu_tenure - 80)
        tabu_sizes.append(tabu_tenure - 80)
        best_cost.append(tabusearch(initialayout, distance_array, flow_array, tabu_list, tabu_tenure - 80, "CHANGING"))

        print("TABU SIZE: ", tabu_tenure - 20 )
        tabu_sizes.append(tabu_tenure - 20)
        best_cost.append(tabusearch(initialayout, distance_array, flow_array, tabu_list, tabu_tenure - 20, "CHANGING"))

        print("BASE TABU SIZE: ", tabu_tenure)
        tabu_sizes.append(tabu_tenure)
        best_cost.append(tabusearch(initialayout, distance_array, flow_array, tabu_list, tabu_tenure, "CHANGING"))

        print("TABU SIZE: ", tabu_tenure + 20 )
        tabu_sizes.append(tabu_tenure + 20 )
        best_cost.append(tabusearch(initialayout, distance_array, flow_array, tabu_list, tabu_tenure + 20, "CHANGING"))

        print("TABU SIZE: ", tabu_tenure + 80 )
        tabu_sizes.append(tabu_tenure + 80)
        best_cost.append(tabusearch(initialayout, distance_array, flow_array, tabu_list, tabu_tenure + 80, "CHANGING"))

        plt.title("CHANGING TABU BY +- 10")
        plt.xticks(tabu_sizes)  
        plt.xlabel('TABU TENURE SIZES')
        plt.ylabel('COST')
        plt.scatter(tabu_sizes, best_cost)
        plt.show()

    elif experiment =='3':
        initialayout = create_random_matrix()
        print("DYNAMIC TABU")
        runcosts = []
        for i in range(20):
            print ("RUN NUMBER: ", i)
            cost = tabusearch(initialayout, distance_array, flow_array, tabu_list, tabu_tenure, "DYNAMIC")
            runcosts.append(cost)
        print("AVERAGE of 20 RUNS: ", sum(runcosts)/len(runcosts))
        plt.title("DYNAMIC TABU")
        plt.xticks([x for x in range(20)])   
        plt.xlabel('RUN NUMBER')
        plt.ylabel('COST')
        plt.scatter([x for x in range(20)], runcosts)
        plt.show()   

    elif experiment =='4':
        runcosts = []
        print("ASPIRATION CRITERIA")
        for i in range(20):
            print ("RUN NUMBER: ", i)
            initialayout = create_random_matrix()
            cost = tabusearch(initialayout, distance_array, flow_array, tabu_list, tabu_tenure, "ASPIRATION" )
            runcosts.append(cost)
        print("AVERAGE of 20 RUNS: ", sum(runcosts)/len(runcosts))
        plt.title("ASPIRATION CRITERIA")
        plt.xticks([x for x in range(20)])   
        plt.xlabel('RUN NUMBER')
        plt.ylabel('COST')
        plt.scatter([x for x in range(20)], runcosts)
        plt.show()   

    elif experiment =='5':
        runcosts = []
        print("ASPIRATION/FREQUENCY CRITERIA")
        for i in range(20):
            print ("RUN NUMBER: ", i)
            initialayout = create_random_matrix()
            cost = tabusearch(initialayout, distance_array, flow_array, tabu_list, tabu_tenure, "ASPIRATION/FREQUENCY" )
            runcosts.append(cost)
        print("AVERAGE of 20 RUNS: ", sum(runcosts)/len(runcosts))
        plt.title("ASPIRATION/FREQUENCY CRITERIA")
        plt.xticks([x for x in range(20)])   
        plt.xlabel('RUN NUMBER')
        plt.ylabel('COST')
        plt.scatter([x for x in range(20)], runcosts)
        plt.show()   

        
        
        
    
tabu_list = [] # (cost, layout)
tabu_tenure = 100

select_experiment(distance_array, flow_array, tabu_list, tabu_tenure)


    