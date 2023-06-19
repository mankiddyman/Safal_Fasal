#In this script will be some test code for accessing geospatial data from the google earth engine

#I am basing this heavily off of https://www.youtube.com/watch?v=2ZuQAd_S-S8

#google earth engine is a cloud based platform for analyzing geospatial data 
#geospatial refers to observations of the earth from space


import ee
#ee.Authenticate()
ee.Initialize()
print(ee.Image('srtm90_v4'))

#now gonna load in some country data
countries = ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017')
Ethiopia = countries.filter(ee.Filter.eq('country_na', 'Ethiopia'))


#print the land elevation
dem=ee.Image('USGS/SRTMGL1_003')


import folium
#folium is a python library for making interactive maps
#define a method for displaying Earth Engine image tiles on a folium map
def add_ee_layer(self, ee_image_object, vis_params, name):
  map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
  folium.raster_layers.TileLayer(
    tiles = map_id_dict['tile_fetcher'].url_format,
    attr = 'Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
    name = name,
    overlay = True,
    control = True
  ).add_to(self)


folium.Map.add_ee_layer = add_ee_layer

vis_params = {
    'min': 0,
    'max': 4000,
    'palette': ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5']}

# Create a folium map object.
my_map = folium.Map(location=[20, 0], zoom_start=3, height=500)
#I wonder if this is where I can specify coordinates

# Add the layer to the map object.
my_map.add_ee_layer(dem.clip(Ethiopia).updateMask(dem.gt(0)), vis_params, 'DEM')

# Add a layer control panel to the map.
my_map.add_child(folium.LayerControl())

# Display the map.
display(my_map)

#okay this is epic
