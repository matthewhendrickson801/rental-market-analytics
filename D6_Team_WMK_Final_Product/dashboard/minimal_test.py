from dash import Dash, html

print("Creating app...")
app = Dash(__name__)
app.layout = html.Div("Hello World")

print("Starting server on http://127.0.0.1:8050")
print("Press Ctrl+C to stop")

if __name__ == '__main__':
    app.run(debug=False, port=8050)
