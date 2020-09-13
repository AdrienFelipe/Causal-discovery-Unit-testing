import cdt
import networkx as nx

data, graph = cdt.data.load_dataset('sachs')
glasso = cdt.independence.graph.Glasso()
skeleton = glasso.predict(data)
new_skeleton = cdt.utils.graph.remove_indirect_links(skeleton, alg='aracne')
nx.adjacency_matrix(skeleton).todense()

# Causal discovery
model = cdt.causality.graph.GES()
output_graph = model.predict(data, new_skeleton)
print(nx.adjacency_matrix(output_graph).todense())

# Scoring.
scores = [metric(graph, output_graph) for metric in (precision_recall, SID, SHD)]
print(scores)

# now we compute the CAM graph without constraints and the associated scores
model2 = cdt.causality.graph.CAM()
output_graph_nc = model2.predict(data)
scores_nc = [metric(graph, output_graph_nc) for metric in (precision_recall, SID, SHD)]
print(scores_nc)

ff = 4
