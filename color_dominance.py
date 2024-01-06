import cv2
import numpy as np
from scipy.spatial.distance import cdist
from collections import Counter
import os
import pandas as pd

def calculate_color_ratio(video_path):
    # 定义17种基本颜色
    basic_colors = {
        'aqua': [0, 255, 255],
        'black': [0, 0, 0],
        'blue': [0, 0, 255],
        'fuchsia': [255, 0, 255],
        'gray': [128, 128, 128],
        'green': [0, 128, 0],
        'lime': [0, 255, 0],
        'maroon': [128, 0, 0],
        'navy': [0, 0, 128],
        'olive': [128, 128, 0],
        'orange': [255, 165, 0],
        'purple': [128, 0, 128],
        'red': [255, 0, 0],
        'silver': [192, 192, 192],
        'teal': [0, 128, 128],
        'white': [255, 255, 255],
        'yellow': [255, 255, 0],
    }

    # 用于统计每帧主导颜色的字典
    frame_dominant_colors = []

    # 读取视频
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    for frame_idx in range(total_frames):
        ret, frame = cap.read()
        if not ret:
            break
        # 将图像转换为 RGB 色彩空间
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 用于统计颜色像素数的字典
        color_counts = {color: 0 for color in basic_colors}

        # 遍历每个像素
        height, width, _ = frame_rgb.shape
        pixels = frame_rgb.reshape((height * width, 3))
        distances = cdist(pixels, list(basic_colors.values()), 'euclidean')
        closest_color_indices = np.argmin(distances, axis=1)

        for i, matched_color_index in enumerate(closest_color_indices):
            matched_color = list(basic_colors.keys())[matched_color_index]
            color_counts[matched_color] += 1

        # print(color_counts)
        # 找到像素最多的颜色作为该帧的主导颜色
        dominant_color = max(color_counts, key=color_counts.get)
        # print(dominant_color)
        frame_dominant_colors.append(dominant_color)

    cap.release()

    # print(frame_dominant_colors)

    # 使用 Counter 统计每个颜色出现的次数
    color_counter = Counter(frame_dominant_colors)

    # 找到出现次数最多的颜色及其出现次数
    most_common_color, count = color_counter.most_common(1)[0]

    print(f'Most Common Color: {most_common_color}, Count: {count}')

    # 统计每个视频中以暖色和冷色为主导色的帧的比率
    warm_colors = ['red', 'yellow', 'orange', 'maroon', 'olive']
    cold_colors = ['aqua', 'blue', 'green', 'navy', 'teal']

    warm_frames = sum(1 for color in frame_dominant_colors if color in warm_colors)
    cold_frames = sum(1 for color in frame_dominant_colors if color in cold_colors)

    warm_ratio = warm_frames / total_frames
    cold_ratio = cold_frames / total_frames

    # print(warm_ratio,cold_ratio)
    print(str(item), "视频中暖色主导的比率：", warm_ratio)
    print(str(item), "视频中冷色主导的比率：", cold_ratio)
    return warm_ratio, cold_ratio

if __name__ == "__main__":
    # calculate_color_ratio("./videos/4.mp4")
    video_path = "./videos"  # 视频路径
    files = os.walk(video_path)
    data = {'Video': [], 'Warm': [], 'Cold': []}
    # print(files)
    for file in files:  # 子文件
        # print(file[2])
        for item in file[2]:
            audio_path = os.path.join(video_path, item)
            value1, value2 = calculate_color_ratio(audio_path)
            data['Video'].append(item)
            data['Warm'].append(value1)
            data['Cold'].append(value2)

        existing_data = pd.read_excel("results.xlsx", engine='openpyxl')
        df = pd.DataFrame(data)
        merged_date = pd.merge(existing_data, df, how='left', left_on='Video', right_on='Video')
        merged_date['Warm'] = merged_date['Warm']
        merged_date['Cold'] = merged_date['Cold']
        merged_date.to_excel("results.xlsx", index=False, engine='openpyxl')