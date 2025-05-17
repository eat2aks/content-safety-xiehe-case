# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 19:18:32 2024

@author: jinyu
"""
import json
import jieba
import pandas as pd
from matplotlib import colors
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 文件名
filename = r"C:\Users\xinyi\Desktop\jupyter\merged_comments.jsonl"

# 存储content字段值的列表
content_list = []
 
# 打开文件并读取
with open(filename, 'r', encoding='utf-8') as file:  # 假设文件是以UTF-8编码的
    for line in file:
        # 解析每一行的JSON对象
        json_obj = json.loads(line)
        
        # 提取content字段的值（如果它存在的话）
        content = json_obj.get('content', None)
        
        # 将content值添加到列表中
        if content is not None:
            content_list.append(content)


#降重
seen = set()
unique_list= []

for x in  content_list:
    if x not in seen:
        seen.add(x)
        unique_list.append(x)

#############################
#%%
#分词

def get_word_frequency(text):
    seg_list = jieba.cut(text)
    word_dict = {}
    for word in seg_list:
        if word in word_dict:
            word_dict[word] += 1
        else:
            word_dict[word] = 1
    sorted_word_dict = sorted(word_dict.items(), key=lambda x: x[1], reverse=True)
    return sorted_word_dict

segmented_text = []

for text in unique_list:
    result = get_word_frequency(text)
    segmented_text.append(result)

#%%
#将所有结果放在一起
# 创建一个空字典来存储合并后的词频
merged_word_freq = {}
 
# 遍历每个子列表
for sublist in segmented_text:
    # 遍历子列表中的每个词频对
    for word, freq in sublist:
        # 如果单词已经在字典中，增加其频率
        if word in merged_word_freq:
            merged_word_freq[word] += freq
        # 否则，在字典中创建一个新条目
        else:
            merged_word_freq[word] = freq
#%%
#去除停用词
stopwords = set()
with open(r"C:\Users\xinyi\Desktop\py\WeiboSpider-master\output\stopwprds_xiao.txt", "r", encoding='utf-8') as f:
     for line in f:
        stopwords.add(line.strip())


# 创建一个新的字典来存储过滤后的词频
filtered_word_freq = {}
 
# 遍历词频字典，并过滤掉停用词
for word, freq in merged_word_freq.items():
    if word not in stopwords:
        filtered_word_freq[word] = freq

    

# 对合并后的词频字典进行排序，得到排序后的列表
sorted_word_freq = sorted(filtered_word_freq.items(), key=lambda x: x[1], reverse=True)
import pandas as pd

sorted_word_freq1 =pd.DataFrame(sorted_word_freq)
sorted_word_freq1.to_excel(r"C:\Users\xinyi\Desktop\py\WeiboSpider-master\output\merged_progress_output2.xlsx",index=False)



sorted_word_freq1=sorted_word_freq1.drop([0,1,6]).reset_index(drop=True)



# 但是，为了生成词云，我们应该将单词和频率放入一个字典中
# 并且我们不需要 DataFrame 的索引
word_freq_dict = dict(zip(sorted_word_freq1[0], sorted_word_freq1[1]))
#%%
from matplotlib import colors

# 建立颜色数组，可更改颜色
#color_list = ['#FF274B']#单个颜色

color_list = colors.ListedColormap(['#0D1B2A',  # 深蓝黑
 '#1B263B',  # 海军蓝
 '#274472',  # 蓝灰
 '#41729F',  # 湖蓝
 '#4D96FF',  # 亮蓝
 '#845EC2',  # 高级紫
 '#D65DB1',  # 玫红紫
 '#FF6F61',  # 番茄红
 '#FFB627']  # 明黄橙

)



#画词云图
import matplotlib.pyplot as plt
mask=plt.imread(r"C:\Users\xinyi\Desktop\py\WeiboSpider-master\output\mask1.jpg")

from wordcloud import WordCloud
# bgimg=imread(r'17.jpg')#设置背景图片
wd=WordCloud(font_path="simhei.ttf",  # 设置词云字体
               background_color="white",  # 背景颜色
               max_words=100,  # 词云显示的最大词数
           #    stopwords=stop_words.add(open(r"J:\0research\tingyongci.txt", 'r', Sencoding='utf-8')),  # 设置停用词
               max_font_size=60,  # 字体最大值
               random_state=30,  # 设置有多少种随机生成状态，即有多少种配色
               width=2000, height=1920,
               margin=4,  # 设置图片默认的大小,margin为词语边缘距离
               colormap=color_list,               #字体颜色
               mask=mask,
               ).generate_from_frequencies(word_freq_dict)
              # image_colors = ImageColorGenerator(bgimg)  # 根据图片生成词云颜色
# 运用matplotlib展现结果
import matplotlib.pyplot as plt
plt.subplots(figsize=(12,8))
plt.imshow(wd)
plt.axis("off")
plt.show()









