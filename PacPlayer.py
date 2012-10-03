from com.orbischallenge.pacman.api.common import *
from com.orbischallenge.pacman.api.python import *
from graph import *
from copy import deepcopy

import math
import random

class PacPlayer(Player):
	'''
	Implements the AI for Pacman player.
	'''
	
	def __init__(self):
		'''
		Constructor for the AI class.
		'''
		
		self.lives = 1
		self.best_moves = []
			
	def find_alternative(self, pac_tile, bad_moves, adjacency_list, ghosts):
		'''
		Finds a path (second best move) from the current PacMan's position
		as an alternative to the best path, that doesn't eventually lead to
		a harmful move.
		
		Keyword arguments:
		pac_tile -- the position of PacMan.
		bad_moves -- a list of position moves to avoid.
		adjacency_list -- Adjacenecy list representation of the maze (graph).
		ghosts -- a list of current Ghost objects invovled in the game.
		
		Return:
		None.
		'''
	
		for move in bad_moves:
			#Remove every bad move (disconnect from the graph).
			try:
				adjacency_list[pac_tile].remove(move)
			
			#If an edge has been already removed (since it was bad),
			#we can't possibly remove it again.
			except ValueError:
				pass
		
		#Instantiate a Breadth First Search object.	
		bfs = BFS(adjacency_list, self.maze)
		
		#Find the shortest path to any DOT or POWER_DOT item from the
		#current position using the BFS object above.
		moves = bfs.search(pac_tile, [MazeItem.POWER_DOT, MazeItem.DOT])

		if moves:		
			#Remove the first path since it's the current position.
			moves.pop(0)
			
			#Update the next set of best moves.
			self.best_moves = path_to_MoveDir(pac_tile, moves)
			
		else:
			#There is a dead-end path since all possible ways
			#are blocked by ghosts; compute and take an escape route.
			self.escape(pac_tile, ghosts)
			
			
	def escape(self, pac_tile, ghosts):
		'''
		Compute and update an alternate escape route for PacMan since
		its possible moves have been blocked by ghosts.
		
		Keyword arguments:
		pac_tile -- the position of PacMan.
		ghosts -- a list of current Ghost objects invovled in the game.
		
		Return:
		None.
		'''
		
		paths = self.bfs.search(pac_tile, [MazeItem.POWER_DOT, MazeItem.DOT], False, True)
		
		new_path = []
		
		#For every path possible, prune any path which may have a ghost
		#sitting over it.
		for path in paths:

			flag = True			
			
			for ghost in ghosts:
				if ghost.tile() in path:
					flag = False
					break
			if flag:
				new_path.append(path)
				
		#List sentinel.			
		last_min = 10000
		last = None
		
		#Find the minimum path among all free paths.
		for path in new_path:
			if len(path) < last_min:
				last_min = len(path)
				last = path
		
		#If there was at least one minimum path, then update the set
		#of next moves.
		if last:
			last.pop(0)
			self.best_moves = path_to_MoveDir(pac_tile, last)
			
	'''
	This is method decides Pacman's moving direction in the next frame. 
	The parameters representing the maze, ghosts, Pacman, and score 
	after the execution of last frame. 
	In the next frame, the game will call this method to set 
	Pacman's direction and let him move.
	'''
	def calculate_direction(self, maze, ghosts, pac, score):
		
		pac_tile = pac.tile()
		
		#Compute a set of new best moves.
		if not self.best_moves:
			
			coords = self.bfs.search(pac_tile, [MazeItem.POWER_DOT, MazeItem.DOT])
		
			coords.pop(0)
			
			self.best_moves = path_to_MoveDir(pac_tile, coords)
		
		#List of moves that would prove harmful eventually (by presence
		#of ghosts).
		bad_next_move = []
			
		for ghost in ghosts:
			
			state = ghost.state()

			#if a ghost is inactive, don't search for it.
			if state is GhostState.IN_HOUSE:
				
				self.in_house_ghosts[ghost.name()] = 1
			
			#Search for all non-dormant ghosts.
			if state not in [GhostState.IN_HOUSE, GhostState.FLEE, GhostState.FRIGHTEN]:
				
				if not self.in_house_ghosts[ghost.name()]:
					
					#Compute moves towards this ghost.
					moves_towards_ghost = self.bfs.search(pac_tile, [ghost.tile()],True)
					
					#No such move possible, move on to the next one.
					if not moves_towards_ghost:
						continue
					
					moves_towards_ghost.pop(0)
					
					#If a ghost is nearby.
					if len(moves_towards_ghost) <= 6:
						
						#If a ghost is too near, evade as soon as possible.
						if len(moves_towards_ghost) <= 2:
							self.escape(pac_tile, ghosts)
							break
						
						#Else find the direction at which the ghost is proceeding and try to go away from it.	
						direction_vector = PyUtil.get_vector(ghost.dir())
						
						next_tile = PyUtil.vector_add(ghost.tile(), direction_vector)
						
						if next_tile in moves_towards_ghost[len(moves_towards_ghost) - 2 : -1]:
						
							bad_next_move.append(moves_towards_ghost.pop(0))
						
				else:
					#Ghost was in a house moment before and
					#will be out soon.
					self.in_house_ghosts[ghost.name()] = 0
		
		#If we have any bad moves, we've to compute an alternate (second
		#best move) instead and take that approach.
		if bad_next_move:
			
			self.find_alternative(pac_tile, bad_next_move, deepcopy(self.maze_adj), ghosts)
		
		#Return and execute the next move (this list gets dynamically 
		#updated by any method handling moves).
		return self.best_moves.pop(0)
	
	'''
	This method will be called by the game whenever a new level starts.
	The parameters representing the game objects at their initial states.
	This method will always be called before calculate_direction and on_new_life.
	'''
	def on_level_start(self, maze, ghosts, pac, score):
		print "Python Player starts new level!"
		
		self.maze = maze
		
		#Initialize all ghosts to be "in house" before start of game.
		self.in_house_ghosts = {GhostName.Blinky:0, GhostName.Pinky:0,\
		                        GhostName.Inky:0, GhostName.Clyde:0}
		
		#An adjacency list representation of the maze (graph).
		self.maze_adj = {}	
		for row in xrange(1, 22):
			
			for column in xrange(1, 23):
				
				self.maze_adj[(row, column)] = maze.accessible_neighbours((row, column))
				
		#Have a search object ready for this graph (to be used by methods).				
		self.bfs = BFS(self.maze_adj, maze)
		
	'''
	This method will be called by the game whenever Pacman receives a new life,
	including the first life.
	The parameters representing the repositioned game objects. 
	This method will always be called before calculate_direction and after on_level_start.
	'''
	def on_new_life(self, maze, ghosts, pac, score):
		print "Python Player starts new life %d !" % self.lives
		self.lives += 1

'''
Get a list of MoveDir objects which Pacman can use to navigate
itself through a path.
start - the starting tile
path - the path leading out of the starting tile, a list of connected
tiles.
'''
def path_to_MoveDir(start, path):
	MoveDir_list = []
	curr_tile = start
	for next_tile in path:
		dir_vector = PyUtil.vector_sub(next_tile, curr_tile)
		MoveDir_list.append(PyUtil.get_MoveDir(dir_vector))
		curr_tile = next_tile
	return MoveDir_list