# -*- coding: utf-8 -*-
"""Digital Hero_Final Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1v03ZxMblz5QADOTyqZmPUrifvgzURck0

# Home Credit Default Risk Project by Digital Hero

## Load the data!
"""

#Import library for loading our data!
import numpy as np
import pandas as pd

from google.colab import drive
# Mount Google Drive
drive.mount('/content/gdrive')

#Load the training data!
df_train = pd.read_csv('/content/gdrive/My Drive/application_train.csv')

df_train.head()

#Cek the structure of our training data!
df_train.shape

df_train.info()

#Load testing data!
df_test = pd.read_csv('/content/gdrive/My Drive/application_test.csv')

df_test.head()

#Check the structure of the testing data!
df_test.shape

"""## Exploratory Data Analysis!"""

#Simple statistics for our numerical variables in training data!
simple_stats = df_train.describe(include = 'all').transpose()
simple_stats

"""Notice that not all features have the same count! It indicates that there some of them have missing values!"""

#For the testing data!
df_test.describe(include = 'all').transpose()

"""From the output above, we can say exactly the same compared to our interpretation toward the training data!

### Check missing data!
"""

#Let's check whether our training data contains missing values or not!
total_missing_values = df_train.isnull().sum().sort_values(ascending = False)
total_non_missing_values = df_train.count().sort_values(ascending = False)
percent_missing_values = total_missing_values/(total_non_missing_values+total_missing_values)*100
df_train_missing = pd.concat([total_missing_values, total_non_missing_values, percent_missing_values], axis = 1, keys = ['Total Missing Values',
                                                                                                                        'Total Non Missing Values',
                                                                                                                        'Percentage of Missing Values'])
df_train_missing.head(20)

"""### Plot 1 : Distribution of Loan Status!"""

import matplotlib.pyplot as plt
import seaborn as sns
sns.countplot(df_train['TARGET'])
plt.title('Counts of Loan Status (0 : Loan is paid on time, 1 : Have Difficulties)')
plt.show()

"""Notice that the number of 0s is much higher than the number of 1s (The number of Loans that are repaid on time is much more than the loans that are not repaid). That means we face an "Imbalanced Class Problem" in Classification!

### Plot 2 : Distribution of the Amount of Credit!
"""

fig, ax = plt.subplots(figsize = (12,6))
sns.distplot(df_train['AMT_CREDIT'], ax = ax)
ax.set_title('Distribution of the amount of credit')
plt.show()

#Check which columns in DataFrame are Categorical

df_train.select_dtypes(exclude=["number","bool_"]).columns

#Get the number of categorical columns

len(df_train.select_dtypes(exclude=["number","bool_"]).columns)

"""### Plot 3 : Categorical Count Charts (Part 1)"""

g = sns.catplot(x="CODE_GENDER", col="TARGET",
                data=df_train, kind="count",
                height=4, aspect=.7)

plt.show()

g = sns.catplot(x="NAME_CONTRACT_TYPE", col="TARGET",
                data=df_train, kind="count",
                height=4, aspect=.7)

g = sns.catplot(x="FLAG_OWN_CAR", col="TARGET",
                data=df_train, kind="count",
                height=4, aspect=.7)

g = sns.catplot(x="FLAG_OWN_REALTY", col="TARGET",
                data=df_train, kind="count",
                height=4, aspect=.7)

g = sns.catplot(x="NAME_TYPE_SUITE", col="TARGET",
                data=df_train, kind="count",
                height=6, aspect=2)

g = sns.catplot(x="NAME_INCOME_TYPE", col="TARGET",
                data=df_train, kind="count",
                height=4, aspect=2.5)

g = sns.catplot(x="NAME_EDUCATION_TYPE", col="TARGET",
                data=df_train, kind="count",
                height=5, aspect=2.5)

g = sns.catplot(x="NAME_FAMILY_STATUS", col="TARGET",
                data=df_train, kind="count",
                height=4, aspect=1.5)

#Plot distribusi fitur Gender.
plt.subplot(1, 2, 1)
sns.countplot(df_train['CODE_GENDER'])
plt.title("Distribusi Fitur Gender!")

plt.subplot(1,2,2)
count = df_train['CODE_GENDER'].value_counts()
count.plot.pie(autopct = '%1.3f%%', figsize = (10,7),explode = [0,0.1,0.2],title = "Persentase nilai pada fitur Gender")

plt.show()

"""### Plot 4 : Categorical Count Charts (Part 2)"""

g = sns.catplot(x="NAME_HOUSING_TYPE", col="TARGET",
                data=df_train, kind="count",
                height=4, aspect=2.1)

plt.show()

g = sns.catplot(x="WEEKDAY_APPR_PROCESS_START", col="TARGET",
                data=df_train, kind="count",
                height=4, aspect=2)

plt.show()

g = sns.catplot(x="FONDKAPREMONT_MODE", col="TARGET",
                data=df_train, kind="count",
                height=4, aspect=2)

plt.show()

g = sns.catplot(x="HOUSETYPE_MODE", col="TARGET",
                data=df_train, kind="count",
                height=4, aspect=1)

plt.show()

g = sns.catplot(x="WALLSMATERIAL_MODE", col="TARGET",
                data=df_train, kind="count",
                height=4, aspect=2)

plt.show()

g = sns.catplot(x="EMERGENCYSTATE_MODE", col="TARGET",
                data=df_train, kind="count",
                height=5, aspect=1)

plt.show()

"""### Handling Anomalies!"""

#Let's take a look to numerical variables in our training data
import numpy as np

df_train.describe(include = [np.number])

"""Notice that 'DAYS_BIRTH' and 'DAYS_EMPLOYED' column's mean are negative! To fix this, we have to take the absolute value of the columns original values!"""

#Absolute value of 'DAYS-BIRTH' column!
df_train['DAYS_BIRTH'] = np.abs(df_train['DAYS_BIRTH'])
(df_train['DAYS_BIRTH']).describe()

#Absolute value of 'DAYS_EMPLOYED column!
df_train['DAYS_EMPLOYED'] = np.abs(df_train['DAYS_EMPLOYED'])
(df_train['DAYS_EMPLOYED']).describe()

"""Also notice that the 'DAYS_EMPLOYED' column is very strange because its max value is 365243 days! It means 1000 years!!! IT IS IMPOSSIBLE! We guess that this can happen by an accident, such as typo, inputting the wrong value, etc

To handle these anomalous variables, we will first replace strange/imposibble values with NaNs! We also want to create new columns for those replaced values!
"""

#Create new column for strange value!
df_train['ANOM_DAYS_EMPLOYED'] = df_train[df_train['DAYS_EMPLOYED'] == 365243].DAYS_EMPLOYED

#Replace those strange values with NaNs!
df_train['DAYS_EMPLOYED'].replace({365243:np.nan}, inplace = True)

#Also apply this method to our testing data!
df_test['ANOM_DAYS_EMPLOYED'] = df_test[df_test['DAYS_EMPLOYED'] == 365243].DAYS_EMPLOYED

#Replace those strange values with NaNs in our testing dataset!
df_test['DAYS_EMPLOYED'].replace({365243:np.nan}, inplace = True)

#Calculate correlations of our target variable to another variables!
corr1 = df_train.corr().TARGET.sort_values()

print('The most positive correlations:\n', corr1.tail())
print('\nThe most negative correlations:\n', corr1.head())

"""###Plot 5: Age Distribution"""

age = pd.DataFrame(df_train[['DAYS_BIRTH', 'TARGET']])
age['Age_Years'] = age['DAYS_BIRTH']/365
age.head()

age['Age_Years'].max()

#Create bin
age['Age_Bins'] = pd.cut(x=age['Age_Years'], bins=[20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70])
age.head()

Groups = age.groupby('Age_Bins').mean()
Groups

plt.figure(figsize=(20, 10))
plt.bar(Groups.index.astype(str), Groups['TARGET'])

plt.title('Age Distribution of Loan Default', fontsize= 30)
plt.xlabel('Age Range', fontsize= 18)
plt.ylabel('Probability of Default', fontsize= 18)
plt.show()

"""There is a clear correlation between the age and the probability of default.

### Check for the types of our data's columns!
"""

df_train.dtypes.value_counts()

"""Recall that "float64" data type shows that the column is filled with decimal number and "int64" type column is filled with integer. Both of them are numerical variables. Then,  "object" data type column is filled with string or categorical variables.

For the categorical variables columns, we need to know how many unique classes in each of them!
"""

#Count of unique classes in each categorical variable column!
df_train.select_dtypes('object').apply(pd.Series.nunique, axis = 0)

"""### Convert categorical variables to numerical variables using One Hot Encoding!"""

#Using One Hot Encoding!
df_train = pd.get_dummies(df_train)
df_test = pd.get_dummies(df_test)

#Check the structure of our new training and testing data!
print('Our new training data shape {}'.format(df_train.shape))
print('Our new testing data shape {}'.format(df_test.shape))

"""We get a problem! Recall that our future machine learning model cannot handle the data where its training is different to our testing data in terms of the number of features!

This is because there are some variables/columns that exist in our training data, but they don't exist in our testing data!

### Equalizing the number of independent variables in our training and testing data!
"""

#Assign the target variable to new variable called "target_train"
target_train = df_train['TARGET']

#Equalizing the number of features in our training and testing data using inner join method!
df_train, df_test = df_train.align(df_test, join = 'inner', axis = 1)

#Insert again our target variable in training data!
df_train['TARGET'] = target_train

#Let's take a look to the shape of our new training and testing data!
print('Our new again training data shape {}'.format(df_train.shape))
print('Our new again testing data shape {}'.format(df_test.shape))

"""### Plot 4 : Heatmap for the most negative correlations!"""

#3 variables with the strongest negative correlations with the target
external_data = df_train[['TARGET', 'EXT_SOURCE_1', 'EXT_SOURCE_2', 'EXT_SOURCE_3']]
corr2 = external_data.corr()
plt.figure(figsize=(12, 10))
sns.heatmap(corr2[(corr2 >= 0.05) | (corr2 <= -0.04)], 
            cmap='viridis', vmax=1.0, vmin=-1.0, linewidths=0.1,
            annot=True, annot_kws={"size": 14}, square=True)

"""Notice that all exterior variables have negative correlations to our target variable So, it's more likely for people to repay the loans on time when the value of exterior variables increase!

### Plot 5 : Heatmap for the most positive correlations!
"""

#3 variables with the strongest positive correlations with the target
positive = df_train[['REGION_RATING_CLIENT', 'REGION_RATING_CLIENT_W_CITY', 'DAYS_EMPLOYED', 'TARGET']]
corr3 = positive.corr()
plt.figure(figsize=(12, 10))
sns.heatmap(corr3[(corr3 >= 0.00000005) | (corr3 <= -0.00000004)], 
            cmap='viridis', vmax=1.0, vmin=-1.0, linewidths=0.1,
            annot=True, annot_kws={"size": 14}, square=True)

"""Also see that 'REGION_RATING_CLIENT_W_CITY' and 'REGION_RATING_CLIENT' are having a strong correlation to each other, it means that our rating of the region is correlated with the cities where our clients live.

## More in Feature Engineering by creating new features!
"""

#New feature no.1 : The Amount of Credit / Total Income of Client
df_train['CREDIT_RELATIVE_W_INCOME'] = df_train['AMT_CREDIT'] / df_train['AMT_INCOME_TOTAL']
df_test['CREDIT_RELATIVE_W_INCOME'] = df_test['AMT_CREDIT'] / df_test['AMT_INCOME_TOTAL']

#New feature no.2 : The Amount of Annuity / Total Income of Client
df_train['ANNUITY_RELATIVE_W_INCOME'] = df_train['AMT_ANNUITY'] / df_train['AMT_INCOME_TOTAL']
df_test['ANNUITY_RELATIVE_W_INCOME'] = df_test['AMT_ANNUITY'] / df_test['AMT_INCOME_TOTAL']

#New feature no.3 : The Amount of Annuity / The Amount of Credit
df_train['LEN_PAYMENT'] = df_train['AMT_ANNUITY'] / df_train['AMT_CREDIT']
df_test['LEN_PAYMENT'] = df_test['AMT_ANNUITY'] / df_test['AMT_CREDIT']

#New feature no.4 : The Amount of Income / Count of Family Members
df_train['INCOME_PER_FAMILY'] = df_train['AMT_INCOME_TOTAL']/ df_train['CNT_FAM_MEMBERS']
df_test['INCOME_PER_FAMILY'] = df_test['AMT_INCOME_TOTAL'] / df_test['CNT_FAM_MEMBERS']

"""## Data Scaling!

We will use normalization since we don't know what kind of distribution our data has!

First, we fill the missing values
"""

#Split the data
X = df_train.drop('TARGET', axis = 1)
y = df_train['TARGET']
df_test_copy = df_test.copy()

#Imputing missing values with median!
from sklearn.impute import SimpleImputer
imp_mean = SimpleImputer(missing_values=np.nan, strategy='median')
imp_mean.fit(X)

X = imp_mean.transform(X)
df_test_copy = imp_mean.transform(df_test)

#Train test split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

"""Then, we will try and compare two different method of normalization; MinMax Scaler and StandardScaler"""

#StandardScaler normalization
from sklearn.preprocessing import StandardScaler
scaler_stan = StandardScaler()
scaler_stan.fit(X_train)

scaler_stan.transform(X_train)
scaler_stan.transform(X_test)

"""#Balancing

As we have imbalanced data, to make our model better in predicting the target label, we will use over-sampling by SMOTE
"""

from imblearn.over_sampling import SMOTE

oversample = SMOTE()
X_train, y_train = oversample.fit_resample(X_train, y_train)

"""#Modelling"""

#LGBM
import lightgbm as lgbm
lgbm_train = lgbm.Dataset(data=X,
                          label=y,
                          free_raw_data=False)
lgbm_params = {
    'boosting': 'dart',
    'application': 'binary',
    'learning_rate': 0.1,
    'min_data_in_leaf': 30,
    'num_leaves': 31,
    'max_depth': -1,
    'feature_fraction': 0.5,
    'scale_pos_weight': 2,
    'drop_rate': 0.02
}

cv_results = lgbm.cv(train_set=lgbm_train,
                     params=lgbm_params,
                     nfold=5,
                     num_boost_round=600,
                     early_stopping_rounds=50,
                     verbose_eval=20,
                     metrics=['auc'])

optimum_boost_rounds = np.argmax(cv_results['auc-mean'])
print('Optimum boost rounds = {}'.format(optimum_boost_rounds))
print('Best CV result = {}'.format(np.max(cv_results['auc-mean'])))

clf = lgbm.train(train_set=lgbm_train,
                 params=lgbm_params,
                 num_boost_round=optimum_boost_rounds)

y_test_pred = clf.predict(X_test)

"""## Model Interpretation: Feature Importances!"""

df_train.drop('TARGET', axis=1, inplace=True)

features = df_train.columns
importances = clf.feature_importance()
indices = np.argsort(importances)

# customized number 
num_features = 10 

plt.figure(figsize=(30,10))
plt.title('Feature Importances')

# only plot the customized number of features
plt.barh(range(num_features), importances[indices[-num_features:]], color='b', align='center')
plt.yticks(range(num_features), [features[i] for i in indices[-num_features:]])
plt.xlabel('Relative Importance')
plt.show()

test_id = df_test['SK_ID_CURR']
predict = clf.predict(df_test_copy)
submission_lgbm = pd.DataFrame({'SK_ID_CURR':test_id,'Target':predict})

#Visualize the first 5 rows
submission_lgbm.head()

# Save the submission dataframe
submission_lgbm.to_csv('/content/gdrive/My Drive/submisi_lgbm.csv', index = False)

"""#Model after feature selection"""

df_train2 = df_train[['LEN_PAYMENT','EXT_SOURCE_3', 'EXT_SOURCE_1', 'EXT_SOURCE_2', 'DAYS_BIRTH', 'DAYS_EMPLOYED', 'AMT_GOODS_PRICE', 'AMT_CREDIT', 'DAYS_ID_PUBLISH', 'AMT_ANNUITY']]

#LGBM
import lightgbm as lgbm
lgbm_train = lgbm.Dataset(data=df_train2,
                          label=y,
                          free_raw_data=False)
lgbm_params = {
    'boosting': 'dart',
    'application': 'binary',
    'learning_rate': 0.1,
    'min_data_in_leaf': 30,
    'num_leaves': 31,
    'max_depth': -1,
    'feature_fraction': 0.5,
    'scale_pos_weight': 2,
    'drop_rate': 0.02
}

cv_results = lgbm.cv(train_set=lgbm_train,
                     params=lgbm_params,
                     nfold=5,
                     num_boost_round=600,
                     early_stopping_rounds=50,
                     verbose_eval=20,
                     metrics=['auc'])

optimum_boost_rounds = np.argmax(cv_results['auc-mean'])
print('Optimum boost rounds = {}'.format(optimum_boost_rounds))
print('Best CV result = {}'.format(np.max(cv_results['auc-mean'])))

clf = lgbm.train(train_set=lgbm_train,
                 params=lgbm_params,
                 num_boost_round=optimum_boost_rounds)

y_test_pred = clf.predict(X_test)

test_id = df_test['SK_ID_CURR']
predict = clf.predict(df_test_copy)
submission_lgbm = pd.DataFrame({'SK_ID_CURR':test_id,'Target':predict})

#Visualize the first 5 rows
submission_lgbm.head()

# Save the submission dataframe
submission_lgbm.to_csv('/content/gdrive/My Drive/submisi(afterFS)_lgbm.csv', index = False)