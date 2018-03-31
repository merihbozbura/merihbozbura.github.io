---
layout: post
title: Principle Component Analysis with R
---

### The North Atlantic Oscillation Has an Effect on Western Turkey's Precipitation Pattern

This is one of the subjects that I am curious about. So, I have shortly worked on it. You can use these statistical methods on any kind of data that you want to study. Outline of this case as follows:

1. Introduction
2. Data and Method
3. Exploratory Data Analysis
4. Linear Regression
5. Principle Component Analysis
6. Conclusions

*I will talk a little bit about meteorology since I mainly want to talk about the R functions to show how to achieve these statistical moethods.* So, if you want, you can find the whole document [here.](https://github.com/merihbozbura/merihbozbura.github.io/blob/master/files/Merih%20Bozbura.pdf) The document was written using Copernicus **LaTeX** template.



#### Introduction

The North Atlantic Oscillation (NAO) is a large-scale natural climate variability that has important impacts on the weather and climate of the North Atlantic region and surrounding continents, especially Europe. 

Strong positive phase of NAO is associated with lower than normal temperatures over southern Europe and the Middle East and it is related to *lower than normal precipitation* over southern and central Europe.Unlike strong positive phase of NAO , negative phase is related to higher than normal temperature over southern Europe and the Middle East and it is associated with *higher than normal precipitation* over southern and central Europe.

Therefore, NAO is expected to have an impact on Turkey. Weather and climate conditions are controlled by NAO in 45 Mediterranean basin along with Turkey.

#### Data and Method

Precipitation data is observation data and it includes all provinces of Turkey between 1970 and 2012. The North Atlantic Oscillation Index data can be found [here.](https://climatedataguide.ucar.edu/climate-data/hurrell-north-atlantic-oscillation-nao-index-pc-based)



```python

def minimum (time1, time2, lat1,lat2,lon1,lon2):

    for t in range(time1,time2):

        candidate_pressures = np.ndarray(0)


        for i in range(lat1,lat2):
            for j in range(lon1,lon2):


                index = {"lattitude": i , "longitude": j}

                rank_of_loop = np.append(rank_of_loop,index)


```





### References

https://www.ncdc.noaa.gov/teleconnections/nao/

https://publications.copernicus.org/for_authors/latex_instructions.html














