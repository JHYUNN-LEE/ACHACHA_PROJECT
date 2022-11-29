from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from pendulum import yesterday
from airflow.operators.dummy import DummyOperator
from crawling_func import crawling_update
from datetime import datetime
from dateutil.relativedelta import relativedelta
import warnings
import pandas as pd
import os

warnings.filterwarnings('ignore')


dag = DAG(
    dag_id= 'lost112_update',
    schedule_interval='@daily',
    start_date=yesterday('Asia/Seoul')
)

category_dict = {
    '가방' : 'PRA000', # 1
    '귀금속' : 'PRO000', # 2
    '도서용품' : 'PRB000', # 3
    '서류' : 'PRC000' , # 4
    '쇼핑백' : 'PRQ000', # 5
    '스포츠용품' : 'PRE000', # 6
    '유가증권' : 'PRM000', # 7
    '의류' : 'PRK000' , # 8
    '자동차' : "PRF000", # 9
    '전자기기' : 'PRG000' , # 10
    '지갑' : 'PRH000', # 11
    '증명서' : 'PRN000', # 12
    '컴퓨터' : 'PRI000', # 13
    '카드' : 'PRP000', # 14
    '현금' : 'PRL000', # 15
    '휴대폰' : 'PRJ000' # 16
}

category_en_dict = {
    '가방' : 'bag', # 1
    '귀금속' : 'jewelry', # 2
    '도서용품' : 'book', # 3
    '서류' : 'document' , # 4
    '쇼핑백' : 'shopping', # 5
    '스포츠용품' : 'sports', # 6
    '유가증권' : 'marketable', # 7
    '의류' : 'cloth' , # 8
    '자동차' : "car", # 9
    '전자기기' : 'electronic' , # 10
    '지갑' : 'wallet', # 11
    '증명서' : 'id', # 12
    '컴퓨터' : 'computer', # 13
    '카드' : 'card', # 14
    '현금' : 'cash', # 15
    '휴대폰' : 'phone' # 16
}

category_list = ['가방', '귀금속', '도서용품', '서류', '쇼핑백', '스포츠용품', '유가증권',
                 '의류', '자동차', '전자기기', '지갑', '증명서', '컴퓨터', '카드', '현금', '휴대폰']

category_en_list = ['bag', 'jewelry', 'book', 'document', 'shopping', 'sports', 'marketable', 'cloth',
                    "car", 'electronic', 'wallet', 'id', 'computer', 'card', 'cash', 'phone']

def all_play():
    enddate = datetime.today()
    startdate = enddate - relativedelta(months=7)
    end_date = enddate.strftime("%Y%m%d")
    start_date = startdate.strftime("%Y%m%d")
    for i in range(len(category_list)):
        crawling_update(category_list[i], start_date, end_date)

# merge_seoul csv 합치는 함수
#def merge_rawdata():
#    folders = os.listdir("/home/ubuntu/csv_data/merge_seoul/")
#    df_all = pd.DataFrame()
#
#    for i in range(0, len(folders)):
#        if folders[i].split('.')[1] == 'csv':
        file = folders[i]
        df = pd.read_csv("/home/ubuntu/csv_data/merge_seoul/"+file, encoding='utf-8-sig')
        df_all = pd.concat([df_all, df])

#    df_all.to_csv('/home/ubuntu/csv_data/merge_seoul/all_merge/merge_seoul.csv', encoding='utf-8-sig', index=False)

# TASK

# 1. RAW DATA 업데이트

append_rawdata = PythonOperator(
    task_id='append_rawdata',
    python_callable=all_play,
    dag=dag
)

# 2. rawdata 합치기

merge_seoul = PythonOperator(
    task_id='merge_seoul',
    python_callable=merge_rawdata,
    dag=dag
)

# TASK2 : HDFS에 저장
mergeddata_upload = BashOperator(
    task_id='mergeddata_upload',
    bash_command=f'hdfs dfs -put -f /home/ubuntu/csv_data/merge_seoul/merge_seoul.csv csv_data/merge_seoul/'
)

# bash 명령어 작성
bash = '''
hdfs dfs -put -f /home/ubuntu/csv_data/img_data/bag_img/*.jpg images/seoul_img_data/bag_img/; 
hdfs dfs -put -f /home/ubuntu/csv_data/img_data/jewelry_img/*.jpg images/seoul_img_data/jewelry_img/;
hdfs dfs -put -f /home/ubuntu/csv_data/img_data/book_img/*.jpg images/seoul_img_data/book_img/;
hdfs dfs -put -f /home/ubuntu/csv_data/img_data/document_img/*.jpg images/seoul_img_data/document_img/;
hdfs dfs -put -f /home/ubuntu/csv_data/img_data/sports_img/*.jpg images/seoul_img_data/sports_img/;
hdfs dfs -put -f /home/ubuntu/csv_data/img_data/shopping_img/*.jpg images/seoul_img_data/shopping_img/;
hdfs dfs -put -f /home/ubuntu/csv_data/img_data/marketable_img/*.jpg images/seoul_img_data/marketable_img/;
hdfs dfs -put -f /home/ubuntu/csv_data/img_data/cloth_img/*.jpg images/seoul_img_data/cloth_img/;
hdfs dfs -put -f /home/ubuntu/csv_data/img_data/car_img/*.jpg images/seoul_img_data/car_img/;
hdfs dfs -put -f /home/ubuntu/csv_data/img_data/electronic_img/*.jpg images/seoul_img_data/electronic_img/;
hdfs dfs -put -f /home/ubuntu/csv_data/img_data/id_img/*.jpg images/seoul_img_data/id_img/;
hdfs dfs -put -f /home/ubuntu/csv_data/img_data/wallet_img/*.jpg images/seoul_img_data/wallet_img/;
hdfs dfs -put -f /home/ubuntu/csv_data/img_data/computer_img/*.jpg images/seoul_img_data/computer_img/;
hdfs dfs -put -f /home/ubuntu/csv_data/img_data/card_img/*.jpg images/seoul_img_data/card_img/;
hdfs dfs -put -f /home/ubuntu/csv_data/img_data/cash_img/*.jpg images/seoul_img_data/cash_img/;
hdfs dfs -put -f /home/ubuntu/csv_data/img_data/phone_img/*.jpg images/seoul_img_data/phone_img/;

'''

# 이미지 업로드

image_upload = BashOperator(
    task_id='image_upload',
    bash_command=bash
)

# local img 폴더 삭제
delete_image = BashOperator(
    task_id='delete_image',
    bash_command='rm -r /home/ubuntu/csv_data/img_data/*'
)


# TASK3 : PYSPARK

append_rawdata >> merge_seoul >> mergeddata_upload >> image_upload >> delete_image