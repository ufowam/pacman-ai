class BFS:
    '''
    A graph object to compute a custom version of Breadth First Search which
    returns the shortest path requested for (to a node, or a kind of node) or
    a list of paths -- see search().
    '''
    
    def __init__(self, adj, maze):
	
        self.adjacency = adj
        self.maze = maze

    def search(self, start, items, ghost=False, all_paths=False):
    	'''
	Perform a custom BFS search on the graph.
	
	Keyword arguments:
	start -- the start node.
	items -- a list of items to look for (and stop searching beyond).
	ghost -- True if searching for a ghost object (search if performed on
		vertices of ghost positions).
	all_paths -- True if searching for a set of paths that lead to closest
			items for each direction available from start.
			
	Return:	
	'''
    
    	#Flags to check if a node has been visited yet.
    	colors = {}
	
	last_discovered = None
	
	paths = []
        
        graph = self.adjacency

	colors[start] = 1
    
        # maintain a queue of paths
        queue = []
        
        # push the first path into the queue
        queue.append([start])
        
        while queue:
            
            # get the first path from the queue
            path = queue.pop(0)	    
            
            # get the last node from the path
            node = path[-1]
                        
	    #Compute all set of paths.
	    if all_paths:
		if self.maze.get_tile_item(node) in items:
			paths.append(path)
            
            #Check if the kind of tile item is any one of the ones being
	    #looked for.
            elif not ghost:
		if self.maze.get_tile_item(node) in items:
		    return path
		
	    #Match any of the given coordinates.
	    else:
		if node in items:
		    return path
            
            # enumerate all adjacent nodes, construct a new path and push it into the queue
            for adjacent in graph.get(node, []):
		if all_paths:
		    if not colors.has_key(adjacent) and self.maze.get_tile_item(node) not in items:
		
			colors[adjacent] = 1
			new_path = list(path)
			new_path.append(adjacent)
			queue.append(new_path)
		else:
		    if not colors.has_key(adjacent):
				    
			colors[adjacent] = 1
			new_path = list(path)
			new_path.append(adjacent)
			queue.append(new_path)		    
		    
	if all_paths:
	    return paths