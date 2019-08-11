import pandas as pd
import numpy as np
import graphviz 
from sklearn import datasets, tree

#read excel file
vba = pd.read_excel('VBA_data.xls')

ufi = vba['UFI']
taxon_ids = vba['TAXON_ID']
scientific_display = vba['SCIENTIFIC_DISPLAY_NME']
reliability = vba['RELIABILITY']
latitude = vba["LATITUDEDD_NUM"]
longitude = vba["LONGITUDEDD_NUM"]

# unique_taxon {key:taxon_id, data: [target_id, scientific_display]}
unique_taxon = {}
data_list = []
target_list = []
current_target_id = 0    
for index in range(len(ufi)):
    try:
        target_id = unique_taxon[taxon_ids[index]][0]
    except:
        unique_taxon[taxon_ids[index]] = [current_target_id, scientific_display[index]]
        target_id = current_target_id
        current_target_id += 1

    if reliability[index] == "Acceptable":
        current_reliability = 0
    elif reliability[index] == "Confirmed":
        current_reliability = 1
    elif reliability[index] == "Unconfirmed":
        current_reliability = 2
    else:
        current_reliability = 3
        
    data_list.append([current_reliability, latitude[index], longitude[index]])
    target_list.append(target_id)


clf = tree.DecisionTreeClassifier()
clf = clf.fit(data_list, target_list)
tree.plot_tree(clf.fit(data_list, target_list)) 
dot_data = tree.export_graphviz(clf, out_file=None) 
graph = graphviz.Source(dot_data) 
graph.render("vba")