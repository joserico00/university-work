import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter
from scapy.all import sniff

def process_packet(packet):
    if packet.haslayer('IP'):
        src_ip = packet['IP'].src
        dst_ip = packet['IP'].dst
        edges.append((src_ip, dst_ip))

def create_graph(edges):
    G = nx.DiGraph()

    # Add nodes and edges to the graph
    for edge in edges:
        src, dst = edge
        if G.has_edge(src, dst):
            G[src][dst]["weight"] += 1
        else:
            G.add_edge(src, dst, weight=1)

    return G

def draw_graph(G):
    pos = nx.spring_layout(G, k=0.3, iterations=50)
    weights = nx.get_edge_attributes(G, "weight")
    labels = {k: f"{k}\n({v})" for k, v in Counter(weights.values()).items()}

    nx.draw_networkx_nodes(G, pos, node_size=700)
    nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")
    nx.draw_networkx_edges(G, pos, edgelist=weights.keys(), width=[v * 0.1 for v in weights.values()])
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8)

    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    edges = []

    # Sniff packets for 60 seconds and call process_packet for each packet
    sniff(prn=process_packet, filter="ip", timeout=60)

    G = create_graph(edges)
    draw_graph(G)
