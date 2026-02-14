Solve this geographical clusterizzation problem:

We have N < 1000 points defined by their geographical coordinates (latitude and longitude). 
We want to cluster these points into the minimal number of clusters such that
the maximum radius of any cluster does not exceed a given distance D.

Distance metric: Haversine (great-circle) for lat/lon accuracy

Radius definition. 2 possibiliies:

    - Max distance from cluster center
    - Max pairwise distance within cluster (diameter)

Provide a solution approach for both possibilities.


