import cv2
import os
import numpy as np
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

# 计算每帧的“感知亮度”
def compute_brightness(image_path):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    lab_image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2LAB)
    # 提取L*通道（亮度）
    l_channel = lab_image[:, :, 0]
    # 计算亮度的平均值
    average_brightness = np.mean(l_channel)
    return average_brightness

def calculate_video_brightness(video_path):
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    i = 0
    timeF = 25  # 每25帧保存一次图像
    j = 0
    mean_brightness = 0
    while ret:
        i = i + 1
        if i % timeF == 0:
            j = j + 1
            # print(i)
            save_image(frame, os.path.join('images', str(item.split('.')[0]), ''), j)  # 保存图像
            img = os.path.join('images', str(item.split('.')[0]), f"{j}.jpg")
            # save_image(frame, os.path.join('images', '99', ''), j)  # 保存图像
            # img = os.path.join('images', '99', f"{j}.jpg")
            mean_brightness = mean_brightness + compute_brightness(img)
        ret, frame = cap.read()
    if j != 0:
        mean_brightness = mean_brightness / j
        # print(mean_brightness)
        print(str(item), "brightness：", mean_brightness)
    else:
        print("error")
    cap.release()
    return mean_brightness

if __name__ == "__main__":
    # calculate_video_brightness('./videos/99 .MP4')
    video_path = "./videos"  # 视频路径
    files = os.walk(video_path)
    data = {'Video': [], 'Brightness': []}
    # print(files)
    for file in files:  # 子文件
        # print(file[2])
        for item in file[2]:
            # 定义要创建的目录
            mkdir(os.path.join('images', str(item.split('.')[0])))
            audio_path = os.path.join(video_path, item)
            value = calculate_video_brightness(audio_path)
            data['Video'].append(item)
            data['Brightness'].append(value)

        existing_data = pd.read_excel("results.xlsx", engine='openpyxl')
        df = pd.DataFrame(data)
        merged_date = pd.merge(existing_data, df, how='left', left_on='Video', right_on='Video')
        merged_date['Brightness'] = merged_date['Brightness']
        merged_date.to_excel("results.xlsx", index=False, engine='openpyxl')
