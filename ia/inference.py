#from matplotlib import pyplot as plt
import tensorflow as tf
import keras
import argparse
import keras.backend as K
from keras.models import load_model
import cv2
import numpy as np
#import seaborn as sns
import pandas as pd
import datetime as dt


class Prev:
    def __init__(self, path: str, names: list, probs: list):
        self.path = path
        self.names = names
        self.probs = probs
        self.date = dt.datetime.now()

    def salvar(self):
        try:
            ds = pd.read_csv("prev.csv", sep=";")
        except:
            ds = pd.DataFrame(columns=["path", "names", "probs", "date"])
            ds.to_csv("prev.csv", sep=";", index=False)
        new_row = pd.DataFrame({"path": [self.path], "names": [self.names], "probs": [self.probs], "date": [self.date]})
        ds = pd.concat([ds, new_row], ignore_index=True)
        ds.to_csv("prev.csv", sep=";", index=False)

    def ler(self):
        try:
            ds = pd.read_csv("prev.csv", sep=",")
            return ds
        except:
            print('Erro ao ler o arquivo prev.csv (Ou ele não existe)')

def get_classes(classes):
    return classes

def get_preds(preds):
    return list(preds.ravel())

def get_pred(preds, classes):
    preds = preds.ravel()
    argM = np.argmax(preds)
    return str(classes[argM]), round(float(preds[argM]), 2)

def print_pred(preds,classes):
    preds = preds.ravel()

    y = len(classes)
    x=""
    for i in range(y):
        preds_rounded = np.around(preds,decimals=4)
        x = x+classes[i]+": "+str(preds_rounded[i])+"%"
        if i!=(y-1):
            x = x+", "
        
        else:
            None
    return x

def image_preprocessing(img):
    img = cv2.imread(img)
    img = cv2.resize(img,(224,224))
    img = np.reshape(img,[1,224,224,3])
    img = 1.0*img/255

    return img

def inference(img):

    classes = ['CNV', 'DME','DRUSEN','NORMAL']

    processsed_img = image_preprocessing(img)
    K.clear_session()
    model = load_model('kermany.hdf5')

    preds = model.predict(processsed_img,batch_size=None,steps=1, verbose=0)
  
    print_pred(preds*100,classes)

    return preds*100, classes
