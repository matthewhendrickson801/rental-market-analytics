"""StateofJax Affordable Housing Dashboard"""
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output
import os

DUVAL_ZIPS = ['32099', '32202', '32204', '32205', '32206', '32207', '32208', '32209', '32210', '32211', '32212', '32214', '32216', '32217', '32218', '32219', '32220', '32221', '32222', '32223', '32224', '32225', '32226', '32227', '32233', '32234', '32244', '32246', '32250', '32254', '32256', '32257', '32258', '32266', '32277']

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'predictions_city_normalized.csv')
df = pd.read_csv(csv_path)
df['geoid'] = df['geoid'].astype(str)
df['predicted_rent'] = df['predicted_rent_normalized']
df['residual'] = df['residual_normalized']
df['actual_rent'] = df['Median Home Rent (2020-2024)']

duval = df[df['geoid'].isin(DUVAL_ZIPS)].copy()
duval['savings'] = -duval['residual']
duval['pct_diff'] = (duval['savings'] / duval['predicted_rent']) * 100

def categorize(row):
    if row['savings'] > 100: return 'Highly Affordable'
    elif row['savings'] > 50: return 'Affordable'
    elif row['savings'] > -50: return 'Market Rate'
    elif row['savings'] > -100: return 'Overpriced'
    else: return 'Highly Overpriced'

duval['category'] = duval.apply(categorize, axis=1)
duval_sorted = duval.sort_values('savings', ascending=False)

app = Dash(__name__)
server = app.server

COLORS = {'background': '#ffffff', 'text': '#2c3e50', 'border': '#e0e0e0', 'affordable': '#27ae60', 'market': '#95a5a6', 'overpriced': '#e74c3c'}

app.layout = html.Div([
    html.Div([
        html.H1('StateofJax Affordable Housing Dashboard', style={'margin': '0', 'fontSize': '28px', 'fontWeight': '600'}),
        html.P('Duval County, Jacksonville Metro | City-Normalized Model (R² = 0.8615)', style={'margin': '5px 0 0 0', 'fontSize': '14px', 'color': '#7f8c8d'})
    ], style={'padding': '20px 40px', 'backgroundColor': COLORS['background'], 'borderBottom': f'2px solid {COLORS["border"]}'}),
    
    html.Div([
        html.Div([
            html.Div([html.Div(f"{len(duval)}", style={'fontSize': '32px', 'fontWeight': '700', 'color': COLORS['text']}), html.Div('Total ZIPs', style={'fontSize': '12px', 'color': '#7f8c8d', 'marginTop': '5px'})], style={'textAlign': 'center', 'padding': '20px'}),
            html.Div([html.Div(f"${duval['actual_rent'].mean():.0f}", style={'fontSize': '32px', 'fontWeight': '700', 'color': COLORS['text']}), html.Div('Avg Actual Rent', style={'fontSize': '12px', 'color': '#7f8c8d', 'marginTop': '5px'})], style={'textAlign': 'center', 'padding': '20px'}),
            html.Div([html.Div(f"${duval['predicted_rent'].mean():.0f}", style={'fontSize': '32px', 'fontWeight': '700', 'color': COLORS['text']}), html.Div('Avg Predicted Rent', style={'fontSize': '12px', 'color': '#7f8c8d', 'marginTop': '5px'})], style={'textAlign': 'center', 'padding': '20px'}),
            html.Div([html.Div(f"{len(duval[duval['savings'] > 0])}", style={'fontSize': '32px', 'fontWeight': '700', 'color': COLORS['affordable']}), html.Div('Affordable ZIPs', style={'fontSize': '12px', 'color': '#7f8c8d', 'marginTop': '5px'})], style={'textAlign': 'center', 'padding': '20px'}),
            html.Div([html.Div(f"${duval[duval['savings'] > 0]['savings'].mean():.0f}", style={'fontSize': '32px', 'fontWeight': '700', 'color': COLORS['affordable']}), html.Div('Avg Savings', style={'fontSize': '12px', 'color': '#7f8c8d', 'marginTop': '5px'})], style={'textAlign': 'center', 'padding': '20px'}),
        ], style={'display': 'flex', 'justifyContent': 'space-around', 'backgroundColor': '#f8f9fa', 'margin': '20px 40px', 'borderRadius': '4px', 'border': f'1px solid {COLORS["border"]}'})
    ]),
    
    html.Div([
        html.Div([dcc.Graph(id='scatter-plot', config={'displayModeBar': False}, style={'height': '400px'})], style={'marginBottom': '30px'}),
        html.Div([dcc.Graph(id='bar-chart', config={'displayModeBar': False}, style={'height': '500px'})], style={'marginBottom': '30px'}),
    ], style={'padding': '0 40px'}),
    
    html.Div([
        html.H3('All Duval County ZIPs', style={'fontSize': '18px', 'fontWeight': '600', 'marginBottom': '15px', 'color': COLORS['text']}),
        dash_table.DataTable(
            id='data-table',
            columns=[
                {'name': 'ZIP', 'id': 'geoid'},
                {'name': 'Actual Rent', 'id': 'actual_rent', 'type': 'numeric', 'format': {'specifier': '$,.0f'}},
                {'name': 'Predicted Rent', 'id': 'predicted_rent', 'type': 'numeric', 'format': {'specifier': '$,.0f'}},
                {'name': 'Savings', 'id': 'savings', 'type': 'numeric', 'format': {'specifier': '$,.0f'}},
                {'name': '% Diff', 'id': 'pct_diff', 'type': 'numeric', 'format': {'specifier': '.1f'}},
                {'name': 'Category', 'id': 'category'},
            ],
            data=duval_sorted.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left', 'padding': '12px', 'fontSize': '13px', 'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif', 'border': f'1px solid {COLORS["border"]}'},
            style_header={'backgroundColor': '#f8f9fa', 'fontWeight': '600', 'color': COLORS['text'], 'border': f'1px solid {COLORS["border"]}'},
            style_data_conditional=[
                {'if': {'filter_query': '{savings} > 100'}, 'backgroundColor': '#d4edda'},
                {'if': {'filter_query': '{savings} > 50 && {savings} <= 100'}, 'backgroundColor': '#e8f5e9'},
                {'if': {'filter_query': '{savings} < -100'}, 'backgroundColor': '#f8d7da'},
                {'if': {'filter_query': '{savings} < -50 && {savings} >= -100'}, 'backgroundColor': '#ffebee'},
            ],
            page_size=35,
        )
    ], style={'padding': '20px 40px', 'marginBottom': '40px'}),
], style={'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif', 'backgroundColor': COLORS['background'], 'minHeight': '100vh'})

@app.callback(Output('scatter-plot', 'figure'), Input('scatter-plot', 'id'))
def update_scatter(_):
    fig = go.Figure()
    colors = duval_sorted['savings'].apply(lambda x: COLORS['affordable'] if x > 50 else (COLORS['overpriced'] if x < -50 else COLORS['market']))
    fig.add_trace(go.Scatter(x=duval_sorted['predicted_rent'], y=duval_sorted['actual_rent'], mode='markers', marker=dict(size=10, color=colors, line=dict(width=1, color='white')), text=duval_sorted['geoid'], hovertemplate='<b>ZIP %{text}</b><br>Predicted: $%{x:.0f}<br>Actual: $%{y:.0f}<extra></extra>'))
    min_val = min(duval_sorted['predicted_rent'].min(), duval_sorted['actual_rent'].min())
    max_val = max(duval_sorted['predicted_rent'].max(), duval_sorted['actual_rent'].max())
    fig.add_trace(go.Scatter(x=[min_val, max_val], y=[min_val, max_val], mode='lines', line=dict(color='#bdc3c7', width=2, dash='dash'), showlegend=False, hoverinfo='skip'))
    fig.update_layout(title='Predicted vs Actual Rent', xaxis_title='Predicted Rent ($)', yaxis_title='Actual Rent ($)', plot_bgcolor='white', paper_bgcolor='white', font=dict(family='-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif', size=12, color=COLORS['text']), title_font=dict(size=16, color=COLORS['text']), xaxis=dict(showgrid=True, gridcolor='#ecf0f1', zeroline=False), yaxis=dict(showgrid=True, gridcolor='#ecf0f1', zeroline=False), margin=dict(l=60, r=40, t=60, b=60))
    return fig

@app.callback(Output('bar-chart', 'figure'), Input('bar-chart', 'id'))
def update_bar(_):
    top_20 = duval_sorted.head(20)
    colors = top_20['savings'].apply(lambda x: COLORS['affordable'] if x > 50 else (COLORS['overpriced'] if x < -50 else COLORS['market']))
    fig = go.Figure()
    fig.add_trace(go.Bar(x=top_20['savings'], y=top_20['geoid'], orientation='h', marker=dict(color=colors, line=dict(width=0)), text=top_20['savings'].apply(lambda x: f'${x:.0f}'), textposition='outside', hovertemplate='<b>ZIP %{y}</b><br>Savings: $%{x:.0f}<extra></extra>'))
    fig.update_layout(title='Top 20 ZIPs by Savings', xaxis_title='Savings ($)', yaxis_title='ZIP Code', plot_bgcolor='white', paper_bgcolor='white', font=dict(family='-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif', size=12, color=COLORS['text']), title_font=dict(size=16, color=COLORS['text']), xaxis=dict(showgrid=True, gridcolor='#ecf0f1', zeroline=True, zerolinecolor='#bdc3c7', zerolinewidth=2), yaxis=dict(showgrid=False, autorange='reversed'), margin=dict(l=80, r=100, t=60, b=60), height=500)
    return fig

if __name__ == '__main__':
    print("="*80)
    print("StateofJax Dashboard - http://127.0.0.1:8050")
    print("="*80)
    app.run(debug=False, port=8050)
