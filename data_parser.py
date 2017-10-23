import pandas as pd
import math
import itertools
from bokeh.palettes import Dark2_5 as palette

def parse_excel_data(directory, sheet_name):
    ds = pd.ExcelFile(directory)
    ds_df = ds.parse(sheet_name)
    return ds_df

def parse_csv_data(directory, encoding):
    df = pd.read_csv(directory, encoding = encoding)
    return df

# def parse_arff_data(directory):
#     dataset = arff.load(open(directory, 'rb'))
#     data = np.array(dataset['data'])
#     df = pd.DataFrame(data)
   # return df

def extract_column_names(df):
	return list(df)

def extract_row_names(df):
	return list(df.index)

def extract_row_by_index(df, i):
    return list(df.iloc[i, :])

def extract_data_missing_rows(df):
    null_df = pd.isnull(df)
    missing_data_rows = []
    for index, row in null_df.iterrows():
        col_indices = [i for i, x in enumerate(list(row)) if x == True]
        if len(col_indices) > 0:
            missing_data_row = {'row': index, 'col': col_indices}
            missing_data_rows.append(missing_data_row)
    return missing_data_rows
    #return pd.isnull(df)

def drop_rows_from_df(df, rows):
    return df.drop(rows)

def build_dic(df, names):
    dic_object = {}
    for name in names:
        dic_object[name] = list(df.loc[:, name])
    return dic_object

def build_row_dic_list(df, names):
    rows_dic_list = []
    for index, row in df.iterrows():
        row_dic = {}
        for e, name in zip(list(row), names):
            row_dic[name] = e
        rows_dic_list.append(row_dic)
    return rows_dic_list

def convert_dic_list_to_dic(dic_list, key):
    return_dic = {}
    for e in dic_list:
        return_dic[e[key]] = e
    return return_dic

def convert_dic_list_to_list_dic(dic_list, key):
    return_dic = {}
    for e in dic_list:
        if e[key] in return_dic:
            return_dic[e[key]].append(e)
        else:
            return_dic[e[key]] = [e]
    return return_dic

#parameters: dataframe, countries list, years list, and dataset's name
def convert_df2json(df, countries, years, ds_name):
	data_json_list = []
	colors = itertools.cycle(palette)
	i = 0
	for country, color in zip(countries, colors):
	    # add the extracted json objects into data_json_list
	    data_json_list.append(extract_data(i, country, color, df, years, ds_name))
	    i += 1
	return data_json_list

# remove the datasets without values, and return the result in json format.
def extract_data(country_indice, country, color, df, years, ds_name):
    tmp_years = []
    tmp_value = []
    # extract all years without data.
    # extract all not nan ages.
    i = 0
    for x in list(df.iloc[country_indice, :]):
        if math.isnan(x) != True:
            tmp_years.append(years[i])
            tmp_value.append(x)
        i += 1
    tmp_json = {"country": country, "years": tmp_years, ds_name: tmp_value, "color": color}
    return tmp_json

def extract_column_by_indice(df, indice):
	return list(df.iloc[:, indice])