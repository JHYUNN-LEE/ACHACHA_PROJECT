import logging
import datetime
import re 


def trace_logger(request):
    # logger 호출 
    logger = logging.getLogger('user_acctive.request')
    
    # 빈 딕셔너리 생성
    content = dict()
    
    # request 값 호출 
    
    now_date = datetime.datetime.now()
    now_date= now_date.strftime('%Y-%m-%d %H:%M:%S')

    method = request.method
    scheme = request.scheme 
    HOST_url = request.get_host()
    active_URL = request.path 

    # user id 있으면 불러오고 없으면 none 처리
    user_id = request.user
    
    # ip 받아오는 방법 
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    


    # 빈 딕셔너리 생성
    content = dict()
    
    # content 딕셔너리 정리 
    content['datetime'] = now_date
    content['scheme'] = scheme
    content['method'] = method
    content['HOST_URL'] = HOST_url
    content['ACTIVE_URL'] = active_URL
    
    # 페이지가 있으면 페이지 붙이기 
    if request.GET.get('page'):
        page = request.GET.get('page')
        content['ACTIVE_URL'] = active_URL + '?page=' + page

    # ip 받아오기 
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
        content['ip'] = ip
    else:
        ip = request.META.get('REMOTE_ADDR')
        content['ip'] = ip
     
    content['USER_ID'] = str(user_id)
    content['USER_STATUS'] = 'view'

    ### 이부부터 사이트에 맞는 request 값을 넣어주세요. ### 

    logger.info(content)   


def trace_logger_context(request, context):
    # logger 호출 
    logger = logging.getLogger('user_acctive.request')
    
    # 빈 딕셔너리 생성
    content = dict()
    
    # request 값 호출 
    
    now_date = datetime.datetime.now()
    now_date= now_date.strftime('%Y-%m-%d %H:%M:%S')

    method = request.method
    scheme = request.scheme 
    HOST_url = request.get_host()
    active_URL = request.path 

    # user id 있으면 불러오고 없으면 none 처리
    user_id = request.user
    
    # ip 받아오는 방법 
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    

    # 빈 딕셔너리 생성
    content = dict()
    
    # content 딕셔너리 정리 
    content['datetime'] = now_date
    content['scheme'] = scheme
    content['method'] = method
    content['HOST_URL'] = HOST_url
    content['ACTIVE_URL'] = active_URL
    
    # ip 받아오기 
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
        content['ip'] = ip
    else:
        ip = request.META.get('REMOTE_ADDR')
        content['ip'] = ip
     
    content['USER_ID'] = str(user_id)
    content['USER_STATUS'] = 'insert'

    content['context'] = context

    ### 이부부터 사이트에 맞는 request 값을 넣어주세요. ### 

    logger.info(content)  



