import tensorflow_hub as hub
import tensorflow as tf


class ModelCategory():
    def __init__(self):
        self.model_dict = {}

    def set_model(self):
        R50x1_object_model = self.model_build_all()

        self.model_dict['bag'] = {'model_name':'R50x1_object', 'model': R50x1_object_model, 'threshold':0.3}
        self.model_dict['cap'] = {'model_name':'R50x1_object', 'model': R50x1_object_model, 'threshold':0.3}
        self.model_dict['card'] = {'model_name':'R50x1_object', 'model':R50x1_object_model, 'threshold':0.5}
        self.model_dict['cloth'] = {'model_name':'R50x1_object', 'model': R50x1_object_model, 'threshold':0.35}
        self.model_dict['document'] = {'model_name':'R50x1_object', 'model': R50x1_object_model, 'threshold':0.35}
        self.model_dict['earphones'] = {'model_name':'R50x1_object', 'model': R50x1_object_model, 'threshold':0.3}
        self.model_dict['wallet'] = {'model_name':'R50x1_object', 'model':R50x1_object_model, 'threshold':0.3}
        self.model_dict['watch'] = {'model_name':'R50x1_object', 'model': R50x1_object_model, 'threshold':0.4}
        self.model_dict['phone'] = {'model_name':'R50x1_object', 'model': R50x1_object_model, 'threshold':0.3}
        self.model_dict['ring'] = {'model_name':'R50x1_object', 'model':R50x1_object_model, 'threshold':0.5}
        self.model_dict['shoes'] = {'model_name':'R50x1_object', 'model': R50x1_object_model, 'threshold':0.5}
        self.model_dict['shopping_bag'] = {'model_name':'R50x1_object', 'model': R50x1_object_model, 'threshold':0.5}
        self.model_dict['car_key'] = {'model_name':'R50x1_object', 'model': R50x1_object_model, 'threshold':0.45}
        self.model_dict['necklace'] = {'model_name':'R50x1_object', 'model': R50x1_object_model, 'threshold':0.6}

    
    def model_build(self, model_name):
        model_path = '/home/ubuntu/image_model/models/' + model_name
        tmp_model = tf.saved_model.load(model_path)
        layer = hub.KerasLayer(tmp_model, input_shape=(224, 224) + (3,))
        model = tf.keras.Sequential([layer])
        model.build([None, 244, 244, 3])
        print(f'=========={model_name} loaded==========')

        return model

    def model_build_all(self):
        model_names = ['R50x1_object']

        for model_name in model_names:
            globals()['{}_model'.format(model_name)] = self.model_build(model_name)
        
        return R50x1_object_model



    
