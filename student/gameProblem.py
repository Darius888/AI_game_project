
'''
    Class gameProblem, implements simpleai.search.SearchProblem
'''


from simpleai.search import SearchProblem
# from simpleai.search import breadth_first,depth_first,astar,greedy
import simpleai.search

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

        if self.canMove(state, self.MOVES[0]): 
            acciones.append(self.MOVES[0])

        if self.canMove(state, self.MOVES[1]):
            acciones.append(self.MOVES[1])

        if self.canMove(state, self.MOVES[2]):
            acciones.append(self.MOVES[2])

        if self.canMove(state, self.MOVES[3]):
            acciones.append(self.MOVES[3])
            
        if self.isShop(state) and state[2] < self.MAXBAGS:
            acciones.append(self.ACTIONS[0])

        if self.isCustomer(state) and state[2] > 0:
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
        return 1


    def heuristic(self, state):
        '''Returns the heuristic for `state`
        '''
        return 0


    def setup (self):
        '''This method must create the initial state, final state (if desired) and specify the algorithm to be used.
           This values are later stored as globals that are used when calling the search algorithm.
           final state is optional because it is only used inside the is_goal() method

           It also must set the values of the object attributes that the methods need, as for example, self.SHOPS or self.MAXBAGS
        '''

        print '\nMAP: ', self.MAP, '\n'
	print 'POSITIONS: ', self.POSITIONS, '\n'
	print 'CONFIG: ', self.CONFIG, '\n'

        initial_state = (self.AGENT_START[0], self.AGENT_START[1], 0, 0)
        final_state = (self.AGENT_START[0], self.AGENT_START[1], 0, 1)
        self.MAP_SIZE = {'x': len(self.MAP), 'y': len(self.MAP[0])}
        self.CUSTOMERS = self.getCustomers()
        self.SHOPS = self.getShops()

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
        
        pps=''
        return (pps)

    def getPendingRequests (self,state):
        ''' Return the number of pending requests in the given position (0-N). 
            MUST return None if the position is not a customer.
            This information is used to show the proper customer image.
        '''
        return None

   # -------------------------------------------------------------- #
   # ---------------------- HELPER METHODS ------------------------ #
   # -------------------------------------------------------------- #

    # Computes the next state when 'move' action is applied
    def move(self, state, direction):
        x = state[0]
        y = state[1]
        pizzas = state[2]
        isSatisfied = state[3]

        if direction not in self.MOVES:
            raise ValueError('Given direction must be one of: ' + self.MOVES + ' but is: ' + direction)

        if direction == self.MOVES[0]:
            next_state = (x-1, y, pizzas, isSatisfied)
        elif direction == self.MOVES[1]:
            next_state = (x, y-1, pizzas, isSatisfied)
        elif direction == self.MOVES[2]:
            next_state = (x+1, y, pizzas, isSatisfied)
        elif direction == self.MOVES[3]:
            next_state = (x, y+1, pizzas, isSatisfied)

        return next_state


    # Computes the next state when 'load' action is applied
    def loadPizzas(self, state):
        x = state[0]
        y = state[1]
        pizzas = self.MAXBAGS
        isSatisfied = state[3]
        next_state = (x, y, pizzas, isSatisfied)        

        return next_state


    # Computes the next state when 'deliver' action is applied
    def deliver(self, state):
        x = state[0]
        y = state[1]
        pizzas = 0
        isSatisfied = 1
        next_state = (x, y, pizzas, isSatisfied)        

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
                    customers[(x, y)] = self.MAP[x][y][2]['objects'] # number of orders (pizzas)
        
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
