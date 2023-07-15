import os
from src.components.emotions_detection import Detect
from src.components.model_training import BuildModel

if __name__ == "__main__":
    obj = BuildModel()
    train = "data/train"
    test = "data/test"
    train_generator,validation_generator,num_train,num_val,batch_size,num_epoch = obj.data_generation(train,test)      
    model = obj.model_creation()
    obj.train_model(model)