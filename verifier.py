import requests
import pandas
from io import StringIO
import sys

def main(argv):
    if len(argv) < 1:
        print("error: missing sheet name")
        return
    if len(argv) < 2:
        print("error: missing first name")
        return
    if len(argv) < 3:
        print("error: missing last name")
        return

    if len(argv) > 3:
        print(f"error: too many arguments (expected 3, got {len(argv)})")
        return

    sheet_name = argv[0]
    url = f"https://docs.google.com/spreadsheets/d/1cJtg4aYy_A7DhR37tjOklZyxTnivPPdF/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    res = requests.get(url)
    if res.status_code != 200:
        print("error: could not download the spreadsheet")
        return

    df = pandas.read_csv(StringIO(res.text))
    if "Lp." not in df:
        print("error: missing \"Lp.\" column")
        return
    if "Kandydat" not in df:
        print("error: missing \"Kandydat\" column")
        return

    df = df[["Lp.", "Kandydat"]]
    in_first = argv[1]
    in_last = argv[2]
    for _, (index, name) in df.iterrows():
        first, last = name.split(" ")
        if "*" not in first and "*" not in last:
            continue
        if first[0] == in_first[0] and last[0] == in_last[0] and len(first) == len(in_first) and len(last) == len(in_last):
            print(f"Found {in_first} {in_last} at {index}")
            return

    print("Not Found")

main(sys.argv[1:])
