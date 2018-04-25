import numpy as np
import pandas as pd
from numpy import genfromtxt

my_data = pd.read_csv("D:\\THOR_3WK_Male_Dec13\\THOR_output_H3K4me1_3wk_M\\CoverageMatrix_10KB_H3K4me1_3wk_M.csv",index_col=0)
##promoter
my_data = my_data.rename(columns = {'Unnamed: 0':'NAME'})
my_data1 = my_data[~(my_data==0).all(axis=1)]
my_data1 = pd.DataFrame(my_data1)
print(my_data1)
my_data1.to_csv("D:\\THOR_3WK_Male_Dec13\\THOR_output_H3K4me1_3wk_M\\CoverageMatrix_10KB_H3K4me1_3wk_M_wo_zero.csv")

def quantileNormalize(df_input):
    df = df_input.copy()
    #compute rank
    dic = {}
    for col in df:
        dic.update({col : sorted(df[col])})
    sorted_df = pd.DataFrame(dic)
    rank = sorted_df.mean(axis = 1).tolist()
    #sort
    for col in df:
        t = np.searchsorted(np.sort(df[col]), df[col])
        df[col] = [rank[i] for i in t]
    return df
data_norm = quantileNormalize(my_data1)
data_norm.to_csv("D:\\THOR_3WK_Male_Dec13\\THOR_output_H3K4me1_3wk_M\\norm_CoverageMatrix_10KB_H3K4me1_3wk_M.csv")

from scipy import stats
def zscore(data):
    df = data.copy()
    df_array = np.array(df)
    data_zscore = stats.zscore(df_array)
    dataframe_zscore = pd.DataFrame(data_zscore,columns=my_data.columns,index = my_data.index)
    return dataframe_zscore
data_zscore = zscore(my_data)
data_zscore.to_csv("D:\\Dr_Katz_Jan30_2018\\DiffReps_CHIP-seq\\Vehicle\\Data\\Heatmap\\GT_H3K27Ac_3wk_M_vs_F_veh_FC_1.5_FDR_0.25.csv_Treat_Control_with_label1_zscore.csv")
