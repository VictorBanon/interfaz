import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px

df = pd.DataFrame({
    "Category": ["A", "B", "C", "D"],
    "Value": [10, 23, 45, 12]
})

fig = px.bar(df, x="Category", y="Value", title="Sample Chart")

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("🚀 Dash App on Render"),
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=10000)
