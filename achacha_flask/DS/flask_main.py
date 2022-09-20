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

# 경고끄기 (option)
import warnings
warnings.filterwarnings('ignore')

# %%

app = Flask(__name__)

# DS
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
@app.route('/', methods=["GET","POST"])
def get_data():
    if request.method == "POST":
        data = request.form #MultiDict 형태
        
        image_str = data['image']
        category = data['category']
        
        # image data 처리
        image_bytes = bytes(image_str, 'utf-8')
        
        decoded_string = io.BytesIO(base64.b64decode(image_bytes))

    #--------------------------------------------------------------------------
        # modeling
        # yolo
    
        global model, model_name
        model = model_category.model_dict[category]['model']
        model_name = model_category.model_dict[category]['model_name']


        start_time = time.time()
        
        global output_path
        output_path = f"../vector_frame/{category}/"  # npy파일 보관된 경로
        if not os.path.exists(output_path):
            print('디렉토리가 없으므로 생성합니다.')
            os.mkdir(output_path)

        # threshold의 디폴트 값은 0.4이고, search_img 함수의 마지막 인자로 넣어주면 바꿀 수 있음
        result = search_img(category, decoded_string)
        
        result = result.astype('str')
        result = json.dumps(result.tolist())
    
        
        print(f'소요시간 : {time.time() - start_time:.3f}초')  # 테스트용 코드 -> 추후 삭제
        print(result)

    return result

if __name__ == "__main__":
    model_category = ModelCategory()
    model_category.set_model()

    
    app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=False)