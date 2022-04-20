from cProfile import label
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xlrd
from matplotlib.pyplot import MultipleLocator

colors = ['#FF0000', '#FFA500', '#FFFF00', '#00FF00', '#228B22', '#00C5CD', '#00BFFF', '#FF7F50', '#8A2BE2', '#8B7B8B']

# 绘制种群每一代个体适应度的变化


pathX = 'Phoneme_raw_data.csv'  #  113.xlsx 在当前文件夹下
df = pd.read_csv(pathX)

print(df)
print(df.shape)

# df.plot()
# plt.show()


x_row = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

print(x_row)

y_column = []
for i in range(10):
    y_column.append(df.iloc[i, 2:].to_numpy())

print(y_column)


fig, ax = plt.subplots()

xticks = list(range(100)) #自定义刻度
ax.set_xticks(xticks)

atitle = "Sound_Phoneme_Individual_Fitness"

plt.title(atitle, fontsize=12) #标题,并设置字体大小
plt.ylabel("Fitness") #纵坐标名字
plt.xlabel("Generation") #横坐标名字
plt.grid(True,linestyle=':') #设置网格
plt.xlim((0,11))    # 坐标轴的取值范围
plt.tick_params(axis='both',which='major',labelsize=14)
x_major_locator=MultipleLocator(1)
ax.xaxis.set_major_locator(x_major_locator)

ls = []
for i in range(len(y_column)):
    l_temp, = plt.plot(x_row, y_column[i], color=colors[i], linewidth=1.5, linestyle="-")   
    ls.append(l_temp)


labels = []
for i in range(10):
    labels.append(f"Individual{i + 1}")

print(labels)

plt.legend(handles=ls, labels=labels, bbox_to_anchor=(0, 0.84), loc=3, borderaxespad=0, ncol=2, prop={'size': 6})
# plt.savefig(f"{atitle}.png")
plt.show()
