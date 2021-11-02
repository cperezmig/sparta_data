import sys
from utils import plot, loadData, parseArgs
from computeOutliers import getOutliers, refine

"""
Outliers detection and removing.
"""

def main(argv=None):
    options = parseArgs()
    path = options.csv
    method = options.method
    col = options.col
    w = options.w
    z = options.z
    cutoff = options.q
    mode = options.mode
    refine = options.refine
    outfile = options.out

    df = loadData(path)
    if len(df) == 0:
        print(f"No data in the file {path}")
        return

    df = getOutliers(df, method=method, col=col, w=w, z=z, cutoff=cutoff)

    if refine:
        df = refine(df)

    if mode == 'plot':
        outliers = df.loc[df['outliers'] == 1, ['dlvd_price']]
        plot(df, outliers)
    elif mode == 'remove':
        df = df.loc[df['outliers'] == 0]
        df.to_csv(outfile, index=True, na_rep='NULL')


if __name__ == "__main__":
    sys.exit(main())
