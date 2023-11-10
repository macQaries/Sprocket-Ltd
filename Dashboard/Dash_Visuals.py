# Import required libraries
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash import dash_table as dt

Cust = 'Customer_RFM.csv'
New = 'NewCust_Predicted.csv'
old = pd.read_csv(Cust)
new = pd.read_csv(New)

old_target = old[old['segment'] == 'platinum']
oldpred = old_target.groupby('customer_id').agg({
    'first_name': lambda x: x.value_counts().index[0],
    'last_name': lambda x: x.value_counts().index[0],
    'gender': lambda x: x.value_counts().index[0],
    'job_title': lambda x: x.value_counts().index[0],
    'job_industry_category': lambda x: x.value_counts().index[0], 
    'wealth_segment': lambda x: x.value_counts().index[0],
    'age': lambda x: x.value_counts().index[0],
    'address': lambda x: x.value_counts().index[0],
    'postcode': lambda x: x.value_counts().index[0],
    'state': lambda x: x.value_counts().index[0],
    'monetary': lambda x: x.value_counts().index[0],
    'segment': lambda x: x.value_counts().index[0]
}).sort_values(by = ['monetary'], ascending = False).reset_index()

new_target = new[new['predicted_segment'] == 'platinum']

day = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
class_day = pd.api.types.CategoricalDtype(ordered = True, categories = day)
old["day_of_the_week"] = old["day_of_the_week"].astype(class_day)
month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
class_month = pd.api.types.CategoricalDtype(ordered = True, categories = month)
old["transaction_month"] = old["transaction_month"].astype(class_month)

def total_revenue_callback():
    revenue = old['list_price'].sum()
    return revenue

def total_profit_callback():
    profit = old['profit'].sum()
    return profit

app = Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP], meta_tags = [{"name": "viewport", "content": "width=device-width"}])
server = app.server

# Parent Div for entire container
app.layout = html.Div((
    
    # Header Div containing two containers
    html.Div([
        # First header container for title and image
        html.Div([
            html.Div([
                dbc.Container(children = [
                    dbc.Row([
                        dbc.Col(html.H6('SPROCKET SALES ANALYSIS'), style = {'margin-bottom': '0px', 'color': 'white'}),
                        dbc.Col(html.Img(src = 'assets/sprocket_logo.png', style = {'width': '100px'}))
                ], justify = 'start')
                ])           
            ])
        ], className = "one-third column", id = "title1"),
        # Second header container for months dropdown
        html.Div([
            html.P('Transaction Month', className = 'fix_label'),
            dcc.Dropdown(id = 'select_month',
                        options = [
                             # update dropdown values using list comphrehension
                             {"label": i, "value": i} for i in month
                             ],
                         placeholder = "select a month",
                         style = {"width": "100%", "padding": "3px", "font-size": "20px", "textAlign": "center"}
                        )
        ], className = "one-half column", id = "title2"),
    # Style the header container
    ], id = 'header', className = 'row flex-display'),

    # First row body Div containing four containers
    html.Div([
        # Body-container for radio button and bar chart
        html.Div([
            dcc.RadioItems(id = 'radio_items1',
                           labelStyle = {'display': 'inline-block'},
                           value = 'state',
                           options = [{'label': 'State', 'value': 'state'},
                                      {'label': 'Segment', 'value': 'wealth_segment'}],
                           style = {'text-align': 'center', 'color': 'white'}, className = 'dcc_compon'),
            dcc.Graph(id = 'bar_chart1',
                      config = {'displayModeBar': 'hover'}, style = {'height': '300px'}),           
        ], className = 'create_container2 three columns', style = {'height': '400px'}),
        # Body-container for donut chart
        html.Div([
            dcc.Graph(id = 'donut_chart1',
                      config = {'displayModeBar': 'hover'}, style = {'height': '300px'}),
        ], className = 'create_container2 three columns', style = {'height': '400px'}),
        # Body-container for line chart
        html.Div([
            dcc.Graph(id = 'line_chart1',
                      config = {'displayModeBar': 'hover'}, style = {'height': '300px'}),
        ], className = 'create_container2 four columns', style = {'height': '400px'}),
        # Body-container for text
        html.Div([
            html.Div([
                html.H6(children =
                        'Total Revenue',
                        style = {'textAlign': 'center',
                                 'color': 'white'}
                ),
                html.P(
                    '${0:,.2f}'.format(total_revenue_callback()),
                    style = {'textAlign': 'center',
                             'color': '#19AAE1',
                             'fontsize': 13,
                             'margin-top': '-10px'},
                )
            ]),
            
            html.Div([
                html.H6(children =
                        'Total Profit',
                        style = {'textAlign': 'center',
                                 'color': 'white'}
                ),
                html.P(
                    '${0:,.2f}'.format(total_profit_callback()),
                    style = {'textAlign': 'center',
                             'color': '#19AAE1',
                             'fontsize': 13,
                             'margin-top': '-10px'},
                )     
            ]),

            html.Div(id = 'text3'),
            html.Div(id = 'text4'),
        ], className = "create_container2 two columns", style = {'height': '400px'}),
    # Style the first row body-container
    ], className = 'row flex-display'),

    # Second row body Div containing three containers
    html.Div([
        # Body-container for radio button and bar chart
        html.Div([
            dcc.RadioItems(id = 'radio_items2',
                           labelStyle = {'display': 'inline-block'},
                           value = 'product_class',
                           options = [{'label': 'Class', 'value': 'product_class'},
                                      {'label': 'Size', 'value': 'product_size'},
                                      {'label': 'Line', 'value': 'product_line'}],
                           style = {'text-align': 'center', 'color': 'white'}, className = 'dcc_compon'),
            dcc.Graph(id = 'bar_chart2',
                      config = {'displayModeBar': 'hover'}, style = {'height': '350px'}),           
        ], className = 'create_container2 three columns', style = {'height': '400px'}),
        # Body-container for radio button and bar chart
        html.Div([
            dcc.RadioItems(id = 'radio_items3',
                           labelStyle = {'display': 'inline-block'},
                           value = 'list_price',
                           options = [{'label': 'Revenue', 'value': 'list_price'},
                                      {'label': 'Profit', 'value': 'profit'}],
                           style = {'text-align': 'center', 'color': 'white'}, className = 'dcc_compon'),
            dcc.Graph(id = 'bar_chart3',
                      config = {'displayModeBar': 'hover'}, style = {'height': '350px'}),           
        ], className = 'create_container2 four columns', style = {'height': '400px'}),
        # Body-container for bubble chart
        html.Div([
            dcc.Graph(id = 'bubble_chart1',
                      config = {'displayModeBar': 'hover'}, style = {'height': '350px'}),
        ], className = 'create_container2 four columns', style = {'height': '400px'}),
    # Style the second row body-container
    ], className = 'row flex-display'),

    # Third row body Div containing three containers
    html.Div([
        # Body-container for table chart
        html.Div([
            html.Label('Top Old Customers to Target', className = 'fix_label'),
            dt.DataTable(oldpred.to_dict('records'),
                         columns = [{'name': i, 'id': i} for i in
                                    oldpred.loc[:, ['first_name', 'last_name', 'gender', 'age',
                                                'job_title', 'job_industry_category', 'wealth_segment',
                                                'address', 'postcode', 'state', 'monetary', 'segment']]], 
                         sort_action = 'native',
                         sort_mode = 'multi',
                         virtualization = True,
                         style_cell = {'textAlign': 'left',
                                       'min-width': '100px',
                                       'backgroundColor': '#1f2c56',
                                       'color': '#FEFEFE',
                                       'border-bottom': '0.01rem solid #19AAE1'},
                         style_as_list_view = True,
                         style_header = {'backgroundColor': '#1f2c56',
                                         'fontWeight': 'bold',
                                         'font': 'orange',
                                         'border': '#1f2c56'},
                         style_data = {'textOverflow': 'hidden', 'color': 'white'},
                         fixed_rows = {'headers': True}
            ), 
        ], className = 'create_container2 five columns', style = {'height': '550px'}),
        # Body-container for table chart
        html.Div([
            html.Label('Top New Predicted Customers to Target', className = 'fix_label'),
            dt.DataTable(new_target.to_dict('records'),
                         columns = [{'name': i, 'id': i} for i in
                                    new_target.loc[:, ['first_name', 'last_name', 'gender',
                                                'age', 'wealth_segment', 'address', 'postcode',
                                                'state', 'predicted_segment']]], 
                        sort_action = 'native',
                        sort_mode = 'multi',
                        virtualization = True,
                        style_cell = {'textAlign': 'left',
                                      'min-width': '100px',
                                      'backgroundColor': '#1f2c56',
                                      'color': '#FEFEFE',
                                      'border-bottom': '0.01rem solid #19AAE1'},
                        style_as_list_view = True,
                        style_header = {'backgroundColor': '#1f2c56',
                                        'fontWeight': 'bold',
                                        'font': 'orange',
                                        'border': '#1f2c56'},
                        style_data = {'textOverflow': 'hidden', 'color': 'white'},
                        fixed_rows = {'headers': True}
            )
        ], className = 'create_container2 five columns', style = {'height': '550px'}),
    # Style the third row body-container
    ], className = 'row flex-display')
# Style the entire container
), id = 'mainContainer')

# Callback function for Radio Button and Bar Chart
@app.callback(Output('bar_chart1', 'figure'),
              [Input('select_month', 'value')],
              [Input('radio_items1', 'value')])
def update_graph(select_month, radio_items1):
    sales1 = old.groupby(['transaction_month', 'state'])['list_price'].sum().reset_index()
    sales2 = sales1[sales1['transaction_month'] == select_month].sort_values(by = ['list_price'], ascending = False)
    sales3 = old.groupby(['transaction_month', 'wealth_segment'])['list_price'].sum().reset_index()
    sales4 = sales3[sales3['transaction_month'] == select_month].sort_values(by = ['list_price'], ascending = False)
    groupsales1 = old.groupby('state')['list_price'].sum().reset_index().sort_values(by = ['list_price'], ascending = False)
    groupsales2 = old.groupby('wealth_segment')['list_price'].sum().reset_index().sort_values(by = ['list_price'], ascending = False)

    if select_month:
        if radio_items1 == 'state':
            return{
                'data':[
                    go.Bar(
                        x = sales2['list_price'],
                        y = sales2['state'],
                        text = sales2['list_price'],
                        texttemplate = '$' + '%{text:.2s}',
                        textposition = 'auto',
                        orientation = 'h',
                        marker = dict(color = '#19AAE1'),

                        hoverinfo = 'text',
                        hovertext = '<b>Month</b>: ' + sales2['transaction_month'].astype(str) + '<br>' +
                                    '<b>State</b>: ' + sales2['state'].astype(str) + '<br>' +
                                    '<b>Revenue</b>: $' + [f'{x:,.2f}' for x in sales2['list_price']] + '<br>'
                    )
                ],

                'layout': go.Layout(
                    plot_bgcolor = '#1f2c56',
                    paper_bgcolor = '#1f2c56',
                    title = {
                        'text': 'Revenue by State in ' + ' ' + str((select_month)),
                        'y': 0.99,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    titlefont = {
                        'color': 'white',
                        'size': 13
                    },
                    hovermode = 'closest',
                    margin = dict(t = 40, r = 0),
                
                    xaxis = dict(
                        title = '<b></b>',
                                color = 'orange',
                                showline = True,
                                showgrid = True,
                                showticklabels = True,
                                linecolor = 'orange',
                                linewidth = 1,
                                ticks = 'outside',
                                tickfont = dict(
                                    family = 'Arial',
                                    size = 10,
                                    color = 'orange'
                                )
                    ),
                    yaxis = dict(
                        title = '<b></b>',
                                autorange = 'reversed',
                                color = 'orange',
                                showline = False,
                                showgrid = False,
                                showticklabels = True,
                                linecolor = 'orange',
                                linewidth = 1,
                                ticks = 'outside',
                                tickfont = dict(
                                    family = 'Arial',
                                    size = 10,
                                    color = 'orange'
                                )
                    ),
                    legend = {
                        'orientation': 'h',
                        'bgcolor': '#1f2c56',
                        'x': 0.5,
                        'y': 1.25,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    font = dict(
                        family = 'sans-serif',
                        size = 15,
                        color = 'white'
                    ),
                )
            }
        
        elif radio_items1 == 'wealth_segment':
            return {
                'data':[
                    go.Bar(
                        x = sales4['list_price'],
                        y = sales4['wealth_segment'],
                        text = sales4['list_price'],
                        texttemplate = '$' + '%{text:.2s}',
                        textposition = 'auto',
                        orientation = 'h',
                        marker = dict(color = '#19AAE1'),

                        hoverinfo = 'text',
                        hovertext = '<b>Month</b>: ' + sales4['transaction_month'].astype(str) + '<br>' +
                                    '<b>Segment</b>: ' + sales4['wealth_segment'].astype(str) + '<br>' +
                                    '<b>Revenue</b>: $' + [f'{x:,.2f}' for x in sales4['list_price']] + '<br>'
                    )
                ],

                'layout': go.Layout(
                    plot_bgcolor = '#1f2c56',
                    paper_bgcolor = '#1f2c56',
                    title = {
                        'text': 'Revenue by Segment in ' + ' ' + str((select_month)),
                        'y': 0.99,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    titlefont = {
                        'color': 'white',
                        'size': 13
                    },
                    hovermode = 'closest',
                    margin = dict(t = 40, r = 0),
                    
                    xaxis = dict(
                        title = '<b></b>',
                                color = 'orange',
                                showline = True,
                                showgrid = True,
                                showticklabels = True,
                                linecolor = 'orange',
                                linewidth = 1,
                                ticks = 'outside',
                                tickfont = dict(
                                    family = 'Arial',
                                    size = 10,
                                    color = 'orange'
                                )
                    ),
                    yaxis = dict(
                        title = '<b></b>',
                                autorange = 'reversed',
                                color = 'orange',
                                showline = False,
                                showgrid = False,
                                showticklabels = True,
                                linecolor = 'orange',
                                linewidth = 1,
                                ticks = 'outside',
                                tickfont = dict(
                                    family = 'Arial',
                                    size = 10,
                                    color = 'orange'
                                )
                    ),
                    legend = {
                        'orientation': 'h',
                        'bgcolor': '#1f2c56',
                        'x': 0.5,
                        'y': 1.25,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    font = dict(
                        family = 'sans-serif',
                        size = 15,
                        color = 'white'
                    ),
                )
            }
    else:
        if radio_items1 == 'state':
            return{
                'data':[
                    go.Bar(
                        x = groupsales1['list_price'],
                        y = groupsales1['state'],
                        text = groupsales1['list_price'],
                        texttemplate = '$' + '%{text:.2s}',
                        textposition = 'auto',
                        orientation = 'h',
                        marker = dict(color = '#19AAE1'),

                        hoverinfo = 'text',
                        hovertext = '<b>State</b>: ' + groupsales1['state'].astype(str) + '<br>' +
                                    '<b>Revenue</b>: $' + [f'{x:,.2f}' for x in groupsales1['list_price']] + '<br>'
                    )
                ],
                'layout': go.Layout(
                    plot_bgcolor = '#1f2c56',
                    paper_bgcolor = '#1f2c56',
                    title = {
                        'text': 'Total Revenue by State',
                        'y': 0.99,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    titlefont = {
                        'color': 'white',
                        'size': 13
                    },
                    hovermode = 'closest',
                    margin = dict(t = 40, r = 0),
                
                    xaxis = dict(
                        title = '<b></b>',
                                color = 'orange',
                                showline = True,
                                showgrid = True,
                                showticklabels = True,
                                linecolor = 'orange',
                                linewidth = 1,
                                ticks = 'outside',
                                tickfont = dict(
                                    family = 'Arial',
                                    size = 10,
                                    color = 'orange'
                                )
                    ),
                    yaxis = dict(
                        title = '<b></b>',
                                autorange = 'reversed',
                                color = 'orange',
                                showline = False,
                                showgrid = False,
                                showticklabels = True,
                                linecolor = 'orange',
                                linewidth = 1,
                                ticks = 'outside',
                                tickfont = dict(
                                    family = 'Arial',
                                    size = 10,
                                    color = 'orange'
                                )
                    ),
                    legend = {
                        'orientation': 'h',
                        'bgcolor': '#1f2c56',
                        'x': 0.5,
                        'y': 1.25,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    font = dict(
                        family = 'sans-serif',
                        size = 15,
                        color = 'white'
                    ),
                )
            }
        elif radio_items1 == 'wealth_segment':
            return {
                'data':[
                    go.Bar(
                        x = groupsales2['list_price'],
                        y = groupsales2['wealth_segment'],
                        text = groupsales2['list_price'],
                        texttemplate = '$' + '%{text:.2s}',
                        textposition = 'auto',
                        orientation = 'h',
                        marker = dict(color = '#19AAE1'),

                        hoverinfo = 'text',
                        hovertext = '<b>Segment</b>: ' + groupsales2['wealth_segment'].astype(str) + '<br>' +
                                    '<b>Revenue</b>: $' + [f'{x:,.2f}' for x in groupsales2['list_price']] + '<br>'
                    )
                ],

                'layout': go.Layout(
                    plot_bgcolor = '#1f2c56',
                    paper_bgcolor = '#1f2c56',
                    title = {
                        'text': 'Total Revenue by Segment',
                        'y': 0.99,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    titlefont = {
                        'color': 'white',
                        'size': 13
                    },
                    hovermode = 'closest',
                    margin = dict(t = 40, r = 0),
                    
                    xaxis = dict(
                        title = '<b></b>',
                                color = 'orange',
                                showline = True,
                                showgrid = True,
                                showticklabels = True,
                                linecolor = 'orange',
                                linewidth = 1,
                                ticks = 'outside',
                                tickfont = dict(
                                    family = 'Arial',
                                    size = 10,
                                    color = 'orange'
                                )
                    ),
                    yaxis = dict(
                        title = '<b></b>',
                                autorange = 'reversed',
                                color = 'orange',
                                showline = False,
                                showgrid = False,
                                showticklabels = True,
                                linecolor = 'orange',
                                linewidth = 1,
                                ticks = 'outside',
                                tickfont = dict(
                                    family = 'Arial',
                                    size = 10,
                                    color = 'orange'
                                )
                    ),
                    legend = {
                        'orientation': 'h',
                        'bgcolor': '#1f2c56',
                        'x': 0.5,
                        'y': 1.25,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    font = dict(
                        family = 'sans-serif',
                        size = 15,
                        color = 'white'
                    ),
                )
            }

@app.callback(Output('donut_chart1', 'figure'),
              [Input('select_month', 'value')])
def update_graph(select_month):
    sales5 = old.groupby(['transaction_month', 'gender'])['list_price'].sum().reset_index()
    female_sales = sales5[(sales5['transaction_month'] == select_month) & (sales5['gender'] == 'Female')]['list_price'].sum()
    male_sales = sales5[(sales5['transaction_month'] == select_month) & (sales5['gender'] == 'Male')]['list_price'].sum()
    gender_sales = old.groupby('gender')['list_price'].sum().reset_index()
    colours = ['#30C9C7', '#7A45D1']

    if select_month:
        return {
            'data': [
                go.Pie(
                    labels = ['Female', 'Male'],
                    values = [female_sales, male_sales],
                    marker = dict(colors = colours),
                    hoverinfo = 'label+value+percent',
                    textinfo = 'label+value',
                    textfont = dict(size = 10),
                    texttemplate = '%{label} <br>$%{value:,.2f}',
                    textposition = 'auto',
                    hole = .7,
                    rotation = 160,
                )
            ],
            'layout': go.Layout(
                    plot_bgcolor = '#1f2c56',
                    paper_bgcolor = '#1f2c56',
                    hovermode = 'x',
                    margin = dict(t = 40, b = 0, l = 0, r = 0),
                    title = {
                        'text': 'Revenue by gender in ' + ' ' + str((select_month)),
                        'y': 0.95,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    titlefont = {
                        'color': 'white',
                        'size': 13
                    },
                    legend = {
                        'orientation': 'h',
                        'bgcolor': '#1f2c56',
                        'xanchor': 'center', 'x': 0.5, 'y': -0.15
                    },
                    font = dict(family = 'sans-serif',
                                size = 12,
                                color = 'white')
            ),
        }
    else:
        return {
            'data': [
                go.Pie(
                    labels = ['Female', 'Male'],
                    values = gender_sales['list_price'],
                    marker = dict(colors = colours),
                    hoverinfo = 'label+value+percent',
                    textinfo = 'label+value',
                    textfont = dict(size = 10),
                    texttemplate = '%{label} <br>$%{value:,.2f}',
                    textposition = 'auto',
                    hole = .7,
                    rotation = 160,
                )
            ],
            'layout': go.Layout(
                    plot_bgcolor = '#1f2c56',
                    paper_bgcolor = '#1f2c56',
                    hovermode = 'x',
                    margin = dict(t = 40, b = 0, l = 0, r = 0),
                    title = {
                        'text': 'Total revenue by gender',
                        'y': 0.95,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    titlefont = {
                        'color': 'white',
                        'size': 13
                    },
                    legend = {
                        'orientation': 'h',
                        'bgcolor': '#1f2c56',
                        'xanchor': 'center', 'x': 0.5, 'y': -0.15
                    },
                    font = dict(family = 'sans-serif',
                                size = 12,
                                color = 'white')
            ),
        }

@app.callback(Output('line_chart1', 'figure'),
              [Input('select_month', 'value')])
def update_graph(select_month):
    sales6 = old.groupby(['transaction_month', 'day_of_the_week'])['list_price'].sum().reset_index()
    sales7 = sales6[sales6['transaction_month'] == select_month]
    day_sales = old.groupby('day_of_the_week')['list_price'].sum().reset_index()

    if select_month:
        return{
            'data':[
                go.Scatter(
                    x = sales7['day_of_the_week'],
                    y = sales7['list_price'],
                    name = 'Day of the Week Sales',
                    text = sales7['list_price'],
                    texttemplate = '%{text:.2s}',
                    textposition = 'bottom left',
                    mode = 'markers+lines+text',
                    line = dict(width = 3, color = 'orange'),
                    marker = dict(size = 10, symbol = 'circle', color = '#19AAE1',
                                  line = dict(color = '#19AAE1', width = 2)),
                    hoverinfo = 'text',
                    hovertext = '<b>Month</b>: ' + sales7['transaction_month'].astype(str) + '<br>' +
                                '<b>Day</b>: ' + sales7['day_of_the_week'].astype(str) + '<br>' +
                                '<b>Revenue</b>: $' + [f'{x:,.2f}' for x in sales7['list_price']] + '<br>'
                )
            ],

            'layout': go.Layout(
                plot_bgcolor = '#1f2c56',
                paper_bgcolor = '#1f2c56',
                title = {
                    'text': 'Day Trend in ' + ' ' + str((select_month)),
                    'y': 0.95,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'
                },
                titlefont = {
                    'color': 'white',
                    'size': 13
                },
                hovermode = 'closest',
                margin = dict(t = 30, l = 0, r = 0),
                
                xaxis = dict(
                    title = '<b></b>',
                            visible = True,
                            color = 'orange',
                            showline = True,
                            showgrid = False,
                            showticklabels = True,
                            linecolor = 'orange',
                            linewidth = 1,
                            ticks = 'outside',
                            tickfont = dict(
                                family = 'Arial',
                                size = 10,
                                color = 'orange'
                            )
                ),
                yaxis = dict(
                    title = '<b></b>',
                            visible = True,
                            color = 'orange',
                            showline = False,
                            showgrid = True,
                            showticklabels = False,
                            linecolor = 'orange',
                            linewidth = 1,
                            ticks = '',
                            tickfont = dict(
                                family = 'Arial',
                                size = 10,
                                color = 'orange'
                            )
                ),
                legend = {
                    'orientation': 'h',
                    'bgcolor': '#1f2c56',
                    'x': 0.5,
                    'y': 1.25,
                    'xanchor': 'center',
                    'yanchor': 'top'
                },
                font = dict(
                    family = 'sans-serif',
                    size = 10,
                    color = 'white'
                ),
            )
        }
    else:
        return{
            'data':[
                go.Scatter(
                    x = day_sales['day_of_the_week'],
                    y = day_sales['list_price'],
                    name = 'Day of the Week Sales',
                    text = day_sales['list_price'],
                    texttemplate = '%{text:.2s}',
                    textposition = 'bottom left',
                    mode = 'markers+lines+text',
                    line = dict(width = 3, color = 'orange'),
                    marker = dict(size = 10, symbol = 'circle', color = '#19AAE1',
                                  line = dict(color = '#19AAE1', width = 2)),
                    hoverinfo = 'text',
                    hovertext = '<b>Day</b>: ' + day_sales['day_of_the_week'].astype(str) + '<br>' +
                                '<b>Revenue</b>: $' + [f'{x:,.2f}' for x in day_sales['list_price']] + '<br>'
                )
            ],

            'layout': go.Layout(
                plot_bgcolor = '#1f2c56',
                paper_bgcolor = '#1f2c56',
                title = {
                    'text': 'Day Trend by Total Revenue',
                    'y': 0.95,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'
                },
                titlefont = {
                    'color': 'white',
                    'size': 13
                },
                hovermode = 'closest',
                margin = dict(t = 30, l = 0, r = 0),
                
                xaxis = dict(
                    title = '<b></b>',
                            visible = True,
                            color = 'orange',
                            showline = True,
                            showgrid = False,
                            showticklabels = True,
                            linecolor = 'orange',
                            linewidth = 1,
                            ticks = 'outside',
                            tickfont = dict(
                                family = 'Arial',
                                size = 10,
                                color = 'orange'
                            )
                ),
                yaxis = dict(
                    title = '<b></b>',
                            visible = True,
                            color = 'orange',
                            showline = False,
                            showgrid = True,
                            showticklabels = False,
                            linecolor = 'orange',
                            linewidth = 1,
                            ticks = '',
                            tickfont = dict(
                                family = 'Arial',
                                size = 10,
                                color = 'orange'
                            )
                ),
                legend = {
                    'orientation': 'h',
                    'bgcolor': '#1f2c56',
                    'x': 0.5,
                    'y': 1.25,
                    'xanchor': 'center',
                    'yanchor': 'top'
                },
                font = dict(
                    family = 'sans-serif',
                    size = 10,
                    color = 'white'
                ),
            )
        }

@app.callback(Output('text3', 'children'),
    [Input('select_month', 'value')]
)
def update_text(select_month):
    sales8 = old.groupby('transaction_month')['list_price'].sum().reset_index()
    current_revenue = sales8[sales8['transaction_month'] == select_month]['list_price'].sum()

    return [
        html.H6(children = 
                'Current Revenue',
                style = {'textAlign': 'center',
                         'color': 'white'}
        ),
        
        html.P('${0:,.2f}'.format(current_revenue),
                style = {'textAlign': 'center',
                         'color': '#19AAE1',
                         'fontsize': 13,
                         'margin-top': '-10px'},
        ),     
    ]

@app.callback(Output('text4', 'children'),
    [Input('select_month', 'value')]
)
def update_text(select_month):
    sales9 = old.groupby('transaction_month')['profit'].sum().reset_index()
    current_profit = sales9[sales9['transaction_month'] == select_month]['profit'].sum()

    return [
        html.H6(children = 
                'Current Profit',
                style = {'textAlign': 'center',
                         'color': 'white'}
        ),
        
        html.P('${0:,.2f}'.format(current_profit),
                style = {'textAlign': 'center',
                         'color': '#19AAE1',
                         'fontsize': 13,
                         'margin-top': '-10px'},
        ),     
    ]

# Callback function for Radio Button and Bar Chart
@app.callback(Output('bar_chart2', 'figure'),
              [Input('select_month', 'value')],
              [Input('radio_items2', 'value')])
def update_graph(select_month, radio_items2):
    sales10 = old.groupby(['transaction_month', 'product_class'])['list_price'].sum().reset_index()
    sales11 = sales10[sales10['transaction_month'] == select_month].sort_values(by = ['list_price'], ascending = False)
    sales12 = old.groupby(['transaction_month', 'product_size'])['list_price'].sum().reset_index()
    sales13 = sales12[sales12['transaction_month'] == select_month].sort_values(by = ['list_price'], ascending = False)
    sales14 = old.groupby(['transaction_month', 'product_line'])['list_price'].sum().reset_index()
    sales15 = sales14[sales14['transaction_month'] == select_month].sort_values(by = ['list_price'], ascending = False)
    groupsales3 = old.groupby('product_class')['list_price'].sum().reset_index().sort_values(by = ['list_price'], ascending = False)
    groupsales4 = old.groupby('product_size')['list_price'].sum().reset_index().sort_values(by = ['list_price'], ascending = False)
    groupsales5 = old.groupby('product_line')['list_price'].sum().reset_index().sort_values(by = ['list_price'], ascending = False)

    if select_month:
        if radio_items2 == 'product_class':
            return{
                'data':[
                    go.Bar(
                        x = sales11['list_price'],
                        y = sales11['product_class'],
                        text = sales11['list_price'],
                        texttemplate = '$' + '%{text:.2s}',
                        textposition = 'auto',
                        orientation = 'h',
                        marker = dict(color = '#19AAE1'),

                        hoverinfo = 'text',
                        hovertext = '<b>Month</b>: ' + sales11['transaction_month'].astype(str) + '<br>' +
                                    '<b>Class</b>: ' + sales11['product_class'].astype(str) + '<br>' +
                                    '<b>Revenue</b>: $' + [f'{x:,.2f}' for x in sales11['list_price']] + '<br>'
                    )
                ],

                'layout': go.Layout(
                    plot_bgcolor = '#1f2c56',
                    paper_bgcolor = '#1f2c56',
                    title = {
                        'text': 'Revenue by Class in ' + ' ' + str((select_month)),
                        'y': 0.99,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    titlefont = {
                        'color': 'white',
                        'size': 13
                    },
                    hovermode = 'closest',
                    margin = dict(t = 40, r = 0),
                
                    xaxis = dict(
                        title = '<b></b>',
                                color = 'orange',
                                showline = True,
                                showgrid = True,
                                showticklabels = True,
                                linecolor = 'orange',
                                linewidth = 1,
                                ticks = 'outside',
                                tickfont = dict(
                                    family = 'Arial',
                                    size = 10,
                                    color = 'orange'
                                )
                    ),
                    yaxis = dict(
                        title = '<b></b>',
                                autorange = 'reversed',
                                color = 'orange',
                                showline = False,
                                showgrid = False,
                                showticklabels = True,
                                linecolor = 'orange',
                                linewidth = 1,
                                ticks = 'outside',
                                tickfont = dict(
                                    family = 'Arial',
                                    size = 10,
                                    color = 'orange'
                                )
                    ),
                    legend = {
                        'orientation': 'h',
                        'bgcolor': '#1f2c56',
                        'x': 0.5,
                        'y': 1.25,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    font = dict(
                        family = 'sans-serif',
                        size = 15,
                        color = 'white'
                    ),
                )
            }
        
        elif radio_items2 == 'product_size':
            return {
                'data':[
                    go.Bar(
                        x = sales13['list_price'],
                        y = sales13['product_size'],
                        text = sales13['list_price'],
                        texttemplate = '$' + '%{text:.2s}',
                        textposition = 'auto',
                        orientation = 'h',
                        marker = dict(color = '#19AAE1'),

                        hoverinfo = 'text',
                        hovertext = '<b>Month</b>: ' + sales13['transaction_month'].astype(str) + '<br>' +
                                    '<b>Size</b>: ' + sales13['product_size'].astype(str) + '<br>' +
                                    '<b>Revenue</b>: $' + [f'{x:,.2f}' for x in sales13['list_price']] + '<br>'
                    )
                ],

                'layout': go.Layout(
                    plot_bgcolor = '#1f2c56',
                    paper_bgcolor = '#1f2c56',
                    title = {
                        'text': 'Revenue by Size in ' + ' ' + str((select_month)),
                        'y': 0.99,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    titlefont = {
                        'color': 'white',
                        'size': 13
                    },
                    hovermode = 'closest',
                    margin = dict(t = 40, r = 0),
                    
                    xaxis = dict(
                        title = '<b></b>',
                                color = 'orange',
                                showline = True,
                                showgrid = True,
                                showticklabels = True,
                                linecolor = 'orange',
                                linewidth = 1,
                                ticks = 'outside',
                                tickfont = dict(
                                    family = 'Arial',
                                    size = 10,
                                    color = 'orange'
                                )
                    ),
                    yaxis = dict(
                        title = '<b></b>',
                                autorange = 'reversed',
                                color = 'orange',
                                showline = False,
                                showgrid = False,
                                showticklabels = True,
                                linecolor = 'orange',
                                linewidth = 1,
                                ticks = 'outside',
                                tickfont = dict(
                                    family = 'Arial',
                                    size = 10,
                                    color = 'orange'
                                )
                    ),
                    legend = {
                        'orientation': 'h',
                        'bgcolor': '#1f2c56',
                        'x': 0.5,
                        'y': 1.25,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    font = dict(
                        family = 'sans-serif',
                        size = 15,
                        color = 'white'
                    ),
                )
            }
        
        elif radio_items2 == 'product_line':
            return {
                'data':[
                    go.Bar(
                        x = sales15['list_price'],
                        y = sales15['product_line'],
                        text = sales15['list_price'],
                        texttemplate = '$' + '%{text:.2s}',
                        textposition = 'auto',
                        orientation = 'h',
                        marker = dict(color = '#19AAE1'),

                        hoverinfo = 'text',
                        hovertext = '<b>Month</b>: ' + sales15['transaction_month'].astype(str) + '<br>' +
                                    '<b>Line</b>: ' + sales15['product_line'].astype(str) + '<br>' +
                                    '<b>Revenue</b>: $' + [f'{x:,.2f}' for x in sales15['list_price']] + '<br>'
                    )
                ],

                'layout': go.Layout(
                    plot_bgcolor = '#1f2c56',
                    paper_bgcolor = '#1f2c56',
                    title = {
                        'text': 'Revenue by Line in ' + ' ' + str((select_month)),
                        'y': 0.99,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    titlefont = {
                        'color': 'white',
                        'size': 13
                    },
                    hovermode = 'closest',
                    margin = dict(t = 40, r = 0),
                    
                    xaxis = dict(
                        title = '<b></b>',
                                color = 'orange',
                                showline = True,
                                showgrid = True,
                                showticklabels = True,
                                linecolor = 'orange',
                                linewidth = 1,
                                ticks = 'outside',
                                tickfont = dict(
                                    family = 'Arial',
                                    size = 10,
                                    color = 'orange'
                                )
                    ),
                    yaxis = dict(
                        title = '<b></b>',
                                autorange = 'reversed',
                                color = 'orange',
                                showline = False,
                                showgrid = False,
                                showticklabels = True,
                                linecolor = 'orange',
                                linewidth = 1,
                                ticks = 'outside',
                                tickfont = dict(
                                    family = 'Arial',
                                    size = 10,
                                    color = 'orange'
                                )
                    ),
                    legend = {
                        'orientation': 'h',
                        'bgcolor': '#1f2c56',
                        'x': 0.5,
                        'y': 1.25,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    font = dict(
                        family = 'sans-serif',
                        size = 15,
                        color = 'white'
                    ),
                )
            }

    else:
        if radio_items2 == 'product_class':
            return{
                'data':[
                    go.Bar(
                        x = groupsales3['list_price'],
                        y = groupsales3['product_class'],
                        text = groupsales3['list_price'],
                        texttemplate = '$' + '%{text:.2s}',
                        textposition = 'auto',
                        orientation = 'h',
                        marker = dict(color = '#19AAE1'),

                        hoverinfo = 'text',
                        hovertext = '<b>Class</b>: ' + groupsales3['product_class'].astype(str) + '<br>' +
                                    '<b>Revenue</b>: $' + [f'{x:,.2f}' for x in groupsales3['list_price']] + '<br>'
                    )
                ],
                'layout': go.Layout(
                    plot_bgcolor = '#1f2c56',
                    paper_bgcolor = '#1f2c56',
                    title = {
                        'text': 'Total Revenue by Class',
                        'y': 0.99,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    titlefont = {
                        'color': 'white',
                        'size': 13
                    },
                    hovermode = 'closest',
                    margin = dict(t = 40, r = 0),
                
                    xaxis = dict(
                        title = '<b></b>',
                                color = 'orange',
                                showline = True,
                                showgrid = True,
                                showticklabels = True,
                                linecolor = 'orange',
                                linewidth = 1,
                                ticks = 'outside',
                                tickfont = dict(
                                    family = 'Arial',
                                    size = 10,
                                    color = 'orange'
                                )
                    ),
                    yaxis = dict(
                        title = '<b></b>',
                                autorange = 'reversed',
                                color = 'orange',
                                showline = False,
                                showgrid = False,
                                showticklabels = True,
                                linecolor = 'orange',
                                linewidth = 1,
                                ticks = 'outside',
                                tickfont = dict(
                                    family = 'Arial',
                                    size = 10,
                                    color = 'orange'
                                )
                    ),
                    legend = {
                        'orientation': 'h',
                        'bgcolor': '#1f2c56',
                        'x': 0.5,
                        'y': 1.25,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    font = dict(
                        family = 'sans-serif',
                        size = 15,
                        color = 'white'
                    ),
                )
            }
        elif radio_items2 == 'product_size':
            return {
                'data':[
                    go.Bar(
                        x = groupsales4['list_price'],
                        y = groupsales4['product_size'],
                        text = groupsales4['list_price'],
                        texttemplate = '$' + '%{text:.2s}',
                        textposition = 'auto',
                        orientation = 'h',
                        marker = dict(color = '#19AAE1'),

                        hoverinfo = 'text',
                        hovertext = '<b>Size</b>: ' + groupsales4['product_size'].astype(str) + '<br>' +
                                    '<b>Revenue</b>: $' + [f'{x:,.2f}' for x in groupsales4['list_price']] + '<br>'
                    )
                ],

                'layout': go.Layout(
                    plot_bgcolor = '#1f2c56',
                    paper_bgcolor = '#1f2c56',
                    title = {
                        'text': 'Total Revenue by Size',
                        'y': 0.99,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    titlefont = {
                        'color': 'white',
                        'size': 13
                    },
                    hovermode = 'closest',
                    margin = dict(t = 40, r = 0),
                    
                    xaxis = dict(
                        title = '<b></b>',
                                color = 'orange',
                                showline = True,
                                showgrid = True,
                                showticklabels = True,
                                linecolor = 'orange',
                                linewidth = 1,
                                ticks = 'outside',
                                tickfont = dict(
                                    family = 'Arial',
                                    size = 10,
                                    color = 'orange'
                                )
                    ),
                    yaxis = dict(
                        title = '<b></b>',
                                autorange = 'reversed',
                                color = 'orange',
                                showline = False,
                                showgrid = False,
                                showticklabels = True,
                                linecolor = 'orange',
                                linewidth = 1,
                                ticks = 'outside',
                                tickfont = dict(
                                    family = 'Arial',
                                    size = 10,
                                    color = 'orange'
                                )
                    ),
                    legend = {
                        'orientation': 'h',
                        'bgcolor': '#1f2c56',
                        'x': 0.5,
                        'y': 1.25,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    font = dict(
                        family = 'sans-serif',
                        size = 15,
                        color = 'white'
                    ),
                )
            }
        
        elif radio_items2 == 'product_line':
            return {
                'data':[
                    go.Bar(
                        x = groupsales5['list_price'],
                        y = groupsales5['product_line'],
                        text = groupsales5['list_price'],
                        texttemplate = '$' + '%{text:.2s}',
                        textposition = 'auto',
                        orientation = 'h',
                        marker = dict(color = '#19AAE1'),

                        hoverinfo = 'text',
                        hovertext = '<b>Line</b>: ' + groupsales5['product_line'].astype(str) + '<br>' +
                                    '<b>Revenue</b>: $' + [f'{x:,.2f}' for x in groupsales5['list_price']] + '<br>'
                    )
                ],

                'layout': go.Layout(
                    plot_bgcolor = '#1f2c56',
                    paper_bgcolor = '#1f2c56',
                    title = {
                        'text': 'Total Revenue by Line',
                        'y': 0.99,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    titlefont = {
                        'color': 'white',
                        'size': 13
                    },
                    hovermode = 'closest',
                    margin = dict(t = 40, r = 0),
                    
                    xaxis = dict(
                        title = '<b></b>',
                                color = 'orange',
                                showline = True,
                                showgrid = True,
                                showticklabels = True,
                                linecolor = 'orange',
                                linewidth = 1,
                                ticks = 'outside',
                                tickfont = dict(
                                    family = 'Arial',
                                    size = 10,
                                    color = 'orange'
                                )
                    ),
                    yaxis = dict(
                        title = '<b></b>',
                                autorange = 'reversed',
                                color = 'orange',
                                showline = False,
                                showgrid = False,
                                showticklabels = True,
                                linecolor = 'orange',
                                linewidth = 1,
                                ticks = 'outside',
                                tickfont = dict(
                                    family = 'Arial',
                                    size = 10,
                                    color = 'orange'
                                )
                    ),
                    legend = {
                        'orientation': 'h',
                        'bgcolor': '#1f2c56',
                        'x': 0.5,
                        'y': 1.25,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    font = dict(
                        family = 'sans-serif',
                        size = 15,
                        color = 'white'
                    ),
                )
            }

# Callback function for Radio Button and Bar Chart
@app.callback(Output('bar_chart3', 'figure'),
              [Input('select_month', 'value')],
              [Input('radio_items3', 'value')])
def update_graph(select_month, radio_items3):
    sales16 = old.groupby(['transaction_month', 'brand'])['list_price'].sum().reset_index()
    sales17 = sales16[sales16['transaction_month'] == select_month].sort_values(by = ['list_price'], ascending = False)
    sales18 = old.groupby(['transaction_month', 'brand'])['profit'].sum().reset_index()
    sales19 = sales18[sales18['transaction_month'] == select_month].sort_values(by = ['profit'], ascending = False)
    groupsales6 = old.groupby('brand')['list_price'].sum().reset_index().sort_values(by = ['list_price'], ascending = False)
    groupsales7 = old.groupby('brand')['profit'].sum().reset_index().sort_values(by = ['profit'], ascending = False)

    if select_month:
        if radio_items3 == 'list_price':
            return{
                'data':[
                    go.Bar(
                        x = sales17['list_price'],
                        y = sales17['brand'],
                        text = sales17['list_price'],
                        texttemplate = '$' + '%{text:.2s}',
                        textposition = 'auto',
                        orientation = 'h',
                        marker = dict(color = '#19AAE1'),

                        hoverinfo = 'text',
                        hovertext = '<b>Month</b>: ' + sales17['transaction_month'].astype(str) + '<br>' +
                                    '<b>Brand</b>: ' + sales17['brand'].astype(str) + '<br>' +
                                    '<b>Revenue</b>: $' + [f'{x:,.2f}' for x in sales17['list_price']] + '<br>'
                    )
                ],

                'layout': go.Layout(
                    plot_bgcolor = '#1f2c56',
                    paper_bgcolor = '#1f2c56',
                    title = {
                        'text': 'Revenue by Brand in ' + ' ' + str((select_month)),
                        'y': 0.99,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    titlefont = {
                        'color': 'white',
                        'size': 13
                    },
                    hovermode = 'closest',
                    margin = dict(t = 40, r = 0),
                
                    xaxis = dict(
                        title = '<b></b>',
                                color = 'orange',
                                showline = True,
                                showgrid = True,
                                showticklabels = True,
                                linecolor = 'orange',
                                linewidth = 1,
                                ticks = 'outside',
                                tickfont = dict(
                                    family = 'Arial',
                                    size = 10,
                                    color = 'orange'
                                )
                    ),
                    yaxis = dict(
                        title = '<b></b>',
                                autorange = 'reversed',
                                color = 'orange',
                                showline = False,
                                showgrid = False,
                                showticklabels = True,
                                linecolor = 'orange',
                                linewidth = 1,
                                ticks = 'outside',
                                tickfont = dict(
                                    family = 'Arial',
                                    size = 10,
                                    color = 'orange'
                                )
                    ),
                    legend = {
                        'orientation': 'h',
                        'bgcolor': '#1f2c56',
                        'x': 0.5,
                        'y': 1.25,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    font = dict(
                        family = 'sans-serif',
                        size = 15,
                        color = 'white'
                    ),
                )
            }
        
        elif radio_items3 == 'profit':
            return {
                'data':[
                    go.Bar(
                        x = sales19['profit'],
                        y = sales19['brand'],
                        text = sales19['profit'],
                        texttemplate = '$' + '%{text:.2s}',
                        textposition = 'auto',
                        orientation = 'h',
                        marker = dict(color = '#19AAE1'),

                        hoverinfo = 'text',
                        hovertext = '<b>Month</b>: ' + sales19['transaction_month'].astype(str) + '<br>' +
                                    '<b>Brand</b>: ' + sales19['brand'].astype(str) + '<br>' +
                                    '<b>Profit</b>: $' + [f'{x:,.2f}' for x in sales19['profit']] + '<br>'
                    )
                ],

                'layout': go.Layout(
                    plot_bgcolor = '#1f2c56',
                    paper_bgcolor = '#1f2c56',
                    title = {
                        'text': 'Profit by Brand in ' + ' ' + str((select_month)),
                        'y': 0.99,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    titlefont = {
                        'color': 'white',
                        'size': 13
                    },
                    hovermode = 'closest',
                    margin = dict(t = 40, r = 0),
                    
                    xaxis = dict(
                        title = '<b></b>',
                                color = 'orange',
                                showline = True,
                                showgrid = True,
                                showticklabels = True,
                                linecolor = 'orange',
                                linewidth = 1,
                                ticks = 'outside',
                                tickfont = dict(
                                    family = 'Arial',
                                    size = 10,
                                    color = 'orange'
                                )
                    ),
                    yaxis = dict(
                        title = '<b></b>',
                                autorange = 'reversed',
                                color = 'orange',
                                showline = False,
                                showgrid = False,
                                showticklabels = True,
                                linecolor = 'orange',
                                linewidth = 1,
                                ticks = 'outside',
                                tickfont = dict(
                                    family = 'Arial',
                                    size = 10,
                                    color = 'orange'
                                )
                    ),
                    legend = {
                        'orientation': 'h',
                        'bgcolor': '#1f2c56',
                        'x': 0.5,
                        'y': 1.25,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    font = dict(
                        family = 'sans-serif',
                        size = 15,
                        color = 'white'
                    ),
                )
            }
    else:
        if radio_items3 == 'list_price':
            return{
                'data':[
                    go.Bar(
                        x = groupsales6['list_price'],
                        y = groupsales6['brand'],
                        text = groupsales6['list_price'],
                        texttemplate = '$' + '%{text:.2s}',
                        textposition = 'auto',
                        orientation = 'h',
                        marker = dict(color = '#19AAE1'),

                        hoverinfo = 'text',
                        hovertext = '<b>Brand</b>: ' + groupsales6['brand'].astype(str) + '<br>' +
                                    '<b>Revenue</b>: $' + [f'{x:,.2f}' for x in groupsales6['list_price']] + '<br>'
                    )
                ],
                'layout': go.Layout(
                    plot_bgcolor = '#1f2c56',
                    paper_bgcolor = '#1f2c56',
                    title = {
                        'text': 'Total Revenue by Brand',
                        'y': 0.99,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    titlefont = {
                        'color': 'white',
                        'size': 13
                    },
                    hovermode = 'closest',
                    margin = dict(t = 40, r = 0),
                
                    xaxis = dict(
                        title = '<b></b>',
                                color = 'orange',
                                showline = True,
                                showgrid = True,
                                showticklabels = True,
                                linecolor = 'orange',
                                linewidth = 1,
                                ticks = 'outside',
                                tickfont = dict(
                                    family = 'Arial',
                                    size = 10,
                                    color = 'orange'
                                )
                    ),
                    yaxis = dict(
                        title = '<b></b>',
                                autorange = 'reversed',
                                color = 'orange',
                                showline = False,
                                showgrid = False,
                                showticklabels = True,
                                linecolor = 'orange',
                                linewidth = 1,
                                ticks = 'outside',
                                tickfont = dict(
                                    family = 'Arial',
                                    size = 10,
                                    color = 'orange'
                                )
                    ),
                    legend = {
                        'orientation': 'h',
                        'bgcolor': '#1f2c56',
                        'x': 0.5,
                        'y': 1.25,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    font = dict(
                        family = 'sans-serif',
                        size = 15,
                        color = 'white'
                    ),
                )
            }
        elif radio_items3 == 'profit':
            return {
                'data':[
                    go.Bar(
                        x = groupsales7['profit'],
                        y = groupsales7['brand'],
                        text = groupsales7['profit'],
                        texttemplate = '$' + '%{text:.2s}',
                        textposition = 'auto',
                        orientation = 'h',
                        marker = dict(color = '#19AAE1'),

                        hoverinfo = 'text',
                        hovertext = '<b>Brand</b>: ' + groupsales7['brand'].astype(str) + '<br>' +
                                    '<b>Profit</b>: $' + [f'{x:,.2f}' for x in groupsales7['profit']] + '<br>'
                    )
                ],

                'layout': go.Layout(
                    plot_bgcolor = '#1f2c56',
                    paper_bgcolor = '#1f2c56',
                    title = {
                        'text': 'Total Profit by Brand',
                        'y': 0.99,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    titlefont = {
                        'color': 'white',
                        'size': 13
                    },
                    hovermode = 'closest',
                    margin = dict(t = 40, r = 0),
                    
                    xaxis = dict(
                        title = '<b></b>',
                                color = 'orange',
                                showline = True,
                                showgrid = True,
                                showticklabels = True,
                                linecolor = 'orange',
                                linewidth = 1,
                                ticks = 'outside',
                                tickfont = dict(
                                    family = 'Arial',
                                    size = 10,
                                    color = 'orange'
                                )
                    ),
                    yaxis = dict(
                        title = '<b></b>',
                                autorange = 'reversed',
                                color = 'orange',
                                showline = False,
                                showgrid = False,
                                showticklabels = True,
                                linecolor = 'orange',
                                linewidth = 1,
                                ticks = 'outside',
                                tickfont = dict(
                                    family = 'Arial',
                                    size = 10,
                                    color = 'orange'
                                )
                    ),
                    legend = {
                        'orientation': 'h',
                        'bgcolor': '#1f2c56',
                        'x': 0.5,
                        'y': 1.25,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    font = dict(
                        family = 'sans-serif',
                        size = 15,
                        color = 'white'
                    ),
                )
            }
        
@app.callback(
    Output('bubble_chart1', 'figure'),
    [Input('select_month', 'value')]
)
def update_graph(select_month):
    sales20 = old.groupby(['transaction_month', 'owns_car', 'job_industry_category', 'age_bin'])['list_price'].sum().reset_index()
    sales21 = sales20[sales20['transaction_month'] == select_month]
    groupsales8 = old.groupby(['owns_car', 'job_industry_category', 'age_bin'])['list_price'].sum().reset_index()

    if select_month:
        return {
            'data': [go.Scatter(
                x = sales21['age_bin'],
                y = sales21['list_price'],
                mode = 'markers',
                marker = dict(
                    size = sales21['list_price'] / 2500,
                    color = sales21['list_price'],
                    colorscale = 'HSV',
                    showscale = False,
                    line = dict(
                        color = 'MediumPurple',
                        width = 2
                    )
                ),
                hoverinfo = 'text',
                hovertext = '<b>Month</b>: ' + sales21['transaction_month'].astype(str) + '<br>' +
                            '<b>Age</b>: $' + sales21['age_bin'].astype(str) + '<br>' +
                            '<b>Job Industry</b>: ' + sales21['job_industry_category'].astype(str) + '<br>' +
                            '<b>Car Owner</b>: ' + sales21['owns_car'].astype(str) + '<br>' +
                            '<b>Revenue</b>: $' + [f'{x:,.2f}' for x in sales21['list_price']] + '<br>'
            )],

            'layout': go.Layout(
                plot_bgcolor = '#1f2c56',
                paper_bgcolor = '#1f2c56',
                title = {
                    'text': 'Revenue by Car Owner, Job Industry, <br> & Age Category in' + ' ' + str((select_month)),
                    'y': 0.95,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'
                },
                titlefont = {
                    'color': 'white',
                    'size': 13
                },
                margin = dict(t = 40, r = 0, l = 0),
                hovermode = 'closest',
                xaxis = dict(
                    title = '<b></b>',
                    color = 'orange',
                    showline = False,
                    showgrid = False,
                    showticklabels = True,
                    linecolor = 'orange',
                    linewidth = 1,
                    ticks = '',
                    tickfont = dict(
                        family = 'Arial',
                        size = 10,
                        color = 'orange'
                    ),
                ),
                yaxis = dict(
                    title = '<b></b>',
                    color = 'orange',
                    visible = True,
                    showline = False,
                    showgrid = True,
                    showticklabels = False,
                    linecolor = 'orange',
                    linewidth = 1,
                    ticks = '',
                    tickfont = dict(
                        family = 'Arial',
                        size = 10,
                        color = 'orange'
                    ),
                ),
                legend = {
                    'orientation': 'h',
                    'bgcolor': '#F2F2F2',
                    'x': 0.5,
                    'y': 1.25,
                    'xanchor': 'center',
                    'yanchor': 'top'
                },
                font = dict(
                    family = 'sans-serif',
                    size = 15,
                    color = 'white'
                ),
            )
        }
    else:
        return {
            'data': [go.Scatter(
                x = groupsales8['age_bin'],
                y = groupsales8['list_price'],
                mode = 'markers',
                marker = dict(
                    size = groupsales8['list_price'] / 30000,
                    color = groupsales8['list_price'],
                    colorscale = 'HSV',
                    showscale = False,
                    line = dict(
                        color = 'MediumPurple',
                        width = 2
                    )
                ),
                hoverinfo = 'text',
                hovertext = '<b>Age</b>: $' + groupsales8['age_bin'].astype(str) + '<br>' +
                            '<b>Job Industry</b>: ' + groupsales8['job_industry_category'].astype(str) + '<br>' +
                            '<b>Car Owner</b>: ' + groupsales8['owns_car'].astype(str) + '<br>' +
                            '<b>Revenue</b>: $' + [f'{x:,.2f}' for x in groupsales8['list_price']] + '<br>'
            )],

            'layout': go.Layout(
                plot_bgcolor = '#1f2c56',
                paper_bgcolor = '#1f2c56',
                title = {
                    'text': 'Total Revenue by Car Owner, Job Industry, <br> & Age Category',
                    'y': 0.95,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'
                },
                titlefont = {
                    'color': 'white',
                    'size': 13
                },
                margin = dict(t = 40, r = 0, l = 0),
                hovermode = 'closest',
                xaxis = dict(
                    title = '<b></b>',
                    color = 'orange',
                    showline = False,
                    showgrid = False,
                    showticklabels = True,
                    linecolor = 'orange',
                    linewidth = 1,
                    ticks = '',
                    tickfont = dict(
                        family = 'Arial',
                        size = 10,
                        color = 'orange'
                    ),
                ),
                yaxis = dict(
                    title = '<b></b>',
                    color = 'orange',
                    visible = True,
                    showline = False,
                    showgrid = True,
                    showticklabels = False,
                    linecolor = 'orange',
                    linewidth = 1,
                    ticks = '',
                    tickfont = dict(
                        family = 'Arial',
                        size = 10,
                        color = 'orange'
                    ),
                ),
                legend = {
                    'orientation': 'h',
                    'bgcolor': '#F2F2F2',
                    'x': 0.5,
                    'y': 1.25,
                    'xanchor': 'center',
                    'yanchor': 'top'
                },
                font = dict(
                    family = 'sans-serif',
                    size = 15,
                    color = 'white'
                ),
            )
        }
    
    

if __name__ == '__main__':
    app.run_server(debug=True)