# DE
from re import M
from flask import request, Flask, redirect
import base64
from PIL import Image
from io import BytesIO
import io
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
import torch
import glob
import keras


# 경고끄기 (option)
import warnings
warnings.filterwarnings('ignore')

# %%

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

def search_img(category, cropped_file, threshold=0.4):
    cos_sim_df = get_cos_sim(cropped_file, category=category)
    df_top_sim = cos_sim_df[cos_sim_df.cos_sim <= threshold].sort_values(by='cos_sim')[1:50]

    return df_top_sim.filename.values

# %%
#@application.route('/')
#@application.route('/flask/', methods=["GET","POST"])
@application.route('/', methods=["GET", "POST"])
def get_data():
    if request.method == "POST":
        data = request.form #MultiDict 형태

        image_str = data['image']
        global category
        category = data['category']

        # image data 처리
        image_bytes = bytes(image_str, 'utf-8')

        decoded_string = io.BytesIO(base64.b64decode(image_bytes))
        
    #--------------------------------------------------------------------------
        # modeling

        # yolo
        # yolo_start_time = time.time()
        # global yolo_model
        # img = crop(decoded_string)
        # print(f'yolo소요시간 : {time.time()-yolo_start_time}초')
        
        global model_category
        global model, model_name
        model = model_category.model_dict[category]['model']
        model_name = model_category.model_dict[category]['model_name']
        threshold = model_category.model_dict[category]['threshold']

        start_time = time.time()
        
        global output_path
        output_path = f"./vector_frame_95/{category}/"
        
        global result
        result = search_img(category,  decoded_string, threshold=threshold)
        
        result = result.astype('str')
        result = json.dumps(result.tolist())
    
        
        print(f'모델 소요시간 : {time.time() - start_time:.3f}초')  # 테스트용 코드 -> 추후 삭제

        print(result)
        print(len(result))

    return result

if __name__ == "__main__":
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
