"""StateofJax Dashboard - Baseball Savant Style"""
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

app = Dash(__name__)
server = app.server

# Baseball Savant exact colors
SAVANT_RED = '#BA0C2F'
SAVANT_ORANGE = '#FF6B35'
SAVANT_YELLOW = '#FFD23F'
SAVANT_GREEN = '#27AE60'
SAVANT_BLUE = '#002D72'

app.layout = html.Div([
    html.Div([
        html.Img(src='data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48Y2lyY2xlIGN4PSIyMCIgY3k9IjIwIiByPSIxOCIgZmlsbD0iIzAwMkQ3MiIvPjwvc3ZnPg==', style={'height': '32px', 'marginRight': '12px'}),
        html.Div([
            html.H1('StateofJax', style={'margin': '0', 'fontSize': '24px', 'fontWeight': '700', 'color': SAVANT_BLUE, 'letterSpacing': '-0.5px'}),
            html.Div('Affordable Housing Dashboard', style={'fontSize': '11px', 'color': '#666', 'marginTop': '2px'})
        ])
    ], style={'display': 'flex', 'alignItems': 'center', 'padding': '12px 24px', 'backgroundColor': 'white', 'borderBottom': f'4px solid {SAVANT_BLUE}'}),
    
    html.Div([
        html.Div([
            html.Div('W', style={'fontSize': '11px', 'fontWeight': '600', 'color': '#999', 'marginBottom': '2px'}),
            html.Div('0', style={'fontSize': '32px', 'fontWeight': '700', 'color': '#333', 'lineHeight': '1'})
        ], style={'padding': '16px 24px', 'textAlign': 'center', 'borderRight': '1px solid #e0e0e0'}),
        html.Div([
            html.Div('L', style={'fontSize': '11px', 'fontWeight': '600', 'color': '#999', 'marginBottom': '2px'}),
            html.Div('0', style={'fontSize': '32px', 'fontWeight': '700', 'color': '#333', 'lineHeight': '1'})
        ], style={'padding': '16px 24px', 'textAlign': 'center', 'borderRight': '1px solid #e0e0e0'}),
        html.Div([
            html.Div('ERA', style={'fontSize': '11px', 'fontWeight': '600', 'color': '#999', 'marginBottom': '2px'}),
            html.Div(f"${int(duval['actual_rent'].mean())}", style={'fontSize': '32px', 'fontWeight': '700', 'color': '#333', 'lineHeight': '1'})
        ], style={'padding': '16px 24px', 'textAlign': 'center', 'borderRight': '1px solid #e0e0e0'}),
        html.Div([
            html.Div('G', style={'fontSize': '11px', 'fontWeight': '600', 'color': '#999', 'marginBottom': '2px'}),
            html.Div(f"{len(duval)}", style={'fontSize': '32px', 'fontWeight': '700', 'color': '#333', 'lineHeight': '1'})
        ], style={'padding': '16px 24px', 'textAlign': 'center', 'borderRight': '1px solid #e0e0e0'}),
        html.Div([
            html.Div('IP', style={'fontSize': '11px', 'fontWeight': '600', 'color': '#999', 'marginBottom': '2px'}),
            html.Div(f"{int(duval['percentile'].mean())}", style={'fontSize': '32px', 'fontWeight': '700', 'color': '#333', 'lineHeight': '1'})
        ], style={'padding': '16px 24px', 'textAlign': 'center'})
    ], style={'display': 'flex', 'backgroundColor': 'white', 'borderBottom': '1px solid #e0e0e0'}),
    
    html.Div([
        html.Div([
            html.Div([
                html.Div('2026 Percentile Rankings', style={'fontSize': '14px', 'fontWeight': '700', 'color': '#333', 'marginBottom': '4px'}),
                html.Div('savant', style={'fontSize': '11px', 'color': SAVANT_BLUE, 'fontWeight': '600', 'marginBottom': '16px'})
            ]),
            
            html.Div([
                html.Div([
                    html.Div('Value', style={'fontSize': '11px', 'fontWeight': '700', 'color': '#666', 'marginBottom': '8px'}),
                    html.Div('savant', style={'fontSize': '9px', 'color': SAVANT_BLUE, 'fontWeight': '600', 'marginBottom': '12px'}),
                    
                    html.Div([
                        html.Div('POOR', style={'fontSize': '9px', 'color': '#999', 'position': 'absolute', 'left': '0'}),
                        html.Div('AVERAGE', style={'fontSize': '9px', 'color': '#999', 'position': 'absolute', 'left': '50%', 'transform': 'translateX(-50%)'}),
                        html.Div('GREAT', style={'fontSize': '9px', 'color': '#999', 'position': 'absolute', 'right': '0'})
                    ], style={'position': 'relative', 'marginBottom': '8px', 'height': '12px'}),
                    
                    html.Div(id='percentile-rows')
                ], style={'width': '100%'})
            ])
        ], style={'backgroundColor': 'white', 'padding': '20px 24px', 'marginBottom': '12px'}),
        
        html.Div([
            html.H3('Statcast Statistics', style={'fontSize': '14px', 'fontWeight': '700', 'color': '#333', 'marginBottom': '16px'}),
            dash_table.DataTable(
                id='stats-table',
                columns=[
                    {'name': 'ZIP', 'id': 'geoid'},
                    {'name': 'Percentile', 'id': 'percentile'},
                    {'name': 'Actual', 'id': 'actual_rent'},
                    {'name': 'Predicted', 'id': 'predicted_rent'},
                    {'name': 'Savings', 'id': 'savings'},
                    {'name': 'Bach%', 'id': 'pct_bachelors_plus'},
                    {'name': 'Income', 'id': 'median_household_income'},
                    {'name': 'Pop', 'id': 'Total Population (2020-2024)'},
                ],
                data=duval.to_dict('records'),
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'right', 'padding': '12px 16px', 'fontSize': '13px', 'fontFamily': 'Arial, sans-serif', 'border': 'none', 'borderBottom': '1px solid #f0f0f0'},
                style_cell_conditional=[{'if': {'column_id': 'geoid'}, 'textAlign': 'left', 'fontWeight': '600', 'color': SAVANT_BLUE}],
                style_header={'backgroundColor': '#fafafa', 'fontWeight': '700', 'color': '#666', 'border': 'none', 'borderBottom': '2px solid #e0e0e0', 'fontSize': '11px', 'textAlign': 'right', 'padding': '12px 16px'},
                page_size=30,
                sort_action='native',
            )
        ], style={'backgroundColor': 'white', 'padding': '20px 24px'}),
    ], style={'padding': '16px', 'backgroundColor': '#f5f5f5'}),
    
], style={'fontFamily': 'Arial, Helvetica, sans-serif', 'backgroundColor': '#f5f5f5', 'minHeight': '100vh'})

@app.callback(Output('percentile-rows', 'children'), Input('percentile-rows', 'id'))
def update_percentile_rows(_):
    rows = []
    for _, row in duval.head(10).iterrows():
        p = row['percentile']
        
        if p >= 80: color = SAVANT_GREEN
        elif p >= 60: color = SAVANT_YELLOW
        elif p >= 40: color = SAVANT_ORANGE
        else: color = SAVANT_RED
        
        rows.append(
            html.Div([
                html.Div(f"ZIP {row['geoid']}", style={'fontSize': '12px', 'fontWeight': '600', 'color': '#333', 'width': '120px'}),
                html.Div(f"{int(row['savings'])}", style={'fontSize': '12px', 'fontWeight': '700', 'color': '#333', 'width': '60px', 'textAlign': 'right'}),
                html.Div([
                    html.Div(style={'width': f'{p}%', 'height': '100%', 'backgroundColor': color, 'borderRadius': '2px'}),
                    html.Div(f"{p}", style={'position': 'absolute', 'right': '-30px', 'top': '50%', 'transform': 'translateY(-50%)', 'fontSize': '11px', 'fontWeight': '700', 'color': '#333'})
                ], style={'flex': '1', 'height': '20px', 'backgroundColor': '#f0f0f0', 'borderRadius': '2px', 'position': 'relative', 'marginLeft': '12px'})
            ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '8px'})
        )
    return rows

if __name__ == '__main__':
    print("="*80)
    print("StateofJax Dashboard - http://127.0.0.1:8050")
    print("="*80)
    app.run(debug=False, port=8050)
