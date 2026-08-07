import sys
import pandas as pd

def main(in_directory):
    data = pd.read_csv(in_directory)
    
    assert not data.empty, "Data is empty."
    assert len(data) > 30, "Not enough data points for a valid statistical analysis."

    print(data)


if __name__=='__main__':
    in_directory = sys.argv[1]
    main(in_directory)

