import pandas as pd
import env

if __name__ == "__main__":
    df = pd.read_csv("result.csv", encoding=env.DEFAULT_ENCODING, index_col=0)

    for i in range(len(df)):
        try:
            df.iloc[i, 0] = df.iloc[i, 0].split("/")[0][2:]
        except Exception as e:
            continue
    
    df.to_csv("./result_parse.csv", encoding=env.DEFAULT_ENCODING)