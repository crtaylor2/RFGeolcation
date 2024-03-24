import math
import utm

def circle_intersection(x0, y0, r0, x1, y1, r1):

    d = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)

    if d > r0 + r1:             # non intersecting
        print("Non intersecting circles")
        return None, None
    if d < abs(r0 - r1):        # one circle within other
        print("One circle within other")
        return None, None
    if d == 0 and r0 == r1:     # coincident circles
        print("Coincident circles")
        return None, None

    a = (r0 ** 2 - r1 ** 2 + d ** 2) / (2 * d)
    h = math.sqrt(r0 ** 2 - a ** 2)
    x2 = x0 + a * (x1 - x0) / d
    y2 = y0 + a * (y1 - y0) / d
    x3 = x2 + h * (y1 - y0) / d
    y3 = y2 - h * (x1 - x0) / d

    x4 = x2 - h * (y1 - y0) / d
    y4 = y2 + h * (x1 - x0) / d

    return (x3, y3), (x4, y4)

def geo_circle_intersection_km(latlon0, radius0, latlon1, radius1):
    return geo_circle_intersection_m(latlon0, radius0 * 1000, latlon1, radius1 * 1000)

def geo_circle_intersection_m(latlon0, radius0, latlon1, radius1):

    # Convert lat/lon to UTM
    x0, y0, zone, letter = utm.from_latlon(latlon0[0], latlon0[1])
    x1, y1, _, _ = utm.from_latlon(latlon1[0], latlon1 [1], force_zone_number=zone)

    # Calculate intersections in UTM coordinates
    a_utm, b_utm = circle_intersection(x0, y0, radius0, x1, y1, radius1)

    if a_utm is None or b_utm is None:
        return a_utm, b_utm
    
    # Convert intersections from UTM back to lat/lon
    a = utm.to_latlon(a_utm[0], a_utm[1], zone, letter)
    b = utm.to_latlon(b_utm[0], b_utm[1], zone, letter)

    return a, b

