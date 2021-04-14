import sys
import json

from search.util import read_board, print_board, print_slide, print_swing, if_killable
from search.node import hex_dist, init_hexgraph, hex_neighbors, h, find_important_tok
from search.ai import bfs, print_shortest_path

def main():
    try:
        with open(sys.argv[1]) as file:
            data = json.load(file)
    except IndexError:
        print("usage: python3 -m search path/to/input.json", file=sys.stderr)
        sys.exit(1)

    # Initialises Hexagon Board with Slide Neighbors
    graph = init_hexgraph(4)
    
    # Converts the Data read from Json file into readable Board Layout
    board = read_board(data)
    upp_toks = []
    low_toks = []
    blok_toks = []
    dist = []
    pred = []
    find_important_tok(data["upper"], data["lower"], upp_toks, low_toks)

    for blok in data["block"]:
        blok_toks.append((blok[1], blok[2]))

    bfs(graph, upp_toks, low_toks, blok_toks, dist, pred)
    find_important_tok(data["upper"], data["lower"], upp_toks, low_toks)
    print_shortest_path(graph, upp_toks, low_toks, blok_toks, dist, pred)