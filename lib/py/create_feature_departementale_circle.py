import re
import json

def main():
    fin= open("../data_origin/comptages-routiers-sur-la-voirie-departementale.geojson","r")
    fout= open("../data_trans/comptages-routiers-sur-la-voirie-departementale_circle.geojson","w+")

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
        if 'properties' in feature and 'tmja_aa' in feature["properties"]:
          # <2000
          # 2000 - 17900
          # 17900 - 33900
          # 33900 - 49900
          # 49900 - 65900
          # > 65900

            x = int(((feature["properties"]["tmja_aa"]).split('(')[0]).split(' ')[0])
            if (x > 65900):
              frequency = 800
              color = '#381a06'
            elif (x > 49900):
              frequency = 400
              color = '#601300'               
            elif (x>33900):
              frequency = 200
              color = '#c53200'
            elif (x>17900):
              frequency = 100
              color = '#eea800'
            elif (x>2000):
              frequency = 50
        
        newFeature["properties"]["frequency"] = frequency
        newFeature["properties"]["color"] = color

        dataout["features"].append(newFeature)

    fout.write(json.dumps(dataout))
    fin.close()
    fout.close()

if __name__== "__main__":
  main()
