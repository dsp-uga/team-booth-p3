#!/usr/bin/env python
# coding: utf-8

# In[1]:


import findspark
findspark.init()
import pyspark


# In[2]:


from pyspark.sql import SparkSession


# In[3]:


import thunder as th
from extraction import NMF
import json
import os


# In[7]:


def configure_spark():
    conf = pyspark.SparkConf().setAppName("Malware_Classification")
    conf = (conf.setMaster('local[4]')
       .set('spark.executor.memory', '3G')
       .set('spark.driver.memory', '4G')
       .set('spark.driver.maxResultSize', '4G'))
    sc = pyspark.SparkContext(conf=conf)
    Spark = SparkSession(sc)
    return sc, Spark


# In[8]:


sc, Spark = configure_spark()


# In[16]:


datapath = '/home/mr_malviya/Desktop/P03_DSP/Data'


# In[17]:

final_output = []
final_regions = []
for filename in os.listdir(datapath):
    path = os.path.join(datapath,filename)
    path = path + '/images'
    data = th.images.fromtif(path , ext='tiff', engine=sc, npartitions= 10)
    algorithm = NMF(k=10, percentile=99, max_iter=50, overlap=0.1)
    model = algorithm.fit(data, chunk_size=(50,50))
    merged = model.merge(0.1)
    name = filename.split('.',1)[1]
    for region in merged.regions:
        coordinates = region.coordinates.tolist()
        neuron = {'coordinates' : coordinates}
        final_regions.append(neuron)
    final_output.append({'dataset':name, 'regions':final_regions})


# In[27]:


with open('submission-' +'.json', 'w') as f:
	f.write(json.dumps(final_output))





