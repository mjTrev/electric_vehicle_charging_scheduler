import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#from mpl_toolkits.basemap import Basemap
#from shapely.geometry import Point, Polygon, MultiPoint, MultiPolygon
#from shapely.prepared import prep
#import fiona
from geopy.geocoders import Nominatim
from matplotlib.collections import PatchCollection
from descartes import PolygonPatch
import json
import datetime
from itertools import takewhile
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#from mpl_toolkits.basemap import Basemap
#from shapely.geometry import Point, Polygon, MultiPoint, MultiPolygon
#from shapely.prepared import prep
#import fiona
from geopy.geocoders import Nominatim
from matplotlib.collections import PatchCollection
from descartes import PolygonPatch
import json
import datetime
from itertools import takewhile
import math
import collections
#Location storage
MONTH=11
YEAR = 2016
FILENAME='LocationHistory.json'
ADDRESS = '649 E 800 N Logan UT'
geolocator = Nominatim(user_agent="specify_your_app_name_here")
HOMELOCATION = geolocator.geocode(ADDRESS,timeout=10)
#HOMELAT = 41.7465082331669
#print (HOMELOCATION.latitude)

with open(FILENAME, 'r') as fh:
    raw = json.loads(fh.read())
#np.fliplr(raw)
ld = pd.DataFrame(raw['locations'])
del raw #free up some memory
# convert to typical units
ld['latitudeE7'] = ld['latitudeE7']/float(1e7) 
ld['longitudeE7'] = ld['longitudeE7']/float(1e7)
ld['timestampMs'] = ld['timestampMs'].map(lambda x: float(x)/1000) #to seconds
ld['datetime'] = ld.timestampMs.map(datetime.datetime.fromtimestamp)
ld.rename(columns={'latitudeE7':'latitude', 'longitudeE7':'longitude', 'timestampMs':'timestamp'}, inplace=True)
ld = ld[ld.accuracy < 1000] #Ignore locations with accuracy estimates over 1000m
ld.reset_index(drop=True, inplace=True) 

def plotDatcharge(ld):
    x=[]
    y=[]
    for i in range(1,30):
       # print(i)
        y.append(i)
        point = timeRange(i,i+1,ld)
       # print(point[point.datetime.Length])
        x.append (chargeToats(point)*100)
        
    #print (y)
    plt.bar(y,x, align='center')
    #plt.xticks(y_pos, objects)
    plt.title('Estimated possible charging time per day')
    plt.ylabel('time available for charging by percent of day')
    plt.xlabel('Days October 2016')
    plt.show()
def plotDataKwh(ld):
    x=[]
    y=[]
    for i in range(1,31):
       # print(i)
        y.append(i)
        point = timeRange(i,i+1,ld)
        x.append (calcEnergy(point))
        
    #print (y)
    plt.bar(y,x, align='center')
    #plt.xticks(y_pos, objects)
    plt.title('Estimated kwh per day')
    plt.ylabel('kwh used per day')
    plt.xlabel('Days October 2016')
    plt.show()
    
def timeRange(x,y,ld):
    ld = ld[ld.datetime>datetime.datetime(YEAR,MONTH,x)]
    ld = ld[ld.datetime<datetime.datetime(YEAR,MONTH,y)]
    return ld
#ld = timeRange(11,12,ld)
#print (np.cos(1))
degrees_to_radians = np.pi/180.0 
ld['phi'] = (90.0 - ld.latitude) * degrees_to_radians 
ld['theta'] = (ld.longitude) * degrees_to_radians
# Compute distance between two GPS points on a unit sphere

ld['distance'] = np.arccos(
    np.sin(ld.phi)*np.sin(ld.phi.shift(-1)) * np.cos(ld.theta - ld.theta.shift(-1)) +
    np.cos(ld.phi)*np.cos(ld.phi.shift(-1))) * 6378.100 # radius of earth in km

ld['speed'] = ld.distance/(ld.timestamp - ld.timestamp.shift(-1))*3600 #km/hr
#def getConvert
#returns an array of all the time you are at home


def timeAtHome(ld):
 
    chargeable = ld[ld.speed<5]
    chargeable = chargeable[chargeable.latitude==chargeable.latitude.shift(-1)]
    chargeable = chargeable[chargeable.longitude==chargeable.longitude.shift(-1)]
    #score= collections.Counter((chargeable['latitude']))
    #THING TO FIX probably won't work if you drive around the equator 
    home=chargeable[abs(chargeable.latitude-HOMELOCATION.latitude)<3]
    #home=chargeable[abs(chargeable.latitude-HOMELAT)<3]
    #print(home['datetime'])
    return home
def chargeToats(ld):
    toats=1
    for y in ld['datetime']:
        toats+=1
    energyUsed=0.0
    ld=timeAtHome(ld)
    for y in ld['datetime']:
        energyUsed=energyUsed+1
   # print(x)
    #print('energy charged in seg')
    energyUsed=(energyUsed)
    #print (energyUsed,"units")
    return energyUsed/toats
def calcEnergy(ld):
    energyUsed=0.0
    
    ld=ld[ld.distance>0]
    ld=ld[ld.speed>0]
    for y in ld['distance']:
       # print (y)
        energyUsed=energyUsed+y
        
   # print(x)
   # print('energy used of day')
    energyUsed=(energyUsed*.621371)/3
    #print (energyUsed,"killo watts")
    
    return energyUsed
'''
ld=ld[ld.datetime>datetime.datetime(2016,10,1,1)]
ld=ld[ld.datetime<datetime.datetime(2016,10,2,2)]
calcEnergy(ld)
'''
    #print(home['datetime'])
def convertToTwenty(ld,i,z):
     x=calcEnergy(ld)
     z.append(x)
     return z
    #chargeToats(ld)   

#state={"EVbat",time}


'''
for i in ld['datetime']:
    print (i.minute)
'''
def storeUse():
    z=[]
    #state={"EVbat",time}
    i=14
    point = timeRange(i,i+1,ld)
    # print(point[point.datetime.Length])
    z.append((calcEnergy(point)))
    print (z[0])
    return (z)
#print (z)
def storePrevCharge():
    w=[]
    for x in range(1,24):
        a=x-1
        ldi=ld[ld.datetime<datetime.datetime(YEAR,MONTH,14,x)]
        ldi=ldi[ldi.datetime>datetime.datetime(YEAR,MONTH,14,a)]
        r = chargeToats(ldi)
        w.append(r)
        w.append(r)
        w.append(r)
    w.append(0)
    w.append(0)
    w.append(0)
    return(w)
def storecharge():
    w=[]
    for x in range(1,24):
        a=x-1
        ldi=ld[ld.datetime<datetime.datetime(YEAR,MONTH,15,x)]
        ldi=ldi[ldi.datetime>datetime.datetime(YEAR,MONTH,15,a)]
        r = chargeToats(ldi)
        w.append(r)
        w.append(r)
        w.append(r)
    w.append(0)
    w.append(0)
    w.append(0)
    
   # print('chargePoint',w)
    return (w) 
def findPrevTime(x):
    
    for i in range(51,71):
        if (x[i]==0):
            #print (x)
            #print (i)
            
            return i+6
    return -1
def findTime(x):
    
    for i in range(15,72):
        if (x[i]==0):
            #print (x)
            #print (i)
            
            return i+6
    return -1
#print(findTime(storecharge()))


#findPrevTime(storePrevCharge()))
#plotDatcharge(ld)
#plotDataKwh(ld)
#print (chargeable['latitude'])
#print (chargeable['latitude':'longitude':'datetime'])


#calcEnergy(ld)
