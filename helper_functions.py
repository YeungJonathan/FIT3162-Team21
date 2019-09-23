import pandas as pd
import matplotlib.pyplot as plt

def concat_files():
    # filenames
    # vba = pd.read_excel('VBA_Raster.xlsx')
    #
    # vba = vba.loc[vba['COMMON_NME'] == "Agile Antechinus"]
    excel_names = ["agile.xlsx", "./absence_datas/agile_antechinus.xlsx"]

    # read them in
    excels = [pd.ExcelFile(name) for name in excel_names]

    # turn them into dataframes
    frames = [x.parse(x.sheet_names[0], header=None, index_col=None) for x in excels]

    # delete the first row for all frames except the first
    # i.e. remove the header row -- assumes it's the first
    frames[1:] = [df[1:] for df in frames[1:]]

    # concatenate them..
    combined = pd.concat(frames)

    # write it out
    combined.to_excel("combined_agile_antechinus.xlsx", header=False, index=False)


def print_graph():
    # read excel files
    vba = pd.read_excel('VBA_data.xls') # VBA (training data)
    input = pd.read_excel('input_observations.xlsx') # input data (observations)

    species_names = vba['COMMON_NME'].unique()

    print(species_names)
    arr = ['Small Triggerplant', 'Common Beard-heath','Brown Treecreeper', 'Southern Brown Tree Frog', 'Agile Antechinus', 'White-browed Treecreeper']
    vba.COMMON_NME.replace(['Small Triggerplant', 'Common Beard-heath','Brown Treecreeper', 'Southern Brown Tree Frog', 'Agile Antechinus', 'White-browed Treecreeper'],
                           [0, 1, 2, 3, 4, 5], inplace=True)

    df = vba[['COMMON_NME','LONGITUDEDD_NUM', 'LATITUDEDD_NUM']]
    small_tiggerplant = df[df['COMMON_NME'] == 0]
    common_beardheath = df[df['COMMON_NME'] == 1]
    brown_treecreeper = df[df['COMMON_NME'] == 2]
    southern_browntree = df[df['COMMON_NME'] == 3]
    agile = df[df['COMMON_NME'] == 4]
    white = df[df['COMMON_NME'] == 5]

    print(df.head())

    show_on_map = [small_tiggerplant, common_beardheath, brown_treecreeper, southern_browntree, agile, white]

    for i in range(len(show_on_map)):
        show_on_map[i].plot(kind="scatter", x="LONGITUDEDD_NUM", y="LATITUDEDD_NUM", alpha=0.4)

    #vba.plot(kind="scatter", x="LONGITUDEDD_NUM", y="LATITUDEDD_NUM", alpha=0.4)

    plt.show()

    print(missing_values_table(vba))


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