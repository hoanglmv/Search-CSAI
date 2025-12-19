# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.
    """
    # Su dung Stack cho DFS
    fringe = util.Stack()
    # Node luu tru: (state, actions_list)
    fringe.push((problem.getStartState(), []))
    
    visited = []

    while not fringe.isEmpty():
        state, actions = fringe.pop()

        if state in visited:
            continue
        
        visited.append(state)

        if problem.isGoalState(state):
            return actions

        for successor, action, stepCost in problem.getSuccessors(state):
            if successor not in visited:
                fringe.push((successor, actions + [action]))
    
    return []

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    # Su dung Queue cho BFS
    fringe = util.Queue()
    fringe.push((problem.getStartState(), []))
    
    visited = [] # List cac state da expanded

    while not fringe.isEmpty():
        state, actions = fringe.pop()

        if state in visited:
            continue
        
        visited.append(state)

        if problem.isGoalState(state):
            return actions

        for successor, action, stepCost in problem.getSuccessors(state):
            if successor not in visited:
                fringe.push((successor, actions + [action]))
                
    return []

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    # Su dung PriorityQueue cho UCS
    fringe = util.PriorityQueue()
    # Node: (state, actions, current_cost)
    # Priority: current_cost
    fringe.push((problem.getStartState(), [], 0), 0)
    
    visited = []

    while not fringe.isEmpty():
        state, actions, currentCost = fringe.pop()

        if state in visited:
            continue
        
        visited.append(state)

        if problem.isGoalState(state):
            return actions

        for successor, action, stepCost in problem.getSuccessors(state):
            if successor not in visited:
                newCost = currentCost + stepCost
                fringe.push((successor, actions + [action], newCost), newCost)
                
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    
    fringe = util.PriorityQueue()
    startState = problem.getStartState()
    
    # Node lưu: (state, actions, g_cost)
    # Priority = g_cost + h_cost
    fringe.push((startState, [], 0), 0 + heuristic(startState, problem))
    
    # Sử dụng Dictionary để lưu chi phí G thấp nhất đã tìm thấy đến state đó
    # closed[state] = lowest_g_cost
    closed = {}

    while not fringe.isEmpty():
        state, actions, gCost = fringe.pop()

        # Quan trọng: Kiểm tra xem state này đã từng được duyệt với chi phí thấp hơn chưa?
        # Nếu đã có đường đi rẻ hơn hoặc bằng gCost đến state này rồi -> Bỏ qua
        if state in closed and closed[state] <= gCost:
            continue
        
        # Nếu đây là đường đi rẻ nhất đến state tính đến giờ -> Ghi nhận
        closed[state] = gCost

        if problem.isGoalState(state):
            return actions

        for successor, action, stepCost in problem.getSuccessors(state):
            newGCost = gCost + stepCost
            newPriority = newGCost + heuristic(successor, problem)
            
            # Chỉ đẩy vào hàng đợi nếu:
            # 1. Chưa từng đến successor này bao giờ
            # 2. HOẶC đường đi mới này rẻ hơn đường đi cũ đã lưu trong closed
            if successor not in closed or newGCost < closed[successor]:
                fringe.push((successor, actions + [action], newGCost), newPriority)
                
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch