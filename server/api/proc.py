# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import random
from random import choice, sample
import numpy as np
import scipy.stats as stats
import pylab as pl
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from scipy.stats import norm
from contextlib import redirect_stdout
import io

f = io.StringIO()

def read_data(file_name):
    df = pd.read_csv(file_name)
    return df

# STEP1
def grouping(df, date_start=None, date_end=None, product=None):
    df["MCGS_Time"] = pd.to_datetime(df["MCGS_Time"], format='%d%m%Y', errors='ignore')
    if date_start is None and date_end is None:
        df_to_show = df.loc[df['Product_name'] == product].sort_values(by=['MCGS_Time'])
        print('product: {}'.format(product))
        print(df_to_show)
    elif product is None:
        if date_start is None:
            df_to_show = df.loc[df['MCGS_Time'] <= date_end].sort_values(by=['MCGS_Time'])
        elif date_end is None:
            df_to_show = df.loc[df['MCGS_Time'] >= date_start].sort_values(by=['MCGS_Time'])
            print(df_to_show)
    else:
        df_to_show = df.loc[df['Product_name'] == product].sort_values(by=['MCGS_Time'])
        print(df_to_show)

def step_1(df, start_date, end_date, product_type):
    grouping(df, start_date, end_date, product_type)

# STEP2
def step_2(df):
    # Product_type = df["Product_type"].value_counts()

    product_type = {'UNDER': 0, 'OVER': 1, 'RIGHT': 2}
    df.Product_type = [product_type[item] for item in df.Product_type]
    # print(df)

    res = df['Product_type'].value_counts(ascending=True)
    value_counts_index = res.index.to_list()
    value_counts_value = res.to_list()
    # print(value_counts_asc)

    res = df['Product_type'].value_counts(ascending=True, normalize=True)
    value_counts_norm = res.to_list()
    # print(value_counts_norm)

    value_counts = []
    product_type_labels = ['UNDER', 'OVER', 'RIGHT']
    for idx, val in enumerate(value_counts_index):
        value_counts.append({
            'product_type': product_type_labels[val],
            'count': value_counts_value[idx],
            'norm': value_counts_norm[idx],
        })
    # print(df['Product_type'].describe())

    # print(df.groupby(['Product_name']).describe())

    # print(df.loc[df['Product_type'] == 2])

    # my_list_1=df.Product_name.unique()

    res = df.groupby(['Product_name'])['Product_type'].value_counts()
    value_counts_group_by_index = res.index.to_list()
    value_counts_group_by_value = res.to_list()
    # print(value_counts_group_by)

    res = df.groupby(['Product_name'])['Product_type'].value_counts(normalize=True)
    value_counts_group_by_norm = res.to_list()
    # print(value_counts_group_by_norm)

    product_names = []
    value_counts_group = []
    for idx, val in enumerate(value_counts_group_by_index):
        if val[0] not in product_names:
            product_names.append(val[0])
            row = {
                'product_name': val[0],
                'counts': []
            }
            row['counts'].append([
                val[1],
                value_counts_group_by_value[idx],
                value_counts_group_by_norm[idx]]
            )
            value_counts_group.append(row)
        else:
            row['counts'].append([
                val[1],
                value_counts_group_by_value[idx],
                value_counts_group_by_norm[idx]]
            )

    # print(df['Product_type'].Counter(item))

    return {
        'value_counts': value_counts,
        'value_counts_group': value_counts_group,
    }

# STEP3
def step_3(df, file_path, prefix):
    df1 = df.loc[df['Product_type'] == 2]

    res = df1['Product_type'].value_counts(ascending=True)
    value_counts = res.to_list()

    res = df1.groupby(['Product_name'])['Weight_g'].describe()
    describe = {
        'columns': res.columns.values.tolist(),
        'index': res.index.values.tolist(),
        'values': res.values.tolist()
    }

    # df2=df1.groupby(['Product_name']).size()

    my_list = df1.Product_name.unique()
    image_list = []

    for item in my_list:
        h = sorted(df1.loc[df1['Product_name'] == item, 'Weight_g'])
        fit = stats.norm.pdf(h, np.mean(h), np.std(h))
        pl.plot(h, fit, '-o')

        pl.hist(h, normed=True)
        plt.title(item)
        # pl.show()
        image_name = '{}_{}.png'.format(prefix, item)
        file_name = os.path.join(file_path, image_name)
        pl.savefig(file_name)
        image_list.append(image_name)

    # df1.hist(by=df1['Product_name'])

    result = {
        'value_counts': value_counts,
        'describe': describe,
        'images': image_list
    }

    return df1, my_list, result

# STEP4
def step_4(df, df1, my_list, batch_size, nominal_weight):
    # grouped = df1.groupby('Product_name')
    # print(grouped.apply(lambda x: x.sample(n=50, replace=True)))
    checkbatches = df1.Product_name.unique()
    TNE = None

    # Rule1
    def check_if_is_accepted():
        dict = {}
        for item in my_list:
            dict[item] = (df['Weight_g'].loc[df['Product_name'] == item]).mean() > nominal_weight - (
            0.379 * (df['Weight_g'].loc[df['Product_name'] == item]).std())
        return dict


    def check_if_is_accepted0503():
        dict = {}
        for item in my_list:
            dict[item] = (df['Weight_g'].loc[df['Product_name'] == item]).mean() > nominal_weight - (
            0.503 * (df['Weight_g'].loc[df['Product_name'] == item]).std())
        return dict


    def rule_1():
        if batch_size >= 501:
            newdict = check_if_is_accepted()

            for key, value in newdict.items():
                if value == False:
                    print("This product is not acceptable according to the 1st rule: ")
                    print(str(key), ' ', str(value))
                else:
                    print("1st Rule: Pass: ")
                    print(str(key), ' ', str(value))

        elif batch_size <= 500:
            newdict1 = check_if_is_accepted0503()

            for key, value in newdict1.items():
                if value == False:
                    print("This product is not acceptable according to the 1st rule: ")
                    print(str(key), ' ', str(value))
                else:
                    print("1st Rule: Pass: ")
                    print(str(key), ' ', str(value))

    # Rule2
    def rule_2():
        for data in my_list:
            h = sorted(df1.loc[df1['Product_name'] == data, 'Weight_g'])
            sample = random.sample(h, k=50)
            print("Sample of ", data)
            print(sample)
            if nominal_weight in range(5, 51):
                TNE = nominal_weight * 9 / 100
            elif nominal_weight in range(51, 101):
                TNE = 4.5
            elif nominal_weight in range(101, 201):
                TNE = nominal_weight * 4.5 / 100
            elif nominal_weight in range(201, 301):
                TNE = 9
            elif nominal_weight in range(301, 501):
                TNE = nominal_weight * 3 / 100
            elif nominal_weight in range(501, 1001):
                TNE = 15
            elif nominal_weight in range(1001, 10001):
                TNE = nominal_weight * 1.5 / 100
            elif nominal_weight in range(10001, 15001):
                TNE = 150
            elif nominal_weight > 15000:
                TNE = nominal_weight / 100
            TU1 = nominal_weight - TNE
            non_acceptable_count = sum(i < TU1 for i in sample)
            if non_acceptable_count / 50 * 100 > 2.5:
                print(data, " can not be acceptable. Defective units == ", non_acceptable_count)
            if batch_size in range(100, 501):
                if non_acceptable_count <= 1:
                    print("2nd Rule: The batch is acceptable")
                elif non_acceptable_count >= 3:
                    print("2nd Rule: The batch is not acceptable")
                elif non_acceptable_count == 2:
                    temp = non_acceptable_count
                    h = sorted(df1.loc[df1['Product_name'] == data, 'Weight_g'])
                    sample = random.sample(h, k=50)
                    print("Sample of batch size (100-500): ", data)
                    print(sample)
                    if nominal_weight in range(5, 51):
                        TNE = nominal_weight * 9 / 100
                    elif nominal_weight in range(51, 101):
                        TNE = 4.5
                    elif nominal_weight in range(101, 201):
                        TNE = nominal_weight * 4.5 / 100
                    elif nominal_weight in range(201, 301):
                        TNE = 9
                    elif nominal_weight in range(301, 501):
                        TNE = nominal_weight * 3 / 100
                    elif nominal_weight in range(501, 1001):
                        TNE = 15
                    elif nominal_weight in range(1001, 10001):
                        TNE = nominal_weight * 1.5 / 100
                    elif nominal_weight in range(10001, 15001):
                        TNE = 150
                    elif nominal_weight > 15000:
                        TNE = nominal_weight / 100
                    TU1 = nominal_weight - TNE
                    non_acceptable_count = sum(i < TU1 for i in sample)
                    temp1 = temp + non_acceptable_count
                    if temp1 <= 4:
                        print("Pass: total defective units: ", temp1)
                        print(data, " Batch is acceptable. == ", non_acceptable_count)
                    elif temp1 >= 5:
                        print("Rejected: total defective units: ", temp1)
                        print(data, "Batch can not be acceptable2. == ", non_acceptable_count)

            if batch_size in range(501, 3201):
                if non_acceptable_count <= 2:
                    print("2nd Rule: The batch is acceptable")
                elif non_acceptable_count >= 5:
                    print("2nd Rule: The batch is not acceptable")
                elif non_acceptable_count in range(3, 5):
                    temp2 = non_acceptable_count
                    h = sorted(df1.loc[df1['Product_name'] == data, 'Weight_g'])
                    sample = random.sample(h, k=50)
                    print("Sample of batch size (501-3200): ", data)
                    print(sample)
                    if nominal_weight in range(5, 51):
                        TNE = nominal_weight * 9 / 100
                    elif nominal_weight in range(51, 101):
                        TNE = 4.5
                    elif nominal_weight in range(101, 201):
                        TNE = nominal_weight * 4.5 / 100
                    elif nominal_weight in range(201, 301):
                        TNE = 9
                    elif nominal_weight in range(301, 501):
                        TNE = nominal_weight * 3 / 100
                    elif nominal_weight in range(501, 1001):
                        TNE = 15
                    elif nominal_weight in range(1001, 10001):
                        TNE = nominal_weight * 1.5 / 100
                    elif nominal_weight in range(10001, 15001):
                        TNE = 150
                    elif nominal_weight > 15000:
                        TNE = nominal_weight / 100
                    TU1 = nominal_weight - TNE
                    non_acceptable_count = sum(i < TU1 for i in sample)
                    temp3 = temp2 + non_acceptable_count
                    if temp1 <= 6:
                        print("Pass: total defective units: ", temp3)
                        print(data, "Batch is acceptable. == ", non_acceptable_count)
                    elif temp3 >= 7:
                        print("Rejected: total defective units: ", temp3)
                        print(data, "Batch can not be acceptable. == ", non_acceptable_count)

            if batch_size > 3201:
                if non_acceptable_count <= 3:
                    print("2nd Rule: The batch is acceptable")
                elif non_acceptable_count >= 7:
                    print("2nd Rule: The batch is not acceptable")
                elif non_acceptable_count in range(4, 7):
                    temp4 = non_acceptable_count
                    h = sorted(df1.loc[df1['Product_name'] == data, 'Weight_g'])
                    sample = random.sample(h, k=50)
                    print("Sample of batch size (>3200): ", data)
                    print(sample)
                    if nominal_weight in range(5, 51):
                        TNE = nominal_weight * 9 / 100
                    elif nominal_weight in range(51, 101):
                        TNE = 4.5
                    elif nominal_weight in range(101, 201):
                        TNE = nominal_weight * 4.5 / 100
                    elif nominal_weight in range(201, 301):
                        TNE = 9
                    elif nominal_weight in range(301, 501):
                        TNE = nominal_weight * 3 / 100
                    elif nominal_weight in range(501, 1001):
                        TNE = 15
                    elif nominal_weight in range(1001, 10001):
                        TNE = nominal_weight * 1.5 / 100
                    elif nominal_weight in range(10001, 15001):
                        TNE = 150
                    elif nominal_weight > 15000:
                        TNE = nominal_weight / 100
                    TU1 = nominal_weight - TNE
                    non_acceptable_count = sum(i < TU1 for i in sample)
                    temp5 = temp4 + non_acceptable_count
                    if temp5 <= 8:
                        print("Pass: total defective units: ", temp5)
                        print(data, "Batch is acceptable. == ", non_acceptable_count)
                    elif temp5 >= 9:
                        print("Rejected: total defective units: ", temp5)
                        print(data, "Batch can not be acceptable. == ", non_acceptable_count)

            if batch_size < 40:
                if non_acceptable_count <= 0:
                    print("2nd Rule: The batch is acceptable")
                elif non_acceptable_count >= 1:
                    print("2nd Rule: The batch is not acceptable")

                if nominal_weight in range(5, 51):
                    TNE = nominal_weight * 9 / 100
                elif nominal_weight in range(51, 101):
                    TNE = 4.5
                elif nominal_weight in range(101, 201):
                    TNE = nominal_weight * 4.5 / 100
                elif nominal_weight in range(201, 301):
                    TNE = 9
                elif nominal_weight in range(301, 501):
                    TNE = nominal_weight * 3 / 100
                elif nominal_weight in range(501, 1001):
                    TNE = 15
                elif nominal_weight in range(1001, 10001):
                    TNE = nominal_weight * 1.5 / 100
                elif nominal_weight in range(10001, 15001):
                    TNE = 150
                elif nominal_weight > 15000:
                    TNE = nominal_weight / 100
                TU1 = nominal_weight - TNE
                non_acceptable_count = sum(i < TU1 for i in sample)
                # if non_acceptable_count / 50 * 100 > 2.5:
                # print(data, " can not be acceptable. Defective units == ", non_acceptable_count)
                # if non_acceptable_count < nominal_weight -2 * TNE:
                #     print("Stop: ΔΙΟΡΘΩΤΙΚΗ ΕΝΕΡΓΕΙΑ")

                # else:
                #     print("3rd Rule: Pass")

            if batch_size in range(40, 80):
                if non_acceptable_count <= 1:
                    print("2nd Rule: The batch is acceptable")
                elif non_acceptable_count >= 2:
                    print("2nd Rule: The batch is not acceptable")

                if nominal_weight in range(5, 51):
                    TNE = nominal_weight * 9 / 100
                elif nominal_weight in range(51, 101):
                    TNE = 4.5
                elif nominal_weight in range(101, 201):
                    TNE = nominal_weight * 4.5 / 100
                elif nominal_weight in range(201, 301):
                    TNE = 9
                elif nominal_weight in range(301, 501):
                    TNE = nominal_weight * 3 / 100
                elif nominal_weight in range(501, 1001):
                    TNE = 15
                elif nominal_weight in range(1001, 10001):
                    TNE = nominal_weight * 1.5 / 100
                elif nominal_weight in range(10001, 15001):
                    TNE = 150
                elif nominal_weight > 15000:
                    TNE = nominal_weight / 100
                TU1 = nominal_weight - TNE
                non_acceptable_count = sum(i < TU1 for i in sample)
                # if non_acceptable_count / 50 * 100 > 2.5:
                # print(data, " can not be acceptable. Defective units == ", non_acceptable_count)
                # if non_acceptable_count < nominal_weight -2 * TNE:
                #     print("Stop: ΔΙΟΡΘΩΤΙΚΗ ΕΝΕΡΓΕΙΑ")

                # else:
                #     print("3rd Rule: Pass")

            if batch_size in range(80, 100):
                if non_acceptable_count <= 2:
                    print("2nd Rule: The batch is acceptable")
                elif non_acceptable_count >= 3:
                    print("2nd Rule: The batch is not acceptable")

                if nominal_weight in range(5, 51):
                    TNE = nominal_weight * 9 / 100
                elif nominal_weight in range(51, 101):
                    TNE = 4.5
                elif nominal_weight in range(101, 201):
                    TNE = nominal_weight * 4.5 / 100
                elif nominal_weight in range(201, 301):
                    TNE = 9
                elif nominal_weight in range(301, 501):
                    TNE = nominal_weight * 3 / 100
                elif nominal_weight in range(501, 1001):
                    TNE = 15
                elif nominal_weight in range(1001, 10001):
                    TNE = nominal_weight * 1.5 / 100
                elif nominal_weight in range(10001, 15001):
                    TNE = 150
                elif nominal_weight > 15000:
                    TNE = nominal_weight / 100
                TU1 = nominal_weight - TNE
                non_acceptable_count = sum(i < TU1 for i in sample)
                # if non_acceptable_count / 50 * 100 > 2.5:
                # print(data, " can not be acceptable. Defective units == ", non_acceptable_count)
                # if non_acceptable_count < nominal_weight -2 * TNE:
                #     print("Stop: ΔΙΟΡΘΩΤΙΚΗ ΕΝΕΡΓΕΙΑ")

                # else:
                # print("3rd Rule: Pass")

    def rule_3():
        # Rule3
        for da in sample:
            if batch_size in range(100, 3201):
                if da < nominal_weight - 2 * TNE:
                    print("Stop: ΔΙΟΡΘΩΤΙΚΗ ΕΝΕΡΓΕΙΑ")
                    break
                elif batch_size in range(100, 3201):
                    print("3rd Rule: Pass")
                    break
            if batch_size in range(1, 100):
                if da < nominal_weight - 2 * TNE:
                    print("Stop: ΔΙΟΡΘΩΤΙΚΗ ΕΝΕΡΓΕΙΑ")
                    break
                elif batch_size in range(1, 100):
                    print("3rd Rule: Pass")
                    break

    rule_1()
    rule_2()
    rule_3()

    # Cross-check-2nd Rule


def test_data(file_path, file_name, options, prefix):
    result = {
        'output': [],
        'images': [],
        'errors': [],
    }
    try:
        with redirect_stdout(f):
            start_date = options['start_date']
            end_date = options['end_date']
            product_type = options['product_type']
            # batch_size = options['product_type']
            # nominal_weight = options['nominal_weight']

            df = read_data(file_name)

            step_1(df, start_date, end_date, product_type)

            result['step_2'] = step_2(df)

            df1, my_list, result_step_3 = step_3(df, file_path, prefix)

            result['step_3'] = result_step_3

            # step_4(df, df1, my_list, batch_size, nominal_weight)

        # print(f.getvalue())

        # result['output'] = f.getvalue().splitlines()


    except Exception as e:
        result['errors'] = ['{}'.format(e)]

    return result


if __name__ == '__main__':
    batch_size = int(input("Please enter the batch size: "))
    nominal_weight = int(input("Please enter the nominal weight: "))

    options = {
        'start_date': '2019-04-15',
        'end_date': None,
        'product_type': None,
        'batch_size': batch_size,
        'nominal_weight': nominal_weight
    }
    prefix = '2019_05_21_06_18_11_951_20190415'
    result = test_data(
        file_path=r'D:\c\f\dmitro\upload',
        file_name=r'D:\c\f\dmitro\upload\2019_05_21_06_18_11_951_20190415-20190430.csv',
        options=options,
        prefix=prefix
    )

    print(result)
