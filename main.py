import dash
import sys
import pdb
import json
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

def all_logs():
    return filter_logs_by_event(None)

def filter_logs_by_event(event_names=None):
    if event_names is None:
        event_names = []

    skip_first_line = True
    events = []
    with open('log_2024-06-06.txt') as f:
        data = f.readlines()
        data = data[9:]
        for line in data:
            # Skip the first line
            if skip_first_line:
                skip_first_line = False
                continue
            # The SeeStar logs use single quotes instead of double quotes
            # JSON requires double-quotes
            valid_json = line.replace('\'', '"')
            data = None
            try:
                data = json.loads(valid_json)
            except:
                continue
            if data.get('Event') is None:
                continue
            if data.get('Event') != 'Stack':
                continue
            fields = ['Timestamp', 'stacked_frame', 'dropped_frame']
            event = {
                field.lower(): int(float(data.get(field)))
                for field in fields
            }
            events.append(event)
        return events

def graph_stuff(events):
    app = Dash(__name__)

    # assume you have a "long-form" data frame
    # see https://plotly.com/python/px-arguments/ for more options
    # pdb.set_trace()
    # df = pd.DataFrame({
    #     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    #     "Amount": [4, 1, 2, 2, 4, 5],
    #     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
    # })

    # fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
    events = all_logs()
    df = pd.DataFrame.from_dict(events)

    fig = px.line(df, x='timestamp', y=['stacked_frame', 'dropped_frame'])

    app.layout = html.Div(children=[
        html.H1(children='Hello Dash'),

        html.Div(children='''
            Dash: A web application framework for your data.
        '''),

        dcc.Graph(
            id='example-graph',
            figure=fig
        )
    ])
    app.run(debug=True)

def main():
    events = all_logs()
    # pdb.set_trace()
    graph_stuff(events)


if __name__ == '__main__':
    main()
