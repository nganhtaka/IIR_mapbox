import re
import json

def main():
    fin= open("../data_origin/voies_mel.geojson","r")

    oneline = fin.read()
    datain = json.loads(oneline)

    dataout = []

    for feature in datain["features"] :
        if 'properties' in feature and 'trafic' in feature["properties"]:
            x = feature["properties"]["trafic"]
            if (x not in dataout):
                dataout.append(x)
                print(x)

    fin.close()

if __name__== "__main__":
  main()
