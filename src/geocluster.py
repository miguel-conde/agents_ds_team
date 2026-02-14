"""
Geographical Clustering Module

This module provides algorithms for clustering geographical points (lat/lon) 
with maximum radius constraints using Haversine distance.

Two clustering approaches:
1. Center-Radius: Max distance from center to any point ≤ D
2. Diameter: Max pairwise distance within cluster ≤ D
"""

import numpy as np
from typing import Tuple, List
from sklearn.neighbors import BallTree


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on Earth.
    
    Uses the Haversine formula to compute distance in kilometers.
    
    Parameters
    ----------
    lat1, lon1 : float
        Latitude and longitude of first point in decimal degrees
    lat2, lon2 : float
        Latitude and longitude of second point in decimal degrees
        
    Returns
    -------
    float
        Distance in kilometers
        
    References
    ----------
    Haversine formula: https://en.wikipedia.org/wiki/Haversine_formula
    """
    # Earth radius in kilometers
    R = 6371.0
    
    # Convert decimal degrees to radians
    lat1_rad = np.radians(lat1)
    lon1_rad = np.radians(lon1)
    lat2_rad = np.radians(lat2)
    lon2_rad = np.radians(lon2)
    
    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = np.sin(dlat/2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    
    distance = R * c
    return distance


def haversine_distance_matrix(points: np.ndarray) -> np.ndarray:
    """
    Compute pairwise Haversine distances for all points.
    
    Parameters
    ----------
    points : np.ndarray
        Array of shape (n_points, 2) with columns [lat, lon]
        
    Returns
    -------
    np.ndarray
        Distance matrix of shape (n_points, n_points)
    """
    n = len(points)
    distances = np.zeros((n, n))
    
    for i in range(n):
        for j in range(i+1, n):
            dist = haversine_distance(
                points[i, 0], points[i, 1],
                points[j, 0], points[j, 1]
            )
            distances[i, j] = dist
            distances[j, i] = dist
            
    return distances


def cluster_by_center_radius(
    points: np.ndarray, 
    D: float
) -> Tuple[np.ndarray, np.ndarray, int]:
    """
    Cluster points where max distance from center to any point ≤ D.
    
    Uses greedy farthest-first algorithm with BallTree for efficiency.
    Guarantees that every point in a cluster is within distance D from
    the cluster center.
    
    Algorithm:
    1. Start with unclustered points
    2. Pick an unclustered point as new center
    3. Assign all unclustered points within radius D to this cluster
    4. Repeat until all points are clustered
    
    Time Complexity: O(n * k * log(n)) where k is number of clusters
    
    Parameters
    ----------
    points : np.ndarray
        Array of shape (n_points, 2) with columns [lat, lon] in decimal degrees
    D : float
        Maximum radius in kilometers
        
    Returns
    -------
    cluster_labels : np.ndarray
        Array of shape (n_points,) with cluster assignments (0 to k-1)
    cluster_centers : np.ndarray
        Array of shape (n_clusters, 2) with [lat, lon] of centers
    n_clusters : int
        Number of clusters created
        
    Examples
    --------
    >>> points = np.array([[37.7749, -122.4194], [37.7849, -122.4094]])
    >>> labels, centers, n = cluster_by_center_radius(points, D=10.0)
    """
    n_points = len(points)
    cluster_labels = -np.ones(n_points, dtype=int)
    cluster_centers_list = []
    current_cluster = 0
    
    # Convert points to radians for BallTree (expects lat, lon in radians)
    points_rad = np.radians(points)
    
    while np.any(cluster_labels == -1):
        # Find first unclustered point as new center
        unclustered_mask = cluster_labels == -1
        unclustered_indices = np.where(unclustered_mask)[0]
        
        # Pick first unclustered point as center
        center_idx = unclustered_indices[0]
        center_point = points[center_idx]
        cluster_centers_list.append(center_point)
        
        # Build BallTree with unclustered points for efficient radius query
        unclustered_points_rad = points_rad[unclustered_mask]
        tree = BallTree(unclustered_points_rad, metric='haversine')
        
        # Query points within radius D (convert to radians for haversine)
        # haversine metric in BallTree uses unit sphere, multiply by Earth radius
        center_rad = points_rad[center_idx:center_idx+1]
        indices = tree.query_radius(center_rad, r=D/6371.0)[0]
        
        # Map back to original indices
        original_indices = unclustered_indices[indices]
        cluster_labels[original_indices] = current_cluster
        
        current_cluster += 1
    
    cluster_centers = np.array(cluster_centers_list)
    return cluster_labels, cluster_centers, current_cluster


def cluster_by_diameter(
    points: np.ndarray, 
    D: float
) -> Tuple[np.ndarray, np.ndarray, int]:
    """
    Cluster points where max pairwise distance within cluster ≤ D.
    
    Uses constrained greedy algorithm with pairwise distance checking.
    This is stricter than center-radius and typically produces more clusters.
    
    Algorithm:
    1. Start with unclustered points
    2. Pick an unclustered point to start new cluster
    3. Greedily add points that maintain diameter constraint
    4. Repeat until all points are clustered
    
    Time Complexity: O(n^2 * k) worst case, where k is number of clusters
    
    Parameters
    ----------
    points : np.ndarray
        Array of shape (n_points, 2) with columns [lat, lon] in decimal degrees
    D : float
        Maximum diameter (pairwise distance) in kilometers
        
    Returns
    -------
    cluster_labels : np.ndarray
        Array of shape (n_points,) with cluster assignments (0 to k-1)
    cluster_centers : np.ndarray
        Array of shape (n_clusters, 2) with [lat, lon] of cluster centroids
    n_clusters : int
        Number of clusters created
        
    Examples
    --------
    >>> points = np.array([[37.7749, -122.4194], [37.7849, -122.4094]])
    >>> labels, centers, n = cluster_by_diameter(points, D=10.0)
    """
    n_points = len(points)
    cluster_labels = -np.ones(n_points, dtype=int)
    cluster_centers_list = []
    current_cluster = 0
    
    # Precompute distance matrix for efficiency
    dist_matrix = haversine_distance_matrix(points)
    
    while np.any(cluster_labels == -1):
        # Find first unclustered point to start new cluster
        unclustered_mask = cluster_labels == -1
        unclustered_indices = np.where(unclustered_mask)[0]
        
        # Start new cluster with first unclustered point
        seed_idx = unclustered_indices[0]
        cluster_points = [seed_idx]
        cluster_labels[seed_idx] = current_cluster
        
        # Try to add more points to this cluster
        for candidate_idx in unclustered_indices[1:]:
            # Check if adding this point violates diameter constraint
            max_dist_to_cluster = max(
                dist_matrix[candidate_idx, pt_idx] for pt_idx in cluster_points
            )
            
            if max_dist_to_cluster <= D:
                cluster_points.append(candidate_idx)
                cluster_labels[candidate_idx] = current_cluster
        
        # Compute cluster centroid (mean position)
        cluster_coords = points[cluster_points]
        centroid = np.mean(cluster_coords, axis=0)
        cluster_centers_list.append(centroid)
        
        current_cluster += 1
    
    cluster_centers = np.array(cluster_centers_list)
    return cluster_labels, cluster_centers, current_cluster


def validate_center_radius_constraint(
    points: np.ndarray,
    cluster_labels: np.ndarray,
    cluster_centers: np.ndarray,
    D: float,
    tolerance: float = 1e-6
) -> Tuple[bool, List[str]]:
    """
    Validate that center-radius constraint is satisfied.
    
    Checks that every point is within distance D from its cluster center.
    
    Parameters
    ----------
    points : np.ndarray
        Original points array of shape (n_points, 2)
    cluster_labels : np.ndarray
        Cluster assignments
    cluster_centers : np.ndarray
        Cluster centers
    D : float
        Maximum radius in kilometers
    tolerance : float
        Numerical tolerance for constraint checking
        
    Returns
    -------
    is_valid : bool
        True if all constraints satisfied
    violations : List[str]
        List of constraint violation messages
    """
    violations = []
    
    for cluster_id in range(len(cluster_centers)):
        cluster_mask = cluster_labels == cluster_id
        cluster_points = points[cluster_mask]
        center = cluster_centers[cluster_id]
        
        for i, point in enumerate(cluster_points):
            dist = haversine_distance(
                point[0], point[1],
                center[0], center[1]
            )
            
            if dist > D + tolerance:
                violations.append(
                    f"Cluster {cluster_id}, point {i}: "
                    f"distance {dist:.3f} km > D={D} km"
                )
    
    return len(violations) == 0, violations


def validate_diameter_constraint(
    points: np.ndarray,
    cluster_labels: np.ndarray,
    D: float,
    tolerance: float = 1e-6
) -> Tuple[bool, List[str]]:
    """
    Validate that diameter constraint is satisfied.
    
    Checks that all pairwise distances within each cluster are ≤ D.
    
    Parameters
    ----------
    points : np.ndarray
        Original points array of shape (n_points, 2)
    cluster_labels : np.ndarray
        Cluster assignments
    D : float
        Maximum diameter in kilometers
    tolerance : float
        Numerical tolerance for constraint checking
        
    Returns
    -------
    is_valid : bool
        True if all constraints satisfied
    violations : List[str]
        List of constraint violation messages
    """
    violations = []
    n_clusters = len(np.unique(cluster_labels))
    
    for cluster_id in range(n_clusters):
        cluster_mask = cluster_labels == cluster_id
        cluster_points = points[cluster_mask]
        
        # Check all pairwise distances
        n = len(cluster_points)
        for i in range(n):
            for j in range(i+1, n):
                dist = haversine_distance(
                    cluster_points[i, 0], cluster_points[i, 1],
                    cluster_points[j, 0], cluster_points[j, 1]
                )
                
                if dist > D + tolerance:
                    violations.append(
                        f"Cluster {cluster_id}, points {i}-{j}: "
                        f"distance {dist:.3f} km > D={D} km"
                    )
    
    return len(violations) == 0, violations


def compute_cluster_statistics(
    points: np.ndarray,
    cluster_labels: np.ndarray,
    cluster_centers: np.ndarray
) -> dict:
    """
    Compute statistics about the clustering result.
    
    Parameters
    ----------
    points : np.ndarray
        Original points array
    cluster_labels : np.ndarray
        Cluster assignments
    cluster_centers : np.ndarray
        Cluster centers
        
    Returns
    -------
    dict
        Statistics including cluster sizes, max radii, max diameters
    """
    n_clusters = len(cluster_centers)
    cluster_sizes = []
    max_radii = []
    max_diameters = []
    
    for cluster_id in range(n_clusters):
        cluster_mask = cluster_labels == cluster_id
        cluster_points = points[cluster_mask]
        cluster_sizes.append(len(cluster_points))
        
        # Compute max radius (distance from center)
        center = cluster_centers[cluster_id]
        radii = [
            haversine_distance(pt[0], pt[1], center[0], center[1])
            for pt in cluster_points
        ]
        max_radii.append(max(radii) if radii else 0.0)
        
        # Compute max diameter (max pairwise distance)
        n = len(cluster_points)
        diameters = []
        for i in range(n):
            for j in range(i+1, n):
                dist = haversine_distance(
                    cluster_points[i, 0], cluster_points[i, 1],
                    cluster_points[j, 0], cluster_points[j, 1]
                )
                diameters.append(dist)
        max_diameters.append(max(diameters) if diameters else 0.0)
    
    return {
        'n_clusters': n_clusters,
        'cluster_sizes': cluster_sizes,
        'mean_cluster_size': np.mean(cluster_sizes),
        'max_cluster_size': max(cluster_sizes),
        'min_cluster_size': min(cluster_sizes),
        'max_radii': max_radii,
        'max_radius_overall': max(max_radii) if max_radii else 0.0,
        'max_diameters': max_diameters,
        'max_diameter_overall': max(max_diameters) if max_diameters else 0.0,
    }
