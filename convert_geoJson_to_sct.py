import json
from settings import SECTOR_COLORS

def decdeg2dms(dd):
   is_positive = dd >= 0
   dd = abs(dd)
   minutes,seconds = divmod(dd*3600,60)
   degrees,minutes = divmod(minutes,60)
   degrees = degrees if is_positive else -degrees
   return (degrees,minutes,seconds)

def geoJSON_to_sct(filepath):
    with open(filepath, 'r') as file:
        data = json.loads(file.read())
    
    def convert_LON(c):
        if c < 0:
            degrees, minutes, seconds = decdeg2dms(c)
            if degrees < 10:
                return "W00{0:.0f}.{1:.0f}.{2:.3f}".format((degrees*-1), minutes, seconds)
            else:
                return "W0{0:.0f}.{1:.0f}.{2:.3f}".format((degrees*-1), minutes, seconds)
        else:
            degrees, minutes, seconds = decdeg2dms(c)
            return "E{0:.0f}.{1:.0f}.{2:.3f}".format(degrees, minutes, seconds)

    def convert_LAT(c):
        if c < 0:
            degrees, minutes, seconds = decdeg2dms(c)
            return "S{0:.0f}.{1:.0f}.{2:.3f}".format(degrees, minutes, seconds)
        else:
            degrees, minutes, seconds = decdeg2dms(c)
            return "N0{0:.0f}.{1:.0f}.{2:.3f}".format(degrees, minutes, seconds)

    def convert_regions():
        output = list()
        output.append("------------------------------")
        output.append("------------REGIONS-----------")
        output.append("------------------------------")
        for item in data["features"]:
            for color in SECTOR_COLORS:
                if color in item["properties"]["name"] and color != "Taxiway_" and color != "Stand_":
                    output.append("{0}".format(SECTOR_COLORS[color]))
                    output.append("; - {0}".format(item["properties"]["name"]))
            t = 0
            if item["properties"]["name"] != "Taxiway_" and item["properties"]["name"] != "Stand_":
                for geo in item["geometry"]["coordinates"]:
                    parse = [x for x in geo]          
                    for i in parse:
                        if type(i) == list:                      
                            i.pop(2)
                            t = 0
                            for c in i[:2]:
                                if t == 0:
                                    i[t] = convert_LON(c)
                                if t == 1:
                                    i[t] = convert_LAT(c)
                                t+=1
                            output.append(str(i[::-1]).replace('[', '').replace(']', '').replace(',', '').replace("'", ""))
        return output

    def convert_taxiways_and_stands():
        output = list()
        
        output.append("------------------------------")
        output.append("--------TAXYWAYS&STANDS-------")
        output.append("------------------------------")
        for item in data["features"]:
            
            #if (item["properties"]["name"] == "Taxiway_W_B"):
            if ("Taxiway_" in item["properties"]["name"] or "Stand_" in item["properties"]["name"]):
                output.append("; - {0}".format(item["properties"]["name"]))
                t = 0
                list_to_four = list()
                for geo in item["geometry"]["coordinates"]:
                    geo.pop(2)
                    if t == 0 and len(list_to_four) == 2:
                        output.append(" ".join(list_to_four))
                    if len(list_to_four) >= 1 and len(list_to_four) / (len(list_to_four) / 2) == 2 and t != 0:
                        lat = convert_LAT(geo[::-1][0])
                        lng = convert_LON(geo[::-1][1])
                        list_to_four.append((lat, lng))
                        if "Taxiway_" in item["properties"]["name"]:
                            output.append("{} {} {}".format(list_to_four[t-1], list_to_four[t], SECTOR_COLORS["Taxiway_"]).replace('(', '').replace(')', '').replace(',', '').replace("'", ""))
                        elif "Stand_" in item["properties"]["name"]:
                            output.append("{} {} {}".format(list_to_four[t-1], list_to_four[t], SECTOR_COLORS["Stand_"]).replace('(', '').replace(')', '').replace(',', '').replace("'", ""))
                    else:
                        lat = convert_LAT(geo[::-1][0])
                        lng = convert_LON(geo[::-1][1])
                        list_to_four.append((lat, lng))
                    
                    t += 1
                              
        return output

    output = convert_regions()
    output += convert_taxiways_and_stands()

    with open('converted/' + filepath.split("/")[1].split(".")[0] + '.sct', 'w') as file:
        file.write("\n".join(output))
