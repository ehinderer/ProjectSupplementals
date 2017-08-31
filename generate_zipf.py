import gocats.gocats as gc
import re
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np 

go_graph = gc.build_graph_interpreter('/home/eugene/go.obo')
cc_graph = gc.build_graph_interpreter('/home/eugene/go.obo', supergraph_namespace='cellular_component')
bp_graph = gc.build_graph_interpreter('/home/eugene/go.obo', supergraph_namespace='biological_process')
mf_graph = gc.build_graph_interpreter('/home/eugene/go.obo', supergraph_namespace='molecular_function')

def corpus_count(graph):
    count_dict = Counter()
    wordRE = re.compile('\w+')
    corpus = list()
    for node in graph.node_list:
        corpus.extend(re.findall(wordRE, node.definition))
        corpus.extend(re.findall(wordRE, node.name))
    for word in corpus:
        count_dict[word] += 1
    return count_dict

def plot_zipf(count_dict, plot_label, position=None):
    if position:
        plt.subplot(position)
    tokens = list()
    counts = list()
    for token_count in count_dict.most_common(len(count_dict)):
        tokens.append(token_count[0])
        counts.append(token_count[1])
    plt.scatter(np.arange(1., len(tokens)+1), np.array(counts))  # Inserting data into scatter plot
    plt.yscale('log')
    plt.xscale('log')
    plt.axis([0, len(tokens), 0, max(counts)])
    plt.xlabel("Word rank")
    plt.ylabel("Absolute word frequency")
    plt.title("Zipf distribution of the {} corpus".format(plot_label))

go_count = corpus_count(go_graph)
cc_count = corpus_count(cc_graph)
bp_count = corpus_count(bp_graph)
mf_count = corpus_count(mf_graph)

plt.figure(1)
plot_zipf(go_count, "entire GO", 221)
plot_zipf(cc_count, "cellular component", 222)
plot_zipf(bp_count, "biological process", 223)
plot_zipf(mf_count, "molecular function", 224)
plt.show()
