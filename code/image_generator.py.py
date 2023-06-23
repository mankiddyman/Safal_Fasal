import ee
import folium
# Define the add_ee_layer method for folium.Map
def add_ee_layer(self, ee_image_object, vis_params, name):
    map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
    folium.raster_layers.TileLayer(
        tiles=map_id_dict['tile_fetcher'].url_format,
        attr='Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
        name=name,
        overlay=True,
        control=True
    ).add_to(self)

# Add the add_ee_layer method to folium.Map
folium.Map.add_ee_layer = add_ee_layer
# Initialize Earth Engine
ee.Initialize()

#I will be generating a series of maps of gaurav's farm in jodhpur, india

plot1=[[72.996971, 26.609907],
      [72.997264, 26.603907],
      [72.999507, 26.604582],
      [72.996971, 26.609907]]
plot2=[[72.996513,26.598166],
       [72.998175,26.598390],
       [72.997975,26.599644],
       [73.001489,26.600283],
       [73.001932,26.597779],
       [72.998389,26.597332],
       [72.998703,26.595786],
       [72.996513,26.596166]]
plot3=[[73.012814,26.590995],
       [73.012860,26.586673],
       [73.018184,26.588124]]

date_1=['2022-03-28','2022-04-04'] #sowing centered around 1st april
date_2=['2022-06-12','2022-06-18'] #growing centered around 15th june
date_3=['2022-09-01','2022-09-30'] #just before harvest centered around 15th september

plot_Id=['plot1','plot2','plot3']
for i,plot_ in enumerate([plot1,plot2,plot3]):
    for date_ in [date_1,date_2,date_3]:
        roi=ee.Geometry.Polygon(plot_)
        #Define the region of interest (example coordinates)


        #want the maximum y coordinate
        for j,coords in enumerate(roi.getInfo()['coordinates']):
            max_y=0
            if coords[j][1]>max_y:
                max_y=coords[j][1]
                max_y_index=j
        # Load Sentinel-2 surface reflectance collection
        collection = ee.ImageCollection('COPERNICUS/S2_SR') \
            .filterDate(date_[0],date_[1] ) \
            .filterBounds(roi) \
            .sort('CLOUDY_PIXEL_PERCENTAGE')

        # Select the first (least cloudy) image from the collection
        image = ee.Image(collection.first())

        # Select the bands you want to display (example: B4, B3, B2 for RGB)
        bands = ['B4', 'B3', 'B2']

        # Create visualization parameters
        visualization = {'bands': bands, 'min': 0, 'max': 3000}

        # Center the map on the polygon's centroid
        centroid = roi.centroid()
        lat, lon = centroid.getInfo()['coordinates'][::-1]  # Reverse coordinates because I entered them in wrong order
        map = folium.Map(location=[lat, lon], zoom_start=12)

        # Add the surface image layer to the map
        map.add_ee_layer(image, visualization, 'Sentinel-2 Surface Image')

        # Add the polygon to the map
        folium.GeoJson(
            data=roi.getInfo(),
            name='Polygon',
            overlay=True,
            control=True
        ).add_to(map)

        # Add layer control
        folium.LayerControl().add_to(map)
        # Add a text box annotation

        date_of_image=ee.Date(image.get('system:time_start')).format('d-M-Y').getInfo()

        text_box = folium.Marker(
            location=[max_y, lon], #printing the text box slightly above the polygon
            icon=folium.DivIcon(
                icon_size=(150, 36),
                html=f'<div style="font-size: 12pt; font-weight: bold">Date: {date_of_image} \n Plot: {plot_Id[i]} </div>',
                )
            )
        map.add_child(text_box)
        # Display the map
        map
        map.save(f'../results/plot_{plot_Id[i]}_date_{date_of_image}.html')
