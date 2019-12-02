import re
import json

def main():
    fin= open("voies_mel.geojson","r")
    fout= open("voies_mel_draw.geojson","w+")

    oneline = fin.read()
    datain = json.loads(oneline)

    dataout = {
       "type":"FeatureCollection",
       "features":[]
    }

    for feature in datain["features"] :
        newFeature = {
            "type": "Feature",
            "geometry": {
              "type": "Point",
              "coordinates": []
            },
            "properties": {
              "frequency": 0
            }
          }

        newFeature["geometry"]["coordinates"] = feature["properties"]["geo_point_2d"][1], feature["properties"]["geo_point_2d"][0]
        
        frequency = 0
        if 'properties' in feature and 'trafic' in feature["properties"]:
          # 0   : VOIE NON CIRCULEE
          # 30  : DESSERTE  MJO INFERIEURE A  1.500 VEH/JOUR
          # 60  : DISTRIBUTION MJO  DE  1.500 A  6.000 VEH/JOUR
          # 90  : LIAISON  MJO  DE  6.000 A 13.000 VEH/JOUR
          # 120 : LIAISON  MJO  DE 13.000 A 30.000 VEH/JOUR
          # 150 : LIAISON  MJO SUPERIEURE A 30.000 VEH/JOUR

            x = feature["properties"]["trafic"]
            if ("30.000" in x):
              if ("13.000" in x):
                frequency = 120
              else:
                frequency = 150
            elif ("6.000" in x):
              if ("13.000" in x):
                frequency = 90
              else:
                frequency = 60
            elif ("1.500" in x):
              frequency = 30
        
        newFeature["properties"]["frequency"] = frequency

        dataout["features"].append(newFeature)

    fout.write(json.dumps(dataout))
    fin.close()
    fout.close()

if __name__== "__main__":
  main()
