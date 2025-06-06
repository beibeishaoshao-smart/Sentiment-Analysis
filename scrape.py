import requests
from bs4 import BeautifulSoup

# 函数：爬取并保存每个页面的 "Full Report" 内容
def scrape_and_save(year, month):
    # 格式化月份为两位数
    month_str = f"{month:02d}"
    # 构建URL
    url = f"https://www.federalreserve.gov/monetarypolicy/beigebook/beigebook{year}{month_str}.htm?summary"

    # 发起GET请求
    response = requests.get(url)
    
    if response.status_code == 200:
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 定位到Full Report下的内容
        content = soup.get_text()
        start_idx = content.find("Prepared at the Federal Reserve Bank of")
        end_idx = content.find("Return to top")

        # 如果找到了Full Report部分，提取该内容
        if start_idx != -1 and end_idx != -1:
            full_report_text = content[start_idx:end_idx].strip()

            # 保存到以年份和月份命名的TXT文件
            file_name = f'national_summary/national_summary_{year}{month_str}.txt'
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(full_report_text)
            
            print(f"{file_name} 内容已成功保存。")
        else:
            print(f"Full Report内容未找到：{url}")
    else:
        print(f"请求失败，状态码: {response.status_code}, URL: {url}")

# 爬取多个年份和月份的数据
for year in range(2011, 2017):  # 从2011年到2016年
    for month in range(1, 13):  # 1到12月
        scrape_and_save(year, month)
