from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import requests
import boto3
import json
import os

timeout = 100

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

# DetailDo에 활용할 manageNum split
def split_manage_num(manageList):
    detailManageList = []

    for num in manageList:
        numsplit = num.split("-")
        detailManageList.append(numsplit)

    return detailManageList

# DetailDo page 정보 가져오기
def detail_crawling(region, manage_num, manage_subnum, start_date, end_date):
    detail_url = 'https://www.lost112.go.kr/find/findDetail.do'

    try:
        # 페이로드
        resp = requests.post(detail_url, data={
            'PRDT_CL_CD01': '',
            'PRDT_CL_CD02': '',
            'START_YMD': start_date,
            'END_YMD': end_date,
            'PRDT_NM': '',
            'DEP_PLACE': '',
            'SITE': '',
            'PLACE_SE_CD': '',
            'FD_LCT_CD': region,
            'IN_NM': '',
            'MDCD': '',
            'SRNO': '',
            'IMEI_NO': '',
            'F_ATC_ID': '',
            'ATC_ID': manage_num,
            'FD_SN': manage_subnum,
            'MENU_NO': ''
        }, timeout=timeout, verify=False)

        # 페이로드 사이트로 불러오기
        soup = bs(resp.text, 'html.parser')
        
        # 적정 태그 찾기
        find_info = soup.find("div", class_="find_info")

        find_nm = find_info.find("p", class_="find_info_name") # 습득물명
        find_01 = find_info.find_all("p", class_="find01") # 항목
        find_02 = find_info.find_all("p", class_="find02") # 항목값
        find_info_txt = soup.find("div", class_="find_info_txt") # 본문
        
        # 태그 딕셔너리로 만들어주기
        detail_dict = {}

        detail_dict['습득물명'] = find_nm.text
        detail_dict['내용'] = find_info_txt.text
        
        # ORG 찾기 & 추가
        frontORG = soup.find('h2', id="lost112_body")
        findORG = frontORG.find_next_sibling("script").get_text()
        textValIdx = findORG.find("ORG_ID") # 948

        valORG = findORG[textValIdx+8:textValIdx+19] # ORG_ID값 추출을 위해 인덱스 위치 계산
        
        detail_dict['ORG_ID'] = valORG
        
        for i in range(len(find_01)):
            detail_dict[find_01[i].text] = find_02[i].text
    
        return detail_dict

    except:
        pass

def mapInfo(valORG, manage_num, manage_subnum, pickup_center):
    mapDo = "https://www.lost112.go.kr/find/map.do"
    
    resp = requests.post(mapDo, data={
        "STUFF_ID" : "0",
        "FD_LST_CODE" : "0",
        "ORG_ID" : valORG,
        "ATC_ID" : manage_num,
        "FD_SN" : manage_subnum,
        "SITE" : "F",
        "DEP_PLACE" : pickup_center
    }, timeout=timeout, verify=False)
    
    # 페이로드 사이트로 불러오기
    soup = bs(resp.text, 'html.parser')
    
    # 주소 찾기
    bodyTag = soup.find('body') # 주소값 값의 이전 tag 찾기
    scriptTagText = bodyTag.find('script').get_text() # 주소 값이 있는 script tag의 text값 가져오기
    
    textValIdx = scriptTagText.find("ADDR") # 527 idx
    endIdx = scriptTagText.find("//주소") # 567 idx
    valADDR = scriptTagText[textValIdx+11:endIdx-11] # 주소값 추출을 위해 인덱스 위치 계산

    return valADDR

def detailDo():
    end = datetime.today()
    start = end - relativedelta(months=1)
    
    end_date = end.strftime("%Y%m%d")
    start_date = start.strftime("%Y%m%d")
    nowdate = datetime.now()
    
    detailDictList = []

    s3 = boto3.client('s3')
    listFilename = nowdate.strftime('%Y%m%d') + '_manageList'
    response = s3.get_object(Bucket='achachanew', Key=f'manageList/{listFilename}.txt')
    body = response['Body'].read().decode('utf-8')
    lines = body.split('\n')        
    detailManageList = split_manage_num(lines)

    for region in region_list:
        for item in detailManageList:
            try:
                detail_dict = detail_crawling(region, item[0], item[1], start_date, end_date)
                detail_dict['주소'] = mapInfo(detail_dict['ORG_ID'], item[0], item[1], detail_dict['보관장소'])
                detailDictList.append(detail_dict)
            except:
                pass

    jsonFilename = nowdate.strftime('%Y%m%d') + '_detailDictList'
    with open(f'{jsonFilename}.json','a') as file:
        json.dump(detailDictList, file, ensure_ascii=False, indent=4)
    
    s3 = boto3.client('s3')

    try:
        s3.upload_file(f'{jsonFilename}.json', "achachanew", f'detailDictList/{jsonFilename}.json')
    except Exception as err:
        print("input error", err)


    #file_path = f'/usr/local/airflow/dags/{jsonFilename}.json'
    file_path = f'{jsonFilename}.json'

    if os.path.exists(file_path):
        os.remove(file_path)
