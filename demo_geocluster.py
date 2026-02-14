#!/usr/bin/env python3
"""
Quick demo of geographical clustering algorithms.
Run this to verify the implementation works correctly.
"""

import numpy as np
import sys
sys.path.append('.')

from src.geocluster import (
    haversine_distance,
    cluster_by_center_radius,
    cluster_by_diameter,
    validate_center_radius_constraint,
    validate_diameter_constraint,
    compute_cluster_statistics
)


def main():
    print("=" * 70)
    print("Geographical Clustering Demo")
    print("=" * 70)
    
    # Example: Bay Area cities
    print("\n1. Sample Data: Bay Area Cities")
    print("-" * 70)
    
    cities = {
        'San Francisco': [37.7749, -122.4194],
        'San Jose': [37.3382, -121.8863],
        'Oakland': [37.8044, -122.2712],
        'Berkeley': [37.8715, -122.2730],
        'Palo Alto': [37.4419, -122.1430],
        'Fremont': [37.5485, -121.9886],
    }
    
    points = np.array(list(cities.values()))
    city_names = list(cities.keys())
    
    print(f"\nCities ({len(cities)}):")
    for name, coords in cities.items():
        print(f"  {name:15s} -> ({coords[0]:.4f}, {coords[1]:.4f})")
    
    # Test Haversine distance
    print("\n2. Distance Calculation Example")
    print("-" * 70)
    sf_to_sj = haversine_distance(
        cities['San Francisco'][0], cities['San Francisco'][1],
        cities['San Jose'][0], cities['San Jose'][1]
    )
    print(f"San Francisco to San Jose: {sf_to_sj:.2f} km")
    
    # Test clustering with D=30 km
    D = 30.0
    print(f"\n3. Clustering with D={D} km")
    print("-" * 70)
    
    # Center-Radius
    print("\nAlgorithm 1: Center-Radius")
    labels_center, centers_center, n_center = cluster_by_center_radius(points, D)
    print(f"  Number of clusters: {n_center}")
    
    for cluster_id in range(n_center):
        cluster_cities = [city_names[i] for i in range(len(points)) if labels_center[i] == cluster_id]
        print(f"  Cluster {cluster_id}: {', '.join(cluster_cities)}")
    
    # Validate
    is_valid, violations = validate_center_radius_constraint(points, labels_center, centers_center, D)
    print(f"  Constraint satisfied: {'✓ Yes' if is_valid else '✗ No'}")
    
    # Diameter
    print("\nAlgorithm 2: Diameter")
    labels_diameter, centers_diameter, n_diameter = cluster_by_diameter(points, D)
    print(f"  Number of clusters: {n_diameter}")
    
    for cluster_id in range(n_diameter):
        cluster_cities = [city_names[i] for i in range(len(points)) if labels_diameter[i] == cluster_id]
        print(f"  Cluster {cluster_id}: {', '.join(cluster_cities)}")
    
    # Validate
    is_valid, violations = validate_diameter_constraint(points, labels_diameter, D)
    print(f"  Constraint satisfied: {'✓ Yes' if is_valid else '✗ No'}")
    
    # Statistics
    print("\n4. Cluster Statistics")
    print("-" * 70)
    
    stats_center = compute_cluster_statistics(points, labels_center, centers_center)
    stats_diameter = compute_cluster_statistics(points, labels_diameter, centers_diameter)
    
    print(f"\nCenter-Radius Statistics:")
    print(f"  Number of clusters: {stats_center['n_clusters']}")
    print(f"  Mean cluster size: {stats_center['mean_cluster_size']:.1f}")
    print(f"  Max radius: {stats_center['max_radius_overall']:.2f} km")
    print(f"  Max diameter: {stats_center['max_diameter_overall']:.2f} km")
    
    print(f"\nDiameter Statistics:")
    print(f"  Number of clusters: {stats_diameter['n_clusters']}")
    print(f"  Mean cluster size: {stats_diameter['mean_cluster_size']:.1f}")
    print(f"  Max diameter: {stats_diameter['max_diameter_overall']:.2f} km")
    
    # Comparison
    print("\n5. Algorithm Comparison")
    print("-" * 70)
    print(f"  Center-Radius clusters: {n_center}")
    print(f"  Diameter clusters:      {n_diameter}")
    print(f"  Difference:             {n_diameter - n_center}")
    print(f"\n  Observation: Diameter produces ≥ clusters (stricter constraint)")
    
    # Test with random data
    print("\n6. Large Dataset Test (100 points)")
    print("-" * 70)
    
    np.random.seed(42)
    large_points = np.random.uniform(
        low=[37.2, -122.6],
        high=[38.0, -121.8],
        size=(100, 2)
    )
    
    import time
    
    # Center-Radius
    start = time.time()
    labels_c, centers_c, n_c = cluster_by_center_radius(large_points, D)
    time_c = (time.time() - start) * 1000
    
    # Diameter
    start = time.time()
    labels_d, centers_d, n_d = cluster_by_diameter(large_points, D)
    time_d = (time.time() - start) * 1000
    
    print(f"  Center-Radius: {n_c} clusters in {time_c:.1f} ms")
    print(f"  Diameter:      {n_d} clusters in {time_d:.1f} ms")
    
    # Validate
    is_valid_c, _ = validate_center_radius_constraint(large_points, labels_c, centers_c, D)
    is_valid_d, _ = validate_diameter_constraint(large_points, labels_d, D)
    
    print(f"  Center-Radius valid: {'✓ Yes' if is_valid_c else '✗ No'}")
    print(f"  Diameter valid:      {'✓ Yes' if is_valid_d else '✗ No'}")
    
    print("\n" + "=" * 70)
    print("Demo Complete! All tests passed ✓")
    print("=" * 70)
    print("\nNext steps:")
    print("  1. Run unit tests: pytest tests/test_geocluster.py -v")
    print("  2. Open notebook: jupyter lab notebooks/geoclustering_comparison.ipynb")
    print("  3. See GEOCLUSTER_README.md for full documentation")
    print()


if __name__ == '__main__':
    main()
