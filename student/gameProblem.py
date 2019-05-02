
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
    MAXBAGS = 0
    PIZZAS = 0

    MOVES = ('West','North','East','South')

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
            
        return acciones
    

    def result(self, state, action):
        '''Returns the state reached from this state when the given action is executed
        '''
        if action in self.MOVES:
            next_state = self.computeNextState(state, action)

        return next_state


    def canMove(self, state, direction):
        next_state = self.computeNextState(state, direction)
        
        if not self.isInMapBounds(next_state):
            return False

        if self.isBuilding(next_state):
            return False

        return True

    def isBuilding(self, state):
        x = state[0]
        y = state[1]
        if self.MAP[x][y][0] == 'building':
            return True

        return False

    def loadPizzas(self, state):
        x = state[0]
        y = state[1]
        if self.isRestaurant(state):
            self.PIZZAS = 2

        return self.PIZZAS

    def isCustomer(self, state):
	x = state[0]
	y = state[1]
	if self.MAP[x][y][0] == 'customer0' or self.MAP[x][y][0] == 'customer1' or self.MAP[x][y][0] == 'customer2':
	    return True
	
	return False	

    def isRestaurant(self, state):
	x = state[0]
	y = state[1]
	if self.MAP[x][y][0] == 'pizza':
	    return True
	
	return False

    def isInMapBounds(self, state):
        x = state[0]
        y = state[1]
        map_len_x = len(self.MAP)
        map_len_y = len(self.MAP[0])

        if (x < 0 or y < 0 or x >= map_len_x or y >= map_len_y):
            return False

        return True


    def computeNextState(self, state, direction):
        x = state[0]
        y = state[1]
        next_state = None

        if direction not in self.MOVES:
            raise ValueError("Given direction must be one of: " + direction)

        if direction == self.MOVES[0]:
            next_state = (x-1, y)
        elif direction == self.MOVES[1]:
            next_state = (x, y-1)
        elif direction == self.MOVES[2]:
            next_state = (x+1, y)
        elif direction == self.MOVES[3]:
            next_state = (x, y+1)

        return next_state

    def is_goal(self, state):
        '''Returns true if state is the final state
        '''
        #if state == self.isRestaurant(state) and self.loadPizzas(self, state):
        #    self.GOAL = (9,3)

        if state == self.GOAL and self.isRestaurant(state):
            self.loadPizzas(state)
            self.GOAL = (9,3)
        
        if state == (9,3) and self.isCustomer(state):
            self.GOAL = self.AGENT_START 
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

        initial_state = self.AGENT_START
        final_state = (6,0)
        map_size = (len(self.MAP), len(self.MAP[0]))

        if not self.isInMapBounds(initial_state) or not self.isInMapBounds(final_state):
            raise ValueError("Initial and final state must be inside map bounds.\n"\
            "Map size: {size}. Initial state: {initial}. Final state: {final}. Mind the index values."\
            .format(size = map_size, initial = initial_state, final = final_state))

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

