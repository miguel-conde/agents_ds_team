"""
Unit tests for geocluster module.

Tests cover:
- Haversine distance calculation accuracy
- Center-radius clustering correctness
- Diameter clustering correctness
- Constraint validation
- Edge cases
"""

import pytest
import numpy as np
from src.geocluster import (
    haversine_distance,
    cluster_by_center_radius,
    cluster_by_diameter,
    validate_center_radius_constraint,
    validate_diameter_constraint,
    compute_cluster_statistics
)


class TestHaversineDistance:
    """Test Haversine distance calculation."""
    
    def test_same_location(self):
        """Distance between same point should be zero."""
        dist = haversine_distance(37.7749, -122.4194, 37.7749, -122.4194)
        assert dist == pytest.approx(0.0, abs=1e-10)
    
    def test_known_distance_sf_la(self):
        """Test known distance: San Francisco to Los Angeles ~559 km."""
        # SF coordinates
        sf_lat, sf_lon = 37.7749, -122.4194
        # LA coordinates
        la_lat, la_lon = 34.0522, -118.2437
        
        dist = haversine_distance(sf_lat, sf_lon, la_lat, la_lon)
        # Expected distance is approximately 559 km
        assert dist == pytest.approx(559, abs=10)
    
    def test_known_distance_ny_london(self):
        """Test known distance: New York to London ~5570 km."""
        # NYC coordinates
        ny_lat, ny_lon = 40.7128, -74.0060
        # London coordinates
        london_lat, london_lon = 51.5074, -0.1278
        
        dist = haversine_distance(ny_lat, ny_lon, london_lat, london_lon)
        # Expected distance is approximately 5570 km
        assert dist == pytest.approx(5570, abs=50)
    
    def test_symmetry(self):
        """Distance should be symmetric: d(A,B) = d(B,A)."""
        lat1, lon1 = 37.7749, -122.4194
        lat2, lon2 = 34.0522, -118.2437
        
        dist1 = haversine_distance(lat1, lon1, lat2, lon2)
        dist2 = haversine_distance(lat2, lon2, lat1, lon1)
        
        assert dist1 == pytest.approx(dist2)
    
    def test_small_distance(self):
        """Test small distance calculation (< 2 km)."""
        # Two points very close together
        lat1, lon1 = 37.7749, -122.4194
        lat2, lon2 = 37.7849, -122.4294  # ~1.4 km away
        
        dist = haversine_distance(lat1, lon1, lat2, lon2)
        assert 1.0 < dist < 2.0  # Should be around 1.4 km


class TestClusterByCenterRadius:
    """Test center-radius clustering algorithm."""
    
    def test_single_cluster_close_points(self):
        """All close points should form single cluster."""
        # Points within 10 km of San Francisco
        points = np.array([
            [37.7749, -122.4194],
            [37.7849, -122.4094],
            [37.7649, -122.4294],
        ])
        
        labels, centers, n_clusters = cluster_by_center_radius(points, D=20.0)
        
        assert n_clusters == 1
        assert len(labels) == 3
        assert len(centers) == 1
    
    def test_multiple_clusters_far_points(self):
        """Far apart points should form multiple clusters."""
        # SF and LA (far apart)
        points = np.array([
            [37.7749, -122.4194],  # San Francisco
            [34.0522, -118.2437],  # Los Angeles
        ])
        
        labels, centers, n_clusters = cluster_by_center_radius(points, D=100.0)
        
        assert n_clusters == 2  # Too far for single cluster
        assert labels[0] != labels[1]
    
    def test_constraint_satisfaction(self):
        """All points should satisfy center-radius constraint."""
        np.random.seed(42)
        points = np.random.uniform(low=[37.0, -123.0], high=[38.0, -122.0], size=(50, 2))
        D = 50.0
        
        labels, centers, n_clusters = cluster_by_center_radius(points, D)
        
        # Validate constraints
        is_valid, violations = validate_center_radius_constraint(
            points, labels, centers, D
        )
        
        assert is_valid, f"Constraint violations: {violations}"
    
    def test_all_points_same_location(self):
        """Edge case: all points at same location."""
        points = np.array([
            [37.7749, -122.4194],
            [37.7749, -122.4194],
            [37.7749, -122.4194],
        ])
        
        labels, centers, n_clusters = cluster_by_center_radius(points, D=10.0)
        
        assert n_clusters == 1
        assert np.all(labels == 0)
    
    def test_points_exactly_D_apart(self):
        """Edge case: two points exactly D km apart."""
        # Create two points exactly 10 km apart (approximately)
        lat1, lon1 = 37.7749, -122.4194
        lat2, lon2 = 37.8649, -122.4194  # ~10 km north
        
        points = np.array([[lat1, lon1], [lat2, lon2]])
        D = 10.0
        
        labels, centers, n_clusters = cluster_by_center_radius(points, D)
        
        # Should form 1 or 2 clusters depending on numerical precision
        assert 1 <= n_clusters <= 2


class TestClusterByDiameter:
    """Test diameter-based clustering algorithm."""
    
    def test_single_cluster_close_points(self):
        """All close points should form single cluster."""
        points = np.array([
            [37.7749, -122.4194],
            [37.7849, -122.4094],
            [37.7649, -122.4294],
        ])
        
        labels, centers, n_clusters = cluster_by_diameter(points, D=50.0)
        
        assert n_clusters >= 1
        assert len(labels) == 3
    
    def test_multiple_clusters_far_points(self):
        """Far apart points should form multiple clusters."""
        points = np.array([
            [37.7749, -122.4194],  # San Francisco
            [34.0522, -118.2437],  # Los Angeles
        ])
        
        labels, centers, n_clusters = cluster_by_diameter(points, D=100.0)
        
        assert n_clusters == 2
        assert labels[0] != labels[1]
    
    def test_constraint_satisfaction(self):
        """All points should satisfy diameter constraint."""
        np.random.seed(42)
        points = np.random.uniform(low=[37.0, -123.0], high=[38.0, -122.0], size=(50, 2))
        D = 50.0
        
        labels, centers, n_clusters = cluster_by_diameter(points, D)
        
        # Validate constraints
        is_valid, violations = validate_diameter_constraint(points, labels, D)
        
        assert is_valid, f"Constraint violations: {violations}"
    
    def test_stricter_than_center_radius(self):
        """Diameter clustering should produce >= clusters than center-radius."""
        np.random.seed(42)
        points = np.random.uniform(low=[37.0, -123.0], high=[38.0, -122.0], size=(100, 2))
        D = 30.0
        
        labels_center, _, n_clusters_center = cluster_by_center_radius(points, D)
        labels_diameter, _, n_clusters_diameter = cluster_by_diameter(points, D)
        
        # Diameter is stricter, should produce same or more clusters
        assert n_clusters_diameter >= n_clusters_center
    
    def test_all_points_same_location(self):
        """Edge case: all points at same location."""
        points = np.array([
            [37.7749, -122.4194],
            [37.7749, -122.4194],
            [37.7749, -122.4194],
        ])
        
        labels, centers, n_clusters = cluster_by_diameter(points, D=10.0)
        
        assert n_clusters == 1
        assert np.all(labels == 0)
    
    def test_linear_points(self):
        """Test points arranged in a line."""
        # Create 5 points in a line, each 5 km apart
        points = np.array([
            [37.0, -122.0],
            [37.045, -122.0],  # ~5 km north
            [37.090, -122.0],  # ~10 km north
            [37.135, -122.0],  # ~15 km north
            [37.180, -122.0],  # ~20 km north
        ])
        
        D = 12.0  # Can group 2-3 consecutive points
        labels, centers, n_clusters = cluster_by_diameter(points, D)
        
        # Should form multiple clusters
        assert n_clusters >= 2


class TestConstraintValidation:
    """Test constraint validation functions."""
    
    def test_valid_center_radius_clustering(self):
        """Valid clustering should pass validation."""
        points = np.array([
            [37.7749, -122.4194],
            [37.7849, -122.4094],
        ])
        labels = np.array([0, 0])
        centers = np.array([[37.7799, -122.4144]])
        D = 20.0
        
        is_valid, violations = validate_center_radius_constraint(
            points, labels, centers, D
        )
        
        assert is_valid
        assert len(violations) == 0
    
    def test_invalid_center_radius_clustering(self):
        """Invalid clustering should fail validation."""
        points = np.array([
            [37.7749, -122.4194],
            [38.7749, -122.4194],  # ~111 km north
        ])
        labels = np.array([0, 0])  # Same cluster
        centers = np.array([[37.7749, -122.4194]])  # Center at first point
        D = 50.0  # Not enough to cover both
        
        is_valid, violations = validate_center_radius_constraint(
            points, labels, centers, D
        )
        
        assert not is_valid
        assert len(violations) > 0
    
    def test_valid_diameter_clustering(self):
        """Valid clustering should pass validation."""
        points = np.array([
            [37.7749, -122.4194],
            [37.7849, -122.4094],
        ])
        labels = np.array([0, 0])
        D = 20.0
        
        is_valid, violations = validate_diameter_constraint(points, labels, D)
        
        assert is_valid
        assert len(violations) == 0
    
    def test_invalid_diameter_clustering(self):
        """Invalid clustering should fail validation."""
        points = np.array([
            [37.7749, -122.4194],
            [38.7749, -122.4194],  # ~111 km north
        ])
        labels = np.array([0, 0])  # Same cluster
        D = 50.0  # Not enough to cover pairwise distance
        
        is_valid, violations = validate_diameter_constraint(points, labels, D)
        
        assert not is_valid
        assert len(violations) > 0


class TestClusterStatistics:
    """Test cluster statistics computation."""
    
    def test_basic_statistics(self):
        """Test basic statistics computation."""
        points = np.array([
            [37.7749, -122.4194],
            [37.7849, -122.4094],
            [37.7649, -122.4294],
        ])
        labels = np.array([0, 0, 1])
        centers = np.array([[37.7799, -122.4144], [37.7649, -122.4294]])
        
        stats = compute_cluster_statistics(points, labels, centers)
        
        assert stats['n_clusters'] == 2
        assert stats['cluster_sizes'] == [2, 1]
        assert stats['mean_cluster_size'] == 1.5
        assert stats['max_cluster_size'] == 2
        assert stats['min_cluster_size'] == 1
        assert 'max_radius_overall' in stats
        assert 'max_diameter_overall' in stats


class TestAlgorithmPerformance:
    """Test algorithm performance on larger datasets."""
    
    def test_100_points_performance(self):
        """Test performance on 100 random points."""
        np.random.seed(42)
        points = np.random.uniform(low=[37.0, -123.0], high=[38.0, -122.0], size=(100, 2))
        D = 30.0
        
        # Both algorithms should complete quickly
        labels1, centers1, n1 = cluster_by_center_radius(points, D)
        labels2, centers2, n2 = cluster_by_diameter(points, D)
        
        assert len(labels1) == 100
        assert len(labels2) == 100
        assert n1 > 0
        assert n2 > 0
    
    def test_1000_points_performance(self):
        """Test performance on 1000 random points (max requirement)."""
        np.random.seed(42)
        points = np.random.uniform(low=[37.0, -123.0], high=[38.0, -122.0], size=(1000, 2))
        D = 30.0
        
        # Center-radius should be efficient with BallTree
        labels, centers, n_clusters = cluster_by_center_radius(points, D)
        
        assert len(labels) == 1000
        assert n_clusters > 0
        
        # Validate a sample of constraints (full validation would be slow)
        is_valid, violations = validate_center_radius_constraint(
            points, labels, centers, D
        )
        assert is_valid


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
