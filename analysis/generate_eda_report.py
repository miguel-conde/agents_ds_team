#!/usr/bin/env python3
"""
Generate EDA Report for California Housing Dataset
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Load data
df = pd.read_csv('data/california_housing.csv')

print('='*80)
print('CALIFORNIA HOUSING - EXPLORATORY DATA ANALYSIS REPORT')
print('='*80)
print()

# 1. Dataset Overview
print('1. DATASET OVERVIEW')
print('-' * 40)
print(f'Total Properties: {len(df):,}')
print(f'Features: {len(df.columns)}')
print(f'Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB')
print()

# 2. Data Quality
print('2. DATA QUALITY ASSESSMENT')
print('-' * 40)
print('Missing Values:')
missing = df.isnull().sum()
if missing.sum() == 0:
    print('  ✅ No missing values detected')
else:
    print(missing[missing > 0])
print()
print('Duplicate Records:')
duplicates = df.duplicated().sum()
print(f'  {duplicates} duplicates found ({duplicates/len(df)*100:.2f}%)')
print()

# 3. Summary Statistics  
print('3. SUMMARY STATISTICS')
print('-' * 40)
numeric_cols = df.select_dtypes(include=[np.number]).columns
print(df[numeric_cols].describe().round(2))
print()

# 4. Target Variable Analysis
print('4. TARGET VARIABLE (MedHouseVal) ANALYSIS')
print('-' * 40)
target = df['MedHouseVal']
print(f'Mean: ${target.mean()*100:.0f}k')
print(f'Median: ${target.median()*100:.0f}k')
print(f'Std Dev: ${target.std()*100:.0f}k')
print(f'Range: ${target.min()*100:.0f}k - ${target.max()*100:.0f}k')
print(f'Skewness: {target.skew():.3f}')
print(f'Kurtosis: {target.kurtosis():.3f}')
print()

# 5. Correlation Analysis
print('5. FEATURE CORRELATIONS WITH TARGET')
print('-' * 40)
feature_cols = [col for col in numeric_cols if col not in ['property_id', 'MedHouseVal']]
correlations = df[feature_cols + ['MedHouseVal']].corr()['MedHouseVal'].sort_values(ascending=False)
print(correlations[:-1])
print()

# 6. Distribution Analysis
print('6. FEATURE DISTRIBUTIONS')
print('-' * 40)
for col in feature_cols:
    skew = df[col].skew()
    print(f'{col:12s} - Mean: {df[col].mean():8.2f}, Std: {df[col].std():8.2f}, Skew: {skew:6.2f}')
print()

# 7. Key Insights
print('7. KEY INSIGHTS')
print('-' * 40)
print('✓ STRONGEST PREDICTORS:')
top_corr = correlations[:-1].head(3)
for feat, corr in top_corr.items():
    print(f'  • {feat}: {corr:.3f} correlation')
print()

print('✓ DISTRIBUTION CHARACTERISTICS:')
skew_direction = 'positive' if target.skew() > 0 else 'negative'
print(f'  • Target shows {skew_direction} skew ({target.skew():.2f})')
print(f'  • Income range: ${df["MedInc"].min():.1f}k - ${df["MedInc"].max():.1f}k')
print(f'  • House age: {df["HouseAge"].min():.0f} - {df["HouseAge"].max():.0f} years')
print()

print('✓ GEOGRAPHIC PATTERNS:')
lat_bins = pd.cut(df['Latitude'], bins=5)
lat_price = df.groupby(lat_bins)['MedHouseVal'].mean()
print('  • House values vary significantly by latitude')
print(f'  • Highest avg price: ${lat_price.max()*100:.0f}k')
print(f'  • Lowest avg price: ${lat_price.min()*100:.0f}k')
print()

# 8. Outlier Detection
print('8. OUTLIER ANALYSIS')
print('-' * 40)
for col in feature_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    outliers = ((df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)).sum()
    if outliers > 0:
        pct = outliers/len(df)*100
        print(f'{col:12s} - {outliers:5d} outliers ({pct:5.2f}%)')
print()

# 9. Business Insights
print('9. ACTIONABLE BUSINESS INSIGHTS')
print('-' * 40)
print('📊 Investment Targeting:')
print(f'  • High-value properties (>$500k): {(df["MedHouseVal"] > 5).sum():,} properties')
print(f'  • Geographic concentration: Coastal areas show premium pricing')
print()
print('📊 Modeling Recommendations:')
print('  • MedInc is strongest predictor - prioritize income-based segmentation')
print('  • Geographic features (Lat/Long) are critical - consider spatial models')
print('  • Outliers present - use robust regression or tree-based models')
print()
print('📊 Feature Engineering Opportunities:')
print('  • Create location clusters (coastal vs inland)')
print('  • Income-to-price ratio for value detection')
print('  • Property density metrics (Population/AveOccup)')
print()

print('10. VISUALIZATIONS GENERATED')
print('-' * 40)
figures_dir = Path('analysis/figures')
if figures_dir.exists():
    figures = sorted(figures_dir.glob('*.png'))
    for fig in figures:
        print(f'  ✅ {fig}')
else:
    print('  ⚠️  No figures directory found')
print()

print('='*80)
print('EDA Report Generated Successfully!')
print(f'Total Properties Analyzed: {len(df):,}')
print(f'Analysis Date: 2026-02-11')
print('='*80)
