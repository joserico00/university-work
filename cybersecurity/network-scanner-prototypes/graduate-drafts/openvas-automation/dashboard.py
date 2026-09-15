import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State, ALL
import pandas as pd
from datetime import datetime as dt
import plotly.express as px
import plotly.graph_objs as go
import json

# Load and prepare the dataset
df = pd.read_csv("data/scan_results.csv")
vulnerability_data = pd.read_csv('data/openvasscan.csv')

# Preparing grouped data
grouped_data = vulnerability_data.groupby(['IP', 'NVT Name', 'Severity']).first().reset_index()
grouped_data['Details'] = grouped_data.apply(lambda row: f"CVSS: {row['CVSS']}\nSeverity: {row['Severity']}\nSummary: {row['Summary']}\nSolution Type: {row['Solution Type']}", axis=1)

# List of unique IPs for the dropdown
unique_ips = vulnerability_data['IP'].unique().tolist()
unique_ips.insert(0, 'All')

# Convert Timestamp to datetime and sort
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df.sort_values('Timestamp', inplace=True)

# Extract unique timestamps
unique_timestamps = df['Timestamp'].unique()

# Prepare data for the timeline graph, grouped by day
df['Date'] = df['Timestamp'].dt.date
ip_count_over_time = df.groupby('Date')['IP'].nunique().reset_index()
ip_count_over_time.columns = ['Date', 'IP_Count']

# Create the Plotly graph
timeline_fig = px.line(ip_count_over_time, x='Date', y='IP_Count', title='Number of IPs Over Time')
timeline_fig.update_layout(
    xaxis_title="Date",
    yaxis_title="IP Count"
)

# Initialize the Dash app
app = dash.Dash(__name__)

# Convert timestamps to strings for slider display
timestamp_options = [{'label': str(ts), 'value': ts} for ts in df['Timestamp'].unique()]
timestamp_values = [ts.value for ts in df['Timestamp']]

def style_status_badge(status):
    emoji_map = {
        'Added': '🟩',
        'Removed': '🟥',
        'Still Active': '⚪'
    }
    return f"{emoji_map.get(status, '⬜')} {status}"


app.layout = html.Div([
    dcc.Tabs(id="tabs", children=[
        dcc.Tab(label='Overview', children=[
            html.Div([
                dcc.RangeSlider(
                    id='time-range-slider',
                    min=0,
                    max=len(unique_timestamps) - 1,
                    value=[0, len(unique_timestamps) - 1],
                    marks={i: {'label': str(ts)[:10]} for i, ts in enumerate(unique_timestamps)},
                    step=1,
                    allowCross=False
                ),
                dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i, "presentation": "markdown"} if i == "Status" else {"name": i, "id": i} 
                    for i in df.columns
                    ] + [{"name": "Status", "id": "Status", "presentation": "markdown"}],
                    sort_action='native',
                    filter_action='native',
                    style_table={'overflowX': 'auto'},
                    style_data_conditional=[{'if': {'column_id': 'Status'}, 'textAlign': 'center', 'width': '120px'}]
                ),
                html.Div([
                    dcc.Graph(
                        id='timeline-graph',
                        figure=timeline_fig
                    ),
                    dcc.Graph(id='open-ports-bar-chart')
                ], style={'display': 'flex', 'flex-direction': 'row'}),
                html.Div([
                    dcc.Graph(id='severity-pie-chart'),
                    dcc.Graph(id='ip-port-heatmap')
                ], style={'display': 'flex', 'flex-direction': 'row'}),
                html.Div([
                    dcc.Graph(id='ip-change-bar-chart'),
                    dash_table.DataTable(
                        id='ip-change-table',
                        columns=[
                            {"name": "IP", "id": "IP"},
                            {"name": "Status", "id": "Status"}
                        ],
                        sort_action='native',
                        filter_action='native',
                        style_table={'overflowX': 'auto'}
                    )
                ], style={'display': 'flex', 'flex-direction': 'row'}),
                html.Div(id='summary-section', style={'padding': '20px'})
            ])
        ]),
        dcc.Tab(label='Vulnerability Analysis', children=[
            html.Div([
                dcc.Dropdown(
                    id='severity-dropdown',
                    options=[{'label': s, 'value': s} for s in ['All', 'High', 'Medium', 'Low']],
                    value='All'
                ),
                dcc.Dropdown(
                    id='ip-dropdown',
                    options=[{'label': ip, 'value': ip} for ip in unique_ips],
                    value='All'
                ),
                dcc.Graph(id='vulnerability-treemap'),
                html.Div(id='details-and-ip-output'),
                html.Div(id='clicked-ip', style={'display': 'none'})
            ])
        ])
    ])
])

@app.callback(
    [Output('table', 'data'),
     Output('table', 'style_data_conditional'),
     Output('timeline-graph', 'figure'),
     Output('open-ports-bar-chart', 'figure'),
     Output('severity-pie-chart', 'figure'),
     Output('ip-port-heatmap', 'figure'),
     Output('ip-change-bar-chart', 'figure'),
     Output('ip-change-table', 'data'),
     Output('summary-section', 'children')],
    [Input('time-range-slider', 'value')]
)
def update_overview_tab(time_range):
    start_index, end_index = time_range
    start_timestamp = unique_timestamps[start_index]
    end_timestamp = unique_timestamps[end_index]

    # Filter data within the selected time range
    filtered_df = df[(df['Timestamp'] >= start_timestamp) & (df['Timestamp'] <= end_timestamp)].copy()

    # Update table
    filtered_df_selected = filtered_df.copy()


    # Determine IPs in the time range
    #all_ips = set(filtered_df['IP'])
    #status_dict = {ip: 'Within Range' for ip in all_ips}

    # Assign badge-style labels using style_status_badge
    #filtered_df_selected['Status'] = filtered_df_selected['IP'].map(status_dict).fillna('Unknown')
   # filtered_df_selected['Status'] = filtered_df_selected['Status'].apply(style_status_badge)
    # Determine IPs in the time range
    all_ips = set(filtered_df['IP'])

    # Get previous IP set
    if start_index > 0:
        prev_timestamp = unique_timestamps[start_index - 1]
    else:
        prev_timestamp = start_timestamp

    prev_ips = set(df[df['Timestamp'] == prev_timestamp]['IP'])
    new_ips = all_ips - prev_ips
    removed_ips = prev_ips - all_ips
    existing_ips = all_ips.intersection(prev_ips)

    # Add dummy rows for removed IPs (with NaNs or placeholders)
    removed_rows = pd.DataFrame({
        "IP": list(removed_ips),
        "Hostname": "", "MAC Address": "", "Protocol": "", "Port": "", "Name": "",
        "State": "", "Product": "", "Version": "", "Extra Info": "",
        "Timestamp": pd.NaT, "Date": None
    })
    filtered_df_selected = pd.concat([filtered_df_selected, removed_rows], ignore_index=True)

    

    # Build status dictionary for badges
    status_dict = {}
    for ip in new_ips:
        status_dict[ip] = 'Added'
    for ip in removed_ips:
        status_dict[ip] = 'Removed'
    for ip in existing_ips:
        status_dict[ip] = 'Still Active'

    # Assign and badge
    filtered_df_selected['Status'] = filtered_df_selected['IP'].map(status_dict).fillna('Unknown')
    filtered_df_selected['Status'] = filtered_df_selected['Status'].apply(style_status_badge)

    # Apply conditional formatting based on the 'Status' column
    style = [
    {
        'if': {
            'filter_query': '{Status} = "Added"',
        },
        'borderLeft': '4px solid green',
        'backgroundColor': '#eaf7ea'  # very light green background
    },
    {
        'if': {
            'filter_query': '{Status} = "Removed"',
        },
        'borderLeft': '4px solid red',
        'backgroundColor': '#fcebea'  # very light red background
    },
    {
        'if': {
            'filter_query': '{Status} = "Still Active"',
        },
        'borderLeft': '4px solid lightgray'
    }
]

    # Update timeline graph, grouped by day
    filtered_df['Date'] = filtered_df['Timestamp'].dt.date
    ip_count_over_time = filtered_df.groupby('Date')['IP'].nunique().reset_index()
    ip_count_over_time.columns = ['Date', 'IP_Count']
    timeline_fig = px.line(ip_count_over_time, x='Date', y='IP_Count', title='Number of IPs Over Time')
    timeline_fig.update_layout(
        xaxis_title="Date",
        yaxis_title="IP Count"
    )

    # Open ports bar chart
    open_ports_count = filtered_df['Port'].value_counts().reset_index()
    open_ports_count.columns = ['Port', 'Count']
    open_ports_bar_chart = px.bar(open_ports_count, x='Port', y='Count', title='Distribution of Open Ports')
    open_ports_bar_chart.update_layout(
        xaxis_title="Port",
        yaxis_title="Count"
    )
    open_ports_bar_chart.update_traces(marker_color='blue', marker_line_color='darkblue', marker_line_width=1.5, opacity=0.8)

    # Severity pie chart
    severity_count = vulnerability_data['Severity'].value_counts().reset_index()
    severity_count.columns = ['Severity', 'Count']
    severity_pie_chart = px.pie(severity_count, names='Severity', values='Count', title='Severity Distribution')

    # IP-Port heatmap
    ip_port_matrix = pd.crosstab(filtered_df['IP'], filtered_df['Port'])
    ip_port_heatmap = go.Figure(data=go.Heatmap(
        z=ip_port_matrix.values,
        x=ip_port_matrix.columns,
        y=ip_port_matrix.index,
        colorscale='Viridis'
    ))
    ip_port_heatmap.update_layout(
        title='IP and Port Correlation Heatmap',
        xaxis_title='Port',
        yaxis_title='IP'
    )

    # Determine IPs added and removed
    if start_index > 0:
        prev_timestamp = unique_timestamps[start_index - 1]
    else:
        prev_timestamp = start_timestamp

    prev_ips = set(df[df['Timestamp'] == prev_timestamp]['IP'])
    new_ips = all_ips - prev_ips
    removed_ips = prev_ips - all_ips
    existing_ips = all_ips.intersection(prev_ips)

    # IP change table
    ip_change_data = []
    for ip in new_ips:
        ip_change_data.append({"IP": ip, "Status": "Added"})
    for ip in removed_ips:
        ip_change_data.append({"IP": ip, "Status": "Removed"})
    for ip in existing_ips:
        ip_change_data.append({"IP": ip, "Status": "Still Active"})

    # IP change bar chart
    ip_change_summary = {
        "Added": len(new_ips),
        "Removed": len(removed_ips),
        "Still Active": len(existing_ips)
    }
    ip_change_bar_chart = px.bar(
        x=list(ip_change_summary.keys()),
        y=list(ip_change_summary.values()),
        title="IP Changes Summary"
    )
    ip_change_bar_chart.update_layout(
        xaxis_title="Change Type",
        yaxis_title="Count"
    )
    ip_change_bar_chart.update_traces(marker_color='purple', marker_line_color='darkblue', marker_line_width=1.5, opacity=0.8)

    # Summary section
    total_unique_ips = len(df['IP'].unique())
    total_vulnerabilities = len(vulnerability_data)
    most_common_ports = filtered_df['Port'].value_counts().head(5).to_dict()
    most_dangerous_vulnerability = vulnerability_data.loc[vulnerability_data['CVSS'].idxmax()]
    most_common_vulnerability = vulnerability_data['NVT Name'].value_counts().idxmax()
    most_common_ip = df['IP'].value_counts().idxmax()
    average_cvss_score = vulnerability_data['CVSS'].mean()
    ips_with_most_vulnerabilities = vulnerability_data['IP'].value_counts().head(5).to_dict()
    
    summary_content = html.Div([
        html.H3("Summary of Interesting Data"),
        html.P(f"Total unique IPs: {total_unique_ips}"),
        html.P(f"Total vulnerabilities recorded: {total_vulnerabilities}"),
        html.P(f"Most dangerous vulnerability (highest CVSS score): {most_dangerous_vulnerability['NVT Name']} with CVSS score {most_dangerous_vulnerability['CVSS']}"),
        html.P(f"Most common vulnerability: {most_common_vulnerability}"),
        html.P(f"Most common IP: {most_common_ip}"),
        html.P(f"Average CVSS score: {average_cvss_score:.2f}"),
        html.H4("Most Common Ports:"),
        html.Ul([html.Li(f"Port {port}: {count} times") for port, count in most_common_ports.items()]),
        html.H4("IPs with the Most Vulnerabilities:"),
        html.Ul([html.Li(f"IP {ip}: {count} vulnerabilities") for ip, count in ips_with_most_vulnerabilities.items()])
    ])

    return (filtered_df_selected.to_dict('records'), style, timeline_fig, open_ports_bar_chart, severity_pie_chart,
            ip_port_heatmap, ip_change_bar_chart, ip_change_data, summary_content)

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

    fig = px.treemap(
        filtered_data,
        path=['IP', 'NVT Name'],
        values='CVSS',
        color='CVSS',
        color_continuous_scale='reds',
        hover_data=['Details']
    )
    return fig, ""  # Reset clicked-ip because of bug

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
            html.Div([html.A(ip, href='#', id={'type': 'dynamic-ip', 'index': ip}, style={'marginRight': '10px', 'cursor': 'pointer'}) for ip in matching_ips])
        ])
    return 'Click on a vulnerability to see details and related IPs.'

if __name__ == '__main__':
    app.run_server(debug=True)
