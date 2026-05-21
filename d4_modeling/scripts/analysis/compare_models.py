import pandas as pd
import pickle
import json

print("="*80)
print("MODEL COMPARISON: Original vs City-Normalized")
print("="*80)

# Load original model results
try:
    with open('../models/regression/xgboost_model.pkl', 'rb') as f:
        original_model = pickle.load(f)
    print("\n✓ Original model found")
except:
    print("\n✗ Original model not found")
    original_model = None

# Load city-normalized model
try:
    with open('../models/regression/xgboost_city_normalized.pkl', 'rb') as f:
        normalized_model = pickle.load(f)
    with open('../models/regression/city_medians.json', 'r') as f:
        city_medians = json.load(f)
    print("✓ City-normalized model found")
except:
    print("✗ City-normalized model not found")
    normalized_model = None

# Load predictions
try:
    orig_pred = pd.read_csv('../data/predictions_original.csv')
    print("✓ Original predictions found")
except:
    print("✗ Original predictions not found - checking alternative locations")
    try:
        orig_pred = pd.read_csv('../results/predictions_original.csv')
        print("✓ Found in results/")
    except:
        orig_pred = None

try:
    norm_pred = pd.read_csv('../data/predictions_city_normalized.csv')
    print("✓ City-normalized predictions found")
except:
    norm_pred = None

print("\n" + "="*80)
print("ORIGINAL MODEL (Absolute Rent Prediction)")
print("="*80)
if orig_pred is not None:
    print(f"Target: Absolute rent ($)")
    print(f"Features: {len([c for c in orig_pred.columns if c not in ['city', 'geoid', 'actual_rent', 'predicted_rent', 'residual']])} features")
    print(f"Data points: {len(orig_pred)}")
    
    # Calculate metrics
    from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
    import numpy as np
    
    if 'actual_rent' in orig_pred.columns and 'predicted_rent' in orig_pred.columns:
        r2 = r2_score(orig_pred['actual_rent'], orig_pred['predicted_rent'])
        rmse = np.sqrt(mean_squared_error(orig_pred['actual_rent'], orig_pred['predicted_rent']))
        mae = mean_absolute_error(orig_pred['actual_rent'], orig_pred['predicted_rent'])
        
        print(f"\nPerformance:")
        print(f"  R² Score: {r2:.4f}")
        print(f"  RMSE: ${rmse:.2f}")
        print(f"  MAE: ${mae:.2f}")
        
        print(f"\nResidual Analysis:")
        print(f"  Mean residual: ${orig_pred['residual'].mean():.2f}")
        print(f"  Std residual: ${orig_pred['residual'].std():.2f}")
        print(f"  Min residual: ${orig_pred['residual'].min():.2f}")
        print(f"  Max residual: ${orig_pred['residual'].max():.2f}")
        
        # Check by city
        print(f"\nBy City:")
        for city in orig_pred['city'].unique()[:5]:
            city_data = orig_pred[orig_pred['city'] == city]
            city_r2 = r2_score(city_data['actual_rent'], city_data['predicted_rent'])
            print(f"  {city}: R² = {city_r2:.4f}, RMSE = ${np.sqrt(mean_squared_error(city_data['actual_rent'], city_data['predicted_rent'])):.2f}")
else:
    print("No data available")

print("\n" + "="*80)
print("CITY-NORMALIZED MODEL (Deviation from City Median)")
print("="*80)
if norm_pred is not None:
    print(f"Target: Deviation from city median rent ($)")
    print(f"Features: {len([c for c in norm_pred.columns if c not in ['city', 'geoid', 'actual_rent', 'predicted_rent_normalized', 'residual_normalized']])} features")
    print(f"Data points: {len(norm_pred)}")
    
    if 'rent_deviation' in norm_pred.columns and 'predicted_deviation' in norm_pred.columns:
        r2 = r2_score(norm_pred['rent_deviation'], norm_pred['predicted_deviation'])
        rmse = np.sqrt(mean_squared_error(norm_pred['rent_deviation'], norm_pred['predicted_deviation']))
        mae = mean_absolute_error(norm_pred['rent_deviation'], norm_pred['predicted_deviation'])
        
        print(f"\nPerformance:")
        print(f"  R² Score: {r2:.4f}")
        print(f"  RMSE: ${rmse:.2f}")
        print(f"  MAE: ${mae:.2f}")
        
        print(f"\nResidual Analysis:")
        print(f"  Mean residual: ${norm_pred['residual_normalized'].mean():.2f}")
        print(f"  Std residual: ${norm_pred['residual_normalized'].std():.2f}")
        print(f"  Min residual: ${norm_pred['residual_normalized'].min():.2f}")
        print(f"  Max residual: ${norm_pred['residual_normalized'].max():.2f}")
        
        # Check by city
        print(f"\nBy City:")
        for city in norm_pred['city'].unique()[:5]:
            city_data = norm_pred[norm_pred['city'] == city]
            if 'rent_deviation' in city_data.columns:
                city_r2 = r2_score(city_data['rent_deviation'], city_data['predicted_deviation'])
                print(f"  {city}: R² = {city_r2:.4f}, RMSE = ${np.sqrt(mean_squared_error(city_data['rent_deviation'], city_data['predicted_deviation'])):.2f}")
else:
    print("No data available")

print("\n" + "="*80)
print("PROS & CONS")
print("="*80)

print("\nORIGINAL MODEL:")
print("PROS:")
print("  ✓ Direct interpretation - predicts actual rent in dollars")
print("  ✓ Easy to explain to stakeholders")
print("  ✓ Residuals = actual affordable housing opportunities")
print("  ✓ Can compare across cities directly")

print("\nCONS:")
print("  ✗ May learn regional shortcuts (e.g., 'Jacksonville = $1,400')")
print("  ✗ High R² might be from city/region features, not housing economics")
print("  ✗ Harder to find true market inefficiencies")
print("  ✗ Model might just memorize city averages")

print("\nCITY-NORMALIZED MODEL:")
print("PROS:")
print("  ✓ Removes regional bias - focuses on within-city variation")
print("  ✓ Better for finding true market inefficiencies")
print("  ✓ More meaningful residuals (deviation from local market)")
print("  ✓ Harder to 'cheat' with geographic features")

print("\nCONS:")
print("  ✗ Less intuitive - predicts deviation, not absolute rent")
print("  ✗ Requires city median lookup to get actual rent")
print("  ✗ Can't directly compare across cities")
print("  ✗ More complex to explain to non-technical stakeholders")

print("\n" + "="*80)
