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


path = '/home/mr_malviya/Desktop/P03_DSP/Data/project3_neurofinder.00.00.test/neurofinder.00.00.test/images/'


# In[17]:


data = th.images.fromtif(path , stop=10, ext='tiff', engine=sc, npartitions= 10)


# In[19]:


algorithm = NMF(k=10, percentile=99, max_iter=50, overlap=0.1)
model = algorithm.fit(data, chunk_size=(50,50))
merged = model.merge(0.1)


# In[26]:


regions = [{'coordinates': region.coordinates.tolist()} for region in merged.regions]
result = [{'dataset': '00.00.test', 'regions': regions}]


# In[27]:


with open('submission-' + '00.00'  +'.json', 'w') as f:
	f.write(json.dumps(result))


# In[34]:


final_regions = []
for region in merged.regions:
    coordinates = region.coordinates.tolist()
    neuron = {'coordinates' : coordinates}
    final_regions.append(neuron)
    


# In[36]:


output = [{'dataset':'00.00.test', 'regions':final_regions}]


# In[38]:


with open('p03-' + '00.00'  +'.json', 'w') as f:
	f.write(json.dumps(result))






