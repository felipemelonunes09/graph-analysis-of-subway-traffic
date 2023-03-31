
import sys
from datetime import datetime

from igraph import Graph, plot

from dataset import data
from logic.RelatioshipTable import RelationshipTable
from logic.StationDataset import StationDataset

DATASET_LOCATION = "./dataset/station"
DATASET_LOCATION_PROJECTION = "./dataset/projection"
DATASET_FORMAT = "json"

join_dict = StationDataset(
    format=DATASET_FORMAT, location=DATASET_LOCATION).get_dictionary() + StationDataset(
    format=DATASET_FORMAT, location=DATASET_LOCATION_PROJECTION).get_dictionary()

table = RelationshipTable(join_dict)

table = table.evaluate_matrix()

for arg in sys.argv[1:]:
    func = getattr(table, arg)
    if func != None:
        table = func()

table = table.arrow_link("Estação Consolação->Estação Paulista")

mx = table.get_matrix()

g = Graph.Adjacency(mx, mode='undirected')
g.vs["label"] = table.get_columns()

plot(g, target=f'{datetime.now().strftime("%d_%m_%Y_%S")}_graph.pdf', bbox=(
    8000, 8000))
