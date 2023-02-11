import plotly.express as px
import pandas as pd



def plotly_bw_car_parking():
    print("getting Data...")
    df = px.data.carshare()
    print(df.head(10))


    fig = px.scatter_mapbox(df,
                            lat="centroid_lat",
                            lon="centroid_lon",
                            color="peak_hour",
                            size="car_hours",
                            title="Carshare Data",
                            width=1200, height=800, zoom=10)

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()





def OSM_Data_Test():
    from OSMPythonTools.nominatim import Nominatim
    from OSMPythonTools.overpass import overpassQueryBuilder
    from OSMPythonTools.overpass import Overpass


    # nominatim = Nominatim()
    # nyc = nominatim.query('NYC')

    # query = overpassQueryBuilder(area=nyc, elementType='node', selector='"highway"="bus_stop"', out='body')

    # query = overpassQueryBuilder(area=nyc.areaId(), elementType='node', selector='"highway"="bus_stop"', out='body')
    # query = overpassQueryBuilder(area='relation/175905', elementType='node', selector='"highway"="bus_stop"', out='body')
    # query = overpassQueryBuilder(area='relation 175905', elementType='node', selector='"highway"="bus_stop"', out='body')

    query = overpassQueryBuilder(bbox=[48.1, 16.3, 48.3, 16.5], elementType='node', selector='"highway"="bus_stop"', out='body', includeGeometry=True)



    overpass = Overpass()
    busStops = overpass.query(query)

    # print(busStops.nodes()[0])
    print(busStops.nodes()[0].tags())




    # print(busStops.elements())






def main():
    # plotly_bw_car_parking()
    OSM_Data_Test()



if __name__ == "__main__":
    main()