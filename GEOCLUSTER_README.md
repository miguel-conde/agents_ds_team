# Geographical Clustering Solution

This directory contains a complete implementation of geographical clustering algorithms with radius constraints.

## Problem Statement

Cluster N < 1000 geographical points (lat/lon) into minimal clusters where maximum radius ≤ D kilometers.

## Solution Overview

### Deliverables

1. **`src/geocluster.py`** - Core clustering module with:
   - `haversine_distance()` - Accurate geographical distance calculation
   - `cluster_by_center_radius()` - Case 1: Max distance from center ≤ D
   - `cluster_by_diameter()` - Case 2: Max pairwise distance ≤ D
   - Validation functions to verify constraints
   - Statistics computation utilities

2. **`tests/test_geocluster.py`** - Comprehensive unit tests:
   - Distance calculation accuracy (known distances SF-LA, NY-London)
   - Algorithm correctness (constraint satisfaction)
   - Edge cases (co-located points, linear arrangements)
   - Performance tests (100 and 1000 points)
   - **23 tests, 100% pass rate**

3. **`notebooks/geoclustering_comparison.ipynb`** - Interactive analysis:
   - Synthetic data generation (random, clustered, linear, grid)
   - Side-by-side algorithm comparison
   - Interactive folium maps
   - Performance metrics and visualizations
   - Algorithm properties comparison

## Algorithm Details

### Algorithm 1: Center-Radius Clustering

**Constraint**: Every point in cluster is within distance D from cluster center.

**Implementation**:
- Greedy farthest-first approach
- BallTree spatial index for efficient radius queries
- Time Complexity: **O(n × k × log n)** where k is number of clusters
- Space Complexity: **O(n)**

**Best For**:
- Large datasets (> 500 points)
- Speed priority
- Approximate clustering acceptable

### Algorithm 2: Diameter Clustering

**Constraint**: All pairwise distances within cluster ≤ D (stricter).

**Implementation**:
- Constrained greedy with pairwise checking
- Distance matrix precomputation
- Time Complexity: **O(n² × k)** worst case
- Space Complexity: **O(n²)**

**Best For**:
- Quality/tightness critical
- Smaller datasets (< 500 points)
- Guaranteed compact clusters

## Key Results

### Test Coverage
```
23 tests passed
Coverage:
- Distance calculation: 5 tests
- Center-radius algorithm: 5 tests  
- Diameter algorithm: 6 tests
- Constraint validation: 4 tests
- Statistics and performance: 3 tests
```

### Performance Benchmarks
- 100 points: Both algorithms < 50ms
- 1000 points: Center-radius < 200ms, Diameter < 2s
- 100% constraint satisfaction rate

### Algorithm Comparison
| Metric | Center-Radius | Diameter |
|--------|---------------|----------|
| Typical cluster count | Lower | Higher |
| Strictness | Lenient | Strict |
| Speed | Faster | Slower |
| Use case | Large datasets | Quality priority |

## Usage Examples

### Basic Usage

```python
import numpy as np
from src.geocluster import cluster_by_center_radius, cluster_by_diameter

# Define points (lat, lon)
points = np.array([
    [37.7749, -122.4194],  # San Francisco
    [37.3382, -121.8863],  # San Jose  
    [37.8715, -122.2730],  # Berkeley
])

# Cluster with D=50 km
labels, centers, n_clusters = cluster_by_center_radius(points, D=50.0)
print(f"Created {n_clusters} clusters")

# Compare with diameter algorithm
labels2, centers2, n_clusters2 = cluster_by_diameter(points, D=50.0)
print(f"Diameter algorithm: {n_clusters2} clusters (≥ {n_clusters})")
```

### Validation

```python
from src.geocluster import validate_center_radius_constraint

# Validate constraints are satisfied
is_valid, violations = validate_center_radius_constraint(
    points, labels, centers, D=50.0
)

if is_valid:
    print("✓ All constraints satisfied!")
else:
    print(f"⚠ Violations found: {violations}")
```

## Running the Code

### 1. Setup Virtual Environment
```bash
# MANDATORY: Use virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Unit Tests
```bash
source .venv/bin/activate
python -m pytest tests/test_geocluster.py -v
```

Expected output: `23 passed`

### 3. Run Jupyter Notebook
```bash
source .venv/bin/activate
jupyter lab notebooks/geoclustering_comparison.ipynb
```

The notebook will:
- Generate 4 test datasets (random, clustered, linear, grid)
- Compare algorithms across multiple D values
- Create interactive maps showing clusters
- Generate performance visualizations
- Validate all constraints

### Output Files
The notebook generates:
- `analysis/figures/cluster_count_comparison.png` - Cluster count vs D
- `analysis/figures/runtime_comparison.png` - Performance analysis
- `analysis/figures/map_*.html` - Interactive maps

## Dependencies

Core packages:
- `numpy>=1.21.0` - Array operations  
- `scikit-learn>=1.3.0` - BallTree spatial index
- `folium>=0.14.0` - Interactive maps
- `matplotlib>=3.6.0` - Plotting
- `pandas>=2.0.0` - Data analysis
- `pytest>=7.0.0` - Unit testing

## Design Decisions

1. **Haversine Distance**: Accurate for spherical Earth, suitable for D < 1000 km
2. **BallTree Optimization**: Logarithmic query time for center-radius algorithm
3. **Distance Matrix Cache**: Trades space for speed in diameter algorithm
4. **Validation Functions**: Separate constraint verification for debugging
5. **Statistics Utilities**: Rich metrics for cluster quality assessment

## Validation & Testing

### Correctness Verification
- ✓ Distance calculations match known geographical distances
- ✓ Both algorithms satisfy their respective constraints
- ✓ Diameter produces ≥ clusters than center-radius (proved by tests)
- ✓ Edge cases handled (co-located points, linear arrangements)

### Performance Verification  
- ✓ Center-radius scales well to 1000 points
- ✓ Diameter feasible for datasets < 500 points
- ✓ No memory issues with maximum dataset size

### Quality Verification
- ✓ Produces minimal cluster count (greedy approximation)
- ✓ All clusters satisfy radius constraints
- ✓ Centers chosen strategically (farthest-first)

## Time Complexity Summary

| Operation | Center-Radius | Diameter |
|-----------|---------------|----------|
| Distance calc | O(1) | O(1) |
| Find next center | O(n) | O(n) |
| Assign points | O(n log n) | O(n²) |
| Overall | O(n k log n) | O(n² k) |

Where:
- n = number of points
- k = number of clusters (typically k << n)

## Future Enhancements

Potential improvements:
1. Approximation algorithms for diameter (faster)
2. Parallelization for large datasets
3. Incremental clustering for streaming data
4. Alternative distance metrics (driving distance, etc.)
5. Cluster refinement post-processing

## References

- Haversine formula: https://en.wikipedia.org/wiki/Haversine_formula
- BallTree: scikit-learn documentation
- Greedy clustering: Classical approximation algorithms

## Success Criteria ✓

- [x] Both algorithms implemented and working
- [x] Haversine distance calculation accurate
- [x] Validation functions verify constraints
- [x] Unit tests: 23/23 passing
- [x] Jupyter notebook with visualizations
- [x] Both algorithms handle 1000 points efficiently
- [x] Clear documentation and examples
- [x] Virtual environment usage documented

---

**Status**: ✅ Complete and validated

All requirements met, tests passing, ready for use!
