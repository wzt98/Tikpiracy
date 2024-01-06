import cv2
import face_recognition
import os
import pandas as pd

def detect_faces(video_path):
    cap = cv2.VideoCapture(video_path)
    score = 0  # 初始得分为0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # 转换为RGB颜色空间（face_recognition库要求）
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # 在当前帧中查找所有人脸
        face_locations = face_recognition.face_locations(rgb_frame)
        # 如果找到人脸，得分为1，然后跳出循环
        if face_locations:
            score = 1
            break
    cap.release()
    print(str(item), "人脸存在得分：", score)
    return score

if __name__ == "__main__":
    video_path = "./videos"  # 视频路径
    files = os.walk(video_path)
    data = {'Video': [], 'Face': []}
    # print(files)
    for file in files:  # 子文件
        # print(file[2])
        for item in file[2]:
            audio_path = os.path.join(video_path, item)
            value = detect_faces(audio_path)
            data['Video'].append(item)
            data['Face'].append(value)

        existing_data = pd.read_excel("results.xlsx", engine='openpyxl')
        df = pd.DataFrame(data)
        merged_date = pd.merge(existing_data, df, how='left', left_on='Video', right_on='Video')
        merged_date['Face'] = merged_date['Face']
        merged_date.to_excel("results.xlsx", index=False, engine='openpyxl')





