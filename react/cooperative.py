import pathFinding
import collections
import math
import sys
import numpy as np

# actions
CATCH_UP = 0
CATCH_LEFT = 1
CATCH_DOWN = 2
CATCH_RIGHT = 3
MOVE_UP = 4
MOVE_LEFT = 5
MOVE_DOWN = 6
MOVE_RIGHT = 7

# state
UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3

state2action_fruit = {UP: CATCH_UP, LEFT: CATCH_LEFT, DOWN: CATCH_DOWN, RIGHT: CATCH_RIGHT}
state2action_move = {UP: MOVE_UP, LEFT: MOVE_LEFT, DOWN: MOVE_DOWN, RIGHT: MOVE_RIGHT}

# graph = pathFinding.Graph()

# graph.constructGraphFromGrid(5)

# print(graph.nodes)
# print(graph.edges)

class VRP:

    number_of_vehicles = 2

    def __init__(self, fruit_list):
        self.number_of_customers = len(fruit_list)
        self.vehicle_cap = len(fruit_list)
        self.fruits = fruit_list

    def process(self):
        nodes = list()
        depot = Node(0, [0,0], 0, True)
        fruit_number = 0
        nodes.append(depot)
        for i in range(1, self.number_of_customers + 1):
            print (fruits[fruit_number])
            nodes.append(Node(i, fruits[fruit_number], 1, False))
            fruit_number += 1
        print (self.number_of_customers)
        distance_matrix = np.array([[0 for x in range(self.number_of_customers + 1)] for y in range(self.number_of_customers + 1)])
        #distance_matrix = [self.number_of_customers + 1][self.number_of_customers + 1]
        for i in range(0, self.number_of_customers+1):
            for j in range(i+1, self.number_of_customers+1):
                x = abs(nodes[i].x - nodes[j].x)
                y = abs(nodes[i].y - nodes[j].y)

                distance = x + y
                distance_matrix[i][j] = distance
                distance_matrix[j][i] = distance

        print_matrix = 1
        if print_matrix == 1:
            for i in range(0, self.number_of_customers+1):
                for j in range(0, self.number_of_customers+1):
                    print(str(distance_matrix[i][j]) + "     " + str(nodes[i].x) + str(nodes[i].y) + "     " +  str(nodes[j].x) + str(nodes[j].y) )


        solution = Solution(self.number_of_customers, self.number_of_vehicles, self.vehicle_cap)
        solution.Greedy(nodes, distance_matrix)
        solution.Solution_print()

    def execute(self):
        return

class Solution:

    def __init__(self, customer_num, vehicle_num, vehicle_cap):
        self.number_of_vehicles = vehicle_num
        self.number_of_customers = customer_num
        self.cost = 0

        self.vehicles = list()
        self.vehicles_for_best_solution = list()

        for i in range(0, self.number_of_vehicles):
            self.vehicles.append(Vehicle(i+1, vehicle_cap))
            self.vehicles_for_best_solution.append(Vehicle(i+1, vehicle_cap))


    def Greedy(self, node_list, cost_matrix ):
        veh_index = 0
        # candidate_cost = None
        # end_cost = None
        # end_cost = 0

        while unassigned_customer_exists(node_list):
            cust_index = 0
            candidate = None
            min_cost = math.inf

            if len(self.vehicles[veh_index].Route) == 0:
                self.vehicles[veh_index].add_node(node_list[0])

            for i in range(1, self.number_of_customers+1):
                if not node_list[i].is_routed:
                    if self.vehicles[veh_index].check_if_fits(node_list[i].demand):
                        candidate_cost = cost_matrix[self.vehicles[veh_index].cur_loc][i]
                        if min_cost > candidate_cost:
                            min_cost = candidate_cost
                            cust_index = i
                            candidate = node_list[i]

            if candidate == None:
                if veh_index+1 < len(self.vehicles):
                    if self.vehicles[veh_index].cur_loc != 0:
                        end_cost = cost_matrix[self.vehicles[veh_index].cur_loc][0]
                        self.vehicles[veh_index].add_node(node_list[0])
                        self.cost += end_cost
                    veh_index = veh_index + 1
                else:
                    print("customers dont fit in any vehicle")
                    sys.exit(0)
            else:
                self.vehicles[veh_index].add_node(candidate)
                node_list[cust_index].is_routed = True
                self.cost += min_cost

        end_cost = cost_matrix[self.vehicles[veh_index].cur_loc][0]
        self.vehicles[veh_index].add_node(node_list[0])
        self.cost += end_cost

    def Solution_print(self):
        for i in range(0, self.number_of_vehicles):
            if len(self.vehicles[i].Route) != 0:
                print("Vehicle " + i + ":")
                rout_size = len(self.vehicles[i].Route)
                for j in range(0, rout_size):
                    if j == rout_size - 1:
                        print(self.vehicles[i].Route[j].node_id)
                    else:
                        print(self.vehicles[i].Route[j].node_id + "->")

        print("Solution Cost " + str(self.cost))

def unassigned_customer_exists(node_list):
    for i in range(0, len(node_list)):
        if not node_list[i].is_routed:
            return True
    return False


class Node:

    def __init__(self, id, pos, demand, depot):
        self.node_id = id
        self.x = pos[0]
        self.y = pos[1]
        self.demand = demand
        self.is_routed = False
        if depot:
            self.isDepot = True
        self.isDepot = False


class Vehicle:

    def __init__(self, id, cap):

        self.vehicle_id = id
        self.capacity = cap
        self.load = 0
        self.cur_loc = 0
        self.closed = False
        self.Route = list()

    def add_node(self, node):
        self.Route.append(node)
        self.load += node.demand
        self.cur_loc = node.node_id

    def check_if_fits(self, dem):
        return self.load + dem <= self.capacity


'''class GraphVRP:

    def __init__(self, list_of_fruits, depot):

        self.nodes = list()
        self.edges = collections.defaultdict(list)
        self.arcs = collections.defaultdict(list)

        self.nodes.append(Node(depot, 0))
        for fruit in list_of_fruits:
            n = Node(fruit, 1)
            self.nodes.append(n)

        for node in self.nodes:
            for node_connection in self.nodes:
                if node.x != node_connection.x or node.y != node_connection.y:
                    self.edges[node].append(node_connection)
                #self.edges[node_connection].append(node)

        for node in self.edges:
            for node_edge in self.edges[node]:
                cost_node = abs(node.x - node_edge.x) + abs(node.y - node_edge.y)
                self.arcs[node].append([node_edge,cost_node])


    def print_node(self):
        for i in self.nodes:
            print(str(i.x) + " " + str(i.y))


    def print_edges(self):
        for i in self.edges:
            for j in self.edges[i]:
                print(str(i.x) + str(i.y) + " : " + str(j.x) + str(j.y))


    def print_arcs(self):
        for i in self.arcs:
            for j in self.arcs[i]:
                print(str(i.x) + str(i.y) + " : " + str(j[0].x) + str(j[0].y) + " cost: " + str(j[1]))

'''

fruits = [[0,1], [2,1], [3,2]]

#g = GraphVRP(fruits, [0,0])

#g.print_node()
#g.print_edges()
#g.print_arcs()


vrp = VRP(fruits)
vrp.process()

