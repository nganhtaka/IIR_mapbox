import re
import json

def main():
    fin= open("../data_origin/comptages-routiers-sur-la-voirie-departementale.geojson","r")

    oneline = fin.read()
    datain = json.loads(oneline)

    dataout = []
    rmin = 6629
    rmax = 9761
    for feature in datain["features"] :
        if 'properties' in feature and 'tmja_aa' in feature["properties"]:
            x = feature["properties"]["tmja_aa"]
            if (x not in dataout):
                dataout.append(x)
                #print(x)
                y = (x.split('(')[0]).split(' ')[0]
                if int(y)<rmin :
                    rmin=int(y)
                if int(y)>rmax:
                    rmax=int(y)

    print(rmin)
    print(rmax)
    fin.close()

if __name__== "__main__":
  main()
