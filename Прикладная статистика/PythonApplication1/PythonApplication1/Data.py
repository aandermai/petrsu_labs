import pandas as pd
import numpy as np
import seaborn as sns
from scipy.stats import spearmanr, kendalltau, chi2_contingency, pearsonr
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures, OneHotEncoder
from sklearn.impute import SimpleImputer
from statsmodels.formula.api import ols
import matplotlib.pyplot as plt
import statsmodels.api as sm

# Load the data
data = pd.read_excel('Book1.xlsx')


data['RankVariable'] = data['Position'].rank(method='dense')

numeric_data = data.iloc[:, :6]

# Calculate the correlation matrix
correlation_matrix = numeric_data.corr()
print(correlation_matrix)

# Plot the heatmap of the correlation matrix
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

# Scatter plots for pairs with significant correlation
alpha = 0.05
significant_pairs = []

for i in range(len(correlation_matrix.columns)):
    for j in range(i+1, len(correlation_matrix.columns)):
        corr_value = correlation_matrix.iloc[i, j]
        if abs(corr_value) > alpha:
            significant_pairs.append((correlation_matrix.columns[i], correlation_matrix.columns[j]))
            sns.scatterplot(data=data, x=correlation_matrix.columns[i], y=correlation_matrix.columns[j])
            plt.title(f'Scatter plot between {correlation_matrix.columns[i]} and {correlation_matrix.columns[j]}')
            plt.show()

# Find the pair with the highest Pearson correlation coefficient
max_corr_pair = correlation_matrix.abs().unstack().idxmax()
x, y = max_corr_pair

# Spearman and Kendall correlation
spearman_corr, spearman_p = spearmanr(data[x], data[y])
kendall_corr, kendall_p = kendalltau(data[x], data[y])

# Chi-square test
contingency_table = pd.crosstab(data[x], data[y])
chi2, chi2_p, _, _ = chi2_contingency(contingency_table)

print(f'Spearman correlation between {x} and {y}: {spearman_corr}, p-value: {spearman_p}')
print(f'Kendall correlation between {x} and {y}: {kendall_corr}, p-value: {kendall_p}')
print(f'Chi-square test between {x} and {y}: chi2: {chi2}, p-value: {chi2_p}')

# Ensure the required columns exist
required_columns = ['X1', 'X2', 'X3', 'X4', 'X5', 'Y']
missing_columns = [col for col in required_columns if col not in data.columns]
if missing_columns:
    raise ValueError(f"Missing required columns: {missing_columns}")

# Linear regression
X = data[['X1', 'X2', 'X3', 'X4', 'X5']]
Y = data['Y']

# Impute missing values
imputer = SimpleImputer(strategy='mean')
X = imputer.fit_transform(X)

linear_regressor = LinearRegression()
linear_regressor.fit(X, Y)
Y_pred = linear_regressor.predict(X)

print(f'Linear Regression Coefficients: {linear_regressor.coef_}')
print(f'Linear Regression Intercept: {linear_regressor.intercept_}')
print(f'Mean Squared Error: {mean_squared_error(Y, Y_pred)}')
print(f'R^2 Score: {r2_score(Y, Y_pred)}')

# Polynomial regression (degree 2)
poly_features = PolynomialFeatures(degree=2)
X_poly = poly_features.fit_transform(X)

poly_regressor = LinearRegression()
poly_regressor.fit(X_poly, Y)
Y_poly_pred = poly_regressor.predict(X_poly)

print(f'Polynomial Regression Coefficients: {poly_regressor.coef_}')
print(f'Polynomial Regression Intercept: {poly_regressor.intercept_}')
print(f'Mean Squared Error: {mean_squared_error(Y, Y_poly_pred)}')
print(f'R^2 Score: {r2_score(Y, Y_poly_pred)}')

# Plotting the regression results
plt.scatter(Y, Y_pred, color='blue', label='Linear Regression')
plt.scatter(Y, Y_poly_pred, color='red', label='Polynomial Regression')
plt.xlabel('Actual Y')
plt.ylabel('Predicted Y')
plt.legend()
plt.title('Regression Analysis')
plt.show()

# Ensure the required columns for ANOVA exist
required_columns_anova = ['Region', 'RankVariable', 'Y']
missing_columns_anova = [col for col in required_columns_anova if col not in data.columns]
if (missing_columns_anova):
    raise ValueError(f"Missing required columns for ANOVA: {missing_columns_anova}")

# One-way ANOVA for factor A (Region)
model_a = ols('Y ~ C(Position)', data=data).fit()
anova_table_a = sm.stats.anova_lm(model_a, typ=2)
print("One-way ANOVA for factor A (Position):")
print(anova_table_a)

# Two-way ANOVA for factors A (Region) and B (RankVariable) without interaction
model_ab_no_interaction = ols('Y ~ C(Position) + C(RankVariable)', data=data).fit()
anova_table_ab_no_interaction = sm.stats.anova_lm(model_ab_no_interaction, typ=2)
print("Two-way ANOVA for factors A (Position) and B (RankVariable) without interaction:")
print(anova_table_ab_no_interaction)

# Two-way ANOVA for factors A (Region) and B (RankVariable) with interaction
model_ab_interaction = ols('Y ~ C(Position) * C(RankVariable)', data=data).fit()
anova_table_ab_interaction = sm.stats.anova_lm(model_ab_interaction, typ=2)
print("Two-way ANOVA for factors A (Position) and B (RankVariable) with interaction:")
print(anova_table_ab_interaction)

# Model summary
print("Model summary for two-way ANOVA with interaction:")
print(model_ab_interaction.summary())
