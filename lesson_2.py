

import matplotlib
print(matplotlib.__path__)

coordination_source = """
{name:'兰州', geoCoord:[103.73, 36.03]},
{name:'嘉峪关', geoCoord:[98.17, 39.47]},
{name:'西宁', geoCoord:[101.74, 36.56]},
{name:'成都', geoCoord:[104.06, 30.67]},
{name:'石家庄', geoCoord:[114.48, 38.03]},
{name:'拉萨', geoCoord:[102.73, 25.04]},
{name:'贵阳', geoCoord:[106.71, 26.57]},
{name:'武汉', geoCoord:[114.31, 30.52]},
{name:'郑州', geoCoord:[113.65, 34.76]},
{name:'济南', geoCoord:[117, 36.65]},
{name:'南京', geoCoord:[118.78, 32.04]},
{name:'合肥', geoCoord:[117.27, 31.86]},
{name:'杭州', geoCoord:[120.19, 30.26]},
{name:'南昌', geoCoord:[115.89, 28.68]},
{name:'福州', geoCoord:[119.3, 26.08]},
{name:'广州', geoCoord:[113.23, 23.16]},
{name:'长沙', geoCoord:[113, 28.21]},
//{name:'海口', geoCoord:[110.35, 20.02]},
{name:'沈阳', geoCoord:[123.38, 41.8]},
{name:'长春', geoCoord:[125.35, 43.88]},
{name:'哈尔滨', geoCoord:[126.63, 45.75]},
{name:'太原', geoCoord:[112.53, 37.87]},
{name:'西安', geoCoord:[108.95, 34.27]},
//{name:'台湾', geoCoord:[121.30, 25.03]},
{name:'北京', geoCoord:[116.46, 39.92]},
{name:'上海', geoCoord:[121.48, 31.22]},
{name:'重庆', geoCoord:[106.54, 29.59]},
{name:'天津', geoCoord:[117.2, 39.13]},
{name:'呼和浩特', geoCoord:[111.65, 40.82]},
{name:'南宁', geoCoord:[108.33, 22.84]},
//{name:'西藏', geoCoord:[91.11, 29.97]},
{name:'银川', geoCoord:[106.27, 38.47]},
{name:'乌鲁木齐', geoCoord:[87.68, 43.77]},
{name:'香港', geoCoord:[114.17, 22.28]},
{name:'澳门', geoCoord:[113.54, 22.19]}
"""
import networkx as nx
import re

city_location = {}
for line in coordination_source.split('\n'):
    if line.startswith('//'): continue
    if line.strip() == '': continue

    city = re.findall("name:'(\w+)'", line)[0]
    # python re referenes: https://docs.python.org/3/library/re.html
    x_y = re.findall("Coord:\[(\d+.\d+),\s(\d+.\d+)\]", line)[0]
    #print(city,x_y)
    x_y = tuple(map(float, x_y))
    city_location[city] = x_y
    #print(city, x_y)
import math

def geo_distance(origin, destination):
    """
    Calculate the Haversine distance.

    Parameters
    ----------
    origin : tuple of float
        (lat, long)
    destination : tuple of float
        (lat, long)

    Returns
    -------
    distance_in_km : float

    Examples
    --------
    >>> origin = (48.1372, 11.5756)  # Munich
    >>> destination = (52.5186, 13.4083)  # Berlin
    >>> round(distance(origin, destination), 1)
    504.2
    """
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d

def get_city_distance(city1, city2):
    return geo_distance(city_location[city1], city_location[city2])
get_city_distance('杭州', '上海')

cities = list(city_location.keys())


threshold = 700
from collections import defaultdict
cities_connection = defaultdict(list)

for c1 in cities:
    for c2 in cities:
        if c1 == c2: continue

        if get_city_distance(c1, c2) < threshold:
            cities_connection[c1].append(c2)

print('city_connection',cities_connection.items())
print('city_connection',cities_connection.keys())

simple_connection_info_src = {
    '北京': ['太原', '沈阳'],
    '太原': ['北京', '西安', '郑州'],
    '兰州': ['西安'],
    '郑州': ['太原'],
    '西安': ['兰州', '长沙'],
    '长沙': ['福州', '南宁'],
    '沈阳': ['北京']
}
simple_connection_info = defaultdict(list)
simple_connection_info.update(simple_connection_info_src)
print(simple_connection_info)


def bfs(graph, start):
    """
    breath first search
    """
    visited = [start]

    seen = set()

    while visited:
        froninter = visited.pop()  #
        if froninter in seen:
            continue
        for successor in graph[froninter]:
            if successor in seen:
                continue
            print(successor)

            visited = visited + [successor] # 我们每次扩展都扩展最新发现的点 -> depth first
            #visited = [successor] + visited  # 我们每次扩展都先考虑已经发现的 老的点 -> breath first

            # 所以说，这个扩展顺序其实是决定了我们的深度优先还是广度优先

        seen.add(froninter)

    return seen

number_grpah = defaultdict(list)

number_grpah.update({
    1: [2, 3],
    2: [1, 4],
    3: [1, 5],
    4: [2, 6],
    5: [3, 7],
    7: [5, 8]
})
print(number_grpah)
print(bfs(number_grpah, 1))

def is_goal(desitination):
    def _wrap(current_path):
        return current_path[-1] == desitination
    return _wrap


def search(graph, start, is_goal, search_strategy):
    pathes = [[start]]
    seen = set()

    while pathes:
        path = pathes.pop(0)
        froniter = path[-1]

        if froniter in seen: continue

        successors = graph[froniter]

        for city in successors:
            if city in path: continue

            new_path = path + [city]

            pathes.append(new_path)

            if is_goal(new_path):
                return new_path
        # print('len(pathes)={}'.format(pathes))
        seen.add(froniter)
        pathes = search_strategy(pathes)

search(cities_connection, start='西安', is_goal=is_goal('上海'), search_strategy=lambda n: n)

def sort_path(cmp_func, beam=-1):
    def _sorted(pathes):
        return sorted(pathes, key=cmp_func)[:beam]
    return _sorted
search(cities_connection, start='北京', is_goal=is_goal('拉萨'), search_strategy=lambda n: n)


def search1(start, destination, connection_grpah, sort_candidate):
    pathes = [[start]]

    visitied = set()

    while pathes:  # if we find existing pathes
        path = pathes.pop(0)
        froninter = path[-1]

        if froninter in visitied:
            continue
        successors = connection_grpah[froninter]

        for city in successors:
            if city in path:
                continue  # eliminate loop

            new_path = path + [city]

            pathes.append(new_path)

            if city == destination:
                return new_path

        visitied.add(froninter)

        pathes = sort_candidate(pathes)  # 我们可以加一个排序函数 对我们的搜索策略进行控制

def search2(start, destination, connection_grpah, sort_candidate):
    pathes = [[start]]

    visitied = set()

    while pathes:  # if we find existing pathes
        path = pathes.pop(0)
        froninter = path[-1]

        if froninter in visitied: continue

        successors = connection_grpah[froninter].keys()

        for city in successors:
            if city in path:
                continue  # eliminate loop

            new_path = path + [city]

            pathes.append(new_path)

            if city == destination:
                return new_path

        visitied.add(froninter)

        pathes = sort_candidate(pathes)  # 我们可以加一个排序函数 对我们的搜索策略进行控制

def transfer_stations_first(pathes):
    return sorted(pathes, key=len)
def transfer_as_much_possible(pathes):
    return sorted(pathes, key=len, reverse=True)


def shortest_path_first(pathes):
    if len(pathes) <= 1: return pathes

    def get_path_distnace(path):
        distance = 0
        for station in path[:-1]:
            distance += get_geo_distance(station, path[-1])

        return distance

    return sorted(pathes, key=get_path_distnace)
print(search1('兰州', '福州', simple_connection_info, sort_candidate=transfer_stations_first))

print(search1('兰州', '福州', simple_connection_info, sort_candidate=transfer_as_much_possible))


