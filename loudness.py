import librosa
import numpy as np
import os
import warnings
from warnings import simplefilter
import pandas as pd

def calculate_loudness(audio_path, frame_size=512, hop_length=256):
    # 从视频中提取音频
    y, sr = librosa.load(audio_path, sr=None)
    rmse = librosa.feature.rms(y=y, frame_length=frame_size, hop_length=hop_length, center=True)
    # 计算整个视频的平均RMSE
    average_rmse = np.mean(rmse[0])
    print(str(item), "loudness：", average_rmse)
    return average_rmse

if __name__ == "__main__":
   video_path = "./videos"  # 视频路径
   warnings.filterwarnings('ignore', category=UserWarning)
   simplefilter(action='ignore', category=FutureWarning)
   files = os.walk(video_path)
   data = {'Video':[], 'Loudness':[]}
   # print(files)
   for file in files:  # 子文件
       # print(file[2])
       for item in file[2]:
           audio_path = os.path.join(video_path,item)
           value = calculate_loudness(audio_path)
           data['Video'].append(item)
           data['Loudness'].append(value)

   df = pd.DataFrame(data)
   file = 'results.xlsx'
   df.to_excel(file, index=False)


