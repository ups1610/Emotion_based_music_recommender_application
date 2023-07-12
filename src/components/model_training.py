from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Flatten
from keras.layers.convolutional import Conv2D
from keras.optimizers import Adam
from keras.layers.pooling import MaxPooling2D
from keras.preprocessing.image import ImageDataGenerator
import os
import sys
import matplotlib as mpl
import matplotlib.pyplot as plt
from dataclasses import dataclass
from src.utils import save_object
from src.exception import CustomException
from src.logger import logging

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifacts','model.h5')

class BuildModel:
    def __init__(self):
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
        mpl.use('TkAgg')
        self.model_trainer_config = ModelTrainerConfig()

    def plot_model_history(self,history):
        """
        Plot Accuracy and Loss curves given the model_history
        """
        try:
            logging.info("Model Result Graph initiated...")

            plt.figure(1)
        
            # summarize history for accuracy
            print(history.history.keys())
            plt.subplot(211)
            plt.plot(history.history['accuracy'])
            plt.plot(history.history['val_accuracy'])
            plt.title('Model Accuracy')
            plt.ylabel('Accuracy')
            plt.xlabel('Epoch')
            plt.legend(['Training', 'Validation'], loc='lower right')
            
            # summarize history for loss
            
            plt.subplot(212)
            plt.plot(history.history['loss'])
            plt.plot(history.history['val_loss'])
            plt.title('Model Loss')
            plt.ylabel('Loss')
            plt.xlabel('Epoch')
            plt.legend(['Training', 'Validation'], loc='upper right')
            
            plt.tight_layout()
            
            plt.show() 
        except Exception as e:
            logging.info("Exception occurs at graph plotting")
            raise CustomException(e,sys)       
    
    def data_generation(self, train, test):
        try:
            
            logging.info("Data gather initiated...")
            train_dir = train
            val_dir = test
    
            num_train = 28709
            num_val = 7178
            batch_size = 64
            num_epoch = 50
            
            train_datagen = ImageDataGenerator(rescale=1./255)
            val_datagen = ImageDataGenerator(rescale=1./255)
            
            train_generator = train_datagen.flow_from_directory(
                    train_dir,
                    target_size=(48,48),
                    batch_size=batch_size,
                    color_mode="grayscale",
                    class_mode='categorical')
            
            validation_generator = val_datagen.flow_from_directory(
                    val_dir,
                    target_size=(48,48),
                    batch_size=batch_size,
                    color_mode="grayscale",
                    class_mode='categorical')
            logging.info("Data generated successfully")
            logging.info(f"train_generator = {train_generator}\nvalidation_generator = {validation_generator}\nnum_train = {num_train}\nnum_val = {num_val}\nbatch_size = {batch_size}\nnum_epoch = {num_epoch}")

            return (train_generator,
                   validation_generator,
                   num_train,
                   num_val,
                   batch_size,
                   num_epoch,
                   )
        except Exception as e:
            logging.info("Error ocurred in data generation")
            raise CustomException(e,sys)
        
    
    def model_creation(self):
        """
        Create the model
        """
        try:
            logging.info("Initiate model creation...")
            model = Sequential()
    
            model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48,48,1)))
            model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
            model.add(MaxPooling2D(pool_size=(2, 2)))
            model.add(Dropout(0.25))
            
            model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
            model.add(MaxPooling2D(pool_size=(2, 2)))
            model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
            model.add(MaxPooling2D(pool_size=(2, 2)))
            model.add(Dropout(0.25))
            
            model.add(Flatten())
            model.add(Dense(1024, activation='relu'))
            model.add(Dropout(0.5))
            model.add(Dense(7, activation='softmax'))

            logging.info("Model created successfully")
    
            return model
        except Exception as e:
            logging.info("Error occured in Model creation.")
            raise CustomException(e,sys)
    
    def train_model(self,model,num_train,batch_size,num_epoch,validation_generator,num_val,train_generator):
        try:
            logging.info("Training initiated...")

            model.compile(loss='categorical_crossentropy',optimizer=Adam(lr=0.0001, decay=1e-6),metrics=['accuracy'])
    
            model_info = model.fit_generator(
                    train_generator,
                    steps_per_epoch=num_train // batch_size,
                    epochs=num_epoch,
                    validation_data=validation_generator,
                    validation_steps=num_val // batch_size)
        
            self.plot_model_history(model_info)
            # model.save_weights('artifacts/model.h5')
            save_object(
                     file_path=self.model_trainer_config.trained_model_file_path,
                     obj=model
                )
            logging.info("Model trained successfully")
        except Exception as e:
            logging.info("Error ocurred in train_model")
            raise CustomException(e,sys)    
            

if __name__ == "__main__":
    obj = BuildModel()
    train = "data/train"
    test = "data/test"
    train_generator,validation_generator,num_train,num_val,batch_size,num_epoch = obj.data_generation(train,test)      
    model = obj.model_creation()
    obj.train_model(model)     

        