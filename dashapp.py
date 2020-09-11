import pandas as pd
import numpy as np 
import plotly.express as px  
import plotly.graph_objects as go
from datetime import datetime
# import dashappfunc

import dash  
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

data = pd.read_csv("C:\\Users\\Sampreeth Salveru\\Downloads\\AG_Discrete_DS06-Jul-2020.csv")
filter_col = [col for col in data if col.startswith(('Drug','Load'))]
col_options = [dict(label=x, value = x) for x in filter_col]

data['Date'] = pd.to_datetime(data['PSDate'])
data['Date'] = data.Date.dt.strftime('%Y-%m-%d')
data['Date'] = data.Date + "  " + data.Purif_BatchNbr
data['PSDate'] = pd.to_datetime(data['PSDate'])
data['Year'] = data['PSDate'].dt.year

excel = pd.read_csv("C:\\Users\\Sampreeth Salveru\\Downloads\\QA.csv")
excel = excel.set_index("Quality Attributes")
# WECO Rule 1
def weco1(col, ucl, lcl):
    if np.isnan(ucl) == False and np.isnan(lcl) == False:
        y = np.array(data[col].dropna())
        rule1 = np.array([])
        for i in range(0,len(y)):
            if(y[i] > ucl or y[i] < lcl):
                rule1 = np.append(rule1, i)
        rule1 = rule1.astype(np.int)
        return rule1
    elif np.isnan(ucl) == True and np.isnan(lcl) == False:
        y = np.array(data[col].dropna())
        rule1 = np.array([])
        for i in range(0,len(y)):
            if(y[i] < lcl):
                rule1 = np.append(rule1, i)
        rule1 = rule1.astype(np.int)
        return rule1
    elif np.isnan(ucl) == False and np.isnan(lcl) == True:
        y = np.array(data[col].dropna())
        rule1 = np.array([])
        for i in range(0,len(y)):
            if(y[i] > ucl):
                rule1 = np.append(rule1, i)
        rule1 = rule1.astype(np.int)
        return rule1
    else: 
        return []

# WECO Rule 4
def weco4(col, mean):
    if np.isnan(mean) == True:
        return []
    else:
        x = data[col].dropna()
        anomalies = x - mean
        signs = np.sign(anomalies)
        signs = np.array(signs)
        A = signs.cumsum()
        A[8:] -= A[:-8]
        rule4 = (np.abs(A)==8).nonzero()[0]
        return rule4

# WECO Rule 5
def weco5(col):
    x = data[col].dropna()
    nub = np.sign(np.diff(x)).astype(np.int8)
    N = 6
    C = nub.cumsum()
    C[N:] -= C[:-N]
    rule5 =(np.abs(C)==N).nonzero()[0]
    return rule5

#WECO Rule Violation Points
def make_rules(col,mean,ucl,lcl, fig):
    rule1 = weco1(col, ucl, lcl)
    rule4 = weco4(col, mean)
    rule5 = weco5(col)
    if len(rule4) > 0:
        fig.add_trace(go.Scatter(x=list(np.array(data.dropna(subset=[col], how = 'any').Date)[rule4]),
            y=list(np.array(data[col].dropna())[rule4]),
            name = f'Rule 4 Violations = {len(rule4)}',
            mode="markers",
            marker=dict(color="yellow"),
            line = dict(color="rgb(82,81,82)")
        ))
    if len(rule5) > 0:
        fig.add_trace(go.Scatter(x=list(np.array(data.dropna(subset=[col], how = 'any').Date)[rule5]),
            y=list(np.array(data[col].dropna())[rule5]),
            name = f'Rule 5 Violations = {len(rule5)}',
            mode="markers",
            marker=dict(color="cyan"),
            line = dict(color="rgb(82,81,82)")
        ))
    if len(rule1) > 0:
        fig.add_trace(go.Scatter(x=list(np.array(data.dropna(subset=[col], how = 'any').Date)[rule1]),
            y=list(np.array(data[col].dropna())[rule1]),
            name = f'Rule 1 Violations = {len(rule1)}',
            mode="markers",
            marker=dict(color="red"),
            line = dict(color="rgb(82,81,82)")
        ))

def make_lines(col, mean, ucl, lcl, usl, lsl, action, action1, fig):
    if np.isnan(mean) == False:
        (fig.add_trace(go.Scatter(
                x=list(data.dropna(subset=[col], how = 'any').Date),
                y=[mean]*len(data.dropna(subset=[col], how = 'any').Date),
                name="Mean = " + str(mean),
                hoverinfo = "skip",
                mode="lines",
                line=dict(color="black",width=1.5))))
    if np.isnan(lcl) == False:
        (fig.add_trace(go.Scatter(
                x=list(data.dropna(subset=[col], how = 'any').Date),
                y=[lcl]*len(data.dropna(subset=[col], how = 'any').Date),
                name="LCL = " + str(lcl),
                hoverinfo = "skip",
                mode="lines",
                line=dict(color="green",width=1.5))))
    if np.isnan(ucl) == False:
        (fig.add_trace(go.Scatter(
                x=list(data.dropna(subset=[col], how = 'any').Date),
                y=[ucl]*len(data.dropna(subset=[col], how = 'any').Date),
                name="UCL = " + str(ucl),
                hoverinfo = "skip",
                mode="lines",
                line=dict(color="green",width=1.5))))
    if np.isnan(lsl) == False:
        (fig.add_trace(go.Scatter(
                x=list(data.dropna(subset=[col], how = 'any').Date),
                y=[lsl]*len(data.dropna(subset=[col], how = 'any').Date),
                name="LSL = " + str(lsl),
                hoverinfo = "skip",
                mode="lines",
                line=dict(color="red",width=1.5))))
    if np.isnan(usl) == False:
        (fig.add_trace(go.Scatter(
                x=list(data.dropna(subset=[col], how = 'any').Date),
                y=[usl]*len(data.dropna(subset=[col], how = 'any').Date),
                name="USL = " + str(usl),
                mode="lines",
                hoverinfo = "skip",
                line=dict(color="red",width=1.5))))
    if np.isnan(action) == False:
        (fig.add_trace(go.Scatter(
                x=list(data.dropna(subset=[col], how = 'any').Date),
                y=[action]*len(data.dropna(subset=[col], how = 'any').Date),
                name="Action Limit = " + str(action),
                mode="lines",
                hoverinfo = "skip",
                line=dict(color="purple",width=1.5))))
    if np.isnan(action1) == False:
        (fig.add_trace(go.Scatter(
                x=list(data.dropna(subset=[col], how = 'any').Date),
                y=[action1]*len(data.dropna(subset=[col], how = 'any').Date),
                name="Action Limit = " + str(action1),
                mode="lines",
                hoverinfo = "skip",
                line=dict(color="purple",width=1.5))))


def campaigns(col):
    y = data.dropna(subset=[col], how = 'any').Year
    end = np.array([])
    for i in range(1,len(y)):
        if y.iloc[i] - y.iloc[i-1] != 0:
            end = np.append(end, i)
        end = end.astype(np.int)
    
    beg = 0
    shades = list()
    end = np.append(end, -1)
    colorlist = px.colors.qualitative.Pastel1+px.colors.qualitative.Pastel2
    for i in range(0,len(end)):
        if i % 2 == 0:
            a = dict(type="rect",
                    # x-reference is assigned to the x-values
                    xref="x",
                    # y-reference is assigned to the plot paper [0,1]
                    yref="paper",
                    x0=(data.dropna(subset=[col], how = 'any').Date).iloc[beg],
                    y0=0,
                    x1=(data.dropna(subset=[col], how = 'any').Date).iloc[end[i]],
                    y1=1,
                    fillcolor=colorlist[i],
                    opacity=0.5,
                    layer="below",
                    line_width=0,
                    )
        else:
            a = dict(type="rect",
                    # x-reference is assigned to the x-values
                    xref="x",
                    # y-reference is assigned to the plot paper [0,1]
                    yref="paper",
                    x0=(data.dropna(subset=[col], how = 'any').Date).iloc[beg],
                    y0=0,
                    x1=(data.dropna(subset=[col], how = 'any').Date).iloc[end[i]],
                    y1=1,
                    fillcolor=colorlist[i],
                    opacity=0.5,
                    layer="below",
                    line_width=0,
                    )
        shades.append(a.copy())
        beg = end[i]
    return shades


# def make_graph(col):
#     mean = excel.loc[col,"Mean"]
#     ucl = excel.loc[col,"UCL"]
#     lcl = excel.loc[col,"LCL"]
#     usl = excel.loc[col,"USL"]
#     lsl = excel.loc[col,"LSL"]
#     action = excel.loc[col,"Action"]
#     action1 = excel.loc[col,"Action1"]
#     units = excel.loc[col,"Units"]
    
#     fig.add_trace(go.Scatter(x=list(data.dropna(subset=[col], how = 'any').Date),
#                          y=list(data[col].dropna()),
#                          name = col,
#                          mode="lines+markers",
#                          line = dict(color="black")
#                          ))

#     make_rules(col, mean, ucl, lcl)
#     make_lines(col,mean, ucl, lcl, usl, lsl, action,action1)

#     fig.update_xaxes(rangeslider_visible=True)
#     fig.update_layout(showlegend=True,title_text="Kovaltry " + col+"  " + datetime.today().strftime('%Y-%m-%d'),
#                       plot_bgcolor='rgb(229,229,229)',
#                       yaxis_title=f"{col}  {units}"
#                      )
#     fig.update_layout(shapes=campaigns(col), height = 700)

# fig = go.Figure()
# make_graph(filter_col[0])


app.layout = html.Div([

    html.H1("CPV Interactive Dashboard", style={'text-align': 'left'}),
    html.Br(),
    dcc.Dropdown(id='col', options = col_options, value=filter_col[0]),

    dcc.Graph(id='graph', figure={})

])

@app.callback(Output('graph', 'figure'), [Input('col', 'value')])
def cb(col):
    mean = excel.loc[col,"Mean"]
    ucl = excel.loc[col,"UCL"]
    lcl = excel.loc[col,"LCL"]
    usl = excel.loc[col,"USL"]
    lsl = excel.loc[col,"LSL"]
    action = excel.loc[col,"Action"]
    action1 = excel.loc[col,"Action1"]
    units = excel.loc[col,"Units"]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(data.dropna(subset=[col], how = 'any').Date),
                         y=list(data[col].dropna()),
                         name = col,
                         mode="lines+markers",
                         line = dict(color="black")
                         ))
    make_rules(col, mean, ucl, lcl, fig)
    make_lines(col,mean, ucl, lcl, usl, lsl, action, action1, fig)

    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(showlegend=True,title_text="Kovaltry " + col+"  " + datetime.today().strftime('%Y-%m-%d'),
                      plot_bgcolor='rgb(229,229,229)',
                      yaxis_title=f"{col}  {units}"
                     )
    fig.update_layout(shapes=campaigns(col = col), height = 700)
    return fig





if __name__ == '__main__':
    app.run_server(debug=True)

