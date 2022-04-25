import json
import geopandas


#for state data
with open('states.geojson', 'r') as f:
    stateData = geopandas.read_file(f)
states = []

#for the output json
with open('states.geojson', 'r') as f:
    geo = json.load(f)
    for feature in geo['features']:
        states.append(feature['properties']['name'])
        feature['properties'].update({  "Population" : 0,
                                        "stroke": "#555555",
                                        "stroke-width": 2,
                                        "stroke-opacity": 1,
                                        "fill": "",
                                        "fill-opacity": .75,
                                        'type': 'state'})

with open('cities.json', 'r') as f:
    cityData = json.load(f)
x = []
y = []
population = []

#for creating dataframe from x and y
for points in cityData:
    x.append(points['longitude'])
    y.append(points['latitude'])
    population.append(points['population'])

#for population and the points 
cityData = geopandas.GeoDataFrame(population, geometry = geopandas.points_from_xy(x, y))

rtree = geopandas.GeoSeries(stateData['geometry'])

city = []

for i in range(cityData[0].count()):
    try:
        #for checking point
        query = rtree.sindex.query(cityData['geometry'][i], predicate='within')[0]

        #for incrementing population
        for feature in geo['features']:
            if states[query] == feature['properties']['name']:
                feature['properties']['Population'] += int(cityData[0][i])

        city.append(states[query])
    except:
        print(cityData['geometry'][i].x, ',', cityData['geometry'][i].y, ': Not in any polygon given')
        city.append('Hawaii')

#for coloring
geo['features'].sort(key = lambda x:x['properties']['Population'])

for i, cities in enumerate(cityData['geometry']):
    x = cities.x
    y = cities.y

    geometry = [[[cities.x + .1, cities.y + .1], [cities.x - .1, cities.y + .1], [cities.x - .1, cities.y - .1], [cities.x + .1, cities.y - .1], [cities.x + .1, cities.y + .1]]]
    geo['features'].append({
      "type": "Feature",
      "properties": {   "stroke": "#555555",
                        "stroke-width": 2,
                        "stroke-opacity": 1,
                        "fill": "",
                        "fill-opacity": 1,
                        'type': 'city',
                        'state': city[i]},
      "geometry": {
        "type": "Polygon",
        "coordinates": geometry
      }
    })

red = 255
stroke = '#ffffff'
colors = []
states = []

for feature in geo['features']:
    if feature['properties']['type'] == 'state':
        states.append(feature['properties']['name'])

        #each state increases the color by 5
        if feature['properties']['Population'] == 0:
            feature['properties']['fill'] = '#ffffff'
            colors.append('#ffffff')
        else:
            red -= 5
            color = "{:02x}".format(red)
            stroke = stroke[:3] + color + color
            feature['properties']['fill'] = stroke
            colors.append(stroke)
    else:
        feature['properties']['fill'] = colors[states.index(feature['properties']['state'])]
    
#for output
with open('Output.geojson', 'w') as f:
    json.dump(geo, f, indent=4)
