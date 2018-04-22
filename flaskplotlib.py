from flask import Flask, make_response
import datetime
from io import BytesIO
import random

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
import networkx as nx
app = Flask(__name__)

@app.route("/simple.png")
def simple():

    fig=Figure()
    ax=fig.add_subplot(111)
    x=[]
    y=[]
    now=datetime.datetime.now()
    delta=datetime.timedelta(days=1)
    for i in range(10):
        x.append(now)
        now+=delta
        y.append(random.randint(0, 1000))
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

@app.route('/graph')
def graph():
    G = nx.Graph()
    G.add_node(1)
    G.add_nodes_from([2, 3])
    H = nx.path_graph(10)
    G.add_nodes_from(H)
    G.add_edge(1,2)
    e = (2,3)
    G.add_edge(*e)
    dot = nx.drawing.nx_pydot.to_pydot(G)
    dot.write_png('write.png')

    # now let's try to display the png instead
    png_output = BytesIO()
    png_output = dot.create_png()
    response = make_response(png_output)
    response.headers['Content-Type'] = 'image/png'
    return response



if __name__ == "__main__":
    app.run()
