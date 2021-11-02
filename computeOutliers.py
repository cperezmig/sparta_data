import pandas as pd
import numpy as np

def getOutliersByZScore(mdf, col='dlvd_price', w=24, z=3):
    """
    An outlier will be that point outside 'z' zscores from a exponentially weighed mean
    """
    df = mdf.copy()

    # Reindex to calculate mean and std for each load_month
    df = df.reset_index().set_index(['generated_on', 'load_month'])
    df.sort_index(inplace=True)

    # unstack load month to have one 'col' column per load_month
    unstacked = df.unstack('load_month')[col]
    # Exponential rolling window
    rolling = unstacked.ewm(span=w)

    # restacking load_month to have the same layout as df
    mu = rolling.mean().stack('load_month')
    mu.sort_index(inplace=True)
    sigma = rolling.std().stack('load_month')
    sigma.sort_index(inplace=True)
    df['mu'] = mu
    df['sigma'] = sigma

    cond = (df[col] > df['mu'] + df['sigma'] * z) | (df[col] < df['mu'] - df['sigma'] * z)
    df['outliers'] = np.where(cond, 1, 0)

    df = df.reset_index().set_index('generated_on')
    df.sort_index(inplace=True)
    df.drop(['mu', 'sigma'], axis=1, inplace=True)

    return df

def getOutliersByQuantile(mdf, col='dlvd_price', cutoff=0.001):
    """
    An outlier will be that point outside the 'cutoff' quantiles.
    """
    df = mdf.copy()

    # Obtain of upper limit
    upper = df.groupby('load_month')['dlvd_price'].quantile(1-cutoff)
    upper = pd.DataFrame(upper).rename(columns={'dlvd_price': 'upper'})
    df = df.join(upper, on='load_month')

    # Obtain of lower limit
    lower = df.groupby('load_month')['dlvd_price'].quantile(cutoff)
    lower = pd.DataFrame(lower).rename(columns={'dlvd_price': 'lower'})
    df = df.join(lower, on='load_month')

    df['outliers'] = np.where((df['dlvd_price'] > df['upper']) | (df['dlvd_price'] < df['lower']), 1, 0)
    df.drop(['upper', 'lower'], axis=1, inplace=True)

    return df

def getOutliers(df, method='zscore', col='dlvd_price', w=24, z=3, cutoff=0.005):
    if method == 'zscore':
        return getOutliersByZScore(df, col, w, z)
    else:
        return getOutliersByQuantile(df, col, cutoff)

def refine(mdf):
    """
    This method counts the number of outliers for a certain timestamp.
    If there are more than 1 outlier per timestamp, it is not an outlier.
    """
    df = mdf.copy()
    suma = df.groupby(level='generated_on')['outliers'].sum()
    outliers = (suma == 1)
    outliers = pd.DataFrame(outliers, columns=['outliers'])
    df['mul_outliers'] = outliers.astype(int)
    df['outliers'] = np.where((df['outliers'] == 1) & (df['mul_outliers'] == 1), 1, 0)
    df.drop(['mul_outliers'], axis=1, inplace=True)
    return df
