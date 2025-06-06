import os
import pandas as pd

# 1. 设置文件夹路径
folder_path = 'national_summary'  # 请替换为你的实际路径

# 2. 获取所有txt文件的列表
file_list = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

# 3. 初始化数据列表
data = []

# 4. 遍历每个文件
for filename in file_list:
    file_path = os.path.join(folder_path, filename)
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取日期信息
    base_name = os.path.splitext(filename)[0]
    parts = base_name.split('_')
    
    if len(parts) >= 2:
        date_str = parts[-1]  # 取最后一部分，日期字符串
        try:
            if len(date_str) == 8:
                # 格式为YYYYMMDD
                date = pd.to_datetime(date_str, format='%Y%m%d')
            elif len(date_str) == 6:
                # 格式为YYYYMM，设为当月第一天
                date = pd.to_datetime(date_str, format='%Y%m')
            else:
                print(f"未知的日期格式：{date_str}，文件名：{filename}")
                date = None
        except ValueError:
            print(f"无法解析日期：{date_str}，文件名：{filename}")
            date = None
    else:
        print(f"文件名格式不匹配，无法提取日期：{filename}")
        date = None
    
    # 添加到数据列表
    data.append({'date': date, 'content': content})

# 5. 转换为DataFrame
df = pd.DataFrame(data)

# 6. 按日期排序
df = df.sort_values('date').reset_index(drop=True)

# 7. 查看数据
print(df.head())
