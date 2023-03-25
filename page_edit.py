
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.graph_objects import Layout
import math


def flatten_list(_2d_list):
    flat_list = []
    # Iterate through the outer list
    for element in _2d_list:
        if type(element) is list:
            # If the element is of type list, iterate through the sublist
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list

def find_income_label(income, income_labels, start_num):
    for label in income_labels:
        label_list = label.split(' - ')
        if float(label_list[0]) <= round(income, 2):
            if round(income, 2) <= float(label_list[1]):
                return income_labels.index(label) + start_num


def make_income_sources(df, income_labels, num_buckets, start_num):
    neighs = df['neighborhood']
    df['total population'] = df['White Alone'] + df['Black/African-American'] +  df['Hispanic'] + \
                             df['Asian alone'] +  df['Other Races']
    pops = df['total population'].tolist()
    sources = []
    targets = []
    size = []
    for i in range(len(neighs)):
        neigh = neighs[i]
        income = float(df['Per Capita Income'].tolist()[i])
        #label = find_income_label(income, income_labels, start_num, neigh)
        sources.append(find_income_label(income, income_labels, start_num))
        targets.append(i + 5)
        size.append(pops[i])
    return sources, targets, size


def make_income_labels(df, num_buckets):
    labels = []
    incomes = df['Per Capita Income'].tolist()
    incomes.sort()
    for i in range(num_buckets):
        idx = round(len(incomes)/ num_buckets) * (i + 1)
        if i >= 1:
            bottom = str(round(float(top) + 1, 2))
        else:
            bottom = '0'
        if idx <= len(incomes):
            top = str(round(incomes[idx], 2))
        else: top = 'above'
        label = bottom + ' - ' + top
        labels.append(label)
    return labels

# registering page 2 in the dashboard
#dash.register_page(__name__)

def make_sankey(link, labels, df, src, targ, year, groups=None, color_map=None, **kwargs):
    # sets parameters for sankey diagram and creates diagram
    pad = kwargs.get('pad', 50)
    thickness = kwargs.get('thickness', 30)
    line_color = kwargs.get('line_color', 'black')

    # link = {'source': df_link['source'], 'target': df_link['target'], 'value': df_link['size']}
    node = {'label': labels, 'pad': pad, 'thickness': thickness, 'line_color': line_color}

    sk = go.Sankey(link=link, node=node)

    # makes grid not visible
    layout = Layout(plot_bgcolor='rgba(0,0,0,0)')
    fig = go.Figure(sk, layout=layout)

    # labels layers
    layers = flatten_list(src + [elem for elem in targ if elem not in src])
    print(layers)
    for x_coor, layer_name in enumerate(layers):
        fig.add_annotation(
            x=x_coor,
            y=1.075,
            xref="x",
            yref="paper",
            text=layer_name.title(),
            showarrow=False,
            # font=dict(
            #     family="Tahoma",
            #     size=16,
            #     color="black"
            # ),
            align="left",
        )

    # removes x and y axes
    fig.update_xaxes(showgrid=False, color='rgba(0,0,0,0)')
    fig.update_yaxes(showgrid=False, color='rgba(0,0,0,0)')

    return fig


def main():
    # reads data into dataframe and prepares for visualization
    demographics = pd.read_excel('2015-2019_neighborhood_tables_2021.12.21.xlsm', sheet_name=11)
    race = pd.read_excel('2015-2019_neighborhood_tables_2021.12.21.xlsm', sheet_name=2)
    overall = race.merge(demographics, on='neighborhood')
    overall = overall.dropna()
    overall['white percent'] = overall['%']
    overall['black percent'] = overall['%.1']
    overall['hispanic percent'] = overall['%.2']
    overall['asian percent'] = overall['%.3']
    overall['other percent'] = overall['%.4']
    overall = overall[['White Alone', 'Black/African-American', 'Hispanic', 'Asian alone', 'Other Races',
                       'Per Capita Income', 'neighborhood']]



    races = ['White Alone', 'Black/African-American', 'Hispanic', 'Asian alone', 'Other Races']
    neighs = overall['neighborhood']
    sources = []
    targets = []
    size = []
    income_labels = make_income_labels(overall, 3)
    labels = races + list(overall['neighborhood']) + income_labels
    for i in range(len(races)):
        for j in range(len(races), len(races) + len(overall['neighborhood'])):
            sources.append(j)
            targets.append(i)
            size.append(overall[races[i]][j - len(races)])


    src, trg, sz = make_income_sources(overall, income_labels, 3, j + 1)
    sources += src
    targets += trg
    size += sz

    size = [500 * elem for elem in size]

    link = {'source': sources, 'target': targets, 'value': size}





    # sets colors for nodes
    color_map = {'Per Capita Income': (0, 100, 0), 'white percent': (200, 0, 200), 'asian percent': (200, 0, 200),
                 'black percent': (200, 0, 200), 'hispanic percent': (200, 0, 200), 'other percent': (200, 0, 200),
                 'neighborhood': (100, 50, 100)}


    # call to make sankey and show visualization
    sankey_fig = make_sankey(link, labels, overall, ['Per Capita Income (USD)', 'Neighborhood'], ['Neighborhood',
                                                                                 'Demographic (%)'],
                                2019, 10, color_map=None)
    sankey_fig.show()

if __name__ == "__main__":
    main()

