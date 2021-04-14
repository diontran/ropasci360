from search.util import print_slide, print_swing, if_killable, what_targ
from search.node import h, hex_neighbors, hex_dist, init_hexgraph

def bfs(graph, upperL, lowerL, blockL, dist, pred):
    queue = [] # 2D Array for queue
    visited = [] # 2D Array to keep track of visited Nodes
    curr = [] # 2D Array of Current Token Locations
    prev = [] # 2D Array of Previous Token Locations
    tokens_ind = [] # Array of Token curr Index
    targ = {"r": [], "s": [], "p": []} # Array of targets
    t = 0 # Turn Counter
    npath = min(len(upperL), len(lowerL)) # Number of Paths
    # Addign Targets to Dictionary
    for lower in lowerL:
        if lower[0] == "s":
            targ["s"].append(lower[1:])
        if lower[0] == "r":
            targ["r"].append(lower[1:])
        if lower[0] == "p":
            targ["p"].append(lower[1:]) 
    # Create 2D Arrays and Dictionaries
    for i in range(npath):
        queue.append([])
        curr.append([])
        prev.append([])
        visited.append({})
        dist.append({})
        pred.append({})
        tokens_ind.append(i)
        for hexa in graph:
            visited[i][hexa] = False
            dist[i][hexa] = 10000
            pred[i][hexa] = -1
    # While Queue isn't Empty
    while queue: 
        # Initiate Visited and Queue
        for ind in tokens_ind:
            if t==0:
                visited[ind][upperL[ind][1:]] = True
                queue[ind].append(upperL[ind])
                dist[ind][upperL[ind][1:]] = 0
                pred[ind][upperL[ind][1:]] = -1
            # Pop from start of queue
            if not queue[ind]:
                lowerL.pop(0)
                return True
            curr[ind] = (queue[ind].pop(0))

        # reset neighbours as current tokens can be different
        graph = init_hexgraph(4)
        for ind in tokens_ind:
            # CHECK IF SWINGABLE AND ADD TO POSSIBLE NEIGHBOURS
            swing_neigh = []
            curr_upps = []
            for upps in curr:
                curr_upps.append(upps[1:])            
            for neighbour in graph[curr[ind][1:]]:        
                if neighbour in curr_upps:
                    # ADD NODES INTO GRAPH
                    swing_neigh = hex_neighbors(neighbour[0], neighbour[1], 4)
                    for sw_neighbour in swing_neigh:
                        if (sw_neighbour not in graph[curr[ind][1:]]) and (sw_neighbour != curr[ind][1:]):
                            graph[curr[ind][1:]].append(sw_neighbour)
            enemy = what_targ(curr[ind][0])
            # CHECK IF CAPTURABLE, IF SO
            if curr[ind][1:] in targ[enemy]:
                mainen = (enemy, curr[ind][1], curr[ind][2])
                targ[enemy].remove(curr[ind][1:])
                lowerL.remove(mainen)
                queue[ind] = [] # reset queue
            if not targ[enemy]:
                tokens_ind.remove(ind)
            if not lowerL:
                return True

            for neighbour in graph[curr[ind][1:]]:
                nT = (upperL[ind][0], neighbour[0], neighbour[1])
                if visited[ind][neighbour] == False: # If neighbour not visited

                    if neighbour not in blockL: # If neighbour also not a block.
                        visited[ind][neighbour] = True
                        # Add to visited and queue
                        queue[ind].append(nT)
                        dist[ind][neighbour] = (dist[ind][curr[ind][1:]]) + 1
                        pred[ind][neighbour] = curr[ind][1:]

                        if not lowerL:
                            return True
            # Keep track of previous node
            prev[ind] = curr[ind]
        t+=1

def print_shortest_path(graph, upperL, lowerL, blockL, dist, pred):
    path = {}
    ord_path = {}
    crawl = []
    paths = min(len(upperL), len(lowerL)) # numnber of paths
    pathl = 0 # largest path length

    # Intialising paths
    for p in range(paths):
        crawl.append(lowerL[p][1:])
        path[lowerL[p]] = [crawl[p]]
        ord_path[lowerL[p]] = [crawl[p]]
    # Adding Predecessors to paths and ordering.
    for p in range(paths):
        while (pred[p][crawl[p]] != -1):
            path[lowerL[p]].append(pred[p][crawl[p]])
            crawl[p] = pred[p][crawl[p]]
            pathl = max(pathl, len(path[lowerL[p]]))
        for i in range(pathl-1, -1, -1):
            if path[lowerL[p]][i]:
                ord_path[lowerL[p]].append(path[lowerL[p]][i])
    # Printing out pathways
    for i in range(1, pathl):
        for p in range(paths):
            if i+1 < len(ord_path[lowerL[p]]):
                prev = ord_path[lowerL[p]][i]
                curr = ord_path[lowerL[p]][i+1]
                if curr in hex_neighbors(prev[0], prev[1], 4):    
                    print_slide(i, prev[0], prev[1], curr[0], curr[1])
                else:
                    print_swing(i, prev[0], prev[1], curr[0], curr[1])