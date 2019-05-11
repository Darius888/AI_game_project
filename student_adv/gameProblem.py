
'''
    Class gameProblem, implements simpleai.search.SearchProblem
'''


from simpleai.search import SearchProblem
# from simpleai.search import breadth_first,depth_first,astar,greedy
import simpleai.search
import itertools
import math

class GameProblem(SearchProblem):

    # Object attributes, can be accessed in the methods below
    
    MAP=None
    POSITIONS=None
    INITIAL_STATE=None
    GOAL=None
    CONFIG=None
    AGENT_START=None
    SHOPS=None
    CUSTOMERS=None
    MAXBAGS = 2
    # Map size (x-dimension size, y-dimension size)
    MAP_SIZE = None

    MOVES = ('West','North','East','South')
    ACTIONS = ('Load', 'Deliver')

   # --------------- Common functions to a SearchProblem -----------------

    def actions(self, state):
        '''Returns a LIST of the actions that may be executed in this state
        '''
        acciones = []
        pizzas = state[2]
        stateClass = StateClass.fromState(state)

        if self.canMove(state, self.MOVES[0]): 
            acciones.append(self.MOVES[0])

        if self.canMove(state, self.MOVES[1]):
            acciones.append(self.MOVES[1])

        if self.canMove(state, self.MOVES[2]):
            acciones.append(self.MOVES[2])

        if self.canMove(state, self.MOVES[3]):
            acciones.append(self.MOVES[3])
            
        if self.isShop(state) and pizzas < self.MAXBAGS and pizzas < stateClass.getNumberOfLeftOrders():
            acciones.append(self.ACTIONS[0])

        if not pizzas < stateClass.getNumberOfLeftOrders():
            print "--------------------------------P", pizzas, "| O", stateClass.getNumberOfLeftOrders(), "| C", stateClass.customers

        if self.isCustomer(state):
            orders = stateClass.customers[(stateClass.x, stateClass.y)]

            if pizzas > 0 and orders > 0:
                acciones.append(self.ACTIONS[1])

        return acciones
    

    def result(self, state, action):
        '''Returns the state reached from this state when the given action is executed
        '''
        if action in self.MOVES:
            next_state = self.move(state, action)

        if action == self.ACTIONS[0]:
            next_state = self.loadPizzas(state)

        if action == self.ACTIONS[1]:
            next_state = self.deliver(state)

        return next_state


    def is_goal(self, state):
        '''Returns true if state is the final state
        '''
        if state == self.GOAL:
            return True

        return False


    def cost(self, state, action, state2):
        '''Returns the cost of applying `action` from `state` to `state2`.
           The returned value is a number (integer or floating point).
           By default this function returns `1`.
        '''
        cost = 0
        x = state[0]
        y = state[1]

        cost = self.getAttribute((x,y),'cost')

       
        if(self.ACTIONS == 'Load'):
            cost = 4

        if(self.ACTIONS == 'Deliver'):
            cost = 4

        if(state2[2] > 0):
            cost += 6

        # if(self.isShop1(state2) and self.ACTIONS == 'Load'):
        #     cost = 3

        # if(self.isShop2(state2) and self.ACTIONS == 'Load'):
        #     cost = 4

        # if(state2[2] == 0):
        #     cost = 1

        # if(state[2] == 1):
        #     cost = 2

        # if(self.state[2] > 0):
        #     cost = 6


        return cost

    def heuristic(self, state):
        '''Returns the heuristic for `state`
        '''
        # print "------------------------------------------------------"
        stateClass = StateClass.fromState(state)
        orders = stateClass.getNumberOfLeftOrders()
        distance = 0

        # initial situation
        if orders > 0 and stateClass.pizzas == 0:
            man_shop_dists = []
            for shop in self.SHOPS:
                man_shop_dist = self.manhattanDistance(shop, (stateClass.x, stateClass.y))
                man_shop_dists.append(man_shop_dist)
            alfa = min(man_shop_dists)
            # print "man - shop", alfa
            distance += alfa
        
        elif orders > 0 and stateClass.pizzas > 0:
            man_cust_dists = []
            for cust in stateClass.getCustomersWithOrders():
                man_cust_dist = self.manhattanDistance(cust, (stateClass.x, stateClass.y))
                man_cust_dists.append(man_cust_dist)
            alfa = min(man_cust_dists)
            # print "man - cust", alfa
            distance += alfa

            

        # get min distance between shops and customers
        # shops_and_customers = []
        # shops_and_customers.extend(self.SHOPS)
        # shops_and_customers.extend(stateClass.getCustomersWithOrders())
        # routes = []
        # routes = list(itertools.combinations(shops_and_customers, 2))
        # shop_customer_dists = []
        # print "bef", len(routes)
        # for route in routes[:]:
        #     if (route[0] in self.SHOPS and route[1] in self.SHOPS) or (route[0] in self.CUSTOMERS.values() and route[1] in self.CUSTOMERS.values()):
        #         print "REM", route
        #         routes.remove(route)               
        #     else:
        #         shop_customer_dists.append(self.manhattanDistance(route[0], route[1]))
        # print routes
        # print "aft", len(routes)
        # print shop_customer_dists

        shop_customer_dists = []
        for customer in stateClass.getCustomersWithOrders():
            temp_dists = []
            shops_and_customers = []
            shops_and_customers.extend(self.SHOPS)
            shops_and_customers.append(customer)

            routes = list(itertools.combinations(shops_and_customers, 2))
            #print "bef", len(routes)
            for route in routes[:]:
                if (route[0] in self.SHOPS and route[1] in self.SHOPS):
                   # print "REM", route
                    routes.remove(route)               
                else:
                    temp_dists.append(self.manhattanDistance(route[0], route[1]))
            
            shop_customer_dists.append(min(temp_dists))
            # print routes
            # print "aft", len(routes)
        # print shop_customer_dists

        coeficient = int(math.ceil((orders - stateClass.pizzas)/float(self.MAXBAGS)))
        shop_customer_dists.sort()
        shop_customer_dists = shop_customer_dists[0:coeficient]
        alfa = sum(shop_customer_dists) # min(shop_customer_dists) * int(math.ceil((orders - stateClass.pizzas)/float(self.MAXBAGS)))
        #print "shops - customers", alfa, "| dists", shop_customer_dists #, "| min ", min(shop_customer_dists), "ceil ", int(math.ceil((orders - stateClass.pizzas)/self.MAXBAGS)), "ord-piz ", (orders - stateClass.pizzas), "/MAX", (orders - stateClass.pizzas)/float(self.MAXBAGS)
        distance += alfa

        # get num of loads and delivers
        alfa = orders
        #print "delivers", alfa
        distance += alfa
        
        alfa = orders - stateClass.pizzas # math.ceil((orders - stateClass.pizzas)/self.MAXBAGS)
        #print "loads", alfa
        distance += alfa

        # min dist between customers if maxbags > 
        if (self.MAXBAGS >= orders or orders <= stateClass.pizzas) and len(stateClass.getCustomersWithOrders()) > 1:
            routes_between_customers = list(itertools.combinations(stateClass.getCustomersWithOrders(), 2))
            cust_cust_dist = []
            for route in routes_between_customers:
                cust_cust_dist.append(self.manhattanDistance(route[0], route[1]))
            
            alfa = max(len(stateClass.getCustomersWithOrders()) - 1, 0) * min(cust_cust_dist)
            #print "cust - cust", alfa
            distance += alfa

        # min between customer and goal
        if stateClass.getNumberOfLeftOrders() != 0:
            cust_goal_dists = []
            for customer in stateClass.getCustomersWithOrders():
                cust_goal_dists.append(self.manhattanDistance(customer, (self.GOAL[0], self.GOAL[1])))

            alfa = min(cust_goal_dists)
            #print "cust - goal", alfa
            distance += alfa
        else:
            alfa = self.manhattanDistance((stateClass.x, stateClass.y), (self.GOAL[0], self.GOAL[1]))
            #print "man - goal", alfa
            distance += alfa
        
        # print "h", distance
        #print stateClass.x, stateClass.y, "| P", stateClass.pizzas, "| O", stateClass.getNumberOfLeftOrders(), "| H", distance, "| C", stateClass.getCustomersWithOrders()
        return distance

    def manhattanDistance(self, point_1, point_2):
        x1 = point_1[0]
        y1 = point_1[1]
        x2 = point_2[0]
        y2 = point_2[1]

        return abs(x1 - x2) + abs(y1 - y2)

    def computePathCost(self, state, route):
        distance = 0
        x = state[0]
        y = state[1]
        route = list(route)
        route.insert(0, (x, y))
        route.append((self.GOAL[0], self.GOAL[1]))

        index = 0
        for index in range(len(route) - 2):
            start_x = route[index][0]
            start_y = route[index][1]
            end_x = route[index + 1][0]
            end_y = route[index + 1][1]
            distance += abs(start_x - end_x) + abs(start_y - end_y)

        return distance

    def setup (self):
        '''This method must create the initial state, final state (if desired) and specify the algorithm to be used.
           This values are later stored as globals that are used when calling the search algorithm.
           final state is optional because it is only used inside the is_goal() method

           It also must set the values of the object attributes that the methods need, as for example, self.SHOPS or self.MAXBAGS
        '''
        self.MAP_SIZE = {'x': len(self.MAP), 'y': len(self.MAP[0])}
        self.CUSTOMERS = self.getCustomers()
        self.SHOPS = self.getShops()

        print '\nMAP: ', self.MAP, '\n'
        print 'POSITIONS: ', self.POSITIONS, '\n'
        print 'CONFIG: ', self.CONFIG, '\n'
        print 'CUSTOMERS', self.CUSTOMERS, '\n'
        print 'SHOPS', self.SHOPS, '\n'   

        # state: (x, y, pizzas, (customer_1_x, customer_1_y, customer_1_orders, customer_2_x, ...))
        stateClass = StateClass(self.AGENT_START[0], self.AGENT_START[1], 0, self.CUSTOMERS)
        initial_state = stateClass.toState()

        stateClass.emptyAllOrders()
        final_state = stateClass.toState()

        # validation and constraints
        if not self.isInMapBounds(initial_state) or not self.isInMapBounds(final_state):
            raise ValueError('Initial and final state must be inside map bounds.\n'\
            'Map size: {size}. Initial state: {initial}. Final state: {final}. Mind the index values.'\
            .format(size = self.MAP_SIZE, initial = initial_state, final = final_state))


        algorithm= simpleai.search.astar
        #algorithm= simpleai.search.breadth_first
        #algorithm= simpleai.search.depth_first
        #algorithm= simpleai.search.limited_depth_first

        return initial_state,final_state,algorithm
        
    def printState (self,state):
        '''Return a string to pretty-print the state '''

        pps=state
        return (pps)

    def getPendingRequests (self,state):
        ''' Return the number of pending requests in the given position (0-N). 
            MUST return None if the position is not a customer.
            This information is used to show the proper customer image.
        '''
        if self.isCustomer(state):
            x = state[0]
            y = state[1]
            stateClass = StateClass.fromState(state)
            orders = stateClass.customers[(x, y)]
            return orders

        return None

   # -------------------------------------------------------------- #
   # ---------------------- HELPER METHODS ------------------------ #
   # -------------------------------------------------------------- #

    # Computes the next state when 'move' action is applied
    def move(self, state, direction):
        x = state[0]
        y = state[1]
        pizzas = state[2]
        customers = state[3]

        if direction not in self.MOVES:
            raise ValueError('Given direction must be one of: ' + self.MOVES + ' but is: ' + direction)

        if direction == self.MOVES[0]:
            next_state = (x-1, y, pizzas, customers)
        elif direction == self.MOVES[1]:
            next_state = (x, y-1, pizzas, customers)
        elif direction == self.MOVES[2]:
            next_state = (x+1, y, pizzas, customers)
        elif direction == self.MOVES[3]:
            next_state = (x, y+1, pizzas, customers)

        return next_state


    # Computes the next state when 'load' action is applied
    def loadPizzas(self, state):
        x = state[0]
        y = state[1]
        pizzas = state[2]
        customers = state[3]

        pizzas += 1
        next_state = (x, y, pizzas, customers)        

        return next_state


    # Computes the next state when 'deliver' action is applied
    def deliver(self, state):
        stateClass = StateClass.fromState(state)
        x = state[0]
        y = state[1]
        pizzas = state[2]
        orders = stateClass.customers[(x, y)]

        # orders_left = max(orders - pizzas, 0)
        # pizzas_left = max(pizzas - orders, 0)
        orders_left = orders - 1
        pizzas_left = pizzas - 1

        stateClass.pizzas = pizzas_left
        stateClass.customers[(x, y)] = orders_left
        next_state = stateClass.toState()   

        return next_state


    def isBuilding(self, state):
        x = state[0]
        y = state[1]
        if self.MAP[x][y][0] == 'building':
            return True

        return False


    def isCustomer(self, state):
        x = state[0]
        y = state[1]

        if (x, y) in self.CUSTOMERS:
            return True

        return False	


    def isShop(self, state):
        x = state[0]
        y = state[1]
        
        if (x, y) in self.SHOPS:
            return True
        
        return False


    def canMove(self, state, direction):
        next_state = self.move(state, direction)
        
        if not self.isInMapBounds(next_state):
            return False

        if self.isBuilding(next_state):
            return False

        return True


    def isInMapBounds(self, state):
        x = state[0]
        y = state[1]
        map_len_x = self.MAP_SIZE['x']
        map_len_y = self.MAP_SIZE['y']

        if (x < 0 or y < 0 or x >= map_len_x or y >= map_len_y):
            return False

        return True


    # Parses the map and searches for customers' locations and their orders.
    # Returns the dictionary with records like: (x, y): number_of_orders.
    def getCustomers(self):
        customers = {}
        for x in range(self.MAP_SIZE['x']):
            for y in range(self.MAP_SIZE['y']):
                if 'customer' in self.MAP[x][y][0]:
                    orders = self.MAP[x][y][2]['objects'] # number of orders (pizzas)
                    if orders == 0:
                        raise ValueError('Customer must order at least 1 pizza. Currently: 0')
                    customers[(x, y)] = orders
        
        return customers

    # Parses the map and searches for shops' locations.
    # Returns the list of tuples: (x, y).
    def getShops(self):
        shops = []
        for x in range(self.MAP_SIZE['x']):
            for y in range(self.MAP_SIZE['y']):
                if 'pizza' in self.MAP[x][y][0]:
                    shops.append((x, y))
        
        return shops

   # -------------------------------------------------------------- #
   # --------------- DO NOT EDIT BELOW THIS LINE  ----------------- #
   # -------------------------------------------------------------- #

    def getAttribute (self, position, attributeName):
        '''Returns an attribute value for a given position of the map
           position is a tuple (x,y)
           attributeName is a string
           
           Returns:
               None if the attribute does not exist
               Value of the attribute otherwise
        '''
        tileAttributes=self.MAP[position[0]][position[1]][2]
        if attributeName in tileAttributes.keys():
            return tileAttributes[attributeName]
        else:
            return None

    def getStateData (self,state):
        stateData={}
        pendingItems=self.getPendingRequests(state)
        if pendingItems >= 0:
            stateData['newType']='customer{}'.format(pendingItems)
        return stateData
        
    # THIS INITIALIZATION FUNCTION HAS TO BE CALLED BEFORE THE SEARCH
    def initializeProblem(self,map,positions,conf,aiBaseName):
        self.MAP=map
        self.POSITIONS=positions
        self.CONFIG=conf
        self.AGENT_START = tuple(conf['agent']['start'])

        initial_state,final_state,algorithm = self.setup()
        if initial_state == False:
            print ('-- INITIALIZATION FAILED')
            return True
      
        self.INITIAL_STATE=initial_state
        self.GOAL=final_state
        self.ALGORITHM=algorithm
        super(GameProblem,self).__init__(self.INITIAL_STATE)
            
        print ('-- INITIALIZATION OK')
        return True
        
    # END initializeProblem 

class StateClass:
 
    def __init__(self, x, y, pizzas, customers):
        self.x = x
        self.y = y
        self.pizzas = pizzas
        self.customers = customers

    def toState(self):
        return (self.x, self.y, self.pizzas, self.customersToTuple(self.customers))

    def customersToTuple(self, dict):
        temp_list = []
        for key in dict.keys():
            temp_list.append(key[0])
            temp_list.append(key[1])
            temp_list.append(dict[key])

        return tuple(temp_list)

    def emptyAllOrders(self):
        for key in self.customers.keys():
            self.customers[key] = 0

    def getCustomersWithOrders(self):
       
        customers_with_orders = []
        for key in self.customers.keys():
            if self.customers[key] != 0:
                
                customers_with_orders.append(key)

        # if len(customers_with_orders) > 1:
        #     print "customers", self.customers 
        return customers_with_orders

    def getNumberOfLeftOrders(self):
        if sum(self.customers.values()) > 7:
            raise ValueError("SUM > 7")
        # print "----------------------------------------SUM", sum(self.customers.values())
        return sum(self.customers.values())

    @staticmethod
    def fromState(state):
        customers_list = list(state[3])
        customers = {}

        if (len(customers_list) % 3) != 0:
            raise ValueError('Incorrect state. Customers tuple has a bad format. '\
                'Should contain triplets: customer_x, customer_y, orders_left, '\
                'but is: {list}'.format(list = customers_list))

        index = 0
        while index < len(customers_list):
            x = customers_list[index]
            y = customers_list[index + 1]
            orders = customers_list[index + 2]
        
            customers[(x, y)] = orders
            index += 3

        x = state[0]
        y = state[1]
        pizzas = state[2]

        return StateClass(x, y , pizzas, customers)