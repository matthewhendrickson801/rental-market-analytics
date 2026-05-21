#!/usr/bin/env python3
print("Script started")

from dash import Dash, html
print("Imports successful")

app = Dash(__name__)
print("App created")

app.layout = html.Div("Hello World")
print("Layout set")

if __name__ == '__main__':
    print("Starting server...")
    app.run(debug=True, port=8050)
