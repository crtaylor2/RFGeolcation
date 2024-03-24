import PointIntersection
import itertools 
import geopy.distance
import math

# ["Location Name", "Latitude", "Longitude", "Distance (km)"]
#WestValley = ["West Valley", 40.6916, -112.0011, 5]
#Taylorsville = ["Taylorsville", 40.6677, -111.9388, 5]
#Kearns = ["Kearns", 40.6599, -111.9963, 5]
#Riverton = ["Riverton", 40.5219, -111.9391, 12]

#All = [WestValley, Taylorsville, Kearns, Riverton]

K201AE = ["K201AE", 40.854944, -111.479639, 35.12]
K202CC = ["K202CC", 40.0905, -111.822139, 74.33]
KUUB = ["KUUB", 40.6313333, -112.131306, 25.79]
K209CJ = ["K209CJ", 40.8080556, -111.890278, 5.62]

All = [K201AE, K202CC, KUUB, K209CJ]

DistancesAll = []
DistanceMap = {}

for index1 in range(len(All)):
    for index2 in range(index1 + 1, len(All)):
        #print("Computing intersection between " + All[index1][0] + " and " + All[index2][0])
        if All[index1][0] not in DistanceMap:
            DistanceMap[All[index1][0]] = {}
        if All[index2][0] not in DistanceMap:
            DistanceMap[All[index2][0]] = {}
        a, b = PointIntersection.geo_circle_intersection_km([All[index1][1], All[index1][2]], All[index1][3],
                                                            [All[index2][1], All[index2][2]], All[index2][3])
        if a is None or b is None:
            continue
        Intersection = [a, b]
        DistancesAll.append(Intersection)
        DistanceMap[All[index1][0]][All[index2][0]] = Intersection
        DistanceMap[All[index2][0]][All[index1][0]] = Intersection
        #print("  First result: " + str(DistanceMap[All[index1][0]][All[index2][0]][0]))
        #print("  Second result: " + str(DistanceMap[All[index1][0]][All[index2][0]][1]))


best_distance = math.inf
best_coords = []

for i in itertools.product([0,1],repeat=len(DistancesAll)):
    index1 = 0
    points = []
    for index2 in range(len(i)):
        points.append(DistancesAll[index1][i[index2]])
        index1 = index1 + 1
    #print(points)
    distance = 0
    for p1 in range(len(points)):
        for p2 in range(p1 + 1, len(points)):
            #print("distance between" + str(points[p1]) + " " + str(points[p2]))
            #print(geopy.distance.geodesic(points[p1], points[p2]).km)
            distance = distance + geopy.distance.geodesic(points[p1], points[p2]).km

    if distance < best_distance:
        #print("found better")
        best_distance = distance
        best_coords = points


if distance < math.inf:
    total_lat = 0
    total_lon = 0

    for p in range(len(best_coords)):
        total_lat = total_lat + best_coords[p][0]
        total_lon = total_lon + best_coords[p][1]

    avg_lat = total_lat / len(best_coords)
    avg_lon = total_lon / len(best_coords)

    print("Final answer: " + str(avg_lat) + ", " + str(avg_lon))
else:
    print("Final answer: I have no idea")
