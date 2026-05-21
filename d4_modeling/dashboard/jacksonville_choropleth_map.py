#!/usr/bin/env python3
"""
Jacksonville Integrated Choropleth Map Dashboard
Shows ZIP codes colored by composite score with hover details
"""

import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, dash_table
import json
from urllib.request import urlopen

# Load the integrated data
print("Loading integrated data...")
df = pd.read_csv('integrated_data.csv')

# Ensure ZIP codes are 5-digit strings
df['ZIP_Code'] = df['ZIP_Code'].astype(str).str.zfill(5)

print(f"Loaded {len(df)} ZIP codes")

# Load GeoJSON for Florida ZIP codes
print("Loading ZIP code boundaries...")
with urlopen('https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/fl_florida_zip_codes_geo.min.json') as response:
    fl_zips = json.load(response)

# Filter to only Jacksonville ZIPs
jax_zip_codes = set(df['ZIP_Code'].values)
fl_zips['features'] = [f for f in fl_zips['features'] if f['properties']['ZCTA5CE10'] in jax_zip_codes]

print(f"Found {len(fl_zips['features'])} ZIP boundaries")

# Create hover text
df['hover_text'] = df.apply(lambda row: 
    f"<b>ZIP {row['ZIP_Code']}</b><br>" +
    f"<b>Composite Score: {row['composite_score']:.1f}</b><br>" +
    f"Population: {row['Population']:,}<br><br>" +
    f"<b>Housing Score: {row['housing_score']:.1f}</b><br>" +
    f"Actual Rent: ${row['Actual_Rent']:,.0f}<br>" +
    f"Predicted Rent: ${row['Predicted_Rent']:,.0f}<br>" +
    f"Difference: ${row['Rent_Difference']:,.0f}<br><br>" +
    f"<b>Spatial Score: {row['spatial_score']:.1f}</b><br>" +
    f"Mismatch Index: {row['Spatial_Mismatch_Index']:.1f}<br>" +
    f"Job Density: {row['Job_Density_Ratio']:.2f}<br>" +
    f"Transit %: {row['Transit_Pct']:.1f}%<br><br>" +
    f"<b>Skills Score: {row['skills_score']:.1f}</b><br>" +
    f"Prediction Error: {row['Skills_Prediction_Error']:.3f}<br>" +
    f"Gap < HS: {row['Skills_Gap_LessThan_HS']:.2f}",
    axis=1
)

# Create the choropleth map
fig = go.Figure(go.Choroplethmapbox(
    geojson=fl_zips,
    locations=df['ZIP_Code'],
    z=df['composite_score'],
    featureidkey="properties.ZCTA5CE10",
    colorscale=[
        [0.0, '#d73027'],    # Red
        [0.333, '#fc8d59'],  # Orange
        [0.5, '#fee090'],    # Yellow
        [0.667, '#91cf60'], # Light green
        [1.0, '#1a9850']     # Green
    ],
    zmin=0,
    zmax=100,
    text=df['hover_text'],
    hovertemplate='%{text}<extra></extra>',
    colorbar=dict(
        title="Composite<br>Score",
        thickness=15,
        len=0.7,
        x=1.02,
        bgcolor='rgba(30, 30, 30, 0.8)',
        tickfont=dict(color='#e0e0e0')
    ),
    marker_opacity=0.65,
    marker_line_width=2,
    marker_line_color='#333333'
))

fig.update_layout(
    mapbox_style="open-street-map",
    mapbox_zoom=9.8,
    mapbox_center={"lat": 30.3322, "lon": -81.6557},
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    height=700,
    paper_bgcolor='#1a1a1a',
    plot_bgcolor='#1a1a1a'
)

# Add city label annotation
fig.add_annotation(
    text="Jacksonville, FL",
    x=0.5,
    y=0.98,
    xref="paper",
    yref="paper",
    showarrow=False,
    font=dict(size=18, color="#e0e0e0", family="Arial"),
    bgcolor="rgba(26, 26, 26, 0.8)",
    bordercolor="#ffffff",
    borderwidth=2,
    borderpad=8
)

# Prepare table data
table_df = df[['ZIP_Code', 'composite_score', 'housing_score', 'spatial_score', 'skills_score', 
               'Population', 'Actual_Rent', 'Predicted_Rent', 'Spatial_Mismatch_Index']].copy()
table_df.columns = ['ZIP', 'Composite', 'Housing', 'Spatial', 'Skills', 
                    'Population', 'Actual Rent', 'Predicted Rent', 'Mismatch Index']
table_df = table_df.sort_values('Composite', ascending=False)
table_df = table_df.round(1)

# Create Dash app
app = Dash(__name__)

app.layout = html.Div([
    # Header
    html.Div([
        html.H1("Jacksonville Integrated Planning Dashboard", 
                style={
                    'textAlign': 'center', 
                    'marginBottom': '5px', 
                    'color': '#e0e0e0',
                    'fontWeight': '300',
                    'letterSpacing': '1px'
                }),
        html.P("Composite Score: Housing Affordability + Job Access + Skills Match",
               style={
                   'textAlign': 'center', 
                   'color': '#a0a0a0', 
                   'fontSize': '16px', 
                   'marginBottom': '20px',
                   'fontWeight': '300'
               })
    ], style={
        'padding': '30px', 
        'backgroundColor': '#1a1a1a',
        'borderBottom': '1px solid #333'
    }),
    
    # Map
    dcc.Graph(
        figure=fig, 
        style={'height': '700px', 'backgroundColor': '#1a1a1a'},
        config={'displayModeBar': False}
    ),
    
    # Info section
    html.Div([
        html.Div([
            html.Div([
                html.H3("About This Dashboard", 
                       style={'color': '#e0e0e0', 'marginBottom': '15px', 'fontWeight': '300'}),
                html.P([
                    "This dashboard integrates three key urban planning dimensions to identify areas of opportunity ",
                    "and concern in Jacksonville. Each ZIP code receives a composite score (0-100) based on:"
                ], style={'marginBottom': '15px', 'color': '#b0b0b0', 'lineHeight': '1.6'}),
                html.Ul([
                    html.Li("Housing Affordability: Predicted vs actual rent (over-predicted = overpriced)", 
                           style={'marginBottom': '8px'}),
                    html.Li("Spatial Mismatch: Job access, transit availability, and commute patterns",
                           style={'marginBottom': '8px'}),
                    html.Li("Skills Gap: Workforce education alignment with local job requirements",
                           style={'marginBottom': '8px'})
                ], style={'marginLeft': '20px', 'marginBottom': '15px', 'color': '#b0b0b0'}),
                html.P([
                    html.Strong("Note: ", style={'color': '#e0e0e0'}), 
                    "Some areas on the map show no data. These ZIP codes were excluded because data was not available ",
                    "across all three datasets (housing predictions, spatial mismatch analysis, and skills gap assessment). ",
                    "Only the 54 ZIP codes with complete data across all dimensions are displayed."
                ], style={'fontSize': '14px', 'color': '#808080', 'fontStyle': 'italic', 'lineHeight': '1.5'})
            ], style={
                'width': '58%', 
                'display': 'inline-block', 
                'verticalAlign': 'top', 
                'padding': '25px'
            }),
            
            html.Div([
                html.H3("Score Distribution", 
                       style={'color': '#e0e0e0', 'marginBottom': '20px', 'fontWeight': '300'}),
                html.Div([
                    html.Div([
                        html.Div(style={
                            'width': '35px', 
                            'height': '35px', 
                            'backgroundColor': '#1a9850', 
                            'display': 'inline-block', 
                            'marginRight': '12px', 
                            'borderRadius': '6px',
                            'boxShadow': '0 2px 4px rgba(0,0,0,0.3)'
                        }),
                        html.Span("Green (66.7-100)", 
                                 style={'fontSize': '17px', 'fontWeight': '400', 'color': '#e0e0e0'}),
                        html.Br(),
                        html.Span("11 ZIP codes - Strong performance across all metrics", 
                                 style={
                                     'fontSize': '14px', 
                                     'color': '#909090', 
                                     'marginLeft': '47px',
                                     'display': 'block',
                                     'marginTop': '4px'
                                 })
                    ], style={'marginBottom': '20px'}),
                    
                    html.Div([
                        html.Div(style={
                            'width': '35px', 
                            'height': '35px', 
                            'backgroundColor': '#fee090', 
                            'display': 'inline-block', 
                            'marginRight': '12px', 
                            'borderRadius': '6px',
                            'boxShadow': '0 2px 4px rgba(0,0,0,0.3)'
                        }),
                        html.Span("Yellow (33.3-66.7)", 
                                 style={'fontSize': '17px', 'fontWeight': '400', 'color': '#e0e0e0'}),
                        html.Br(),
                        html.Span("32 ZIP codes - Moderate performance, room for improvement", 
                                 style={
                                     'fontSize': '14px', 
                                     'color': '#909090', 
                                     'marginLeft': '47px',
                                     'display': 'block',
                                     'marginTop': '4px'
                                 })
                    ], style={'marginBottom': '20px'}),
                    
                    html.Div([
                        html.Div(style={
                            'width': '35px', 
                            'height': '35px', 
                            'backgroundColor': '#d73027', 
                            'display': 'inline-block', 
                            'marginRight': '12px', 
                            'borderRadius': '6px',
                            'boxShadow': '0 2px 4px rgba(0,0,0,0.3)'
                        }),
                        html.Span("Red (0-33.3)", 
                                 style={'fontSize': '17px', 'fontWeight': '400', 'color': '#e0e0e0'}),
                        html.Br(),
                        html.Span("11 ZIP codes - Priority areas needing intervention", 
                                 style={
                                     'fontSize': '14px', 
                                     'color': '#909090', 
                                     'marginLeft': '47px',
                                     'display': 'block',
                                     'marginTop': '4px'
                                 })
                    ], style={'marginBottom': '20px'}),
                ])
            ], style={
                'width': '38%', 
                'display': 'inline-block', 
                'verticalAlign': 'top', 
                'padding': '25px', 
                'backgroundColor': '#242424', 
                'borderRadius': '8px', 
                'margin': '20px',
                'boxShadow': '0 4px 6px rgba(0,0,0,0.3)'
            })
        ])
    ], style={'backgroundColor': '#1a1a1a', 'padding': '20px'}),
    
    # Data table
    html.Div([
        html.H2("Complete ZIP Code Data", 
               style={
                   'textAlign': 'center', 
                   'color': '#e0e0e0', 
                   'marginBottom': '25px',
                   'fontWeight': '300',
                   'letterSpacing': '1px'
               }),
        dash_table.DataTable(
            data=table_df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in table_df.columns],
            style_table={'overflowX': 'auto'},
            style_cell={
                'textAlign': 'center',
                'padding': '12px',
                'fontFamily': 'Arial, sans-serif',
                'backgroundColor': '#242424',
                'color': '#e0e0e0',
                'border': '1px solid #333'
            },
            style_header={
                'backgroundColor': '#1a1a1a',
                'color': '#e0e0e0',
                'fontWeight': 'bold',
                'fontSize': '14px',
                'border': '1px solid #333',
                'textTransform': 'uppercase',
                'letterSpacing': '0.5px'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#2a2a2a'
                },
                {
                    'if': {
                        'filter_query': '{Composite} >= 66.7',
                        'column_id': 'Composite'
                    },
                    'backgroundColor': '#1a4d2e',
                    'color': '#90ee90',
                    'fontWeight': 'bold'
                },
                {
                    'if': {
                        'filter_query': '{Composite} < 33.3',
                        'column_id': 'Composite'
                    },
                    'backgroundColor': '#4d1a1a',
                    'color': '#ff6b6b',
                    'fontWeight': 'bold'
                }
            ],
            page_size=20,
            sort_action='native',
            filter_action='native'
        )
    ], style={'padding': '40px', 'backgroundColor': '#1a1a1a'})
], style={'backgroundColor': '#1a1a1a', 'minHeight': '100vh'})

if __name__ == '__main__':
    print("\n" + "="*80)
    print("JACKSONVILLE CHOROPLETH MAP DASHBOARD")
    print("="*80)
    print(f"📊 Loaded {len(df)} Jacksonville ZIPs")
    print("🗺️  Open your browser to: http://127.0.0.1:8050")
    print("="*80 + "\n")
    app.run(debug=True, port=8050)
