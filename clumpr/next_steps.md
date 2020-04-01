# Other Clustering Methods
There is another clustering method that is possible. For an event that is a child of some mapping node involving g, it has two mapping node children involving g' and g'' (for an SDT event). So for two events that are siblings (both events involving g), we can compare them by adding up the PDV entries of their children (or by looking at the average event support within the MPRs rooted at their children). In both cases, it is probably wise to weight these measurements by the number of MPRs in the subgraph rooted at each mapping node.

This induces a measurement (although not a true metric) between events in the recon graph. If we compute this metric between every possible pair of events (events that are not siblings cannot be compared), this can be thought of as a graph, where the nodes are events and the edges are weighted with the distance between the events that they connect. This graph will have one fully connected component for each level of the recon graph.

The user can then input a number k, which is not exactly the number of clusters, but denotes the number of new components to create. We then apply the MST clustering algorithm. This works by taking a graph, sorting its edges from smallest to largest weight, then inserting edges in increasing order until there are k components (or equivalently removing the edge of largest weight until there are k components). In this case, we remove or insert edges until there are k+h components, where h is the height of the recon graph (the number of initial components before changing any edges).

Because there are k new components, some of the initial fully connected components have been divided into multiple components, which can be thought of as sets of events. This functions like a decision tree for MPRs, with one cluster of MPRs corresponding to a choice of components. A given MPR is in that cluster if its events on every level fall within the set of events for each component of the cluster. For example, assume that the user specified 3 extra components for a recon graph with 4 levels. Say that the components for level 1 and 3 were not separated at all, but the component for level 2 was broken in two and the component for level 4 was broken into 3 pieces for 3 total additional components, as specified. This induces at most 6 total clusters, with each cluster having one choice of an event set in level 2, and one choice in level 4.

"At most" is because these might not all be possible. Some of the events in level 4 may not be reachable from some events in level 2. This means that it is possible that one of the clusterings does not actually contain any MPRs because its choices of events are not reachable from each other. In order to compute various metrics over the clustering, we can produce a reconciliation graph for each cluster by taking a subset of the whole recon graph and only including the events that are within that cluster.

This clustering method has the advantages that it is not depth-limited, the resulting clustering is a true partition of MPR-space, and it can be computed relatively efficiently (since the DP table resulting from computing the PDV already contains all of the information that is required for populating the edges). The main disadvantage is that there is no easy way to control the actual number of clusters that will be produced.

# Extensions to Hierarchical Method

## Different Improvement Statistics
The improvement is not a very fair measurement to use when determining the true number of clusters. This can be seen by making an idealized assumption: assume for the moment that when two clusters are induced, each cluster contains half the number of MPRs of its parent graph. Now, when we divide a cluster in two and the pairwise distance goes down by half in each child, we get an improvement of 2. If we then divide this further into 3 clusters and the pairwise distance goes down by half in each child, we only get an improvement of 1.33. This is unfair to the second clustering operation because it accomplished the exact same amount of improvement as the first clustering operation, but it did not attain the same improvement score. Naively, since it is only clustering a graph with half as many MPRs, it will only have half as much of an impact.

Now let's return to the real world where things are not as balanced. We are interested in determining the true number of clusters, and to do that one natural thing to do is to threshold the improvement. Once the improvement of adding a cluster falls below the threshold, we will say that that is the true number of clusters and stop. The earlier argument say that the threshold should be "adaptive", or based on how much improvement we could reasonably expect, given the size of the cluster that is being broken apart.

One way to do this is to calculate improvement in a different way. When we calculate the improvement from two clusters to one cluster, we compute the Weighted Average Score (WAS) for the two clusters and the WAS for one cluster (which is really just the score) and find the ratio. When going from three to two clusters, we can compute the WAS for the clusters that were merged, and divide by the WAS for the cluster that they were merged into (without respect to any of the other clusters). It's possible that maximizing this ratio is equivalent to maximizing the total WAS when computing the clustering, but that doesn't really matter: this is mostly useful for evaluation.

This idea supports the intuition of true clusters. If a bimodal distribution is broken up into two unimodal distributions, that will typically be a big win under this understanding of improvement even if it is modest under the old understanding because the change was made smaller by taking an average over all of the existing clusters. That's as it should be because breaking up a bimodal distribution seems intuitively like evidence that the algorithm found a true cluster.

## Revisiting S1-S2 Comparison
Previous plots showed that when we obtain a clustering using one objective and then evaluate it based on both objectives, there is a slight positive correlation between the improvements of the two objectives, but not a strong correlation. That experimental result was designed to test whether one objective can be used as a proxy for another objective. If the two improvements are highly correlated, then maximizing one will usually maximize the other. However, it is possible for the two improvements not to be highly correlated but for the objectives to still result in the same clustering. The naive way to measure this would be to compare the improvement scores for clusterings generated with both metrics. This in some way corresponds to the distance between the points for a given family (one on the plot generated using support and the other on the plot generated using pairwise distance).
If it turns out that each of the points are actually on top of each other (so that despite the improvements not correlating, each metric still induced the same clusterings), then that is strong evidence that the two objectives proxy each other.

More fundamental is a notion of distance between two clusterings. To do that, we can look at the distance between two recon graphs as some generalization of the symmetric set distance (i.e. the number of nodes that are present in one recon graph but not the other). This might be simplistic, but it is actually a true metric. Now to find the distance between two clusterings, we find the pairing (a bijection between the clusters from one group and the clusters from the other) that induces the least total distance and the sum of the distances of that pairing is the distance between the two clusterings. Note that this is also a true metric if the distance used is a metric: this means that the choice of metric could be something other than symmetric set difference as long as it has the metric properties. Now there is a way to actually compare our two metrics -- by looking at the average distance between the clusterings that they produce. If maximizing one objective is the same as maximizing the other objective, then we expect the average clustering distance to be low (and vice versa).
