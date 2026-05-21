#!/usr/bin/env python3
"""
Jacksonville Integrated Map Dashboard
Interactive choropleth map showing composite planning score
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import json
import requests
from io import BytesIO
from zipfile import ZipFile
import geopandas as gpd

print("=" * 80)
print("JACKSONVILLE INTEGRATED MAP DASHBOARD")
print("=" * 80)

# Load integrated data
print("\n[1/4] Loading integrated data...")
df = pd.read_csv('dashboard/integrated_data.csv')
df['ZIP_Code'] = df['ZIP_Code'].astype(str).str.split('.').str[0]  # Clean ZIP format
print(f"  Loaded {len(df)} ZIPs with composite scores")

# Download Florida ZIP boundaries from Census
print("\n[2/4] Downloading Florida ZIP code boundaries...")
print("  (This may take a minute...)")

try:
    # Try to download from Census TIGER
    url = "https://www2.census.gov/geo/tiger/TIGER2020/ZCTA5/tl_2020_us_zcta510.zip"
    response = requests.get(url, timeout=60)
    
    if response.status_code == 200:
        # Extract shapefile from zip
        with ZipFile(BytesIO(response.content)) as zip_file:
            zip_file.extractall('dashboard/temp_shp')
        
        # Load shapefile
        gdf = gpd.read_file('dashboard/temp_shp/tl_2020_us_zcta510.shp')
        
        # Filter to Florida ZIPs (starts with 32 or 33)
        florida_zips = gdf[gdf['ZCTA5CE10'].str.startswith(('32', '33'))].copy()
        
        # Filter to our ZIPs
        our_zips = df['ZIP_Code'].unique()
        florida_zips = florida_zips[florida_zips['ZCTA5CE10'].isin(our_zips)]
        
        print(f"  ✅ Downloaded {len(florida_zips)} ZIP boundaries")
        
        # Merge with our data
        florida_zips = florida_zips.merge(
            df, 
            left_on='ZCTA5CE10', 
            right_on='ZIP_Code', 
            how='inner'
        )
        
        print(f"  ✅ Matched {len(florida_zips)} ZIPs with data")
        
        # Convert to GeoJSON for Plotly
        geojson = json.loads(florida_zips.to_json())
        
        use_real_boundaries = True
        
    else:
        print(f"  ⚠️  Download failed (status {response.status_code})")
        use_real_boundaries = False
        
except Exception as e:
    print(f"  ⚠️  Error downloading boundaries: {e}")
    use_real_boundaries = False

if not use_real_boundaries:
    print("\n  Using fallback: scatter plot with ZIP locations")
    # We'll create a scatter plot instead
    geojson = None

print("\n[3/4] Creating interactive map...")

# Initialize Dash app
app = Dash(__name__)

if use_real_boundaries:
    # Create choropleth map with real boundaries
    fig = px.choropleth(
        florida_zips,
        geojson=geojson,
        locations='ZIP_Code',
        featureidkey="properties.ZIP_Code",
        color='composite_score',
        color_continuous_scale=[
            [0.0, '#d73027'],    # Red
            [0.33, '#fc8d59'],   # Orange
            [0.5, '#fee08b'],    # Yellow
            [0.67, '#d9ef8b'],   # Light green
            [1.0, '#1a9850']     # Green
        ],
        range_color=[0, 100],
        hover_data={
            'ZIP_Code': True,
            'composite_score': ':.1f',
            'housing_score': ':.1f',
            'spatial_score': ':.1f',
            'skills_score': ':.1f',
            'Actual_Rent': ':$,.0f',
            'Predicted_Rent': ':$,.0f',
            'Rent_Difference': ':+$,.0f',
            'Spatial_Mismatch_Index': ':.1f',
            'Population': ':,.0f'
        },
        labels={
            'composite_score': 'Composite Score',
            'housing_score': 'Housing (Affordability)',
            'spatial_score': 'Spatial (Job Access)',
            'skills_score': 'Skills (Workforce)',
            'Actual_Rent': 'Actual Rent',
            'Predicted_Rent': 'Predicted Rent',
            'Rent_Difference': 'Rent Difference',
            'Spatial_Mismatch_Index': 'Spatial Mismatch',
            'Population': 'Population'
        },
        title='Jacksonville Integrated Planning Dashboard<br><sub>Composite Score: Housing Affordability + Job Access + Skills Match</sub>'
    )
    
    fig.update_geos(
        fitbounds="locations",
        visible=False
    )
    
else:
    # Fallback: Create scatter plot
    # Estimate lat/lon from ZIP (very rough)
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['ZIP_Code'],
        y=df['composite_score'],
        mode='markers',
        marker=dict(
            size=15,
            color=df['composite_score'],
            colorscale=[
                [0.0, '#d73027'],
                [0.33, '#fc8d59'],
                [0.5, '#fee08b'],
                [0.67, '#d9ef8b'],
                [1.0, '#1a9850']
            ],
            cmin=0,
            cmax=100,
            colorbar=dict(title="Composite<br>Score"),
            line=dict(width=1, color='white')
        ),
        text=[
            f"ZIP: {row['ZIP_Code']}<br>" +
            f"Score: {row['composite_score']:.1f}<br>" +
            f"Housing: {row['housing_score']:.1f}<br>" +
            f"Spatial: {row['spatial_score']:.1f}<br>" +
            f"Skills: {row['skills_score']:.1f}<br>" +
            f"Rent: ${row['Actual_Rent']:.0f}"
            for _, row in df.iterrows()
        ],
        hovertemplate='%{text}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Jacksonville Integrated Planning Dashboard<br><sub>Composite Score: Housing Affordability + Job Access + Skills Match</sub>',
        xaxis_title='ZIP Code',
        yaxis_title='Composite Score (0-100)',
        height=700
    )

fig.update_layout(
    font=dict(size=12),
    title_font=dict(size=18),
    height=700,
    margin=dict(l=0, r=0, t=80, b=0)
)

print("  ✅ Map created")

# Create app layout
app.layout = html.Div([
    html.Div([
        html.H1("Jacksonville Integrated Planning Dashboard", 
                style={'textAlign': 'center', 'color': '#2c3e50'}),
        html.P("Composite Score: Housing Affordability + Job Access + Skills Match",
               style={'textAlign': 'center', 'color': '#7f8c8d', 'fontSize': 14}),
    ], style={'padding': '20px'}),
    
    dcc.Graph(
        id='map',
        figure=fig,
        style={'height': '700px'}
    ),
    
    html.Div([
        html.Div([
            html.H3("Score Legend", style={'color': '#2c3e50'}),
            html.Div([
                html.Span("🟢 ", style={'fontSize': 20}),
                html.Span("Green (66.7-100): ", style={'fontWeight': 'bold'}),
                html.Span("Best - Affordable housing + good job access + skills match")
            ], style={'marginBottom': '10px'}),
            html.Div([
                html.Span("🟡 ", style={'fontSize': 20}),
                html.Span("Yellow (33.3-66.7): ", style={'fontWeight': 'bold'}),
                html.Span("Moderate - Mixed performance across metrics")
            ], style={'marginBottom': '10px'}),
            html.Div([
                html.Span("🔴 ", style={'fontSize': 20}),
                html.Span("Red (0-33.3): ", style={'fontWeight': 'bold'}),
                html.Span("Critical - Overpriced + poor job access + skills gap")
            ]),
        ], style={'flex': 1, 'padding': '20px'}),
        
        html.Div([
            html.H3("Top 5 ZIPs", style={'color': '#27ae60'}),
            html.Div(id='top-zips', children=[
                html.Div(f"{row['ZIP_Code']}: {row['composite_score']:.1f}", 
                         style={'marginBottom': '5px'})
                for _, row in df.nlargest(5, 'composite_score').iterrows()
            ])
        ], style={'flex': 1, 'padding': '20px'}),
        
        html.Div([
            html.H3("Bottom 5 ZIPs", style={'color': '#e74c3c'}),
            html.Div(id='bottom-zips', children=[
                html.Div(f"{row['ZIP_Code']}: {row['composite_score']:.1f}", 
                         style={'marginBottom': '5px'})
                for _, row in df.nsmallest(5, 'composite_score').iterrows()
            ])
        ], style={'flex': 1, 'padding': '20px'}),
    ], style={'display': 'flex', 'justifyContent': 'space-around', 'padding': '20px', 
              'backgroundColor': '#ecf0f1', 'marginTop': '20px'}),
    
    html.Div([
        html.P("Data Sources: Housing predictions (Matthew), Spatial mismatch (Khanh), Skills gap (William)",
               style={'textAlign': 'center', 'color': '#95a5a6', 'fontSize': 12, 'marginTop': '20px'})
    ])
])

print("\n[4/4] Starting dashboard server...")
print("\n" + "=" * 80)
print("✅ DASHBOARD READY!")
print("=" * 80)
print("\n🌐 Open your browser to: http://127.0.0.1:8050")
print("\nPress Ctrl+C to stop the server")
print("=" * 80 + "\n")

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
