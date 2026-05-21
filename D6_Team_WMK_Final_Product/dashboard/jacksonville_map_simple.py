#!/usr/bin/env python3
"""
Jacksonville Integrated Map Dashboard - Simple Version
Interactive visualization without requiring geopandas
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, callback
import json

print("=" * 80)
print("JACKSONVILLE INTEGRATED MAP DASHBOARD")
print("=" * 80)

# Load integrated data
print("\n[1/3] Loading integrated data...")
df = pd.read_csv('dashboard/integrated_data.csv')
df['ZIP_Code_str'] = df['ZIP_Code'].astype(int).astype(str)
print(f"  Loaded {len(df)} ZIPs with composite scores")

# Sort by composite score for better visualization
df = df.sort_values('composite_score', ascending=False)

print("\n[2/3] Creating interactive visualizations...")

# Create main scatter plot (ZIP vs Score)
fig_main = go.Figure()

# Add scatter trace
fig_main.add_trace(go.Scatter(
    x=list(range(len(df))),
    y=df['composite_score'],
    mode='markers+text',
    marker=dict(
        size=20,
        color=df['composite_score'],
        colorscale=[
            [0.0, '#d73027'],    # Red
            [0.33, '#fc8d59'],   # Orange
            [0.5, '#fee08b'],    # Yellow
            [0.67, '#d9ef8b'],   # Light green
            [1.0, '#1a9850']     # Green
        ],
        cmin=0,
        cmax=100,
        colorbar=dict(
            title="Composite<br>Score",
            thickness=20,
            len=0.7
        ),
        line=dict(width=2, color='white'),
        showscale=True
    ),
    text=df['ZIP_Code_str'],
    textposition='top center',
    textfont=dict(size=9),
    customdata=df[[
        'ZIP_Code_str', 'composite_score', 'housing_score', 'spatial_score', 
        'skills_score', 'Actual_Rent', 'Predicted_Rent', 'Rent_Difference',
        'Spatial_Mismatch_Index', 'Population', 'Mismatch_Tier', 'Transport_Verdict'
    ]],
    hovertemplate='<b>ZIP %{customdata[0]}</b><br>' +
                  '<br><b>Composite Score: %{customdata[1]:.1f}</b><br>' +
                  '━━━━━━━━━━━━━━━━━━━━<br>' +
                  '🏠 Housing (Affordability): %{customdata[2]:.1f}<br>' +
                  '🚗 Spatial (Job Access): %{customdata[3]:.1f}<br>' +
                  '🎓 Skills (Workforce): %{customdata[4]:.1f}<br>' +
                  '<br><b>Housing Details:</b><br>' +
                  'Actual Rent: $%{customdata[5]:,.0f}<br>' +
                  'Predicted Rent: $%{customdata[6]:,.0f}<br>' +
                  'Difference: $%{customdata[7]:+,.0f}<br>' +
                  '<br><b>Spatial Details:</b><br>' +
                  'Mismatch Index: %{customdata[8]:.1f}<br>' +
                  'Tier: %{customdata[10]}<br>' +
                  'Transport: %{customdata[11]}<br>' +
                  '<br>Population: %{customdata[9]:,.0f}<br>' +
                  '<extra></extra>'
))

fig_main.update_layout(
    title={
        'text': 'Jacksonville Integrated Planning Dashboard<br>' +
                '<sub>Composite Score: Housing Affordability + Job Access + Skills Match</sub>',
        'x': 0.5,
        'xanchor': 'center'
    },
    xaxis_title='ZIP Codes (sorted by score)',
    yaxis_title='Composite Score (0-100)',
    height=600,
    hovermode='closest',
    plot_bgcolor='#f8f9fa',
    font=dict(size=12),
    title_font=dict(size=18),
    margin=dict(l=60, r=60, t=100, b=60),
    xaxis=dict(
        showticklabels=False,
        showgrid=True,
        gridcolor='#e0e0e0'
    ),
    yaxis=dict(
        range=[0, 105],
        showgrid=True,
        gridcolor='#e0e0e0'
    )
)

# Add horizontal lines for thresholds
fig_main.add_hline(y=66.67, line_dash="dash", line_color="green", 
                   annotation_text="Green Threshold", annotation_position="right")
fig_main.add_hline(y=33.33, line_dash="dash", line_color="orange", 
                   annotation_text="Yellow Threshold", annotation_position="right")

print("  ✅ Main visualization created")

# Create breakdown bar chart
fig_breakdown = go.Figure()

# Get top 10 and bottom 10
top10 = df.nlargest(10, 'composite_score')
bottom10 = df.nsmallest(10, 'composite_score')
breakdown_df = pd.concat([top10, bottom10])

for metric, color in [('housing_score', '#3498db'), ('spatial_score', '#e74c3c'), ('skills_score', '#f39c12')]:
    fig_breakdown.add_trace(go.Bar(
        name=metric.replace('_', ' ').title(),
        x=breakdown_df['ZIP_Code_str'],
        y=breakdown_df[metric],
        marker_color=color
    ))

fig_breakdown.update_layout(
    title='Top 10 & Bottom 10 ZIPs - Score Breakdown',
    xaxis_title='ZIP Code',
    yaxis_title='Score (0-100)',
    barmode='group',
    height=400,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

print("  ✅ Breakdown chart created")

# Initialize Dash app
app = Dash(__name__)

# Create app layout
app.layout = html.Div([
    html.Div([
        html.H1("Jacksonville Integrated Planning Dashboard", 
                style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '5px'}),
        html.P("Composite Score: Housing Affordability + Job Access + Skills Match",
               style={'textAlign': 'center', 'color': '#7f8c8d', 'fontSize': 16, 'marginTop': '0px'}),
    ], style={'padding': '20px', 'backgroundColor': '#ecf0f1'}),
    
    # Main map
    dcc.Graph(
        id='main-map',
        figure=fig_main
    ),
    
    # Stats row
    html.Div([
        html.Div([
            html.H3(f"{len(df[df['composite_score'] >= 66.67])}", 
                    style={'color': '#27ae60', 'fontSize': 48, 'margin': '0'}),
            html.P("Green ZIPs", style={'color': '#7f8c8d', 'margin': '0'}),
            html.P("(Score ≥ 66.7)", style={'color': '#95a5a6', 'fontSize': 12, 'margin': '0'})
        ], style={'flex': 1, 'textAlign': 'center', 'padding': '20px'}),
        
        html.Div([
            html.H3(f"{len(df[(df['composite_score'] >= 33.33) & (df['composite_score'] < 66.67)])}", 
                    style={'color': '#f39c12', 'fontSize': 48, 'margin': '0'}),
            html.P("Yellow ZIPs", style={'color': '#7f8c8d', 'margin': '0'}),
            html.P("(Score 33.3-66.7)", style={'color': '#95a5a6', 'fontSize': 12, 'margin': '0'})
        ], style={'flex': 1, 'textAlign': 'center', 'padding': '20px'}),
        
        html.Div([
            html.H3(f"{len(df[df['composite_score'] < 33.33])}", 
                    style={'color': '#e74c3c', 'fontSize': 48, 'margin': '0'}),
            html.P("Red ZIPs", style={'color': '#7f8c8d', 'margin': '0'}),
            html.P("(Score < 33.3)", style={'color': '#95a5a6', 'fontSize': 12, 'margin': '0'})
        ], style={'flex': 1, 'textAlign': 'center', 'padding': '20px'}),
        
        html.Div([
            html.H3(f"{df['composite_score'].mean():.1f}", 
                    style={'color': '#3498db', 'fontSize': 48, 'margin': '0'}),
            html.P("Average Score", style={'color': '#7f8c8d', 'margin': '0'}),
            html.P(f"(Range: {df['composite_score'].min():.1f}-{df['composite_score'].max():.1f})", 
                   style={'color': '#95a5a6', 'fontSize': 12, 'margin': '0'})
        ], style={'flex': 1, 'textAlign': 'center', 'padding': '20px'}),
    ], style={'display': 'flex', 'justifyContent': 'space-around', 'backgroundColor': '#ffffff', 
              'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'margin': '20px'}),
    
    # Breakdown chart
    dcc.Graph(
        id='breakdown-chart',
        figure=fig_breakdown
    ),
    
    # Legend and top/bottom lists
    html.Div([
        html.Div([
            html.H3("Score Interpretation", style={'color': '#2c3e50'}),
            html.Div([
                html.Span("🟢 ", style={'fontSize': 24}),
                html.Span("Green (66.7-100): ", style={'fontWeight': 'bold', 'color': '#27ae60'}),
                html.Span("Best opportunities - Affordable + good job access + skills match")
            ], style={'marginBottom': '15px'}),
            html.Div([
                html.Span("🟡 ", style={'fontSize': 24}),
                html.Span("Yellow (33.3-66.7): ", style={'fontWeight': 'bold', 'color': '#f39c12'}),
                html.Span("Moderate - Mixed performance, needs attention")
            ], style={'marginBottom': '15px'}),
            html.Div([
                html.Span("🔴 ", style={'fontSize': 24}),
                html.Span("Red (0-33.3): ", style={'fontWeight': 'bold', 'color': '#e74c3c'}),
                html.Span("Critical issues - Overpriced + poor access + skills gap")
            ]),
        ], style={'flex': 1, 'padding': '20px'}),
        
        html.Div([
            html.H3("🏆 Top 5 ZIPs", style={'color': '#27ae60'}),
            html.Div([
                html.Div([
                    html.Span(f"#{i+1}. ", style={'fontWeight': 'bold'}),
                    html.Span(f"ZIP {row['ZIP_Code_str']}: ", style={'fontWeight': 'bold'}),
                    html.Span(f"{row['composite_score']:.1f}", style={'color': '#27ae60', 'fontWeight': 'bold'}),
                    html.Br(),
                    html.Span(f"  H:{row['housing_score']:.0f} S:{row['spatial_score']:.0f} K:{row['skills_score']:.0f}", 
                             style={'fontSize': 12, 'color': '#7f8c8d'})
                ], style={'marginBottom': '10px'})
                for i, (_, row) in enumerate(df.nlargest(5, 'composite_score').iterrows())
            ])
        ], style={'flex': 1, 'padding': '20px'}),
        
        html.Div([
            html.H3("⚠️ Bottom 5 ZIPs", style={'color': '#e74c3c'}),
            html.Div([
                html.Div([
                    html.Span(f"#{i+1}. ", style={'fontWeight': 'bold'}),
                    html.Span(f"ZIP {row['ZIP_Code_str']}: ", style={'fontWeight': 'bold'}),
                    html.Span(f"{row['composite_score']:.1f}", style={'color': '#e74c3c', 'fontWeight': 'bold'}),
                    html.Br(),
                    html.Span(f"  H:{row['housing_score']:.0f} S:{row['spatial_score']:.0f} K:{row['skills_score']:.0f}", 
                             style={'fontSize': 12, 'color': '#7f8c8d'})
                ], style={'marginBottom': '10px'})
                for i, (_, row) in enumerate(df.nsmallest(5, 'composite_score').iterrows())
            ])
        ], style={'flex': 1, 'padding': '20px'}),
    ], style={'display': 'flex', 'justifyContent': 'space-around', 'padding': '20px', 
              'backgroundColor': '#ecf0f1', 'marginTop': '20px'}),
    
    # Footer
    html.Div([
        html.P("Data Sources: Housing predictions (Matthew), Spatial mismatch (Khanh), Skills gap (William)",
               style={'textAlign': 'center', 'color': '#95a5a6', 'fontSize': 12, 'marginTop': '20px'}),
        html.P("H = Housing (Affordability) | S = Spatial (Job Access) | K = Skills (Workforce Match)",
               style={'textAlign': 'center', 'color': '#95a5a6', 'fontSize': 11})
    ])
], style={'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#f8f9fa'})

print("\n[3/3] Starting dashboard server...")
print("\n" + "=" * 80)
print("✅ DASHBOARD READY!")
print("=" * 80)
print(f"\n📊 Loaded {len(df)} Jacksonville ZIPs")
print(f"🟢 Green: {len(df[df['composite_score'] >= 66.67])} ZIPs")
print(f"🟡 Yellow: {len(df[(df['composite_score'] >= 33.33) & (df['composite_score'] < 66.67)])} ZIPs")
print(f"🔴 Red: {len(df[df['composite_score'] < 33.33])} ZIPs")
print("\n🌐 Open your browser to: http://127.0.0.1:8050")
print("\nPress Ctrl+C to stop the server")
print("=" * 80 + "\n")

if __name__ == '__main__':
    app.run(debug=True, port=8050)
