import pandas as pd
import numpy as np
import graphviz 
from sklearn import datasets, tree

def missing_values_table(df):
    mis_val = df.isnull().sum()
    mis_val_percent = 100 * df.isnull().sum() / len(df)
    mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
    mis_val_table_ren_columns = mis_val_table.rename(
        columns={0: 'Missing Values', 1: '% of Total Values'})
    mis_val_table_ren_columns = mis_val_table_ren_columns[
        mis_val_table_ren_columns.iloc[:, 1] != 0].sort_values(
        '% of Total Values', ascending=False).round(1)
    print("Your selected dataframe has " + str(df.shape[1]) + " columns.\n"
                                                              "There are " + str(mis_val_table_ren_columns.shape[0]) +
          " columns that have missing values.")
    return mis_val_table_ren_columns


def main():
    # read excel files
    print('########################## OPENING FILES #####################################\n')
    print('Opening excel files VBA_data (train model) and input_observations (input data)....')
    print('##############################################################################\n\n\n')

    vba = pd.read_excel('VBA_data.xls')  # VBA (training data)
    input = pd.read_excel('input_observations.xlsx')  # input data (observations)

    # missing data and outliers
    # displays the % of missing values in a column
    print('#################  DATA PREPROCESSING: MISSING DATA AND OUTLIERS############\n')
    print('Creating table.....')
    print(missing_values_table(vba))
    print('##############################################################################\n\n\n')

    # predictors to build our tree model
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

    print('Building tree...')
    # iterate through excel spreadsheet
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

    print('Rendering tree graph...')
    graph = graphviz.Source(dot_data)
    graph.render("vba")
    print('Tree graph can be seen in vba.pdf')

main()

