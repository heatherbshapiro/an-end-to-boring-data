
# coding: utf-8

# # Learning Pandas and Matplotlib

# In[ ]:




# ### Importing libraries and data

# In[88]:

get_ipython().system(u'curl -L https://www.dropbox.com/s/qsodvwpcyu3mxei/NYC%20Restaurants.csv?dl=1 -o NYC_Restaurants.csv')


# In[89]:

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')


# ### Read NYC Restaurant CSV

# In[90]:

rests = pd.read_csv("NYC_Restaurants.csv")


# In[91]:

mRests = rests[rests['BORO']=="MANHATTAN"] ## Look at only Manhattan Data


# In[92]:

mRests['BORO']


# In[93]:

list(mRests.columns.values)


# In[94]:

mRests = mRests[mRests['GRADE']!="Not Yet Graded"] ## Remove stores that have not been graded yet


# In[95]:

mRests = mRests[pd.notnull(mRests["GRADE"])] ## Remove Stores that have no grade


# In[96]:

mRests=mRests[pd.notnull(mRests["SCORE"])] ## Remove stores with no score


# In[97]:

mRests["SCORE"].describe()


# In[98]:

mRests["GRADE"] = mRests["GRADE"].astype("category",categories = ["A","B","C","P","Z"], ordered = True) ## redefine score levels


# In[99]:

mRests = mRests.reset_index(drop=True)
mRests.head()


# ## Plotting with Pandas and Matplotlib

# ### Using Matplotlib

# In[100]:

f, ax = plt.subplots() ## creates figure area with axes
# histogram our data with numpy
data = mRests['SCORE']

plt.hist(data)
plt.xlabel('Score')
plt.ylabel('Frequency')
plt.title("Frequency of Restaurant Scores")

plt.show()


# ### Using Pandas

# In[101]:

plt.style.use('seaborn-colorblind')


# In[102]:

plt.style.available


# In[103]:

mRests["SCORE"].hist(bins=20)
plt.title("Frequency of Restaurant Score")


# In[104]:

mRests["GRADE"].value_counts().plot(kind = "pie")


# In[105]:

mRests['CRITICAL FLAG'].value_counts().plot(kind='bar')


# # Seaborn

# In[106]:

## pip install seaborn
import seaborn as sns
sns.set(style="whitegrid", color_codes=True)


# In[107]:

sns.stripplot(x="GRADE", y = "SCORE", data = mRests) #without jitter


# In[108]:

sns.stripplot(x="GRADE", y = "SCORE", data = mRests, jitter = True)


# In[109]:

sns.stripplot(x="GRADE", y = "SCORE", hue = "CRITICAL FLAG", data = mRests, jitter = True)


# In[110]:

sns.boxplot(x="GRADE",y="SCORE", hue = "CRITICAL FLAG", data = mRests)


# In[111]:

sns.barplot(x="GRADE", y = "SCORE", hue = "CRITICAL FLAG", data = mRests)


# ## Convert Addresses to Lat/Long 

# In[112]:

# !pip install -e git+https://github.com/pwdyson/inflect.py#egg=inflect


# In[113]:

# !conda update anaconda --y


# In[114]:

get_ipython().system(u'pip install inflect')


# In[115]:

import inflect
p = inflect.engine()
word_to_number_mapping = {}

for i in range(1, 200):
    word_form = p.number_to_words(i)  # 1 -> 'one'
    ordinal_word = p.ordinal(word_form)  # 'one' -> 'first'
    ordinal_number = p.ordinal(i)  # 1 -> '1st'
    word_to_number_mapping[ordinal_word] = ordinal_number  # 'first': '1st'
    


# In[116]:

import re
for i in range(len(mRests)):

    street= mRests['STREET'][i].split()    
    for j in range(len(street)):
        if street[j].lower() in word_to_number_mapping:
            
            street[j]=  word_to_number_mapping[street[j].lower()]
#     streetFull = ' '.join(street)
    for j in range(len(street)):
        if re.findall(r'([0-9]+(st|rd|th|nd)+)', street[j].lower())==[]:
            if(filter(str.isdigit, street[j])!=''):
                val=int(filter(str.isdigit, street[j]))
                street[j]=street[j].replace(str(val), str(p.ordinal(val)))    
        streetFull = ' '.join(street)
        mRests.set_value(i,'STREET',streetFull)
  


# In[117]:

mRests["STREET"]


# In[118]:

mRests["Address"]=mRests['BUILDING'].map(str)+ " " + mRests['STREET'].map(str)+ ", " + mRests['ZIPCODE'].map(str)


# ### Sample data with same seed every time

# In[119]:

# import random
np.random.seed(seed=10)
rows = np.random.choice(mRests.index.values, 100)
samp = mRests.ix[rows]
# samp = random.sample(mRests,90)
samp= samp.reset_index(drop=True)
samp


# ### Geocode Addresses

# In[123]:

# import time
# from rate_limited_queue import RateLimitedQueue, RateLimit
# from geopy.geocoders import Nominatim
# # import geopy
# geolocator = Nominatim()
# # location = geolocator.geocode("501 WEST 51st STREET, 10019")
# # print(location.address)
# mRests['lat']= 0.00
# mRests['long'] = 0.00

# samp = mRests.sample(90)
# samp=samp.reset_index(drop=True)

# addresses = samp['Address'].str.cat(sep='\n ')

# for j in range(0,2):
# #     print "this is j " + str(j)
#     for i in range(0+(45*j),45+(45*(j))):
# #     for i in range(len(samp)):
#         print i
#         #     address=' '.join(mRests['Address'][i].split())
#         address=samp['Address'][i]
#         #     print address

#         g = geolocator.geocode(mRests['Address'][i])
#         #     print g
#         lat = g.latitude
#         lon = g.longitude
#         samp.set_value(i,'lat',lat)
#         samp.set_value(i,'long',lon)

#     time.sleep(60)


# In[120]:

with open ('out.txt','w') as f: ##save addresses to txt file to batch geocode
 for i in range(len(samp)):
    f.write(samp['Address'][i]+ '\n')


# In[121]:

get_ipython().system(u"curl -L 'https://www.dropbox.com/s/p4145z5odvlypez/address.csv?dl=1' -o address.csv")


# In[122]:

adds = pd.read_csv("address.csv")
samp['lat']= adds['latitude']
samp['long']= adds['longitude']


# # Using Basemap

# In[124]:

get_ipython().system(u'conda install basemap --yes')


# In[125]:

from mpl_toolkits.basemap import Basemap]


# In[171]:

map = Basemap(projection='merc',
    resolution = 'h', area_thresh = .01,
    lat_0=40.7831, lon_0= -73.9712,
    llcrnrlon=-74.03, llcrnrlat=40.701,
    urcrnrlon=-73.86, urcrnrlat=40.901)
 
#     40.7831, -73.9712
    


# In[172]:

map.drawcoastlines()
map.drawcountries()
map.drawstates()
map.drawrivers()
map.fillcontinents(color = 'gainsboro')
map.drawmapboundary(fill_color='steelblue')
map.plot(samp['lat'][1],samp['long'][1],'bo', markersize = 24)


# # Using Folium

# In[127]:

get_ipython().system(u'pip install folium')


# In[165]:

import folium

mCluster = folium.Map(location=[40.7831, -73.9712], zoom_start =12)
marker_cluster = folium.MarkerCluster().add_to(mCluster)
for i in range(len(samp)):
    if samp["GRADE"][i] =="A":
        folium.Marker([samp['lat'][i],samp['long'][i]], popup= "Name: " + str(samp['DBA'][i])+ '\n' + "Score: " + str(samp["SCORE"][i]) + '\n'+'Grade: '+ str(samp["GRADE"][i]),
                      icon=folium.Icon(color="green", icon='no-sign')).add_to(marker_cluster)
    elif samp["GRADE"][i]=="B":
         folium.Marker([samp['lat'][i],samp['long'][i]], popup= "Name: " + str(samp['DBA'][i])+ '\n' + "Score: " + str(samp["SCORE"][i]) + '\n'+'Grade: '+ str(samp["GRADE"][i]),
                      icon=folium.Icon(color='blue',icon='no-sign')).add_to(marker_cluster)
    else:
         folium.Marker([samp['lat'][i],samp['long'][i]], popup= "Name: " + str(samp['DBA'][i])+ '\n' + "Score: " + str(samp["SCORE"][i]) + '\n'+'Grade: '+ str(samp["GRADE"][i]),
                      icon=folium.Icon(color='red',icon='no-sign')).add_to(marker_cluster)


# In[166]:

mCluster


# In[129]:

m = folium.Map(location=[40.7831, -73.9712], zoom_start =12)
# marker_cluster = folium.MarkerCluster().add_to(m)
for i in range(len(samp)):
    if samp["GRADE"][i] =="A":
        folium.Marker([samp['lat'][i],samp['long'][i]], popup= "Name: " + str(samp['DBA'][i])+ '\n' + "Score: " + str(samp["SCORE"][i]) + '\n'+'Grade: '+ str(samp["GRADE"][i]),
                      icon=folium.Icon(color="green", icon='no-sign')).add_to(m)
    elif samp["GRADE"][i]=="B":
         folium.Marker([samp['lat'][i],samp['long'][i]], popup= "Name: " + str(samp['DBA'][i])+ '\n' + "Score: " + str(samp["SCORE"][i]) + '\n'+'Grade: '+ str(samp["GRADE"][i]),
                      icon=folium.Icon(color='blue',icon='no-sign')).add_to(m)
    else:
         folium.Marker([samp['lat'][i],samp['long'][i]], popup= "Name: " + str(samp['DBA'][i])+ '\n' + "Score: " + str(samp["SCORE"][i]) + '\n'+'Grade: '+ str(samp["GRADE"][i]),
                      icon=folium.Icon(color='red',icon='no-sign')).add_to(m)


# In[160]:

m


# In[130]:

m.save('restaurants.html')


# # Using Bokeh

# In[131]:

from bokeh.io import output_notebook
output_notebook()


# In[159]:

from bokeh.charts import Histogram, output_file, show

# create a new plot with a title and axis labels
p1=Histogram(samp['SCORE'])
# output_file("histogram.html")



# In[158]:

show(p1)


# In[157]:

from bokeh.charts import Histogram, output_file, show
from bokeh.sampledata.autompg import autompg as df

p2 = Histogram(mRests,'SCORE', color='GRADE',
              title="Score Grouped by Grade", bins = 15,
              legend='top_right')

# output_file("histogram_color.html")


# In[154]:

show(p2)


# In[153]:

from bokeh.models.widgets import Panel, Tabs
from bokeh.io import output_file, show
from bokeh.plotting import figure

tab1 = Panel(child=p1, title="Frequency of Score")
tab2 = Panel(child=p2, title="By Grade")

tabs = Tabs(tabs=[ tab1, tab2 ])
output_file("tabs.html")




# In[152]:

show(tabs)


# # Using Plotly

# In[135]:

import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
init_notebook_mode(connected=True)


# In[143]:

x = mRests['GRADE']

tr1 = go.Histogram(x=x, histnorm='probability density', 
                xbins=dict(start=np.min(x), size= 0.25, end= np.max(x)),
                marker=dict(color='rgb(0,0,100)'))
title =" Probability Density of Grades"

layout = dict(
            title=title,
            autosize= True,
            bargap= 0.015,
            height= 600,
            width= 700,       
            hovermode= 'x',
            xaxis=dict(
            autorange= True,
            zeroline= False),
            yaxis= dict(
            autorange= True,
            showticklabels= True,
           ))
fig1 = go.Figure(data=go.Data([tr1]), layout=layout)



# In[144]:

iplot(fig1)


# In[146]:

x = samp['SCORE']

tr1 = go.Histogram(x=x, histnorm='probability density', 
                xbins=dict(start=np.min(x), size= 0.25, end= np.max(x)),
                marker=dict(color='rgb(0,0,100)'))

title =" Probability Density of Scores"

layout = dict(
            title=title,
            autosize= True,
            bargap= 0.015,
            height= 600,
            width= 700,       
            hovermode= 'x',
            xaxis=dict(
            autorange= True,
            zeroline= False),
            yaxis= dict(
            autorange= True,
            showticklabels= True,
           ))
fig2 = go.Figure(data=go.Data([tr1]), layout=layout)


# In[147]:

iplot(fig2)


# In[148]:

trace = go.Histogram(x=mRests['SCORE'])

data = go.Data([trace])


fig = dict(data=data)


# In[149]:

iplot(fig)


# In[150]:

samp['text'] = "Name: " + samp['DBA'].astype(str)+ '\n' + "Score: " + samp["SCORE"].astype(str) + '\n'+'Grade: '+ samp["GRADE"].astype(str)

scl = [ [0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],    [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"] ]

data = [ dict(
        type = 'scattergeo',
        locationmode = 'USA-states',
        lon = samp['long'],
        lat = samp['lat'],
        text = samp['text'],
        mode = 'markers',
        marker = dict( 
            size = 8, 
            opacity = 0.8,
            reversescale = True,
            autocolorscale = False,
            symbol = 'square',
            line = dict(
                width=1,
                color='rgba(102, 102, 102)'
            ),
            colorscale = scl,
            cmin = 0,
            color = samp['SCORE'],
            cmax = samp['SCORE'].max(),
            colorbar=dict(
                title="Restaurant Score"
            )
        ))]

layout = dict(
        title = 'Restaurant Scores',
#         colorbar = True,   
        geo = dict(
            scope='usa',
#             projection=dict( type='albers usa' ),
            showland = True,
            landcolor = "rgb(250, 250, 250)",
            subunitcolor = "rgb(217, 217, 217)",
            countrycolor = "rgb(217, 217, 217)",
            countrywidth = 0.5,
            subunitwidth = 0.5        
        ),
    )

fig = dict( data=data, layout=layout )


# In[151]:

iplot(fig)

