---
layout: post
title: The North Atlantic Oscillation Has an Effect on Western Turkey's Precipitation Pattern
---

This is one of the subjects that I am curious about. So, I have shortly worked on it. You can use these statistical methods on any kind of data that you want to study. Outline of this case as follows:

1. Introduction
2. Data and Method
3. Exploratory Data Analysis
4. Linear Regression
5. Principle Component Analysis
6. Conclusions

*I will talk a little bit about meteorology since I mainly want to talk about the R functions to show how to achieve these statistical moethods.* So, if you want, you can find the whole document [here.](https://github.com/merihbozbura/merihbozbura.github.io/blob/master/files/Merih%20Bozbura.pdf)

![Image of Avatar The Last Airbender]()



```python

def minimum (time1, time2, lat1,lat2,lon1,lon2):

    for t in range(time1,time2):

        candidate_pressures = np.ndarray(0)


        for i in range(lat1,lat2):
            for j in range(lon1,lon2):


                index = {"lattitude": i , "longitude": j}

                rank_of_loop = np.append(rank_of_loop,index)


```





















