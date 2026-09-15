import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State, ALL
import pandas as pd
from datetime import datetime as dt
import plotly.express as px
import json
# Load and prepare the dataset
df = pd.read_csv("scan_results.csv")

# Convert Timestamp to datetime and sort
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df.sort_values('Timestamp', inplace=True)

# Extract unique timestamps
unique_timestamps = df['Timestamp'].unique()

# Dictionary to track IP states at each timestamp
ip_states = {timestamp: set() for timestamp in unique_timestamps}
# Sort by timestamp for easier processing
df.sort_values(by='Timestamp', inplace=True)
# Prepare data for the timeline graph
ip_count_over_time = df.groupby('Timestamp')['IP'].nunique().reset_index()
ip_count_over_time.columns = ['Timestamp', 'IP_Count']

# Create the Plotly graph
timeline_fig = px.line(ip_count_over_time, x='Timestamp', y='IP_Count', title='Number of IPs Over Time')

# Initialize the Dash app
app = dash.Dash(__name__)

# Create slider marks (sample, adjust according to your data)
slider_marks = {i: {'label': str(time)} for i, time in enumerate(df['Timestamp'].unique())}
legend = html.Div([
    html.Div([
        html.Span(style={'display': 'inline-block', 'width': '20px', 'height': '20px', 'backgroundColor': 'blue'}),
        html.Span(' New', style={'marginRight': '20px'}),
        html.Span(style={'display': 'inline-block', 'width': '20px', 'height': '20px', 'backgroundColor': 'green'}),
        html.Span(' Existing', style={'marginRight': '20px'}),
        html.Span(style={'display': 'inline-block', 'width': '20px', 'height': '20px', 'backgroundColor': 'red'}),
        html.Span(' Gone', style={'marginRight': '20px'}),
        html.Span(style={'display': 'inline-block', 'width': '20px', 'height': '20px', 'backgroundColor': 'grey'}),
        html.Span(' Unknown')
    ], style={'padding': '10px'})
])

# Convert timestamps to strings for dropdown display
timestamp_options = [{'label': str(ts), 'value': str(ts)} for ts in df['Timestamp'].unique()]
app.layout = html.Div([
    dcc.Tabs(id="tabs", children=[
        dcc.Tab(label='IP Table', children=[
            html.Div([
                legend,  # Your existing legend
                dcc.Dropdown(
                    id='timestamp-dropdown',
                    options=timestamp_options,
                    value=str(df['Timestamp'].max())
                ),
                dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in df.columns],
                    data=[]
                )
            ])
        ]),
        dcc.Tab(label='Timeline Graph', children=[
            dcc.Graph(
                id='timeline-graph',
                figure=timeline_fig
            )
        ]),
        dcc.Tab(label='Tab 3', children=[
            html.Div([
                # Content for Tab 3
            ])
        ])
    ])
])
@app.callback(
    Output('table', 'data'),
    Output('table', 'style_data_conditional'),
    [Input('timestamp-dropdown', 'value')]
)
def update_table(selected_timestamp_str):
    selected_timestamp = pd.to_datetime(selected_timestamp_str)

    # Find the index of the selected timestamp
    timestamp_index = list(unique_timestamps).index(selected_timestamp)

    # Determine the previous timestamp
    # Ensure that there is a previous timestamp (i.e., the selected one isn't the first)
    if timestamp_index > 0:
        prev_timestamp = unique_timestamps[timestamp_index - 1]
    else:
        prev_timestamp = selected_timestamp  # Handle edge case where there is no previous timestamp

    # Find the previous timestamp    # Get sets of IPs for the immediately preceding and selected timestamps
    prev_ips = set(df[df['Timestamp'] == prev_timestamp]['IP'])
    selected_ips = set(df[df['Timestamp'] == selected_timestamp]['IP'])

    filtered_df_selected = df[df['Timestamp'].isin([prev_timestamp, selected_timestamp])].copy()


    # Determine new, existing, and gone IPs
    new_ips = selected_ips - prev_ips
    existing_ips = selected_ips.intersection(prev_ips)
    gone_ips = prev_ips - selected_ips
    print("Previous IPs:", prev_ips)
    print("Selected IPs:", selected_ips)
    print("Gone IPs:", gone_ips)
    # Assign 'Status' to each row in filtered_df_selected
    # Create a status dictionary for all IPs
    all_ips = prev_ips.union(selected_ips)
    status_dict = {ip: ('Existing' if ip in existing_ips else 'New' if ip in new_ips else 'Gone') for ip in all_ips}

    # Add a 'Status' column to filtered_df_selected
    filtered_df_selected['Status'] = filtered_df_selected['IP'].map(status_dict).fillna('Unknown')

    # Apply conditional formatting based on the 'Status' column
    style = [
        {
            'if': {
                'filter_query': '{Status} = "New"',
            },
            'backgroundColor': 'blue',
            'color': 'white'
        },
        {
            'if': {
                'filter_query': '{Status} = "Existing"',
            },
            'backgroundColor': 'green',
            'color': 'white'
        },
        {
            'if': {
                'filter_query': '{Status} = "Gone"',
            },
            'backgroundColor': 'red',
            'color': 'white'
        },
        {
            'if': {
                'filter_query': '{Status} = "Unknown"',
            },
            'backgroundColor': 'grey',
            'color': 'white'
        }
]
    
    
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




    
    return filtered_df_selected.to_dict('records'), style
if __name__ == '__main__':
    app.run_server(debug=True)