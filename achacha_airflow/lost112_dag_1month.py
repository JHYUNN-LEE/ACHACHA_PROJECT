from airflow import DAG

# Operators
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# py files
import lost112_listDo_1month as script1
import lost112_detailDo_1month as script2
import lost112_imageGet_1month as script3


# ETC
from pendulum import yesterday
from datetime import datetime
from dateutil.relativedelta import relativedelta
import warnings

warnings.filterwarnings('ignore')

#---------- input 값 -----------
category_list = ['가방', '귀금속', '도서용품', '서류', '쇼핑백', '스포츠용품', '유가증권',
                 '의류', '자동차', '전자기기', '지갑', '증명서', '컴퓨터', '카드', '현금', '휴대폰']

region_list = ['서울', '경기도']

# input category dict
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

# input save_name dict
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

# input region
region_dict = {'서울' : 'LCA000', '경기도' : 'LCI000'}

region_en_dict = {'서울' : 'Seoul', '경기도' : 'Gyeonggi'}

dag = DAG(
    dag_id = '1month',
    schedule_interval = None,
    start_date = yesterday('Asia/Seoul')
)

listDo = PythonOperator(
    task_id = 'listDo',
    python_callable = script1.listDo,
    dag=dag
)

 detailDo = PythonOperator(
     task_id = 'detailDo',
     python_callable = script2.detailDo,
     dag=dag
 )

 imageGet = PythonOperator(
     task_id = 'imageGet',
     python_callable = script3.imageGet,
     dag=dag
 )
