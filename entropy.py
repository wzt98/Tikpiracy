import cv2
import numpy as np
import os
from PIL import Image, ImageStat
import pandas as pd

# 创建文件夹
def mkdir(path):
    # 引入模块
    import os
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    # path = path.rstrip("\\")
    # 判断路径是否存在
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        os.makedirs(path)
        # print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        # print(path + ' 目录已存在')
        return False

# 保存图片
def save_image(image, addr, num):
    address = os.path.join(addr, f"{num}.jpg")
    cv2.imwrite(address, image)

def calculate_entropy(image):
    # 转为灰度图
    gray_image = Image.open(image).convert('L')
    gray_array = np.array(gray_image)
    # 计算每个灰度颜色像素的占比
    pixel_freq = np.zeros(256)
    for i in range(gray_array.shape[0]):
        for j in range(gray_array.shape[1]):
            pixel_freq[gray_array[i, j]] += 1
    pixel_freq /= (gray_array.shape[0] * gray_array.shape[1])
    # 计算熵得分
    entropy = 0
    for i in range(256):
        if pixel_freq[i] > 0:
            entropy -= pixel_freq[i] * np.log2(pixel_freq[i])
    # 归一化
    entropy = entropy / np.log2(256) * 8
    return entropy

def calculate_video_entropy(video_path):
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    i = 0
    timeF = 25  # 每25帧保存一次图像
    j = 0
    mean_entropies = 0

    while ret:
        i = i + 1
        if i % timeF == 0:
            j = j + 1
            save_image(frame, os.path.join('images', str(item.split('.')[0]), ''), j)  # 保存图像
            img = os.path.join('images', str(item.split('.')[0]), f"{j}.jpg")
            mean_entropies = mean_entropies + calculate_entropy(img)
        ret, frame = cap.read()
    mean_entropies = mean_entropies / j
    print(str(item), "entropy：", mean_entropies)
    cap.release()
    return mean_entropies


if __name__ == "__main__":
    video_path = "./videos"  # 视频路径
    files = os.walk(video_path)
    data = {'Video': [], 'Entropy': []}
    # print(files)
    for file in files:  # 子文件
        # print(file[2])
        for item in file[2]:
            # 定义要创建的目录
            mkdir(os.path.join('images', str(item.split('.')[0])))
            audio_path = os.path.join(video_path, item)
            value = calculate_video_entropy(audio_path)
            data['Video'].append(item)
            data['Entropy'].append(value)

        existing_data = pd.read_excel("results.xlsx", engine='openpyxl')
        df = pd.DataFrame(data)
        merged_date = pd.merge(existing_data, df, how='left', left_on='Video', right_on='Video')
        merged_date['Entropy'] = merged_date['Entropy']
        merged_date.to_excel("results.xlsx", index=False, engine='openpyxl')


