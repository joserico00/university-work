import dash
from dash import Dash, dcc, html

from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load and prepare your data
vulnerability_data = pd.read_csv('openvasscan.csv')
# ... [data preparation steps]
# Global definition of grouped_data
color_map = {'Low': 'green', 'Medium': 'yellow', 'High': 'red'}
vulnerability_data['Color'] = vulnerability_data['Severity'].map(color_map)

grouped_data = vulnerability_data.groupby(['IP', 'NVT Name']).first().reset_index()
grouped_data['Details'] = grouped_data.apply(lambda row: f"CVSS: {row['CVSS']}\nSeverity: {row['Severity']}\nSummary: {row['Summary']}\nSolution Type: {row['Solution Type']}", axis=1)

# List of unique IPs for the dropdown
unique_ips = vulnerability_data['IP'].unique().tolist()
unique_ips.insert(0, 'All')  # Adding 'All' option at the beginning

# Initialize the Dash app
app = dash.Dash(__name__)

# Set up the layout of the app
app.layout = html.Div([
    dcc.Dropdown(
        id='severity-dropdown',
        options=[
            {'label': 'All', 'value': 'All'},
            {'label': 'High', 'value': 'High'},
            {'label': 'Medium', 'value': 'Medium'},
            {'label': 'Low', 'value': 'Low'}
        ],
        value='All'  # default value
    ),
    dcc.Dropdown(
        id='ip-dropdown',
        options=[{'label': ip, 'value': ip} for ip in unique_ips],
        value='All'  # default value
    ),
    dcc.Graph(id='vulnerability-treemap'),
    html.Div(id='clicked-ip', style={'display': 'none'}),

    html.Div(id='details-and-ip-output') 
    
])

# Callback to update the treemap
@app.callback(
    Output('vulnerability-treemap', 'figure'),
    [Input('severity-dropdown', 'value'),
     Input('ip-dropdown', 'value'),
     Input('clicked-ip', 'children'),
     Input('ip-list-output', 'children')]  # Assuming 'ip-list-output' is the ID for your related IPs list
)
def update_treemap(selected_severity, selected_ip,clicked_ip):
    filtered_data = grouped_data
    if selected_severity != 'All':
        filtered_data = filtered_data[filtered_data['Severity'] == selected_severity]
    if selected_ip != 'All':
        filtered_data = filtered_data[filtered_data['IP'] == selected_ip]
    if clicked_ip:
        filtered_data = filtered_data[filtered_data['IP'] == clicked_ip]


    fig = px.treemap(filtered_data, 
                     path=['IP', 'NVT Name'], 
                     values='CVSS', 
                     color='Severity',
                     hover_data=['Details'],
                     color_discrete_map={'Low': 'green', 'Medium': 'yellow', 'High': 'red'}  # Explicit color mapping

                     )
    return fig


@app.callback(
    Output('details-and-ip-output', 'children'),
    [Input('vulnerability-treemap', 'clickData')]
)
def display_details_and_ips(clickData):
    if clickData is not None:
        # Extract the clicked vulnerability details
        clicked_vuln = clickData['points'][0]['label'].split('<br>')[0]  # Adjust if label format differs
        details = clickData['points'][0]['customdata'][0]

        # Find matching IPs
        matching_ips = vulnerability_data[vulnerability_data['NVT Name'] == clicked_vuln]['IP'].unique()

        # Create content to display
        details_content = html.Div([
            html.H4("Vulnerability Details:"),
            html.Pre(details),
            html.H4("Related IPs with the same vulnerability:"),
            html.Div([dcc.Link(ip, href='#', id={'type': 'dynamic-ip', 'index': ip}) for ip in matching_ips])

        ])

        return details_content

    return 'Click on a vulnerability to see details and related IPs.'

@app.callback(
    Output('clicked-ip', 'children'),
    [Input({'type': 'dynamic-ip', 'index': 'ALL'}, 'n_clicks'),
    State({'type': 'dynamic-ip', 'index': 'ALL'}, 'index')]
)


def update_clicked_ip(n_clicks, index):
    # Determine which IP was clicked
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        clicked_ip = json.loads(button_id)['index']
        return clicked_ip
    
    
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

