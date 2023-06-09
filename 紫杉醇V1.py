# %%
#Q1：ALK有40阴性。意思是剩下60是阳性吗？还是没参加测试。
#Q2：有人又失访，又PFS事件，哪个当截尾信息呢？
#Q3：生存分析的事件变量怎么算？

# %%
import numpy as np
import pandas as pd
import os
from openpyxl import utils
import warnings
import statistics
warnings.filterwarnings("ignore", category=UserWarning)
from scipy.stats import fisher_exact

from lifelines import KaplanMeierFitter
import matplotlib.pyplot as plt
from lifelines import CoxPHFitter

# %%
统计 = pd.read_excel('C:/Users/NC-O10/Dropbox/云蜚科技/脂质紫杉醇/紫杉醇干净的数据.xlsx', sheet_name='统计用100例')
交差 = pd.read_excel('C:/Users/NC-O10/Dropbox/云蜚科技/脂质紫杉醇/紫杉醇干净的数据.xlsx', sheet_name='交差100例')

# %%
## 一. 描述性分析

# %%
#年龄recoding
from datetime import datetime
确诊年龄= 统计['确诊年龄']
df = pd.DataFrame(确诊年龄)

# Remove rows with NA values
年龄 = df.dropna()
#print(年龄)
中位数_年龄=np.mean(年龄)
年龄max=np.max(年龄)
年龄min=np.min(年龄)
print(中位数_年龄)
print(年龄min)
print(年龄max)
#recode 年龄 greater than mean=1, lower than mean=0
# Assuming you have a DataFrame with an 'Age' column
# Sample age values with NA
ages = 统计['确诊年龄']
年龄_中位 = pd.DataFrame({'Age': ages})
# Fill NA values with a specific value (e.g., 0)
年龄_中位['Age'] = 年龄_中位['Age'].fillna(64)

#print(年龄_中位)
年龄recode = pd.DataFrame({'Age': 统计['确诊年龄']})

# Calculate the mean age
mean_age = 64.1

# Create a new column for recoded categories
年龄recode['Age_Category'] = ''
年龄recode=年龄recode.fillna(0)
# Recode ages based on mean
年龄recode.loc[年龄recode['Age'] > mean_age, 'Age_Category'] = '1'
年龄recode.loc[年龄recode['Age'] < mean_age, 'Age_Category'] = '0'

# Print the updated DataFrame
#print(年龄recode)
ALK=统计['ALK']
ALK=统计['ALK'].fillna(1)
ALK_recoded = ALK.where(ALK != '阴性', 0)
#print(ALK_recoded)
#calculate the fisher's exact test p-value
from scipy.stats import fisher_exact
import pandas as pd
# Assuming you have a DataFrame with exposure and outcome columns
紫杉醇_年龄 = pd.DataFrame({'Exposure': 年龄recode['Age_Category'],
                   'Outcome': ALK_recoded})
# Use replace() method to recode the variable
# Extract the exposure and outcome columns as separate variables
exposure = 紫杉醇_年龄['Exposure']
outcome = 紫杉醇_年龄['Outcome']
# Perform Fisher's exact test
odds_ratio, p_value = fisher_exact(pd.crosstab(exposure, outcome))
# Print the results
#print("Odds Ratio:", odds_ratio)
print("p-value:", p_value)

# %%
#性别
age=统计['性别'].describe()
print(age)

# %%
#清病理
病理=统计['清病理'].value_counts()
print(病理)

# %%
#TNM
TNM=统计['TNM分期'].value_counts()
print(TNM)

# %%
#EGFR
EGFR=统计['EGFR'].value_counts()
print(EGFR)

# %%
#ALK
ALK=统计['ALK'].value_counts()
print(ALK)

# %%
#用药周期
用药周期=统计['最大用药周期数更新'].value_counts()
print(用药周期)

# %%
#剂量
剂量=统计['紫杉醇脂质体总剂量（mg）'].describe()
print(剂量)

# %%
#联合通用名
联合通用名=统计['联合免疫用药通用名'].value_counts()
print(联合通用名)

# %%
#联合用药周期
联合用药周期=统计['联合免疫用药周期数'].value_counts()
print(联合用药周期)

# %%


# %%
## 二. 生存分析

# %%
#是否失访
失访=统计['是否失访'].value_counts()
print(失访)
#是否回顾
回顾=统计['是否回顾'].value_counts()
print(回顾)
#有无PFS事件
PFS=统计['有无PFS事件'].value_counts()
print(PFS)


# %%

# Convert date columns to datetime data type
联合用药时间={'start':统计['联合免疫用药开始日期'] ,'end': 统计['联合免疫用药结束日期']}
联合时间=pd.DataFrame(联合用药时间)
联合时间['start'] = pd.to_datetime(联合时间['start'] )
联合时间['end'] = pd.to_datetime(联合时间['end'])

# Subtract the columns and create a new column with the result
联合时间['date_difference'] = 联合时间['end'] - 联合时间['start']

# Print the resulting dataset
print(联合时间['date_difference'])


# %%


# %%
data = {
    'time': 联合时间['date_difference'],
    'event': 统计['有无PFS事件']
}

df = pd.DataFrame(data)

# Fit Kaplan-Meier estimator
kmf = KaplanMeierFitter()
kmf.fit(df['time'], event_observed=df['event'])

# Generate KM curve
kmf.plot()
plt.xlabel('Time')
plt.ylabel('Survival Probability')
plt.title('Kaplan-Meier Curve')
plt.show()

# %%
import pandas as pd
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test

# Create two sample datasets for comparison
group1 = {
    'time': [10, 15, 20, 25, 30],
    'event': [1, 0, 1, 0, 1]
}

group2 = {
    'time': [10, 15, 20, 25, 30],
    'event': [0, 0, 0, 0, 0]
}

df_group1 = pd.DataFrame(group1)
df_group2 = pd.DataFrame(group2)

# Fit Kaplan-Meier estimators for each group
kmf_group1 = KaplanMeierFitter()
kmf_group1.fit(df_group1['time'], event_observed=df_group1['event'])

kmf_group2 = KaplanMeierFitter()
kmf_group2.fit(df_group2['time'], event_observed=df_group2['event'])

# Perform log-rank test
results = logrank_test(df_group1['time'], df_group2['time'], df_group1['event'], df_group2['event'])

# Print the log-rank test statistic and p-value
print("Log-Rank Test Statistic: %.2f" % results.test_statistic)
print("Log-Rank Test p-value: %.4f" % results.p_value)

# %%
#logrank for 2 groups
import pandas as pd
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test

# Create two sample datasets for comparison
group1 = {
    'time': [10, 15, 20, 25, 30],
    'event': [1, 0, 1, 0, 1]
}

group2 = {
    'time': [5, 10, 15, 20, 25],
    'event': [1, 1, 0, 1, 0]
}

df_group1 = pd.DataFrame(group1)
df_group2 = pd.DataFrame(group2)

# Fit Kaplan-Meier estimators for each group
kmf_group1 = KaplanMeierFitter()
kmf_group1.fit(df_group1['time'], event_observed=df_group1['event'])

kmf_group2 = KaplanMeierFitter()
kmf_group2.fit(df_group2['time'], event_observed=df_group2['event'])

# Perform log-rank test
results = logrank_test(df_group1['time'], df_group2['time'], df_group1['event'], df_group2['event'])

# Print the log-rank test statistic and p-value
print("Log-Rank Test Statistic: %.2f" % results.test_statistic)
print("Log-Rank Test p-value: %.4f" % results.p_value)

# %%
import pandas as pd
from lifelines import CoxPHFitter
import matplotlib.pyplot as plt

# Create a sample dataset
data = {
    'time': [5, 10, 15, 20, 25, 30],
    'event': [1, 1, 0, 1, 0, 1]
}

df = pd.DataFrame(data)

# Fit Cox proportional hazards model
cph = CoxPHFitter()
cph.fit(df, 'time', event_col='event')

# Generate survival curve
survival_prob = cph.predict_survival_function(df)

# Plot the survival curve
plt.plot(survival_prob.index, survival_prob.values)
plt.xlabel('Time')
plt.ylabel('Survival Probability')
plt.title('Survival Curve')
plt.show()

# Get hazard ratios
hr = cph.hazard_ratios_
print(hr)

# %%
import pandas as pd
from lifelines import KaplanMeierFitter
import matplotlib.pyplot as plt

# Create two sample datasets for comparison
group1 = {
    'time': [10, 15, 20, 25, 30],
    'event': [1, 0, 1, 0, 1]
}

group2 = {
    'time': [5, 10, 15, 20, 25],
    'event': [1, 1, 0, 1, 0]
}

df_group1 = pd.DataFrame(group1)
df_group2 = pd.DataFrame(group2)

# Fit Kaplan-Meier estimators for each group
kmf_group1 = KaplanMeierFitter()
kmf_group1.fit(df_group1['time'], event_observed=df_group1['event'])

kmf_group2 = KaplanMeierFitter()
kmf_group2.fit(df_group2['time'], event_observed=df_group2['event'])

# Plot KM curves
plt.figure(figsize=(8, 6))
kmf_group1.plot(label='Group 1')
kmf_group2.plot(label='Group 2')
plt.xlabel('Time')
plt.ylabel('Survival Probability')
plt.title('Kaplan-Meier Curves')
plt.legend()
plt.show()

# %%
import pandas as pd
from lifelines import CoxPHFitter

# Create a sample dataset
data = {
    'time': [5, 10, 15, 20, 25, 30],
    'event': [1, 1, 0, 1, 0, 1],
    'group': [0, 0, 1, 1, 0, 1],
    'censored': [0, 1, 0, 1, 0, 1],
    'sex': [1, 0, 1, 0, 0, 1],
    'age': [20, 25, 30, 35, 40, 45]
}

df = pd.DataFrame(data)

# Fit Cox proportional hazards model
cph = CoxPHFitter()
cph.fit(df, 'time', event_col='event', show_progress=False)

# Get the hazard ratios
hr = cph.hazard_ratios_

# Print the hazard ratios
print(hr)

# %%
## 三. 疗效评估

# %%
疗效评价=统计['最佳疗效']

# number of PR
# Count the occurrences of a specific string in a column
PR = 'PR'
count = (统计['最佳疗效'] == PR).sum()
# Print the count
print("Count of '{}' is {}".format(PR, count))

# number of SD
# Count the occurrences of a specific string in a column
SD = 'SD'
count = (统计['最佳疗效'] == SD).sum()
# Print the count
print("Count of '{}' is {}".format(SD, count))

# number of PD
# Count the occurrences of a specific string in a column
PD = 'PD'
count = (统计['最佳疗效'] == PD).sum()
# Print the count
print("Count of '{}' is {}".format(PD, count))
# number of CR
# Count the occurrences of a specific string in a column
CR = 'CR'
count = (统计['最佳疗效'] == CR).sum()
# Print the count
print("Count of '{}' is {}".format(CR, count))

#PR SD PD CR
PR=51/(51+50+18+13)
print("PR='{}'".format(PR))
SD=50/(51+50+18+13)
print("SD='{}'".format(SD))
PD=18/(51+50+18+13)
print("PD='{}'".format(PD))
CR=13/(51+50+18+13)
print("CR='{}'".format(CR))

#ORR DCR
ORR=CR+PR
print("ORR='{}'".format(ORR))
DCR=ORR+SD
print("DCR='{}'".format(DCR))


