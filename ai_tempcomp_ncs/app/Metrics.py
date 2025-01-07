from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
import _thread
import os
import numpy as np
from math import log10, sqrt
import cv2
import tensorflow as tf

import sklearn.metrics
from keras import backend as K
import matplotlib.pyplot as plt
import matplotlib

class _metrics:
    def cal_base(self,y_true,y_pred):
        #https://blog.csdn.net/weixin_43509263/article/details/101638713
        y_pred_poistive=K.round(K.clip(y_pred,0,1))
        y_pred_negative=1-y_pred_poistive
        y_positive=K.round(K.clip(y_true,0,1))
        y_negative=1-y_positive
        TP=K.sum(y_positive*y_pred_poistive)
        TN=K.sum(y_negative*y_pred_negative)
        FP=K.sum(y_negative*y_pred_poistive)
        FN=K.sum(y_positive*y_pred_negative)
        return TP,TN, FP,FN
    def acc(self,TN, FP, FN, TP):
        ACC=(TP+TN)/(TP+FP+FN+TN)
        return ACC

    def SSIM(self,y_true,y_pred):
        value=compare_ssim(y_true,y_pred)
        
        return value

    def sensitivity(self,TN, FP, FN, TP):
        #recall
        SE=TP/(TP+FN)
        return SE
    
    def presision(self,TN, FP, FN, TP):
        PC=TP/(TP+FP)
        return PC

    def specificity(self,TN, FP, FN, TP):
        SP=TN/(TN+FP)
        return SP

    def F1_Score(self,TN, FP, FN, TP):
        SE=self.sensitivity(TN, FP, FN, TP)
        PC=self.presision(TN, FP, FN, TP)
        F1=2*SE*PC/(SE+PC)
        return F1
    def recall(self,TN, FP, FN, TP):
        RECALL=TP/(TP+FN)
        return RECALL

    def Rate(self,y_true,y_pred):
        TP,TN,FP,FN=self.cal_base(y_true,y_pred)
        SP=TN/(TN+FP)
        return SP

    def IOU(self,target,prediction):
        intersection = np.logical_and(target, prediction)
        union = np.logical_or(target, prediction)
        union_sum=np.sum(union)
        print('union_sum:',union_sum)

        if(union_sum==0):
            union_sum=1
        iou_score = np.sum(intersection) / union_sum
        return iou_score

    def PSNR(self,original, compressed):
        mse = np.mean((original - compressed) ** 2)
        if(mse == 0):  # MSE is zero means no noise is present in the signal .
                    # Therefore PSNR have no importance.
            return 100
        max_pixel = 255.0
        psnr = 20 * log10(max_pixel / sqrt(mse))
        return psnr


    def plot_history(self,history,save_path):
        # summarize history for accuracy
        plt.plot(history.history['loss'])
        plt.title('mean_squared_error')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['loss'], loc='upper left')
        
        plt.savefig(save_path)
        plt.show()


