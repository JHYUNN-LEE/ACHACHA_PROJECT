import tensorflow_hub as hub
import tensorflow as tf

class ModelCategory():
    def __init__(self):
        self.model_dict = {}

    def set_model(self):
        self.model_dict['wallet'] = {'model_name':'R50x1_object', 'model':self.__get_model_build('R50x1_object')}
        self.model_dict['phone'] = {'model_name':'R50x1_object', 'model':self.__get_model_build('R50x1_object')}
        self.model_dict['cap'] = {'model_name':'R50x1_object', 'model':self.__get_model_build('R50x1_object')}
        self.model_dict['card'] = {'model_name':'R50x1_object', 'model':self.__get_model_build('R50x1_object')}
        self.model_dict['bag'] = {'model_name':'R50x1_object', 'model':self.__get_model_build('R50x1_object')}
        self.model_dict['book'] = {'model_name':'R50x1_object', 'model':self.__get_model_build('R50x1_object')}
        self.model_dict['shopping_bag'] = {'model_name':'R50x1_object', 'model':self.__get_model_build('R50x1_object')}
        self.model_dict['earphones'] = {'model_name':'R50x1_object', 'model':self.__get_model_build('R50x1_object')}
        self.model_dict['car_key'] = {'model_name':'R50x1_object', 'model':self.__get_model_build('R50x1_object')}
        self.model_dict['shoes'] = {'model_name':'R50x1_object', 'model':self.__get_model_build('R50x1_object')}
        self.model_dict['document'] = {'model_name':'R50x1_object', 'model':self.__get_model_build('R50x1_object')}
        self.model_dict['watch'] = {'model_name':'R50x1_object', 'model':self.__get_model_build('R50x1_object')}

    def __get_model_build(self, model_name):
        model_path = '../models/' + model_name # 모델이 있는 상대경로의 디렉토리 이름을 model_name과 동일하게 설정
        tmp_model = tf.saved_model.load(model_path)

        layer = hub.KerasLayer(tmp_model, input_shape=(224, 224) + (3,))
        model = tf.keras.Sequential([layer])
        model.build([None, 244, 244, 3])

        return model