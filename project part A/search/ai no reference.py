from search.util import print_slide, print_swing, if_killable, what_targ
from search.node import h, hex_neighbors, hex_dist, init_hexgraph

def bfs(graph, upperL, lowerL, blockL, dist, pred):
    og_graph = {}
    queue = []
    visited = []
    curr = [] # 2D Array of Current Token Locations
    prev = [] # 2D Array of Previous Token Locations
    tokens_ind = [] # Array of Token curr Index
    targ = {"r": [], "s": [], "p": []} # Array of targets
    t = 0 # Turn Counter
    # Addign Targets tp Dictionary
    for lower in lowerL:
        if lower[0] == "s":
            targ["s"].append(lower[1:])
        if lower[0] == "r":
            targ["r"].append(lower[1:])
        if lower[0] == "p":
            targ["p"].append(lower[1:]) 

    npath = min(len(upperL), len(lowerL))
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

    while queue: # While Queue isn't Empty
        # Initiate Visited and Queue
        for ind in tokens_ind:
            if t==0:
                visited[ind][upperL[ind][1:]] = True
                queue[ind].append(upperL[ind])
                dist[ind][upperL[ind][1:]] = 0
                pred[ind][upperL[ind][1:]] = -1
            # Pop from start of queue
            curr[ind] = (queue[ind].pop(0))

        # reset neighbours as current tokens can be different
        graph = init_hexgraph(4)

        for ind in tokens_ind:
            for p in range(0): # hiding swing neighbours
                print("ok")
                #swing_neigh = []
                #curr_upps = []
                # Add avalibale upper tokrns to curr_upps
                #for upps in curr:
                #    curr_upps.append(upps[1:])            
                #for neighbour in graph[curr[ind][1:]]:        
                #    if neighbour in curr_upps:
                #        # ADD NODES INTO GRAPH
                #        swing_neigh = hex_neighbors(neighbour[0], neighbour[1], 4)
                #        for sw_neighbour in swing_neigh:
                #            if (sw_neighbour not in graph[curr[ind][1:]]) and (sw_neighbour != curr[ind][1:]):
                #                graph[curr[ind][1:]].append(sw_neighbour)
            enemy = what_targ(curr[ind][0])
            # CHECK IF CAPTURABLE, IF SO
            if curr[ind][1:] in targ[enemy]:
                mainen = (enemy, curr[ind][1], curr[ind][2])
                targ[enemy].remove(curr[ind][1:])
                lowerL.remove(mainen)
                print(upperL[ind], " HAS TAKEN DOWN TARGET", mainen)
                queue[ind] = [] # reset queue
                #for hexa in graph:
                    #visited[i][hexa] = False
            if not targ[enemy]:
                print("No more Target Enemies")
                tokens_ind.remove(ind)
            if not lowerL:
                print("ALL ENEMIES HAVE BEEN CAPTURED")
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
    crawl = []
    paths = min(len(upperL), len(lowerL))
    
    # Intialising paths
    for p in range(paths):
        #print(lowerL[p][1:])
        crawl.append(lowerL[p][1:])
        path[lowerL[p]] = [crawl[p]]
    
    for p in range(paths):
        t = 0 
        while (pred[p][crawl[p]] != -1):
            path[lowerL[p]].append(pred[p][crawl[p]])
            crawl[p] = pred[p][crawl[p]]
        t+=1
        
        c = 1
        for i in range(len(path[lowerL[p]])-1, -1, -1):
            if path[lowerL[p]][i-1] != path[lowerL[p]][-1]:
                prev = path[lowerL[p]][i]
                curr = path[lowerL[p]][i-1]
                if curr in hex_neighbors(prev[0], prev[1], 4):
                    print_slide(c, prev[0], prev[1], curr[0], curr[1])
                else:
                    print_swing(c, prev[0], prev[1], curr[0], curr[1])
            c += 1