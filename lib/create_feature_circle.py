import re
import json

def main():
    fin= open("voies_mel.geojson","r")
    fout= open("voies_mel_draw_circle.geojson","w+")

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
              "frequency": 0,
              "color" : '#f4eaac'
            }
          }

        newFeature["geometry"]["coordinates"] = feature["properties"]["geo_point_2d"][1], feature["properties"]["geo_point_2d"][0]
        
        frequency = 0
        color = '#f4eaac'
        if 'properties' in feature and 'trafic' in feature["properties"]:
          # 0   : VOIE NON CIRCULEE
          # 50  : DESSERTE  MJO INFERIEURE A  1.500 VEH/JOUR
          # 100  : DISTRIBUTION MJO  DE  1.500 A  6.000 VEH/JOUR
          # 200  : LIAISON  MJO  DE  6.000 A 13.000 VEH/JOUR
          # 400 : LIAISON  MJO  DE 13.000 A 30.000 VEH/JOUR
          # 800 : LIAISON  MJO SUPERIEURE A 30.000 VEH/JOUR

            x = feature["properties"]["trafic"]
            if ("30.000" in x):
              if ("13.000" in x):
                frequency = 400
                color = '#601300'
              else:
                frequency = 800
                color = '#381a06'
            elif ("6.000" in x):
              if ("13.000" in x):
                frequency = 200
                color = '#c53200'
              else:
                frequency = 100
                color = '#eea800'
            elif ("1.500" in x):
              frequency = 50
        
        newFeature["properties"]["frequency"] = frequency
        newFeature["properties"]["color"] = color

        dataout["features"].append(newFeature)

    fout.write(json.dumps(dataout))
    fin.close()
    fout.close()

if __name__== "__main__":
  main()
