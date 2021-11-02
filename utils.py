import sys
import pandas as pd
import matplotlib.pyplot as plt
from optparse import OptionParser

def plot(df, outliers=None):
    """
    Plot each load_month as a different series.
    If an outliers dataframe is included, plot those as green points
    """
    fig, ax = plt.subplots(figsize=(10,6))
    for m in df['load_month'].unique():
        ax.plot(df[df.load_month==m].index, df[df.load_month==m]["dlvd_price"], label=m)

    if outliers is not None:
        ax.scatter(outliers.index, outliers['dlvd_price'], color='green', s=100, alpha=0.5, label='Anomaly')

    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Delivery price")
    ax.legend(loc='best')
    plt.show()

def loadData(path):
    """
    Loading CSV with pandas. As the generated_on column may have different formats, we
    let pandas guess them by using 'to_datetime'. Also, in case of duplicates
    are found, we keep only the last value. In case NA values are found in the
    'dlvd_price' column, we discard that row.
    """
    assert(len(path) > 0)
    df = pd.read_csv(path)
    df['generated_on'] = pd.to_datetime(df['generated_on'])
    df.drop_duplicates(subset=['generated_on', 'load_month'], keep='last')
    df.dropna(subset=['dlvd_price'])
    df = df.set_index('generated_on')
    df.sort_index(inplace=True)
    return df

def parseArgs():
    """
    In charge of building and parsing the different command line options
    """
    parser = OptionParser()
    parser.add_option("-c", "--csv", dest="csv", type="string",
                      help="Specifies the csv file.")
    parser.add_option("-m", "--mode", dest="mode", type="string",
                      help="Specifies the mode ('plot', 'remove'). Default plot.",
                      default='plot')
    parser.add_option("-o", "--output", dest="out", type="string",
                      help="Specifies the output file.")
    parser.add_option("-r", "--refine", dest="refine", action="store_true",
                      help="Specifies if must refine the search. Default False",
                      default=False)
    parser.add_option("-M", "--method", dest="method", type="string",
                      help="Specifies the method  to search outliers ('zscore', 'quantile'). Default 'zscore'.",
                      default='zscore')
    parser.add_option("-C", "--column", dest="col", type="string",
                      help="Specifies the column to clean. Default 'dlvd_price'.",
                      default='dlvd_price')
    parser.add_option("-w", "--window", dest="w", type="int",
                      help="Specifies the window size to use with zscore method. Default 24.",
                      default=24)
    parser.add_option("-z", "--zscore", dest="z", type="float",
                      help="Specifies the maximum allowed zscore to use with zscore method. Default 3.0.",
                      default=3.0)
    parser.add_option("-q", "--quantile", dest="q", type="float",
                      help="Specifies the quantile useed with quantile method. Default 0.005.",
                      default=0.005)

    (options, args) = parser.parse_args()

    if len(sys.argv[1:]) < 1:
        parser.error('Incorrect number of parameters')
    if not options.csv:
        parser.error('CSV file not specified')
    if options.mode == 'remove' and not options.out:
        parser.error('Remove mode but no output file specified')

    return options
