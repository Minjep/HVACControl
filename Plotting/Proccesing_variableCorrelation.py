import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn import preprocessing
import numpy as np

from AirmasterDataLib.process.filter_data import  loadPklFile

def variable_correlation(data,columns_to_be_compared):
    columns_to_be_included =['rqf','rqt','t_ar','t_ao','rh_ar','rh_ao','co2_ar','co2_ao']
    data = data[columns_to_be_included]
    num_columns = len(columns_to_be_compared)
    num_keys = len(data.keys())
    matrix = [[0 for _ in range(num_keys)] for _ in range(num_columns)]
    delays = [0,15*60,30*60,45*60,60*60]
    
    array_of_dataframe = []
    
    for delay_index in range(len(delays)):
        matrix = [[0 for _ in range(num_keys)] for _ in range(num_columns)]
        for column_index in range(num_columns):
            for key_index in range(num_keys):
                if delay_index == 0:
                    extracted_data_1 = data[columns_to_be_compared[column_index]]
                    extracted_data_2 = data[data.keys()[key_index]]
                    extracted_data_1 = extracted_data_1.reset_index(drop=True)
                    extracted_data_2 = extracted_data_2.reset_index(drop=True)
                else:
                    extracted_data_1 = data[columns_to_be_compared[column_index]][delays[delay_index]:]
                    extracted_data_2 = data[data.keys()[key_index]][:-delays[delay_index]]
                    extracted_data_1 = extracted_data_1.reset_index(drop=True)
                    extracted_data_2 = extracted_data_2.reset_index(drop=True)
                value = extracted_data_1.corr(extracted_data_2)
                matrix[column_index][key_index] = value
        array_of_dataframe.append(pd.DataFrame(matrix, columns=data.keys(), index=columns_to_be_compared))
    
    matrix_to_plot = pd.concat(array_of_dataframe, axis=0)
         
    x_axis_labels = list(data.keys())
    y_axis_labels = ['t_ar_0min', 'co2_ar_0min','t_ar_15min', 'co2_ar_15min','t_ar_30min', 'co2_ar_30min','t_ar_45min', 'co2_ar_45min','t_ar_60min', 'co2_ar_60min']  
    plt.figure(figsize=(8, 6))
    sns.heatmap(matrix_to_plot, cmap='viridis', annot=True, fmt=".2f", cbar=True,xticklabels=x_axis_labels, yticklabels=y_axis_labels)
    plt.xlabel('Key Index')
    plt.ylabel('Column Index')
    plt.title('Heatmap of Matrix with delay ')
    plt.tight_layout()
    plt.show()

   
    
def vif(data, string='', pressure=''):
    vif_data = pd.DataFrame()
    
    
    columns_to_be_included =['t_ar','t_ao','co2_ar','co2_ao','rh_ar','rh_ao']
    X = data[columns_to_be_included]
    vif_data["feature"] = X.columns
    
    vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))]

    

    # Make a bar plot of the data
    feature = vif_data['feature']
    vif = vif_data['VIF']

    # Figure Size
    fig, ax = plt.subplots(figsize=(16, 9))
    ax_left = 0.185
    ax_bottom = 0.11
    ax_width = 0.9-ax_left
    ax_height = 0.88-ax_bottom
    ax.set_position([ax_left, ax_bottom, ax_width, ax_height])

    # Horizontal Bar Plot
    ax.barh(feature, vif, color='g')

    # Remove axes splines
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)

    # Remove x, y Ticks
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    ax.set_xlabel('VIF', fontsize=18)
    ax.set_ylabel('', fontsize=18)
    plt.yticks(fontsize=20)
    plt.xticks(fontsize=20)

    # Add padding between axes and labels
    ax.xaxis.set_tick_params(pad=5)
    ax.yaxis.set_tick_params(pad=10)

    # Add x, y gridlines
    ax.grid(color='grey',
            linestyle='-.', linewidth=0.5,
            alpha=0.2)

    # Show top values
    ax.invert_yaxis()

    # Add annotation to bars
    for i in ax.patches:
        plt.text(i.get_width() + 0.2, i.get_y() + 0.5,
                 str(round((i.get_width()), 2)),
                 fontsize=24, fontweight='bold',
                 color='grey')

    # Add Plot Title
    ax.set_title(string.upper() + ' features and their corresponding VIF',
                 loc='left', fontsize=24)

    if not pressure:
        plt.savefig(string + "_vif_no_pressure.png")
    else:
        plt.savefig(string + "_vif_with_pressure.png")

    # Show Plot
    plt.show()
    
def main():
    dataFinal = loadPklFile("finalData.pkl")
    vif(dataFinal)
    columns_to_be_compared = ['t_ar','co2_ar']
    variable_correlation(dataFinal,columns_to_be_compared)       

if __name__ == "__main__":
    
    main()