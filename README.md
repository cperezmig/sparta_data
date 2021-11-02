Detecting outliers
==================

This repo holds the code for an implementation that solves [Sparta Data Exercise](https://github.com/SpartaCommodities/data_test).

Index:
------

1. [Installation](#installation)
2. [Usage](#usage)
3. [Answers to the test](#test)
4. [Discussion](#discussion)

### 1. Installation:<a name="installation"></a>
```
$ virtualenv -p python3.8 .env
$ source .env/bin/activate
$ pip install -r requirements.txt
```

### 2. Usage:<a name="usage"></a>
The script is able to plot and remove outliers from a CSV file.
The default method is "plot", to show detected outliers.
In case "remove", method used, an output file is required.

The script takes several parameters to control it. A common use to plot outliers will be:
```
python ./outliers.py -c RBOB_data_test.csv
```

By default the 'zscore' method is used. In case we want to try the 'quantile' method:
```
python ./outliers.py -c RBOB_data_test.csv -M quantile
```

If we want to remove them and store the result in a new file:
```
python ./outliers.py -c RBOB_data_test.csv -m remove -o output.csv
```

In case of doubts, there is some help at hand:
```
Usage: outliers.py [options]

Options:
  -h, --help            show this help message and exit
  -c CSV, --csv=CSV     Specifies the csv file.
  -m MODE, --mode=MODE  Specifies the mode ('plot', 'remove'). Default plot.
  -o OUT, --output=OUT  Specifies the output file.
  -r, --refine          Specifies if must refine the search. Default False
  -M METHOD, --method=METHOD
                        Specifies the method  to search outliers ('zscore',
                        'quantile'). Default 'zscore'.
  -C COL, --column=COL  Specifies the column to clean. Default 'dlvd_price'.
  -w W, --window=W      Specifies the window size to use with zscore method.
                        Default 24.
  -z Z, --zscore=Z      Specifies the maximum allowed zscore to use with
                        zscore method. Default 3.0.
  -q Q, --quantile=Q    Specifies the quantile useed with quantile method.
                        Default 0.005.
```

### 3. Answers to the test:<a name="test"></a>

Regarding the questions defined in the test:

1. Create a script that can read the data sequentially, and solve any format problems that could appear.
- I have developed a program composed of 3 python files, the main of which is in outliers.py. Function loadData
from the utils.py file has the code required to load the data and fix some format problems detected, specially in the date format.
This function will return a pandas dataframe ordered by the 'generated_on' column.

2. Plot the data to find the outliers.
- In order to plot the data, the function 'plot' in utils.py has been developed. It uses the matplotlib
library and uses subplots in order to plot each of the 'load_month' series presented in the file
as a separate line in the same plot.

3. Iterate the read script to detect the outliers and save the data cleaned in a separated csv.
- The function getOutliers in computeOutliers.py is able to detect the outliers using two different techniques.
Each of this technique has been developed as a separate function in the same file. Also, a refinement
function has been proposed. In order to clean and save the data as a separated csv, ordinary pandas code
has been used. This can be found in lines 35 and 36 of outliers.py.

### 4. Discussion:<a name="discussion"></a>
As can be seen, there are two detecting methods implemented: quantile (or Winsorization) and zscore.

1. The 'quantile' method will remove everything that is outside the quantile range
  [q, 1-q], where q is 0.005 by default.

2. The 'zscore' method will obtain the zscores for each value. If a certain value
  exceeds a certain zscore threshold, usually 2 or 3, it is considered a
  outlier. A zscore is a metric obtained by removing to a value its mean and
  dividing by its standard deviation.  To improve the method, the mean and std
  are obtained from a sliding exponentially weighed window.

While it seems that the quantile method
is easier to configure and better detecting outliers, it is clear that the data is not stationary,
so removing by a fixed value would only be valid for a short period. This threshold should be recalculated often
or search for a method that takes into account non-stationary series.

The zscore method seems to found more false positives and is more difficult to configure, but I think as
this zscore is calculated using an exponential moving window, it is more robust against non-stationary
data.

Finally, a refinement method to avoid false positives is proposed in function refine of computeOutliers. This method takes into
consideration the great correlation that exists between the different 'load_data' series. If all
the series has the same spike in the same timestamp, I think this should not be considered as an
outlier. This process is not activated by default and should be adapted to the business logic behind each CSV.
