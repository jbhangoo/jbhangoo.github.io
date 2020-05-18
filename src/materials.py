# -*- coding: utf-8 -*-
"""
Apply techniques of Machine Learning course to sample data
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, RANSACRegressor
from sklearn.metrics import mean_squared_error, r2_score

SUPERCONDUCTOR_COLUMNS = ['number_of_elements', 'mean_atomic_mass', 'wtd_mean_atomic_mass', 'gmean_atomic_mass',
                          'wtd_gmean_atomic_mass', 'entropy_atomic_mass', 'wtd_entropy_atomic_mass', 'range_atomic_mass',
                          'wtd_range_atomic_mass', 'std_atomic_mass', 'wtd_std_atomic_mass', 'mean_fie', 'wtd_mean_fie',
                          'gmean_fie', 'wtd_gmean_fie', 'entropy_fie', 'wtd_entropy_fie', 'range_fie', 'wtd_range_fie',
                          'std_fie', 'wtd_std_fie', 'mean_atomic_radius', 'wtd_mean_atomic_radius', 'gmean_atomic_radius',
                          'wtd_gmean_atomic_radius', 'entropy_atomic_radius', 'wtd_entropy_atomic_radius',
                          'range_atomic_radius', 'wtd_range_atomic_radius', 'std_atomic_radius', 'wtd_std_atomic_radius',
                          'mean_Density', 'wtd_mean_Density', 'gmean_Density', 'wtd_gmean_Density', 'entropy_Density',
                          'wtd_entropy_Density', 'range_Density', 'wtd_range_Density', 'std_Density', 'wtd_std_Density',
                          'mean_ElectronAffinity', 'wtd_mean_ElectronAffinity', 'gmean_ElectronAffinity',
                          'wtd_gmean_ElectronAffinity', 'entropy_ElectronAffinity', 'wtd_entropy_ElectronAffinity',
                          'range_ElectronAffinity', 'wtd_range_ElectronAffinity', 'std_ElectronAffinity',
                          'wtd_std_ElectronAffinity', 'mean_FusionHeat', 'wtd_mean_FusionHeat', 'gmean_FusionHeat',
                          'wtd_gmean_FusionHeat', 'entropy_FusionHeat', 'wtd_entropy_FusionHeat', 'range_FusionHeat',
                          'wtd_range_FusionHeat', 'std_FusionHeat', 'wtd_std_FusionHeat', 'mean_ThermalConductivity',
                          'wtd_mean_ThermalConductivity', 'gmean_ThermalConductivity', 'wtd_gmean_ThermalConductivity',
                          'entropy_ThermalConductivity', 'wtd_entropy_ThermalConductivity', 'range_ThermalConductivity',
                          'wtd_range_ThermalConductivity', 'std_ThermalConductivity', 'wtd_std_ThermalConductivity',
                          'mean_Valence', 'wtd_mean_Valence', 'gmean_Valence', 'wtd_gmean_Valence', 'entropy_Valence',
                          'wtd_entropy_Valence', 'range_Valence', 'wtd_range_Valence', 'std_Valence', 'wtd_std_Valence',
                          'critical_temp']


df_super = pd.read_csv("superconductor.csv")

# Quick view to verify we have the right file and reasonable data
print (df_super.head())
df_super.describe()

# Look at distributions of each attribute
fig, axs = plt.subplots(ncols=17, nrows=5, figsize=(20, 10))
index = 0
axs = axs.flatten()
for k,v in df_super.items():
    sns.boxplot(y=k, data=df_super, ax=axs[index])
    index += 1
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=5.0)
plt.show()

'''
Several features appear to be well distributed without outliers. Include target attribute 'critical_temp'
Double check by generating boxplots for those features
Re-arrange the feature list to put similar sounding column names together, to make them easier to follow
'''

unskewed_indexes = [6, 7, 9, 12, 17, 18, 19, 20, 26, 27, 29, 30, 56, 65, 67, 69, 70, 76, 77, ]
unskewed_columns = ['wtd_mean_fie', 'range_fie', 'wtd_range_fie', 'std_fie', 'wtd_std_fie', 'wtd_gmean_atomic_mass',
                    'range_atomic_mass', 'range_atomic_radius', 'std_atomic_mass',  'wtd_entropy_atomic_mass',
                    'wtd_entropy_atomic_radius', 'std_atomic_radius', 'wtd_std_atomic_radius', 'wtd_entropy_Density',
                    'wtd_entropy_FusionHeat', 'entropy_ThermalConductivity', 'range_ThermalConductivity', 'std_ThermalConductivity',
                    'wtd_std_ThermalConductivity', 'wtd_entropy_Valence', 'range_Valence', 'mean_Valence', 'critical_temp', ]
fig, axs = plt.subplots(ncols=5, nrows=4, figsize=(10, 10))
index = 0
plotpos = 0
axs = axs.flatten()
for k,v in df_super.items():
    if index in unskewed_indexes:
        sns.boxplot(y=k, data=df_super, ax=axs[plotpos])
        plotpos += 1
    index += 1
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=5.0)
plt.show()

'''
Correlation Analysis and Feature Selection of attributes and selected subset
'''

# Heat map: Thresholded and centered on 0 as the lighest shade in the color map. Makes strong correlations stand out
independent_columns = [ 'wtd_entropy_atomic_mass',
                          'wtd_range_atomic_mass',  'wtd_std_atomic_mass',
                          'wtd_entropy_fie', 'wtd_range_fie',
                          'wtd_std_fie','wtd_mean_atomic_radius',
                           'wtd_mean_Density',
                           'wtd_mean_ElectronAffinity', 'wtd_mean_FusionHeat',
                          'wtd_range_ThermalConductivity',
                          'critical_temp']

corr_matrix = df_super[independent_columns].corr()
corr_matrix[np.abs(corr_matrix) < 0.7] = 0
highlist_extremes = {}
plt.figure(figsize=(12,8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, fmt=".2f")
plt.show()

"""
Visualize possible dependency of target column of selected attributes
"""

sns.pairplot(df_super[independent_columns], height=2.5, aspect=1);
plt.show()

'''
Pairplots showed some feature dependency that did not come out of the correlation matrix heat map.
Reduce the feature set a little more
'''

# Isolate one feature to test it alone
X = df_super['wtd_entropy_Density'].values.reshape(-1,1)
y = df_super['critical_temp'].values

lr = LinearRegression()
lr.fit(X, y)
y_pred = lr.predict(X)

# Metric: r^2
print (r2_score(y, y_pred))

'''
Low fitness means it should not be included
'''

regression_columns = [ 'wtd_entropy_atomic_mass',
                          'wtd_range_atomic_mass',  'wtd_std_atomic_mass',
                          'wtd_range_fie',
                          'wtd_std_fie','wtd_mean_atomic_radius',
                           'wtd_mean_Density',
                           'wtd_mean_FusionHeat',
                          'wtd_range_ThermalConductivity',
                          'critical_temp']

'''
 Split data into training and test sets, then evaluate linear regression model
'''
X = df_super.iloc[:, :-1].values
y = df_super['critical_temp'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

#
# 1. Use full feature set
#

lr = LinearRegression()
lr.fit(X_train, y_train)
y_train_pred = lr.predict(X_train)
y_test_pred = lr.predict(X_test)

# Metric: Mean Squared Error (MSE)

print (mean_squared_error(y_train, y_train_pred))
print (mean_squared_error(y_test, y_test_pred))

# Metric: Coefficient of Determination, $R^2$

print (r2_score(y_train, y_train_pred))
print (r2_score(y_test, y_test_pred))

#
# 2. Try with reduced set of independent_columns
#

X = df_super[regression_columns]
y = df_super['critical_temp'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

lr = LinearRegression()
lr.fit(X_train, y_train)
y_train_pred = lr.predict(X_train)
y_test_pred = lr.predict(X_test)

# Metric: Mean Squared Error (MSE)

print (mean_squared_error(y_train, y_train_pred))
print (mean_squared_error(y_test, y_test_pred))

# Metric: Coefficient of Determination, $R^2$"

print (r2_score(y_train, y_train_pred))
print (r2_score(y_test, y_test_pred))
