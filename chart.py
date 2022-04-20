# -*- coding: utf-8 -*-
from base64 import standard_b64decode
from fileinput import filename
from tkinter.ttk import Style
import xlwt
import time
import pandas as pd
import numpy as np
import codecs
import csv
import os
from xlwt import *
 


# 对于当前目录中的UCR数据集进行统计并制表
# 统计标准LSTM-FCN在UCR2018上的表现，数据集保存为./std_output.csv，由std_benchmark.ipynb可得。
# 统计优化后的LSTM-FCN模型在各个数据集上的表现，保存格式为./xxx_raw_data.csv, 以Adiac数据集为例，保存为./Adiac_raw_data.csv，由NAS4TSC可得。
# 输出文件为DatasetChart.xls，包含优化前后的数据对比图。

all_dataset = ['ACSF1', 'Adiac', 'AllGestureWiimoteX', 'AllGestureWiimoteY', 'AllGestureWiimoteZ', 
               'ArrowHead', 'Beef', 'BeetleFly', 'BirdChicken', 'BME', 'Car', 'CBF', 'Chinatown', 
               'ChlorineConcentration', 'CinCECGTorso', 'Coffee', 'Computers', 'CricketX', 'CricketY', 
               'CricketZ', 'Crop', 'DiatomSizeReduction', 'DistalPhalanxOutlineAgeGroup', 
               'DistalPhalanxOutlineCorrect', 'DistalPhalanxTW', 'DodgerLoopDay', 'DodgerLoopGame', 
               'DodgerLoopWeekend', 'Earthquakes', 'ECG200', 'ECG5000', 'ECGFiveDays', 'ElectricDevices', 
               'EOGHorizontalSignal', 'EOGVerticalSignal', 'EthanolLevel', 'FaceAll', 'FaceFour', 'FacesUCR', 
               'FiftyWords', 'Fish', 'FordA', 'FordB', 'FreezerRegularTrain', 'FreezerSmallTrain', 'Fungi', 
               'GestureMidAirD1', 'GestureMidAirD2', 'GestureMidAirD3', 'GesturePebbleZ1', 'GesturePebbleZ2', 
               'GunPoint', 'GunPointAgeSpan', 'GunPointMaleVersusFemale', 'GunPointOldVersusYoung', 'Ham', 
               'HandOutlines', 'Haptics', 'Herring', 'HouseTwenty', 'InlineSkate', 'InsectEPGRegularTrain', 
               'InsectEPGSmallTrain', 'InsectWingbeatSound', 'ItalyPowerDemand', 'LargeKitchenAppliances', 
               'Lightning2', 'Lightning7', 'Mallat', 'Meat', 'MedicalImages', 'MelbournePedestrian', 
               'MiddlePhalanxOutlineAgeGroup', 'MiddlePhalanxOutlineCorrect', 'MiddlePhalanxTW', 
               'MixedShapesRegularTrain', 'MixedShapesSmallTrain', 'MoteStrain', 'NonInvasiveFetalECGThorax1', 
               'NonInvasiveFetalECGThorax2', 'OliveOil', 'OSULeaf', 'PhalangesOutlinesCorrect', 'Phoneme', 
               'PickupGestureWiimoteZ', 'PigAirwayPressure', 'PigArtPressure', 'PigCVP', 'PLAID', 'Plane', 
               'PowerCons', 'ProximalPhalanxOutlineAgeGroup', 'ProximalPhalanxOutlineCorrect', 'ProximalPhalanxTW', 
               'RefrigerationDevices', 'Rock', 'ScreenType', 'SemgHandGenderCh2', 'SemgHandMovementCh2', 
               'SemgHandSubjectCh2', 'ShakeGestureWiimoteZ', 'ShapeletSim', 'ShapesAll', 'SmallKitchenAppliances', 
               'SmoothSubspace', 'SonyAIBORobotSurface1', 'SonyAIBORobotSurface2', 'StarLightCurves', 'Strawberry', 
               'SwedishLeaf', 'Symbols', 'SyntheticControl', 'ToeSegmentation1', 'ToeSegmentation2', 'Trace', 
               'TwoLeadECG', 'TwoPatterns', 'UMD', 'UWaveGestureLibraryAll', 'UWaveGestureLibraryX', 
               'UWaveGestureLibraryY', 'UWaveGestureLibraryZ', 'Wafer', 'Wine', 'WordSynonyms', 'Worms', 
               'WormsTwoClass', 'Yoga']


print("ALL_DATASET_LEN", len(all_dataset))


available_dataset = [
            'ACSF1', 'Adiac', 'ArrowHead', 'Beef', 'BeetleFly', 'BirdChicken', 'BME', 'Car', 'CBF', 'Chinatown', 'ChlorineConcentration', 
            'CinCECGTorso', 'Coffee', 'Computers', 'CricketX', 'CricketY', 'CricketZ', 'DiatomSizeReduction', 'DistalPhalanxOutlineAgeGroup', 
            'DistalPhalanxOutlineCorrect', 'DistalPhalanxTW','Earthquakes', 'ECG200', 'ECG5000', 'ECGFiveDays', 'EOGHorizontalSignal', 
            'EOGVerticalSignal', 'EthanolLevel','FaceAll', 'FaceFour', 'FacesUCR', 'FiftyWords', 'Fish', 'FordA', 'FreezerRegularTrain', 'FreezerSmallTrain', 'Fungi', 
            'GunPoint','GunPointAgeSpan', 'GunPointMaleVersusFemale', 'GunPointOldVersusYoung', 'Ham', 
            'HandOutlines', 'Haptics', 'Herring', 'HouseTwenty', 'InlineSkate', 'InsectEPGRegularTrain', 'InsectEPGSmallTrain', 'InsectWingbeatSound', 'ItalyPowerDemand', 'LargeKitchenAppliances',             
            'Lightning2', 'Lightning7', 'Mallat', 'Meat', 'MedicalImages',  'MiddlePhalanxOutlineAgeGroup', 'MiddlePhalanxOutlineCorrect',  'MiddlePhalanxTW',  
            'MixedShapesRegularTrain', 'MixedShapesSmallTrain', 'MoteStrain', 'NonInvasiveFetalECGThorax1','OliveOil', 'OSULeaf', 'PhalangesOutlinesCorrect', 'Phoneme', 
            'PigAirwayPressure', 'PigArtPressure', 'PigCVP',  'Plane', 'PowerCons', 'ProximalPhalanxOutlineAgeGroup', 'ProximalPhalanxOutlineCorrect', 'ProximalPhalanxTW', 
            'RefrigerationDevices', 'Rock', 'ScreenType', 'SemgHandGenderCh2', 'SemgHandMovementCh2', 'SemgHandSubjectCh2', 
            'ShapeletSim', 'ShapesAll', 'SmallKitchenAppliances', 'SmoothSubspace', 'SonyAIBORobotSurface1', 'SonyAIBORobotSurface2', 'Strawberry', 
            'SwedishLeaf', 'Symbols', 'SyntheticControl', 'ToeSegmentation1', 'ToeSegmentation2', 'Trace', 'TwoLeadECG', 'TwoPatterns', 'UMD',
            'UWaveGestureLibraryX', 'UWaveGestureLibraryY', 'UWaveGestureLibraryZ', 'Wafer', 'Wine', 'WordSynonyms', 'Worms', 'WormsTwoClass', 'Yoga'
]
print("AVAILABLE_DATASET_LEN", len(available_dataset))


abnormal_dataset = [
            # Abnormal
            ['AllGestureWiimoteX', 'AllGestureWiimoteY', 'AllGestureWiimoteZ', 'DodgerLoopDay', 'DodgerLoopGame', 'DodgerLoopWeekend', 
            'GestureMidAirD1', 'GestureMidAirD2', 'GestureMidAirD3', 'GesturePebbleZ1', 'GesturePebbleZ2', 'PickupGestureWiimoteZ', 'PLAID',
            'ShakeGestureWiimoteZ', 'MelbournePedestrian'],
            # Too calculate consumption
            ['Crop', 'ElectricDevices', 'FordB', 'NonInvasiveFetalECGThorax2', 'StarLightCurves', 'UWaveGestureLibraryAll']

]



print("ABNORMAL_DATASET_LEN", len(abnormal_dataset))






#创建一个空列表，存储当前目录下的CSV文件全称
file_name = []
 
#获取当前目录下的CSV文件名
def name():
  #将当前目录下的所有文件名称读取进来
  a = os.listdir()
  for j in a:
    #判断是否为CSV文件，如果是则存储到列表中
    if os.path.splitext(j)[1] == '.csv':
      file_name.append(j)
 
 
#将CSV文件内容导入到csv_storage列表中
def csv_new(storage):
  #创建一个空列表，用于存储CSV文件数据
  csv_storage = []
  with codecs.open(storage, 'r', encoding='utf-8') as fp:
    fp_key = csv.reader(fp)
    for csv_key in fp_key:
      csv_reader = csv.DictReader(fp, fieldnames=csv_key)
      for row in csv_reader:
        csv_dict = dict(row)
        csv_storage.append(csv_dict)
  for i in csv_storage:
    print(i)
 


# 生成表格文件
def create_file(content):
    # 初始化样式
    style_head = xlwt.XFStyle()
    # 初始化字体相关
    font = xlwt.Font()
    font.name = "微软雅黑"
    font.bold = True
    # 必须是数字索引
    font.colour_index = 1
    # 初始背景图案
    bg = xlwt.Pattern()
    # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
    bg.pattern = xlwt.Pattern.SOLID_PATTERN
    # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray
    bg.pattern_fore_colour = 4

    # 设置字体
    style_head.font = font
    # 设置背景
    style_head.pattern = bg


    #创建一个样式----------------------------
    better_style = XFStyle()
    pattern = Pattern()
    pattern.pattern = Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = Style.colour_map['yellow'] #设置单元格背景色为黄色
    better_style.pattern = pattern

    original_better_style = XFStyle()
    pattern = Pattern()
    pattern.pattern = Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = Style.colour_map['red'] #设置单元格背景色为黄色
    original_better_style.pattern = pattern

    equal_style = XFStyle()
    pattern = Pattern()
    pattern.pattern = Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = Style.colour_map['turquoise'] #设置单元格背景色为黄色
    equal_style.pattern = pattern

    error_style = XFStyle()
    pattern = Pattern()
    pattern.pattern = Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = Style.colour_map['tan'] #设置单元格背景色为黄色
    error_style.pattern = pattern

    # 创建一个excel
    excel = xlwt.Workbook(encoding='utf-8')
    # 添加工作区
    sheet = excel.add_sheet("演示表格")
    # xlwt中是行和列都是从0开始计算的
    first_col_1 = sheet.col(1)
    first_col_3 = sheet.col(3)
    # 设置创建时间宽度
    first_col_1.width = 256 * 15
    # 设置存储路径列宽度
    first_col_3.width = 256 * 100
    # 标题信息
    head = ["Dataset", "Standard_ACC", "NAS_ACC"]
    for index, value in enumerate(head):
        sheet.write(0, index, value, style_head)
    
    amount = 0
    improve = 0
    poorer = 0
    equal = 0
    error = 0
    # 循环写入
    for index, value_list in enumerate(content, 1):
        # 写入dataset
        sheet.write(index, 0, value_list[0])
        # 判断哪个大
        if value_list[1] < value_list[2]:
            sheet.write(index, 1, value_list[1])
            sheet.write(index, 2, value_list[2], style=better_style)
            improve += 1
        elif value_list[1] > value_list[2]:
            sheet.write(index, 1, value_list[1], style=original_better_style)
            sheet.write(index, 2, value_list[2])
            poorer += 1
        elif value_list[1] == 0 or value_list[2] == 0:
            sheet.write(index, 1, value_list[1], style=error_style)
            sheet.write(index, 2, value_list[2], style=error_style)
            error += 1
        else:
            sheet.write(index, 1, value_list[1], style=equal_style)
            sheet.write(index, 2, value_list[2], style=equal_style)
            equal += 1
        
        amount += 1
        # for i, value in enumerate(value_list)
        #     sheet.write(index, i, value)

    # 保存excel
    file_name = 'DatasetChart'
    excel.save(f"./{file_name}.xls")
    print(f"total amount: {amount}")
    print(f"Improve Performance: {improve}")
    print(f"Equal Performance: {equal}")
    print(f"Poorer Performance: {poorer}")
    print(f"Error: {error}")
    return file_name



 
#创建一个空列表，存储当前目录下的CSV文件全称
file_name = []
 
#获取当前目录下的CSV文件名
def name():
    #将当前目录下的所有文件名称读取进来
    a = os.listdir()
    for j in a:
        #判断是否为CSV文件，如果是则存储到列表中
        if os.path.splitext(j)[1] == '.csv':
          file_name.append(j)
 
 
#将CSV文件内容导入到csv_storage列表中
def csv_new(storage):
    #创建一个空列表，用于存储CSV文件数据
    csv_storage = []
    with codecs.open(storage, 'r', encoding='utf-8') as fp:
        fp_key = csv.reader(fp)
        for csv_key in fp_key:
          csv_reader = csv.DictReader(fp, fieldnames=csv_key)
          for row in csv_reader:
            csv_dict = dict(row)
            csv_storage.append(csv_dict)
  
    high = 0
    for i in csv_storage:
        # print(i['9'])
        if high < float(i['9']):
          high = float(i['9'])
    # print(storage, ' ', high)
    return high
 

std_LSTMFCN = {}



if __name__ == '__main__':
    

#运行获取当前目录下所有的CSV文件
    name()
    # print(file_name)
    print("FILE_AMOUNT:", len(file_name))
    df = pd.read_csv("./std_output.csv")
    

    # 将多个CSV文件逐个读取
    data_list = []
    ds_name_from_csv = []
    for name in file_name:
        ds_name_from_csv.append(name[:-13])
    

    for name in all_dataset:
        if name in abnormal_dataset[1]:
            new_tuple = (name, 0, 0)
        elif name in abnormal_dataset[0]:
            a = df[(df.Database==name)].index.tolist()
            new_tuple = (name, float(df['LSTM_FCN'][a]), csv_new(f"{name}_raw_data.csv"))
        elif name in available_dataset:
            a = df[(df.Database==name)].index.tolist()
            new_tuple = (name, float(df['LSTM_FCN'][a]), csv_new(f"{name}_raw_data.csv"))
        else:
            continue
        print(new_tuple)
        data_list.append(new_tuple)
            


    data_list.sort(key= lambda dataset: dataset[0])
    data = create_file(data_list)
    print("success")
    # print(data)
