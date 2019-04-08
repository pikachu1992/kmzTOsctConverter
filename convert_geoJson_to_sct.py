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
    
    output = list()

    for item in data["features"]:
        for color in SECTOR_COLORS:
            if color in item["properties"]["name"] and color != "Taxiway_":
                output.append("{0}".format(SECTOR_COLORS[color]))
        output.append("; - {0}".format(item["properties"]["name"]))
        t = 0
        y = 0
        string_parse = ""
        for geo in item["geometry"]["coordinates"]:
            parse = [x for x in geo]           
            for i in parse:
                if type(i) == list:
                    string_parse = ""
                    i.pop(2)
                    t = 0
                    for c in i[:2]:
                        if t == 0:
                            if c < 0:
                                degrees, minutes, seconds = decdeg2dms(c)
                                if degrees < 10:
                                    i[t] = "W00{0:.0f}.{1:.0f}.{2:.3f}".format((degrees*-1), minutes, seconds)
                                else:
                                    i[t] = "W0{0:.0f}.{1:.0f}.{2:.3f}".format((degrees*-1), minutes, seconds)
                            else:
                                degrees, minutes, seconds = decdeg2dms(c)
                                i[t] = "E{0:.0f}.{1:.0f}.{2:.3f}".format(degrees, minutes, seconds)

                        if t == 1:
                            if c < 0:
                                degrees, minutes, seconds = decdeg2dms(c)
                                i[t] = "S{0:.0f}.{1:.0f}.{2:.3f}".format(degrees, minutes, seconds)
                            else:
                                degrees, minutes, seconds = decdeg2dms(c)
                                i[t] = "N0{0:.0f}.{1:.0f}.{2:.3f}".format(degrees, minutes, seconds)
                        t+=1
                    output.append(str(i[::-1]).replace('[', '').replace(']', '').replace(',', '').replace("'", ""))
                else:
                    if len(parse) > 2:
                        parse.pop(2)
                    if type(i) == float:
                        str_coord = []
                        if len(string_parse.split()) == 4:
                            if i < 0:
                                degrees, minutes, seconds = decdeg2dms(i)
                                str_coord.append("S{0:.0f}.{1:.0f}.{2:.3f}".format(degrees, minutes, seconds))
                            else:
                                degrees, minutes, seconds = decdeg2dms(i)
                                str_coord.append("N0{0:.0f}.{1:.0f}.{2:.3f}".format(degrees, minutes, seconds))   

                            if string_parse.split()[0][0] == 'W':
                                string = string_parse.split()[:2][::-1] + string_parse.split()[2:][::-1]
                            else:
                                string = string_parse.split()[:2] + string_parse.split()[2:]
                            string_parse = str(string).replace('[', '').replace(']', '').replace(',', '').replace("'", "") + " {0}".format(SECTOR_COLORS["Taxiway_"])
                            output.append(string_parse)
                            string_parse = ""
                        else:
                            data = parse
                            if i < 0:
                                degrees, minutes, seconds = decdeg2dms(i)
                                if degrees < 10:
                                    str_coord.append("W00{0:.0f}.{1:.0f}.{2:.3f}".format((degrees*-1), minutes, seconds))
                                else:
                                    str_coord.append("W0{0:.0f}.{1:.0f}.{2:.3f}".format((degrees*-1), minutes, seconds))
                            else:
                                if i < 0:
                                    degrees, minutes, seconds = decdeg2dms(i)
                                    str_coord.append("S{0:.0f}.{1:.0f}.{2:.3f}".format(degrees, minutes, seconds))
                                else:
                                    degrees, minutes, seconds = decdeg2dms(i)
                                    str_coord.append("N0{0:.0f}.{1:.0f}.{2:.3f}".format(degrees, minutes, seconds))
                            
                            string_parse += str(str_coord).replace('[', '').replace(']', '').replace(',', '').replace("'", "")+" "
                            


            
                        

                            
                            

    with open('converted/' + filepath.split("/")[1].split(".")[0] + '.sct', 'w') as file:
        file.write("\n".join(output))
