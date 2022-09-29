# DE
from re import M
from flask import request, Flask, redirect
import base64
from PIL import Image
from io import BytesIO
import io
#from app_test_copy import *
# from werkzeug.utils import secure_filename
from model_category import ModelCategory
import json

# DS
from model_category import ModelCategory
import sys
import os
import pandas as pd
import tensorflow_hub as hub
import tensorflow as tf
import numpy as np
from PIL import Image
import numpy as np
import time
from scipy.spatial import distance
<<<<<<< HEAD
=======
import torch
import glob
import keras

>>>>>>> c975e6ae3a21e17a6cced9804125e970818ef0a4

# 경고끄기 (option)
import warnings
warnings.filterwarnings('ignore')

# %%

<<<<<<< HEAD
app = Flask(__name__)

# DS
=======
application = Flask(__name__)

# DS


#%%

# def crop(input_file):
#     """
#     im = Image.open(input_file).convert('RGB')
#     result = yolo_model(im)
#     result_df = result.pandas().xyxy[0]
#     name = result.pandas().xyxy[0]['name'][0]
#     im = im.crop( (result_df['xmin'], result_df['ymin'], result_df['xmax'], result_df['ymax']) )
#     im.save(f'/home/ubuntu/WEB_SERVICE_ACHACHA/FLASK/yolo/uploaded_file_crop/real_{category}_pred_{name}_{time.strftime("%H_%M_%S")}.jpg')
#     """
#
#     im_raw = Image.open(input_file).convert('RGB')
#     result = yolo_model(im_raw)
#     result_df = result.pandas().xyxy[0]
#     print(result_df)
#     name = result.pandas().xyxy[0]['name'][0]
#     im_cropped = im_raw.crop((result_df['xmin'], result_df['ymin'], result_df['xmax'], result_df['ymax']))
#     im_cropped.save(f'/home/ubuntu/WEB_SERVICE_ACHACHA/FLASK/yolo/uploaded_file_crop/real_{category}_pred_{name}_{time.strftime("%H_%M_%S")}.jpg')
#
#     im_raw_filename = f'real_{category}_pred_{name}_{time.strftime("%H_%M_%S")}'
#     im_raw.save('/home/ubuntu/WEB_SERVICE_ACHACHA/FLASK/yolo/uploaded_file_raw/' + im_raw_filename + '.jpg')
#     tmp_text = str(result.pandas().xyxy[0][['name', 'xmin', 'ymin', 'xmax', 'ymax']].loc[0].values)
#
#     f = open('/home/ubuntu/WEB_SERVICE_ACHACHA/FLASK/yolo/label_text/' + im_raw_filename + '.txt', 'w')
#     f.write(tmp_text)
#     f.close()
#
#     return im_cropped
    
#%%

>>>>>>> c975e6ae3a21e17a6cced9804125e970818ef0a4
def extract(file):
    # global model
    file = Image.open(file).convert('RGB').resize((224, 224))
    file = np.array(file) / 255.0  # 정규화

    embedding = model.predict(file[np.newaxis, ...])
    feature_np = np.array(embedding)
    flattened_feature = feature_np.flatten()

    return flattened_feature

# %%

def get_dataframe(category):
    # global output_path
    # global model_name
    tmp_filename = np.load(output_path + f'{category}_filename({model_name}).npy', allow_pickle=True)
    tmp_output = np.load(output_path + f'{category}_output({model_name}).npy', allow_pickle=True)
    df = pd.DataFrame({'filename': tmp_filename, 'output': tmp_output})
    return df

# %%

def get_cos_sim(file, category, metric='cosine'):
    file2vec = extract(file)  # 이미지 벡터화
    df = get_dataframe(category)  # 데이터프레임 가져오기
    df = df.append({'filename': file, 'output': file2vec}, ignore_index=True)
    cos_sim_array = np.zeros((len(df)))
    for i in range(0, len(df)):
        cos_sim_array[i] = distance.cdist([file2vec], [df.iloc[i, 1]], metric)[0]  # 벡터화된 이미지 기준
    df['cos_sim'] = cos_sim_array
    return df  # 런타임 비교용


# %%

# crop된 파일을 인풋 파일으로 넣어줘야함
def search_img(category, cropped_file, threshold=0.4):
    # global image_path
    # global output_path
    cos_sim_df = get_cos_sim(cropped_file, category=category)
    df_top_sim = cos_sim_df[cos_sim_df.cos_sim <= threshold].sort_values(by='cos_sim')[1:50]

    return df_top_sim.filename.values

<<<<<<< HEAD
#--------------------------------------------------------------------------
@app.route('/', methods=["GET","POST"])
def get_data():
    if request.method == "POST":
        data = request.form #MultiDict 형태
        
=======
# %%
#@application.route('/')
#@application.route('/flask/', methods=["GET","POST"])
@application.route('/', methods=["GET", "POST"])
def get_data():
    if request.method == "POST":
        data = request.form #MultiDict 형태

>>>>>>> c975e6ae3a21e17a6cced9804125e970818ef0a4
        image_str = data['image']
        category = data['category']
        
        # image data 처리
        image_bytes = bytes(image_str, 'utf-8')
        
        # base64_string = read_string()
        decoded_string = io.BytesIO(base64.b64decode(image_bytes))
<<<<<<< HEAD
        # img = Image.open(decoded_string)
        
        # img.show()
=======
        
>>>>>>> c975e6ae3a21e17a6cced9804125e970818ef0a4
    #--------------------------------------------------------------------------
        # modeling
        # yolo
<<<<<<< HEAD
    
        # crop(input_file) # 인s파일 잘라내기 + 카테고리 판단해주기
        # category = input('category :')  # 카테고리 이미지 전달
        # input_file = input('image_path :')  # 입력 이미지 전달
=======
        # yolo_start_time = time.time()
        # global yolo_model
        # img = crop(decoded_string)
        # print(f'yolo소요시간 : {time.time()-yolo_start_time}초')
        
        global model_category
>>>>>>> c975e6ae3a21e17a6cced9804125e970818ef0a4
        global model, model_name
        model = model_category.model_dict[category]['model']
        model_name = model_category.model_dict[category]['model_name']


        start_time = time.time()
        
        global output_path
<<<<<<< HEAD
        # image_path = f"../crops/{category}/" # crops된 이미지 경로
        output_path = f"../vector_frame/{category}/"  # npy파일 보관된 경로
        if not os.path.exists(output_path):
            print('디렉토리가 없으므로 생성합니다.')
            os.mkdir(output_path)

        # threshold의 디폴트 값은 0.4이고, search_img 함수의 마지막 인자로 넣어주면 바꿀 수 있음
        result = search_img(category, decoded_string)
=======
        output_path = f"./vector_frame_95/{category}/"
        
        global result
        result = search_img(category,  decoded_string, threshold=threshold)
>>>>>>> c975e6ae3a21e17a6cced9804125e970818ef0a4
        
        result = result.astype('str')
        # print(result1)
        # result = result.tolist()
        # print(type(result2))
        # result3 = json.dumps(result2)
        result = json.dumps(result.tolist())
<<<<<<< HEAD
        
        # print(result3)  # 인자로 input_file이 아닌 crops된 파일의 경로로 바꿔줘야함
        # print(type(result3))   
        
        print(f'소요시간 : {time.time() - start_time:.3f}초')  # 테스트용 코드 -> 추후 삭제
=======
    
        
        print(f'모델 소요시간 : {time.time() - start_time:.3f}초')  # 테스트용 코드 -> 추후 삭제

>>>>>>> c975e6ae3a21e17a6cced9804125e970818ef0a4
        print(result)
        # print(type(json.dumps(result2)))
        # print(json.dumps(result2))
                
    # return redirect("http://localhost:8000/fast_image/image/upload", json.dumps(result2))
    # return json.dumps(result2)
    return result

if __name__ == "__main__":
<<<<<<< HEAD
    model_category = ModelCategory()
    model_category.set_model()

    
    app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=False)
=======
    start_time = time.time()
    physical_devices = tf.config.experimental.list_physical_devices('GPU')
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
    os.environ['CUDA_LAUNCH_BLOCKING'] = "1"
#     gpu cash 지워주기
    import gc
    gc.collect()
    torch.cuda.empty_cac
    #
    # yolo = Yolo()
    # yolo_model = yolo.load_model()
    # #
    # gc.collect()
    # torch.cuda.empty_cache()
    
    model_category = ModelCategory()
    model_category.set_model()

    print(f'-------모델세팅완료------- 소요시간 : {time.time() - start_time:.3f}초')
    gc.collect()
    torch.cuda.empty_cache()
    try:
        application.run(host="0.0.0.0", debug=True, use_reloader=False)
    except Exception as e: print(e)
>>>>>>> c975e6ae3a21e17a6cced9804125e970818ef0a4
