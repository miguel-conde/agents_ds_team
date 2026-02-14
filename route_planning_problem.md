# Route Planning Feasibility Analysis

## Purpose

This document describes a **retrospective diagnostic model** for validating the feasibility of current sales representative assignments. Using **actual observed data** from the existing system, we derive empirical travel metrics to identify potential workload issues, inefficient routes, or infeasible assignments.

We will use a derived **time-distance matrix** to feed a first-class route planning algorithm. This is the final objective of this analysis.

## Data Sources

We analyze historical data from a route planning system that assigns daily visits to sales representatives. The analysis uses **actual observed data** from a table with the following structure:

| rep_id | store_id | latitude | longitude | visit_frequency | time_visit |
|--------|----------|----------|-----------|-----------------|------------|

Where: - `rep_id`: The unique identifier for the sales representative. - `store_id`: The unique identifier for the store to be visited. - `latitude`: The latitude coordinate of the store location. - `longitude`: The longitude coordinate of the store location. - `visit_frequency`: **\[Actual Data\]** The observed number of times the store was visited within the past year. - `time_visit`: **\[Actual Data\]** The observed average time spent at the store during visits, measured in minutes.

## Observed Working Patterns

Each representative works **225 days per year** and **8 hours per day** (these are policy parameters). From observed time allocation data, each representative dedicates a percentage **P** of their working time to field work (traveling between stores and conducting visits). The remaining time (1-P) is used for administrative tasks, meetings, and other non-field activities.

**Note**: P is derived from actual time tracking data or company policy, not assumed.

The number of Points of Sale (PoS) assigned to representative $r$ is denoted as $N_r$.

## Time Budget Calculation

Based on observed working patterns, we calculate the total available time for field work (visits + travel) for each representative:

$$
\text{Total Available Time} = 225 \text{ days/year} \times 8 \text{ hours/day} \times 60 \text{ minutes/hour} \times P
$$

Using **actual visit data**, the total yearly time spent on visits for representative $r$ is:

$$
\text{Total Visit Time}_r = \sum_{i=1}^{N_r} \text{visit_frequency}_i \times \text{time_visit}_i
$$

The **implied travel time** (residual field work time after visits) for representative $r$ is:

$$
\text{Total Travel Time}_r = \text{Total Available Time} - \text{Total Visit Time}_r
$$

**Interpretation**: This represents the time that must have been spent traveling, given observed visit patterns and field work allocation.

## Travel Frequency Estimation

We estimate the number of trips the representative makes based on observed visit patterns.

The average number of daily visits is:

$$
\text{Average Daily Visits}_r = \sum_{i=1}^{N_r} \frac{\text{visit_frequency}_i}{225}
$$

Assuming each day includes returning to a starting location (home/office), the average number of trips per day is:

$$
\text{Average Trips per Day}_r = \text{Average Daily Visits}_r + 1
$$

Therefore, the total number of trips per year is:

$$
\text{Total Trips}_r = \text{Average Trips per Day}_r \times 225
$$

## Geographic Distance Analysis

Using the latitude and longitude coordinates from actual store locations, we build a distance matrix to estimate travel distances. The distance between two points is calculated using the **Haversine formula**, which provides the great-circle (straight-line) distance between two points on Earth's surface:

$$
d = 2r \arcsin\left( \sqrt{\sin^2\left(\frac{\Delta \phi}{2}\right) + \cos(\phi_1) \cos(\phi_2) \sin^2\left(\frac{\Delta \lambda}{2}\right)} \right)
$$

Where: - $d$ is the distance between the two points (km) - $r$ is the radius of the Earth (mean radius = 6,371 km) - $\phi_1$ and $\phi_2$ are the latitudes of the two points in radians - $\Delta \phi$ is the difference in latitudes (in radians) - $\Delta \lambda$ is the difference in longitudes (in radians)

**Note**: Haversine provides straight-line distance. Actual road distances are typically 1.3-1.5× larger.

From the distance matrix, we estimate the average travel distance for representative $r$ based on their assigned stores (e.g., mean of pairwise distances weighted by visit frequency).

The estimated total annual travel distance for representative $r$ is:

$$
\text{Total Travel Distance}_r = \text{Total Trips}_r \times \text{Average Travel Distance}_r
$$

## Derived Metric: Empirical Average Speed

Using the implied travel time (from time budget analysis) and estimated travel distance (from geographic analysis), we derive the **empirical average speed** that would be required for the current assignments to be feasible:

$$
\text{Empirical Average Speed}_r = \frac{\text{Total Travel Distance}_r}{\text{Total Travel Time}_r} \quad \text{(km/min)}
$$

**Critical Interpretation**: This is **not an assumed speed**—it's a **diagnostic metric**.

-   If Empirical Average Speed ≈ 0.8-1.0 km/min (48-60 km/h): Feasible urban/mixed driving
-   If Empirical Average Speed \> 1.5 km/min (90 km/h): Assignment likely infeasible (representative would need unrealistic sustained highway speeds)
-   If Empirical Average Speed \< 0.5 km/min (30 km/h): Potential inefficiency or scheduling issues

This metric allows us to **validate current assignments** and identify representatives with infeasible workloads before operational problems occur.

## Constructing the Time-Distance Matrix

### Objective

The ultimate goal of this analysis is to construct a **time-distance matrix** that accurately represents the time required to travel between any pair of stores assigned to a representative. This matrix serves as the critical input for route optimization algorithms (TSP solvers, OR-tools, etc.) that will determine efficient daily visit schedules.

### Basic Construction Method

For representatives with **compact, contiguous territories** (low fragmentation), the time matrix can be constructed using a single empirical speed:

#### Step 1: Calculate Road Distances

Convert straight-line Haversine distances to realistic road distances using a **road network factor** (circuity factor):

$$
d_{\text{road}}(i,j) = d_{\text{Haversine}}(i,j) \times f_{\text{road}}
$$

Where:
- $d_{\text{Haversine}}(i,j)$ is the great-circle distance between stores $i$ and $j$
- $f_{\text{road}}$ is the road network factor (typically 1.3-1.5)
  - Urban grid networks: $f_{\text{road}} \approx 1.3$
  - Mixed urban/rural: $f_{\text{road}} \approx 1.4$  
  - Mountainous/coastal: $f_{\text{road}} \approx 1.5-1.6$

#### Step 2: Convert Distance to Time

Using the representative's empirical average speed, calculate travel times:

$$
t(i,j) = \frac{d_{\text{road}}(i,j)}{\text{Empirical Speed}_r}
$$

This produces a symmetric time matrix $T_r$ where $T_r[i,j] = t(i,j)$ represents the travel time (in minutes) between stores $i$ and $j$.

#### Step 3: Validation Checks

Before feeding to optimization algorithm, validate the time matrix:

1. **Symmetry**: For undirected graphs, $t(i,j) = t(j,i)$
2. **Positivity**: All times $> 0$
3. **Realism**: No unrealistic times (e.g., 5 min for 50km distance)
4. **Approximate triangle inequality**: $t(i,k) \leq t(i,j) + t(j,k) + \epsilon$ (allow small violations due to road networks)
5. **Budget consistency**: 
   $$
   \sum_{\text{all trips}} t(i,j) \approx \text{Total Travel Time}_r \text{ (from time budget)}
   $$

### When Basic Method Fails: The Clustering Problem

However, a critical problem arises when territories are **geographically fragmented into distant clusters**.

## The Clustering Problem: Methodological Limitation

### Problem Statement

Some representatives have their assigned PoS distributed in **geographically distant clusters** rather than in a contiguous territory. This spatial fragmentation creates a critical limitation in the basic feasibility analysis described above.

### Why This Matters: The Averaging Fallacy

The current methodology calculates **average travel distance** across all store pairs. This approach **masks clustering patterns** because:

**Example:** - **Representative A**: 20 stores in one compact urban area (all within 10km radius) - **Representative B**: 10 stores in City X, 10 stores in City Y (150km apart)

Both might show similar average pairwise distances (\~40-50km), but their routing efficiency is dramatically different: - Rep A: Daily routes of 5-6 stores, \~30km total driving - Rep B: Must dedicate separate days to each cluster, occasional 150km inter-cluster trips

**The average distance metric cannot distinguish between these scenarios.**

### Intra-cluster vs. Inter-cluster Dynamics

The routing problem should decompose into two fundamentally different types of travel:

#### **Intra-cluster Travel** (Within Cluster)

-   **Frequency**: Daily/frequent
-   **Distance**: Short (5-20km per trip)
-   **Speed**: Lower (urban driving, 40-50 km/h)
-   **Efficiency**: High (can visit multiple stores per trip)
-   **Time pattern**: Distributed across most working days

#### **Inter-cluster Travel** (Between Clusters)

-   **Frequency**: Occasional (weekly, monthly, or as-needed)
-   **Distance**: Long (50-200km per trip)
-   **Speed**: Higher (highway driving, 80-100 km/h)
-   **Efficiency**: Low (dedicated travel time, no store visits during transit)
-   **Time pattern**: Concentrated on specific "cluster transition" days

### Impact on Empirical Speed Calculation

When clusters are distant, the empirical average speed becomes **bimodal but reported as uni-modal**:

$$
\text{True Pattern: } \begin{cases}
\text{Speed}_{\text{intra}} \approx 0.7 \text{ km/min (urban)} \\
\text{Speed}_{\text{inter}} \approx 1.3 \text{ km/min (highway)}
\end{cases}
$$

$$
\text{Reported: } \text{Speed}_{\text{avg}} \approx 0.9\text{-}1.1 \text{ km/min (mixed)}
$$

**Diagnostic implications:** - **Elevated empirical speed** (\>1.0 km/min): Suggests significant inter-cluster travel or territory fragmentation - **Cannot be diagnosed from speed alone**: A feasible mixed pattern (50% urban, 50% highway) looks identical to an infeasible compressed pattern (all urban but unrealistic density)

### Implications for Time Budget Model

The "average daily visits" assumption **breaks down** when representatives dedicate full days to specific clusters:

**Current Model Assumes:**

```         
Every workday: Visit 2-3 stores from mixed clusters (averaged)
```

**Reality for Clustered Territories:**

```         
Week 1: Mon-Thu in Cluster A (15 stores), Fri in Cluster B (3 stores)
Week 2: Mon-Wed in Cluster A (12 stores), Thu-Fri travel + Cluster C (5 stores)
```

This creates: - **Temporal inefficiency**: Full days "lost" to inter-cluster travel - **Visit batching**: Stores in distant clusters visited intensively when accessed - **Higher variance**: Some weeks heavily field-focused, others admin-focused

### Enhanced Methodology for Clustered Territories

For representatives with fragmented territories, a **cluster-aware time matrix** is required. The following methodology ensures the optimization algorithm receives realistic time estimates.

#### **Step 1: Geographic Clustering Detection**

Apply spatial clustering algorithms to identify geographic groupings:

**Algorithm Selection:**
- **DBSCAN** (recommended): Density-based clustering that handles arbitrary shapes and identifies outliers
  - Parameters: $\epsilon$ (max distance between neighbors), $\text{MinPts}$ (minimum cluster size)
  - Advantage: No need to specify number of clusters in advance
- **K-means**: When number of clusters is known or suspected
- **Silhouette analysis**: Validate cluster quality (score > 0.5 indicates good separation)

**Inputs:** Latitude/longitude coordinates for all stores assigned to representative $r$

**Outputs:** 
- Cluster label for each store: $c_i \in \{1, 2, ..., K\}$
- Outlier stores (may form singleton clusters)

#### **Step 2: Derive Cluster-Specific Speeds**

Once clusters are identified, separate the observed travel patterns into intra-cluster and inter-cluster components to derive **two distinct empirical speeds**.

##### **Intra-cluster Speed Calculation**

For each cluster $c$, calculate travel statistics for within-cluster trips:

$$
\text{Intra-cluster Distance}_c = \frac{\sum_{i,j \in c, i \neq j} d_{\text{road}}(i,j)}{|\{(i,j) : i,j \in c, i \neq j\}|}
$$

$$
\text{Intra-cluster Trips}_c = \text{Total visits to cluster } c - 1
$$

$$
\text{Intra-cluster Travel Distance}_c = \text{Intra-cluster Trips}_c \times \text{Intra-cluster Distance}_c
$$

Sum across all clusters:

$$
\text{Total Intra Distance}_r = \sum_{c=1}^{K} \text{Intra-cluster Travel Distance}_c
$$

##### **Inter-cluster Speed Calculation**

$$
\text{Total Inter Distance}_r = \text{Total Travel Distance}_r - \text{Total Intra Distance}_r
$$

##### **Constrained Optimization Approach**

**Mathematical Problem:**
- **2 unknowns**: $\text{Speed}_{\text{intra},r}$ and $\text{Speed}_{\text{inter},r}$
- **1 constraint**: Time budget equation

$$
\frac{\text{Total Intra Distance}_r}{\text{Speed}_{\text{intra},r}} + \frac{\text{Total Inter Distance}_r}{\text{Speed}_{\text{inter},r}} = \text{Total Travel Time}_r
$$

This system is **under-constrained**. We need a second constraint to derive unique speeds.

**Solution Strategy:**

Introduce speed ratio $\alpha = \frac{\text{Speed}_{\text{inter}}}{\text{Speed}_{\text{intra}}}$ and realistic speed ranges:
- $\text{Speed}_{\text{intra}} \in [0.6, 0.9]$ km/min (36-54 km/h, urban/mixed driving)
- $\text{Speed}_{\text{inter}} \in [1.0, 1.4]$ km/min (60-84 km/h, highway driving)

With $\text{Speed}_{\text{inter}} = \alpha \cdot \text{Speed}_{\text{intra}}$, the constraint becomes:

$$
\text{Speed}_{\text{intra},r} = \frac{\text{Total Intra Distance}_r + \frac{\text{Total Inter Distance}_r}{\alpha}}{\text{Total Travel Time}_r}
$$

$$
\text{Speed}_{\text{inter},r} = \alpha \cdot \text{Speed}_{\text{intra},r}
$$

**Algorithm:**

```
For α in [1.3, 1.5, 1.7, 2.0, 2.2]:
    Calculate v_intra = (d_intra + d_inter/α) / t_total
    Calculate v_inter = α × v_intra
    
    IF 0.6 ≤ v_intra ≤ 0.9 AND 1.0 ≤ v_inter ≤ 1.4:
        Use this (v_intra, v_inter) pair
        BREAK
    
IF no solution found in ideal ranges:
    Use α = 1.6 (midpoint of typical range)
    Calculate speeds and proceed
```

**Rationale**: This approach ensures speeds satisfy both the time budget and realistic driving characteristics for urban vs. highway travel

**Edge case handling:**
If no inter-cluster trips observed (single compact cluster), fall back to basic single-speed method.

#### **Step 3: Construct Cluster-Aware Time Matrix**

**Algorithm:**

```
For each store pair (i, j) assigned to representative r:
    
    # Calculate road distance
    d_road = Haversine(i, j) × road_factor
    
    # Determine if same cluster
    IF cluster(i) == cluster(j):
        # Intra-cluster trip
        time[i, j] = d_road / Speed_intra,r
    ELSE:
        # Inter-cluster trip  
        time[i, j] = d_road / Speed_inter,r
    
    # Ensure symmetry
    time[j, i] = time[i, j]
```

**Pseudocode implementation:**

$$
t(i,j) = \begin{cases}
\frac{d_{\text{road}}(i,j)}{\text{Speed}_{\text{intra},r}} & \text{if } c_i = c_j \\
\frac{d_{\text{road}}(i,j)}{\text{Speed}_{\text{inter},r}} & \text{if } c_i \neq c_j
\end{cases}
$$

This produces a **heterogeneous time matrix** that accurately reflects that:
- Short trips within clusters are slower (urban congestion)
- Long trips between clusters are faster (highway speeds)

#### **Step 4: Validation and Quality Checks**

**Cluster fragmentation score:** $$
F_r = \frac{\text{Number of clusters}}{\text{Total stores}} \times \frac{\text{Max inter-cluster distance}}{\text{Mean intra-cluster distance}}
$$

-   $F_r < 0.1$: Compact territory (low fragmentation) → Use basic single-speed method
-   $0.1 \leq F_r < 0.3$: Moderate fragmentation → Use cluster-aware method recommended
-   $F_r \geq 0.3$: High fragmentation → Cluster-aware method **required**

**Time Matrix Quality Checks:**

1. **Speed differential validation:**
   $$
   1.2 \leq \frac{\text{Speed}_{\text{inter},r}}{\text{Speed}_{\text{intra},r}} \leq 2.0
   $$
   If outside this range, review clustering quality or road factor assumptions.

2. **Intra-cluster consistency:**
   For stores in the same cluster, times should be relatively uniform:
   $$
   \text{CV}_{\text{intra}} = \frac{\sigma(t_{\text{same cluster}})}{\mu(t_{\text{same cluster}})} < 0.5
   $$

3. **Travel time budget reconciliation:**
   $$
   \left| \sum_{\text{expected trips}} t(i,j) - \text{Total Travel Time}_r \right| < 0.15 \times \text{Total Travel Time}_r
   $$
   Deviation should be less than 15% to ensure matrix is consistent with observed data.

4. **Cluster separation validation:**
   Mean inter-cluster time should be significantly higher than mean intra-cluster time:
   $$
   \frac{\bar{t}_{\text{inter}}}{\bar{t}_{\text{intra}}} > 2.0
   $$
   If not, clustering may be too granular or data may not support multi-speed approach.

### Implementation Workflow Summary

**Automated Decision Tree for Time Matrix Construction:**

This workflow is fully automated and requires no manual inspection or human intervention.

```
1. Calculate empirical average speed for representative r

2. Run clustering algorithm (DBSCAN recommended) on all assigned stores
   - Parameters: ε = median pairwise distance × 0.3, MinPts = 3
   - Output: Number of clusters K_r and cluster assignments

3. Calculate fragmentation score F_r:
   F_r = (K_r / N_r) × (max_inter_cluster_dist / mean_intra_cluster_dist)

4. Decision Logic:

   IF F_r < 0.1:
      → Use BASIC METHOD (single speed)
      → time[i,j] = d_road(i,j) / Speed_r for all pairs
      → Validate basic checks
      → Export with method="basic"
   
   ELSE IF F_r ≥ 0.1:
      → Use CLUSTER-AWARE METHOD (required)
      
      a. Separate trips into intra-cluster and inter-cluster
      b. Calculate Speed_intra,r and Speed_inter,r
      
      c. Validate speed differential:
         IF Speed_inter / Speed_intra < 1.2:
            → Speed differential too small, fall back to BASIC METHOD
            → Log warning: "Clustering detected but speeds not distinguishable"
         ELSE:
            → Construct heterogeneous time matrix:
               time[i,j] = d_road(i,j) / Speed_intra,r   if cluster(i) == cluster(j)
               time[i,j] = d_road(i,j) / Speed_inter,r   if cluster(i) ≠ cluster(j)
      
      d. Validate budget reconciliation (within 15%)
      
      e. Export with method="cluster_aware"
      
      f. IF F_r ≥ 0.3:
         → Set flag: territory_redesign_recommended = true
         → Log alert: "High fragmentation detected, consider territory redesign"

5. Automated Quality Checks (all representatives):
   - Validate all times > 0
   - Validate matrix symmetry
   - Validate travel time budget reconciliation
   - IF any check fails: raise exception with diagnostic information
```

**Key Automation Parameters:**

- **Clustering threshold**: No manual tuning; use ε = 0.3 × median distance
- **Method selection**: Purely based on F_r threshold (< 0.1 vs ≥ 0.1)
- **Speed validation**: Automated check for 1.2× minimum differential
- **Quality gates**: Hard failures on validation errors, no human judgment required

### Actionable Insights for Optimization

**For Compact Territories** ($F_r < 0.1$):
- Time matrix ready for standard TSP/VRP optimization
- Can use daily routing strategies
- Focus optimization on visit sequencing

**For Moderately Fragmented Territories** ($0.1 \leq F_r < 0.3$):
- Use cluster-aware time matrix
- Consider cluster-based routing: optimize within-cluster sequences first
- May benefit from multi-day planning horizon (weekly optimization)

**For Highly Fragmented Territories** ($F_r \geq 0.3$):
1. **Immediate**: Use cluster-aware time matrix with separate speeds
2. **Optimization strategy**: 
   - Implement cluster-day scheduling (e.g., "Mondays are Cluster A days")
   - Optimize routes within each cluster independently
   - Plan inter-cluster transitions for specific days
3. **Long-term recommendation**: 
   - Consider territory redesign to reduce fragmentation
   - Reassign distant clusters to geographically closer representatives
   - May require organizational policy changes to increase P or reduce visit frequency

### Quality Assurance Before Deployment

Before using the time matrix in production optimization:

✅ **Mandatory Checks:**
1. All times are positive and realistic
2. Matrix dimensions match number of assigned stores
3. Symmetry holds (or asymmetry is intentional and documented)
4. Total implied travel time ≈ observed travel time (±15%)
5. Speed values are within realistic ranges (0.5-1.5 km/min)

✅ **Recommended Validation:**
- Sample 5-10 store pairs and validate times against GPS/routing API
- Compare optimizer-generated routes with actual historical routes
- Run sensitivity analysis: ±10% speed perturbation should not drastically change optimal routes

### Data Export Format

**Time Matrix Output Specification:**

```json
{
  "representative_id": "REP_001",
  "method": "cluster_aware",  // or "basic"
  "fragmentation_score": 0.42,
  "num_clusters": 3,
  "speed_intra_km_per_min": 0.75,
  "speed_inter_km_per_min": 1.25,
  "road_factor": 1.4,
  "time_matrix": [
    [0, 15.3, 48.2, ...],     // Times in minutes
    [15.3, 0, 52.1, ...],
    [48.2, 52.1, 0, ...],
    ...
  ],
  "store_ids": ["S001", "S002", "S003", ...],
  "cluster_assignments": [1, 1, 2, ...],
  "validation_passed": true,
  "validation_errors": []
}
```

### Methodological Summary

⚠️ **Critical Points:**

1. **Basic single-speed method** is suitable ONLY for compact territories ($F_r < 0.1$)
2. **Cluster-aware method** is REQUIRED when $F_r \geq 0.1$ to avoid systematic bias in optimization
3. **Using wrong method produces suboptimal routes**: Single-speed matrix for fragmented territory will cause optimizer to favor unrealistic inter-cluster trips
4. **Validation is mandatory**: Always reconcile time matrix totals with observed travel time budget

The time-distance matrix is the **foundation** of route optimization. Investing in accurate speed derivation and cluster detection will directly improve the quality of optimized routes and representative workload balance.

---

## Annex: Constraint-Based Clustering Tools

### Overview

In prior work, we developed specialized **constraint-based clustering algorithms** specifically designed for geographical points with maximum distance constraints. These tools (implemented in `src/geocluster.py`) provide an alternative to density-based methods like DBSCAN and can be particularly valuable for the store clustering problem in this analysis.

### Available Clustering Algorithms

#### **1. Center-Radius Clustering**
```python
from src.geocluster import cluster_by_center_radius

labels, centers, n_clusters = cluster_by_center_radius(points, D)
```

**Constraint**: Maximum distance from cluster center to any point ≤ D

**Algorithm**: Greedy farthest-first with BallTree optimization
- Time complexity: O(n·k·log n)
- Guarantees every point is within radius D from its cluster center
- Produces fewer, larger clusters (more lenient constraint)

**Use case**: When representatives can handle larger territories with central depot/hub model.

#### **2. Diameter-Based Clustering**
```python
from src.geocluster import cluster_by_diameter

labels, centers, n_clusters = cluster_by_diameter(points, D)
```

**Constraint**: Maximum pairwise distance within cluster ≤ D

**Algorithm**: Constrained greedy with pairwise distance validation
- Time complexity: O(n²·k)
- Guarantees all points in a cluster are within distance D of each other
- Produces more, tighter clusters (stricter constraint)

**Use case**: When tight, compact clusters are needed for efficient daily routing.

### Comparison with DBSCAN/K-means

| Feature | DBSCAN | K-means | Center-Radius | Diameter |
|---------|--------|---------|---------------|----------|
| **Input** | ε, MinPts | k clusters | Max radius D | Max diameter D |
| **Constraint Type** | Density-based | Centroid-based | Hard radius limit | Hard diameter limit |
| **Cluster Count** | Variable | Fixed | Minimized | Minimized |
| **Guarantees** | Density threshold | Variance minimization | All points ≤ D from center | All pairs ≤ D apart |
| **Outlier Handling** | Yes (noise points) | No | No | No |
| **Best For** | Unknown cluster count | Known cluster count | Radius-based service areas | Tight routing clusters |

### Application to Route Planning Problem

#### **Scenario 1: New Territory Assignment**

When designing territories from scratch, use constraint-based clustering:

```python
import numpy as np
from src.geocluster import cluster_by_diameter, compute_cluster_statistics

# Load store locations
stores = np.array([
    [37.7749, -122.4194],  # lat, lon
    [37.3382, -121.8863],
    # ... more stores
])

# Cluster with 30 km max diameter (tight daily routes)
D_max_daily = 30  # km
labels, centers, n_clusters = cluster_by_diameter(stores, D_max_daily)

# Compute statistics
stats = compute_cluster_statistics(stores, labels, centers)
print(f"Created {n_clusters} clusters")
print(f"Max diameter: {stats['max_diameter_overall']:.1f} km")
print(f"Mean cluster size: {stats['mean_cluster_size']:.1f} stores")
```

**Advantage**: Guarantees that any cluster can be visited in a single day with manageable travel distances.

#### **Scenario 2: Analyzing Existing Assignments**

For the retrospective analysis described in this document, constraint-based clustering can **validate** whether existing territories are naturally compact:

```python
from src.geocluster import (
    cluster_by_center_radius,
    validate_center_radius_constraint
)

# Get stores for representative r
rep_stores = stores[stores['rep_id'] == 'REP_001'][['latitude', 'longitude']].values

# Try to cluster with realistic D values
D_test_values = [20, 30, 40, 50]  # km

for D in D_test_values:
    labels, centers, n_clusters = cluster_by_center_radius(rep_stores, D)
    
    print(f"D={D} km: {n_clusters} clusters, {len(rep_stores)/n_clusters:.1f} stores/cluster")
    
    # If n_clusters = 1, territory is compact within D radius
    if n_clusters == 1:
        print(f"  ✓ Territory is compact (all stores within {D} km radius)")
        break
    elif n_clusters >= 4:
        print(f"  ⚠ Territory is highly fragmented")
```

**Interpretation**:
- `n_clusters = 1` at D=30km → Compact territory, use basic single-speed method
- `n_clusters ≥ 3` at D=30km → Fragmented territory, use cluster-aware method

#### **Scenario 3: Hybrid Approach with DBSCAN**

Combine density-based (DBSCAN) with constraint-based validation:

```python
from sklearn.cluster import DBSCAN
from src.geocluster import validate_diameter_constraint

# Use DBSCAN for initial clustering (finds natural groups)
coords_rad = np.radians(stores)
db = DBSCAN(eps=0.005, min_samples=3, metric='haversine').fit(coords_rad)
labels_dbscan = db.labels_

# Validate that DBSCAN clusters satisfy diameter constraint
D_max = 40  # km
is_valid, violations = validate_diameter_constraint(stores, labels_dbscan, D_max)

if not is_valid:
    print(f"⚠ DBSCAN clusters violate D={D_max} km constraint")
    print(f"   Use diameter-based clustering instead for guaranteed constraint satisfaction")
    
    labels_final, centers_final, n = cluster_by_diameter(stores, D_max)
else:
    print(f"✓ DBSCAN clusters satisfy D={D_max} km constraint")
    labels_final = labels_dbscan
```

### Integration with Enhanced Methodology

The constraint-based tools can **replace or complement** DBSCAN in Step 1 of the Enhanced Methodology:

**Original (Section: Enhanced Methodology for Clustered Territories)**:
```
Step 1: Geographic Clustering Detection
- DBSCAN: Detect arbitrary-shaped clusters with density threshold
- K-means: If number of clusters is known/suspected
```

**Enhanced with Constraint-Based Tools**:
```
Step 1: Geographic Clustering Detection

Option A (Exploratory - when cluster structure is unknown):
  → Use DBSCAN to discover natural density-based groups
  → Validate with constraint-based tools
  
Option B (Prescriptive - when D_max is known):
  → Use cluster_by_diameter(stores, D_max) directly
  → Guarantees all clusters satisfy distance constraints
  → Produces minimum number of compliant clusters
  
Option C (Diagnostic - analyzing existing assignments):
  → Test multiple D values with cluster_by_center_radius
  → Determine minimum D that produces single cluster
  → Use as fragmentation metric
```

### Recommended Workflow for This Analysis

```python
# STEP 1: Diagnostic - Test territory compactness
def diagnose_territory_compactness(stores, D_threshold=30):
    """Determine if territory is compact or fragmented."""
    labels, centers, n = cluster_by_center_radius(stores, D_threshold)
    
    fragmentation_score = n  # Number of clusters at D_threshold
    
    if n == 1:
        return "compact", None
    else:
        # Territory is fragmented, use diameter clustering for tight groups
        labels_tight, centers_tight, n_tight = cluster_by_diameter(stores, D_threshold)
        return "fragmented", (labels_tight, centers_tight, n_tight)

# STEP 2: Speed Calculation - Use cluster assignments
compactness, cluster_info = diagnose_territory_compactness(rep_stores, D=30)

if compactness == "compact":
    # Use basic single-speed method (as described in document)
    speed = calculate_empirical_speed_basic(rep_data)
    
elif compactness == "fragmented":
    labels, centers, n_clusters = cluster_info
    
    # Calculate intra-cluster and inter-cluster speeds separately
    speed_intra, speed_inter = calculate_cluster_speeds(
        rep_stores, labels, centers, rep_data
    )
    
    # Build cluster-aware time matrix
    time_matrix = build_cluster_aware_matrix(
        rep_stores, labels, speed_intra, speed_inter
    )
```

### Tool Validation

The constraint-based clustering tools have been validated in `notebooks/geoclustering_comparison.ipynb`:

**Key Findings**:
- ✓ All clusterings satisfy their respective constraints (100% validation pass rate)
- ✓ Diameter clustering produces ≥ clusters than center-radius (as expected)
- ✓ Both algorithms run efficiently on datasets up to 1000 points
- ✓ Center-radius is 2-3× faster than diameter for large datasets
- ✓ Interactive maps confirm visual coherence of clusters

### Code Location

- **Implementation**: `src/geocluster.py`
- **Validation notebook**: `notebooks/geoclustering_comparison.ipynb`
- **Test suite**: `tests/test_geocluster.py`

### Advantages for Route Planning Analysis

1. **Hard Guarantees**: Unlike DBSCAN, guarantees that clusters satisfy distance constraints
2. **Optimization Objective**: Minimizes number of clusters (fewer fragments = better territory design)
3. **Validation Built-in**: Tools include constraint validation functions
4. **Haversine Native**: Uses appropriate distance metric for lat/lon coordinates
5. **Production Ready**: Includes statistics, validation, and visualization support

### When to Use Each Approach

**Use DBSCAN when**:
- Cluster structure is unknown
- Need to identify outliers/noise points
- Density-based grouping is more natural for the data

**Use Constraint-Based Clustering when**:
- Have explicit distance constraints (e.g., "max 30 km diameter")
- Need guaranteed minimum number of clusters
- Designing new territories from scratch
- Validating existing territories against distance standards

**Use Both (Hybrid) when**:
- Want natural groupings (DBSCAN) but need to validate constraints
- Need to compare multiple clustering approaches
- Building decision support system with multiple options

### Conclusion

The existing constraint-based clustering tools (`geocluster.py`) provide a valuable **complement** to the DBSCAN-based approach outlined in the main document. They are particularly well-suited for:

1. **Prescriptive applications**: Designing optimal territories with guaranteed distance constraints
2. **Validation**: Checking if existing territories meet distance standards
3. **Automation**: Removing subjectivity from cluster definition (constraint-based vs. density hyperparameters)

For the **retrospective diagnostic analysis** described in this document, constraint-based clustering offers a **quantitative, deterministic** method for detecting territory fragmentation and defining intra/inter-cluster speed calculations.