import librosa
import librosa.display
import os
import warnings
from warnings import simplefilter
import pandas as pd

def calculate_video_tempo(video_path):
    y, sr = librosa.load(video_path)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    print(str(item), "tempo：", tempo)
    return tempo

if __name__ == "__main__":
   video_path = "./videos"  # 视频路径
   warnings.filterwarnings('ignore', category=UserWarning)
   simplefilter(action='ignore', category=FutureWarning)
   files = os.walk(video_path)
   data = {'Video':[], 'Tempo':[]}
   # print(files)
   for file in files:  # 子文件
       # print(file[2])
       for item in file[2]:
           audio_path = os.path.join(video_path, item)
           value = calculate_video_tempo(audio_path)
           data['Video'].append(item)
           data['Tempo'].append(value)

   existing_data = pd.read_excel("results.xlsx", engine='openpyxl')
   df = pd.DataFrame(data)
   merged_date = pd.merge(existing_data, df, how = 'left', left_on= 'Video', right_on='Video')
   merged_date['Tempo'] = merged_date['Tempo']
   merged_date.to_excel("results.xlsx", index=False, engine='openpyxl')



