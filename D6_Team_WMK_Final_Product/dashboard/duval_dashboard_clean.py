"""StateofJax Affordable Housing Dashboard"""
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, html, dcc, dash_table, Input, Output
import os

DUVAL_ZIPS = ['32099', '32202', '32204', '32205', '32206', '32207', '32208', '32209', '32210', '32211', '32212', '32214', '32216', '32217', '32218', '32219', '32220', '32221', '32222', '32223', '32224', '32225', '32226', '32227', '32233', '32234', '32244', '32246', '32250', '32254', '32256', '32257', '32258', '32266', '32277']

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'predictions_city_normalized.csv')
df_all = pd.read_csv(csv_path)
df_all['geoid'] = df_all['geoid'].astype(str)
df_all['predicted_rent'] = df_all['predicted_rent_normalized']
df_all['residual'] = df_all['residual_normalized']
df_all['actual_rent'] = df_all['Median Home Rent (2020-2024)']
df_all['savings'] = -df_all['residual']
df_all['percentile'] = (df_all['savings'].rank(pct=True) * 100).round(0).astype(int)

duval = df_all[df_all['geoid'].isin(DUVAL_ZIPS)].copy()
duval = duval.sort_values('percentile', ascending=False)

for col in ['actual_rent', 'predicted_rent', 'savings', 'median_household_income', 'Total Population (2020-2024)']:
    if col in duval.columns:
        duval[col] = duval[col].round(0).astype(int)

for col in ['pct_bachelors_plus', 'pct_hs_only']:
    if col in duval.columns:
        duval[col] = duval[col].round(1)

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    # Header
    html.Div([
        html.H1('StateofJax Affordable Housing Dashboard', style={'margin': '0', 'fontSize': '28px', 'fontWeight': '600', 'color': '#1a1a1a'}),
        html.P('Duval County, Jacksonville Metro | Affordability Analysis', style={'margin': '8px 0 0 0', 'fontSize': '14px', 'color': '#666'})
    ], style={'padding': '24px 32px', 'backgroundColor': 'white', 'borderBottom': '3px solid #0066cc'}),
    
    # Key Metrics
    html.Div([
        html.Div([
            html.Div('Total ZIPs', style={'fontSize': '12px', 'color': '#666', 'marginBottom': '8px', 'fontWeight': '500'}),
            html.Div(f"{len(duval)}", style={'fontSize': '36px', 'fontWeight': '700', 'color': '#1a1a1a'})
        ], style={'flex': '1', 'padding': '20px', 'textAlign': 'center', 'borderRight': '1px solid #e0e0e0'}),
        
        html.Div([
            html.Div('Average Rent', style={'fontSize': '12px', 'color': '#666', 'marginBottom': '8px', 'fontWeight': '500'}),
            html.Div(f"${int(duval['actual_rent'].mean()):,}", style={'fontSize': '36px', 'fontWeight': '700', 'color': '#1a1a1a'})
        ], style={'flex': '1', 'padding': '20px', 'textAlign': 'center', 'borderRight': '1px solid #e0e0e0'}),
        
        html.Div([
            html.Div('Avg Percentile', style={'fontSize': '12px', 'color': '#666', 'marginBottom': '8px', 'fontWeight': '500'}),
            html.Div(f"{int(duval['percentile'].mean())}", style={'fontSize': '36px', 'fontWeight': '700', 'color': '#0066cc'})
        ], style={'flex': '1', 'padding': '20px', 'textAlign': 'center', 'borderRight': '1px solid #e0e0e0'}),
        
        html.Div([
            html.Div('Below Market', style={'fontSize': '12px', 'color': '#666', 'marginBottom': '8px', 'fontWeight': '500'}),
            html.Div(f"{len(duval[duval['savings'] > 0])}", style={'fontSize': '36px', 'fontWeight': '700', 'color': '#00a86b'})
        ], style={'flex': '1', 'padding': '20px', 'textAlign': 'center', 'borderRight': '1px solid #e0e0e0'}),
        
        html.Div([
            html.Div('Avg Savings', style={'fontSize': '12px', 'color': '#666', 'marginBottom': '8px', 'fontWeight': '500'}),
            html.Div(f"${int(duval[duval['savings'] > 0]['savings'].mean()):,}", style={'fontSize': '36px', 'fontWeight': '700', 'color': '#00a86b'})
        ], style={'flex': '1', 'padding': '20px', 'textAlign': 'center'})
    ], style={'display': 'flex', 'backgroundColor': 'white', 'marginBottom': '16px'}),
    
    # Percentile Chart
    html.Div([
        html.H3('Affordability Percentile Rankings', style={'fontSize': '18px', 'fontWeight': '600', 'color': '#1a1a1a', 'marginBottom': '8px'}),
        html.P('Percentile rank vs all 2,128 ZIPs in dataset (100 = most affordable)', style={'fontSize': '13px', 'color': '#666', 'marginBottom': '20px'}),
        dcc.Graph(id='percentile-chart', config={'displayModeBar': False}, style={'height': '400px'})
    ], style={'backgroundColor': 'white', 'padding': '24px 32px', 'marginBottom': '16px'}),
    
    # Data Table
    html.Div([
        html.H3('ZIP Code Details', style={'fontSize': '18px', 'fontWeight': '600', 'color': '#1a1a1a', 'marginBottom': '20px'}),
        dash_table.DataTable(
            id='data-table',
            columns=[
                {'name': 'ZIP Code', 'id': 'geoid'},
                {'name': 'Percentile', 'id': 'percentile'},
                {'name': 'Actual Rent', 'id': 'actual_rent'},
                {'name': 'Predicted Rent', 'id': 'predicted_rent'},
                {'name': 'Savings', 'id': 'savings'},
                {'name': 'Bachelor %', 'id': 'pct_bachelors_plus'},
                {'name': 'HS Only %', 'id': 'pct_hs_only'},
                {'name': 'Med Income', 'id': 'median_household_income'},
                {'name': 'Population', 'id': 'Total Population (2020-2024)'},
            ],
            data=duval.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_cell={
                'textAlign': 'right',
                'padding': '14px 16px',
                'fontSize': '14px',
                'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
                'border': 'none',
                'borderBottom': '1px solid #f0f0f0'
            },
            style_cell_conditional=[
                {'if': {'column_id': 'geoid'}, 'textAlign': 'left', 'fontWeight': '600', 'color': '#0066cc'}
            ],
            style_header={
                'backgroundColor': '#f8f9fa',
                'fontWeight': '600',
                'color': '#1a1a1a',
                'border': 'none',
                'borderBottom': '2px solid #dee2e6',
                'fontSize': '13px',
                'textAlign': 'right',
                'padding': '14px 16px'
            },
            style_data_conditional=[
                {'if': {'filter_query': '{percentile} >= 90'}, 'backgroundColor': '#d4edda'},
                {'if': {'filter_query': '{percentile} >= 75 && {percentile} < 90'}, 'backgroundColor': '#e8f5e9'},
                {'if': {'filter_query': '{percentile} < 25'}, 'backgroundColor': '#f8d7da'},
            ],
            page_size=30,
            sort_action='native',
            filter_action='native',
        )
    ], style={'backgroundColor': 'white', 'padding': '24px 32px'}),
    
], style={'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif', 'backgroundColor': '#f5f7fa', 'minHeight': '100vh', 'padding': '16px'})

@app.callback(Output('percentile-chart', 'figure'), Input('percentile-chart', 'id'))
def update_chart(_):
    fig = go.Figure()
    
    def get_color(p):
        if p >= 90: return '#00a86b'
        if p >= 75: return '#52c41a'
        if p >= 50: return '#faad14'
        if p >= 25: return '#ff7a45'
        return '#f5222d'
    
    colors = [get_color(p) for p in duval['percentile']]
    
    fig.add_trace(go.Bar(
        y=duval['geoid'],
        x=duval['percentile'],
        orientation='h',
        marker=dict(color=colors, line=dict(width=0)),
        text=duval['percentile'].astype(str),
        textposition='outside',
        textfont=dict(size=11, color='#1a1a1a', family='-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'),
        hovertemplate='<b>ZIP %{y}</b><br>Percentile: %{x}<br>Savings: $%{customdata:,}<extra></extra>',
        customdata=duval['savings']
    ))
    
    fig.update_layout(
        xaxis_title='Affordability Percentile',
        yaxis_title='',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif', size=12, color='#1a1a1a'),
        xaxis=dict(
            showgrid=True,
            gridcolor='#f0f0f0',
            range=[0, 105],
            tickfont=dict(size=11)
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(size=11),
            autorange='reversed'
        ),
        margin=dict(l=60, r=60, t=20, b=50),
        height=400
    )
    return fig

if __name__ == '__main__':
    print("="*80)
    print("StateofJax Dashboard - http://127.0.0.1:8050")
    print("="*80)
    app.run(debug=False, port=8050)
