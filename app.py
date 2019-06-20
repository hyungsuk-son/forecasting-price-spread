import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
from matplotlib import pyplot as plt
import seaborn as sns
from datetime import datetime
from textwrap import dedent
# Plotly
import plotly.plotly as py
import plotly.tools as tls
# fig_to_uri
from io import BytesIO
import base64
# To register the converters:
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

commodities = ['broccoli', 'iceberg_lettuce', 'potatoes', 'tomatoes']

def fig_to_uri(in_fig, close_all=True, **save_args):
    # type: (plt.Figure) -> str
    """
    Save a figure as a URI
    :param in_fig:
    :return:
    """
    out_img = BytesIO()
    in_fig.savefig(out_img, format='png', **save_args)
    if close_all:
        in_fig.clf()
        plt.close('all')
    out_img.seek(0)  # rewind file
    encoded = base64.b64encode(out_img.read()).decode("ascii").replace("\n", "")
    return "data:image/png;base64,{}".format(encoded)

# Converting to Plotly's Figure object..
#plotly_fig = tls.mpl_to_plotly(fig_plot_save_produce)

# Dash app
app = dash.Dash()

server = app.server

app.layout = html.Div([
    html.H1('Forecasting agricultural product price',
    ),

    dcc.Markdown(dedent('''
    ## Show farm-gate price and retail price for selected commodity

    Please select a commodity
    ''')
    ),

    dcc.Dropdown(
    id='product-dropdown',
    options=[{'label': i, 'value': i} for i in commodities],
    multi=False,
    #value=['broccoli']
    value='broccoli'
    ),
    #dcc.Graph(id='graph-with-dropdown'),
    #html.Div([html.Img(id = 'product_plot',src='')])
    html.Div([html.Img(id = 'product_plot', style={
                    'height' : '50%',
                    'width' : '50%',
                    'float' : 'left',
                    'position' : 'relative',
                    'padding-top' : 0,
                    'padding-right' : 0
    },)])

])

@app.callback(
    dash.dependencies.Output('product_plot', 'src'),
    [dash.dependencies.Input('product-dropdown', 'value')])
def update_figure(product_name):

    #input_data = pd.read_csv('../Data/farm-to-retail-price/'+product_name[0]+'.csv')
    input_data = pd.read_csv('../Data/farm-to-retail-price/'+product_name+'.csv')

    # Date to Index
    input_data.index = input_data["Year"]
    del input_data["Year"]

    plt.rcParams['xtick.labelsize']=14
    plt.rcParams['ytick.labelsize']=14
    plt.figure(figsize=(10,5))
    plt.xticks(rotation=45)

    datelist = pd.to_datetime(input_data.index, format='%Y')
    plt.plot_date(datelist, input_data['Retail'], '-o')
    plt.plot_date(datelist, input_data['Farm'],'-o')

    #graphtitle = product_name[0]
    graphtitle = product_name

    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Price (cents/lb)', fontsize=14)
    plt.title(graphtitle)
    plt.legend(loc='best')

    #figpng = plt.savefig(product_name[0]+'.png')

    out_url = fig_to_uri(plt)

    return out_url
    #return plt.figure()
    #return str('broccoli.jpg')
    #return product_name[0]+'.png'
    #return 'data:image/png;base64,'+product_name[0]+'.png'


if __name__ == '__main__':
    app.run_server(debug=True)
