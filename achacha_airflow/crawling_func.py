import pandas as pd
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
import warnings
import urllib.request
import os
warnings.filterwarnings('ignore')

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

# list.do에서 list를 마지막 페이지까지추출하는 함수입니다.
def list_crawling(category_key, pageidx, start_date, end_date):
    list_url = 'https://www.lost112.go.kr/find/findList.do'

    resp = requests.post(list_url, data={
        'PRDT_CL_CD01': category_key,
        'PRDT_CL_CD02': '',
        'START_YMD': start_date,
        'END_YMD': end_date,
        'PRDT_NM': '',
        'DEP_PLACE': '',
        'SITE': '',
        'PLACE_SE_CD': '',
        'FD_LCT_CD': 'LCA000',
        'IN_NM': '',
        'ATC_ID': '',
        'MDCD': '',
        'SRNO': '',
        'IMEI_NO': '',
        'F_ATC_ID': '',
        'pageIndex': pageidx,
        'MENU_NO': ''

    })

    # payload 대로 데이터 불러오기
    soup = bs(resp.text, 'html.parser')
    table = soup.find("table")

    # 관리번호 풀네임으로 가져오기
    tr_tags = table.find_all("tr")

    manage_num = []
    for i in range(1, len(tr_tags)):
        a_tag = tr_tags[i].find("a")
        a_tag_list = a_tag['href'].split("'")

        manage_num.append(a_tag_list[1] + '-' + a_tag_list[3])

    # 불러온 태그 테이블로 만들rl
    list_df = pd.read_html(str(table))
    list_df = list_df[0]

    list_df['관리번호'] = pd.DataFrame(manage_num)

    manage_split = list_df['관리번호'].str.split("-")

    list_df['관리번호_token'] = manage_split.str.get(0)
    list_df['관리번호_sub'] = manage_split.str.get(1)

    return list_df

# 마지막 페이지를 찾아주는 함수입니다.
def last_page(category_key, start_date, end_date):
    list_url = 'https://www.lost112.go.kr/find/findList.do'
    resp = requests.post(list_url, data={
        'PRDT_CL_CD01': category_key,
        'PRDT_CL_CD02': '',
        'START_YMD': start_date,
        'END_YMD': end_date,
        'PRDT_NM': '',
        'DEP_PLACE': '',
        'SITE': '',
        'PLACE_SE_CD': '',
        'FD_LCT_CD': 'LCA000',
        'IN_NM': '',
        'ATC_ID': '',
        'MDCD': '',
        'SRNO': '',
        'IMEI_NO': '',
        'F_ATC_ID': '',
        'pageIndex': 1,
        'MENU_NO': ''
    })

    # payload 대로 데이터 불러오기
    soup = bs(resp.text, 'html.parser')
    last = soup.find("a", class_ = "last")
    last_split =  last['onclick'].split("(")
    last_split_2 = last_split[1].split(")")
    last_num = int(last_split_2[0])

    return last_num

# detail.do 사이트의 디테일 정보를 테이블로 만들어주는 함수입니다.
def detail_crawling(category_key, manage_num, manage_subnum, start_date, end_date):
    detail_url = 'https://www.lost112.go.kr/find/findDetail.do'

    # 페이로드
    resp = requests.post(detail_url, data={
        'PRDT_CL_CD01': category_key,
        'PRDT_CL_CD02': '',
        'START_YMD': start_date,
        'END_YMD': end_date,
        'PRDT_NM': '',
        'DEP_PLACE': '',
        'SITE': '',
        'PLACE_SE_CD': '',
        'FD_LCT_CD': 'LCA000',
        'IN_NM': '',
        'MDCD': '',
        'SRNO': '',
        'IMEI_NO': '',
        'F_ATC_ID': '',
        'ATC_ID': manage_num,
        'FD_SN': manage_subnum,
        'MENU_NO': ''
    })

    # 페이로드 사이트로 불러오기
    soup = bs(resp.text, 'html.parser')
    # 적정 태그 찾기
    find_info = soup.find("div", class_="find_info")

    find_nm = find_info.find("p", class_="find_info_name")
    find_01 = find_info.find_all("p", class_="find01")
    find_02 = find_info.find_all("p", class_="find02")

    find_info_txt = soup.find("div", class_="find_info_txt")

    # 태그 딕셔너리로 만들어주기
    detail_dict = {}

    detail_dict['습득물명'] = find_nm.text
    detail_dict['내용'] = find_info_txt.text

    for i in range(len(find_01)):
        detail_dict[find_01[i].text] = find_02[i].text

    return detail_dict

def col_split(table):
    table = table[['습득물명', '관리번호', '습득장소', '내용', '습득일',
                   '물품분류', '보관장소', '유실물상태', '보관장소연락처']]

    # 습득물명 분류
    name_list = table['습득물명'].str.split(" : ")
    table['습득물명'] = name_list.str.get(1)

    # 카테고리 세분화
    manage_list = table['물품분류'].str.split(' > ')
    table['대분류'] = manage_list.str.get(0)
    table['소분류'] = manage_list.str.get(1)

    pickdate_list = table['습득일'].str.split(' ')
    table['습득일자'] = pickdate_list.str.get(0)
    table['습득시간'] = pickdate_list.str.get(1)

    # 삭제
    table = table.drop(["물품분류"], axis=1)
    table = table.drop(["습득일"], axis=1)

    return table

def append_image(category_key, manage_num, manage_subnum, start_date, end_date):
    detail_url = 'https://www.lost112.go.kr/find/findDetail.do'
    resp = requests.post(detail_url, data={
        'PRDT_CL_CD01': category_dict[category_key],
        'PRDT_CL_CD02': '',
        'START_YMD': start_date,
        'END_YMD': end_date,
        'PRDT_NM': '',
        'DEP_PLACE': '',
        'SITE': '',
        'PLACE_SE_CD': '',
        'FD_LCT_CD': 'LCA000',
        'IN_NM': '',
        'MDCD': '',
        'SRNO': '',
        'IMEI_NO': '',
        'F_ATC_ID': '',
        'ATC_ID': manage_num,
        'FD_SN': manage_subnum,
        'MENU_NO': ''
    })

    soup = bs(resp.text, 'html.parser')
    # imgurl 만들기
    div_detail = soup.find("div", class_="findDetail")
    # print(div_detail)
    img1 = div_detail.find("img")["src"]
    if not "no_img" in img1:
        img = img1
    imgUrl = ("https://www.lost112.go.kr" + img)
    num = soup.find("p", class_="find02").text
    # 이미지 저장 코드

    folder_path = "/home/ubuntu/csv_data/img_data/"+category_en_dict[category_key] + "_img"
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    urllib.request.urlretrieve(imgUrl, folder_path + "/"+num+'.jpg')

def split_manage_num(manage_list):
    detail_manage = []

    for i in manage_list:
        manage_split = i.split("-")

        detail_manage.append(manage_split)

    return detail_manage

def merge_table(listdo, detaildo):
    listdo = listdo[['관리번호', '분실자명']]

    # 함수적용
    detaildo = col_split(detaildo)

    # 머지
    merge_df = pd.merge(listdo, detaildo, left_on='관리번호', right_on='관리번호', how='inner')

    return merge_df

def crawling_update(category, start_date, end_date):
    # 모든 list_data 가져오기
    last_num = last_page(category_dict[category], start_date, end_date)
    all_df = pd.DataFrame()
    for i in tqdm(range(1, last_num + 1)):
        df = list_crawling(category_dict[category], i, start_date, end_date)
        all_df = all_df.append(df)

    new_manage_num = list(all_df['관리번호'])

    # list_data 업데이트
    list_path = "/home/ubuntu/csv_data/merge_seoul/" + category_en_dict[category] + "_seoul.csv"
    org_category_df = pd.read_csv(list_path, encoding="utf-8")
    org_manage_num = list(org_category_df['관리번호'])

    update_manage_num = []

    # 추가 데이터 리스트 산출
    for value in new_manage_num:
        if value not in org_manage_num:
            update_manage_num.append(value)

    # listdo 데이터 업테이트 해주기
    update_df = all_df[all_df['관리번호'].isin(update_manage_num)]
    
    ### 기존 리스트 데이터 불러오기
    listdo_saved_path = "/home/ubuntu/csv_data/list_data/" + category_en_dict[category] + "_listdo.csv"
    org_listdo_df = pd.read_csv(listdo_saved_path, encoding='utf-8')
    
    ### 합치기 및 저장
    update_listdo_df = pd.concat([update_df, org_listdo_df])
    update_listdo_df.to_csv(listdo_saved_path, encoding='utf-8-sig', index=False)

    # detaildo 데이터 업데이트 해주기
    detail_input_num = split_manage_num(update_manage_num)

    detail_data = []

    for i in detail_input_num:
        try:
            detail_dict = detail_crawling(category, i[0], i[1], start_date, end_date)
            append_image(category, i[0], i[1], start_date, end_date)
        except:
            pass

        detail_data.append(detail_dict)
    detail_df = pd.DataFrame(detail_data)

    # raw 관리번호와 새로운 관리번호 비교하여 detail_do update
    detaildo_saved_path = "/home/ubuntu/csv_data/detail_data/" + category_en_dict[category] + ".csv"
    org_detaildo_df = pd.read_csv(detaildo_saved_path, encoding="utf-8")
    ### 합치기 밒 저장
    update_detaildo_df = pd.concat([detail_df, org_detaildo_df])
    update_detaildo_df.to_csv(detaildo_saved_path, encoding='utf-8-sig', index=False)

    # 테이블 머지하기
    merge_df = merge_table(update_listdo_df, update_detaildo_df)

    # 수령여부 체크하기
    merge_manage_num = list(merge_df['관리번호'])

    delete_manage_list = []
    for value in merge_manage_num:
        if value not in new_manage_num:
            delete_manage_list.append(value)

    merge_df['수령여부'] = 0

    for i in range(len(merge_df)):
        if merge_df['관리번호'][i] in delete_manage_list:
            merge_df['수령여부'][i] = 'Y'
        else:
            merge_df['수령여부'][i] = 'N'

    ## 저장
    merge_save_path = "/home/ubuntu/csv_data/merge_seoul/" + category_en_dict[category] + "_seoul.csv"
    merge_df.to_csv(merge_save_path, encoding='utf-8-sig', index=False)

    return merge_df


# 집에서 해야 할 일
# 성재님 csv spark 합치고, 수란님 spark 에어플로우로 자동화