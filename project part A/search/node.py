from search.util import print_slide, print_swing, if_killable, what_targ



def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def hex_dist(x, y):
    z = -x-y
    return max(abs(x), abs(y), abs(z))

def hex_neighbors(x,y,n):
    neigh_list = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if not (i == 0 and j == 0): # Not itself
                if hex_dist(x,y)<(n+1): # Inside Range
                    if hex_dist(x+i,y+j)<(n+1):
                        neigh_list.append((x+i,y+j))
    return neigh_list

def init_hexgraph(n):
    graph = {}
    for x in range(-n, n+1):
        for y in range(-n, n+1):
            nlist = hex_neighbors(x, y, n)
            graph[(x, y)] = nlist
    return graph

def find_important_tok(uppdata, lowdata, upplist, lowlist):
    for upp in uppdata:
        for low in lowdata:
            if if_killable(upp[0], low[0]):
                lowlist.append((low[0], low[1], low[2]))
                cupp = (upp[0], upp[1], upp[2])
                if cupp not in upplist:
                    upplist.append((cupp))