import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import numpy as np
import os
import seaborn as sns
import MyFactorTester as FT
from MyFactorTester import process,perform,plot,tool
from MyFactorTester import report
from MyFactorTester.prepare_datas import load_data,Factor,save_cache,load_cache
import json
import tempfile

#加载设置
path=tempfile.gettempdir()
settings=json.load(open(path+r'\CUI_12345.json','r'))

#初始化

periods=[k for k,j in settings['periods'].items() if j]  #持仓期

if not settings['read_cache']:
    load_data(settings['data_path'])  # 加载股票数据,加载的时候要多个持仓期一起加载
    save_cache(settings['data_path'])  #保存缓存。如果加载出错，注释掉此行代码
else:
    load_cache(settings['data_path'])  #加载缓存

#尝试多种方法读取因子值
try:
    with open(settings['factor_name'],encoding='utf-8') as f:
        if settings['factor_name'].endswith('.csv'):
            factor_df=pd.read_csv(f,index_col=0,parse_dates=True)
        elif settings['factor_name'].endswith('.pkl'):
            factor_df=pd.read_pickle(settings['factor_name'])
        elif settings['factor_name'].endswith('.p'):
            factor_df=pd.read_pickle(settings['factor_name'],compression='zip')
        else:
            raise NotImplementedError
except:
    with open(settings['factor_name'],encoding='gbk') as f:
        if settings['factor_name'].endswith('.csv'):
            factor_df=pd.read_csv(f,index_col=0,parse_dates=True)
        elif settings['factor_name'].endswith('.pkl'):
            factor_df=pd.read_pickle(settings['factor_name'])
        elif settings['factor_name'].endswith('.p'):  #压缩过的因子
            factor_df=pd.read_pickle(settings['factor_name'],compression='zip')
        else:
            raise NotImplementedError

# 把行与列处理成标准格式
factor_df.columns=factor_df.columns.astype('str')
factor_df.index=pd.to_datetime(factor_df.index)

factor=Factor(factor_df)

print('因子值加载完毕，开始进行预处理')
