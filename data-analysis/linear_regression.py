import math
import numpy as np
import pandas as pd
from sklearn import gaussian_process
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, DotProduct
import scipy.stats as stats
from sklearn.model_selection import train_test_split
from data_analysis import getError, calculateErrorFromMin
import random

approaches_df = getError()

approaches_df.reset_index(drop=True, inplace=True)

train_errors, test_errors = train_test_split(approaches_df['error'], test_size=0.2)


def IsolationForestRegression():

    # approaches_df['timeOfPrediction'] = pd.to_datetime(approaches_df['timeOfPrediction'])

    model = IsolationForest(n_estimators=100, max_samples='auto', contamination=float(0.04), max_features=1.0)

    model.fit((approaches_df[['error']]).to_numpy())

    approaches_df['anomaly'] = model.predict((approaches_df[['error']]).to_numpy())

    # approaches_df['outliers'] = pd.Series(model.predict(approaches_df[['timeToStation']])).apply(lambda x: 'yes' if (x == -1) else 'no')

    # print(approaches_df.loc[approaches_df['anomaly'] == 1])

    for approach in approaches_df.iterrows():
        if approach[1]['anomaly'] == 1:
            plt.scatter(approach[1]['timeToStation'], approach[1]['error'], c='#1f77b4')
        else:
            plt.scatter(approach[1]['timeToStation'], approach[1]['error'], c='#ff0000')

    plt.gca().invert_xaxis()
    plt.show()

# IsolationForestRegression()

def NormalDistribution():

    mean = train_errors.mean()

    variance = train_errors.var()

    sigma = math.sqrt(variance)

    x = np.linspace(mean - 3*sigma, mean + 3*sigma, 100)

    plt.plot(x, stats.norm.pdf(x, mean, sigma))

    plt.show()

# NormalDistribution()

def generateBaselineConfidence():
    mean_train = train_errors.mean()

    variance_train = train_errors.var()

    sigma_train = math.sqrt(variance_train)

    confidence_95 = (mean_train - 2*sigma_train, mean_train + 2*sigma_train)

    return confidence_95
    

def getMetric():
    interval = generateBaselineConfidence()

    tries = len(test_errors)

    successes = 0

    for error in test_errors:
        if interval[0] <= error <= interval[1]:
            successes += 1

    print(successes / tries)

getMetric()

def GaussianProcess():

    randIndexList = random.sample(range(approaches_df.shape[0]), 50)

    X, X_train = approaches_df['timeToStation'].to_numpy().reshape(-1, 1), approaches_df['timeToStation'].to_numpy().reshape(-1, 1)

    # X_train = approaches_df.iloc[randIndexList]['timeToStation'].to_numpy().reshape(-1, 1)

    y, y_train = approaches_df['error'].to_numpy().reshape(-1, 1), approaches_df['error'].to_numpy().reshape(-1, 1)

    # y_train = approaches_df.iloc[randIndexList]['error'].to_numpy().reshape(-1, 1)

    kernel = 1 * RBF(length_scale=1.0, length_scale_bounds=(1e-2, 1e2))

    # kernel = DotProduct()

    gaussian_process = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=9)

    gaussian_process.fit(X_train, y_train)

    gaussian_process.kernel_

    mean_prediction, std_prediction = gaussian_process.predict(X, return_std=True)

    plt.plot(X, y, label=r"$f(x) = x \sin(x)$", linestyle="dotted")
    plt.scatter(X_train, y_train, label="Observations")
    plt.plot(X, mean_prediction, label="Mean prediction")
    plt.fill_between(
    X.ravel(),
    mean_prediction - 1.96 * std_prediction,
    mean_prediction + 1.96 * std_prediction,
    alpha=0.5,
    label=r"95% confidence interval",
)
    plt.legend()
    plt.xlabel("$x$")
    plt.ylabel("$f(x)$")
    _ = plt.title("Gaussian process regression on noise-free dataset")

    plt.show()

# GaussianProcess()