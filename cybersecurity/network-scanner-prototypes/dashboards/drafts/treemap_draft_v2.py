import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State, ALL
import plotly.express as px
import pandas as pd
import json

# Load and prepare your data
vulnerability_data = pd.read_csv('openvasscan.csv')

# Mapping for severity colors
color_map = {'Low': 'green', 'Medium': 'yellow', 'High': 'red'}
vulnerability_data['Severity Color'] = vulnerability_data['Severity'].map(color_map)

# Preparing grouped data
grouped_data = vulnerability_data.groupby(['IP', 'NVT Name', 'Severity']).first().reset_index()
grouped_data['Details'] = grouped_data.apply(lambda row: f"CVSS: {row['CVSS']}\nSeverity: {row['Severity']}\nSummary: {row['Summary']}\nSolution Type: {row['Solution Type']}", axis=1)


# List of unique IPs for the dropdown
unique_ips = vulnerability_data['IP'].unique().tolist()
unique_ips.insert(0, 'All')  # Adding 'All' option

# Initialize the Dash app
app = dash.Dash(__name__)

# Set up the layout of the app

app.layout = html.Div([
    dcc.Dropdown(
        id='severity-dropdown',
        options=[{'label': s, 'value': s} for s in ['All', 'High', 'Medium', 'Low']],
        value='All'  # Default value
    ),
    dcc.Dropdown(
        id='ip-dropdown',
        options=[{'label': ip, 'value': ip} for ip in unique_ips],
        value='All'  # Default value
    ),
    dcc.Graph(id='vulnerability-treemap'),
    html.Div(id='details-and-ip-output'),
    html.Div(id='clicked-ip', style={'display': 'none'})
])  
@app.callback(
    [Output('vulnerability-treemap', 'figure'),
     Output('clicked-ip', 'children')],
    [Input('severity-dropdown', 'value'),
     Input('ip-dropdown', 'value'),
     Input({'type': 'dynamic-ip', 'index': ALL}, 'n_clicks')],
    [State({'type': 'dynamic-ip', 'index': ALL}, 'index')]
)
def update_treemap(selected_severity, selected_ip, n_clicks, ip_indices):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'] if ctx.triggered else None
    # Determine if the callback was triggered by a related IP link click
    if ctx.triggered and 'dynamic-ip' in ctx.triggered[0]['prop_id']:
        # Extract clicked IP
        triggered_info = ctx.triggered[0]
        button_id = triggered_info['prop_id'].split('}.')[0] + '}'
        clicked_ip = json.loads(button_id)['index']
    else:
        clicked_ip = None
    
    # Filter data based on severity, dropdown IP, or clicked related IP
    filtered_data = grouped_data.copy()
    if selected_severity != 'All':
        filtered_data = filtered_data[filtered_data['Severity'] == selected_severity]
    if selected_ip != 'All':
        filtered_data = filtered_data[filtered_data['IP'] == selected_ip]
    if clicked_ip:
        filtered_data = filtered_data[filtered_data['IP'] == clicked_ip]
    print("Filtered Data:", filtered_data.head())

    fig = px.treemap(
        filtered_data,
        path=['IP', 'NVT Name'],
        values='CVSS',
        color='Severity Color',
        hover_data=['Details']
    )
    return fig, ""  # Reset clicked-ip
# Callback to display details and related IPs
@app.callback(
    Output('details-and-ip-output', 'children'),
    [Input('vulnerability-treemap', 'clickData')]
)
def display_details_and_ips(clickData):
    if clickData is not None:
        clicked_vuln = clickData['points'][0]['label'].split('<br>')[0]
        details = clickData['points'][0]['customdata'][0]
        matching_ips = vulnerability_data[vulnerability_data['NVT Name'] == clicked_vuln]['IP'].unique()
        
        return html.Div([
            html.Pre(f'Details of Selected Vulnerability:\n{details}'),
            html.H4("Related IPs with the same vulnerability:"),
            html.Div([html.A(ip, href='#', id={'type': 'dynamic-ip', 'index': ip}, style={'cursor': 'pointer'}) for ip in matching_ips])

        ])
    return 'Click on a vulnerability to see details and related IPs.'


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

