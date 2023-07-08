def wind_converter(deg):
    if deg <= 11.25 and deg >= 0 or deg > 348.75 and deg <=360:
        direction = "N"
    elif deg > 11.25 and deg <= 33.75:
        direction = "NNE"
    elif deg > 33.75 and deg <=56.25:
        direction = "NE"
    elif deg > 56.25 and deg <= 78.75:
        direction = "ENE"
    elif deg > 78.75 and deg <= 101.25:
        direction = "E"
    elif deg > 101.25 and deg <= 123.75:
        direction = "ESE"
    elif deg > 123.75 and deg <= 146.25:
        direction = "SE"
    elif deg > 146.25 and deg <= 168.75:
        direction = "SSE"
    elif deg > 167.75 and deg <= 191.25:
        direction = "S"
    elif deg > 191.25 and deg <= 213.75:
        direction = "SSW"
    elif deg > 213.75 and deg <= 236.25:
        direction = "SW"
    elif deg > 236.25 and deg <= 258.75:
        direction = "WSW"
    elif deg > 258.75 and deg <= 281.25:
        direction = "W"
    elif deg > 281.25 and deg <= 303.75:
        direction = "WNW"
    elif deg > 303.75 and deg <= 326.25:
        direction = "NW"
    elif deg > 326.25 and deg <=348.75:
        direction = "NNW"
    return direction
