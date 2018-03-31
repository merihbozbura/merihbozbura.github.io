---
layout: post
title: Principle Component Analysis with R
---

#### **The North Atlantic Oscillation Has an Effect on Western Turkey's Precipitation Pattern**

This is one of the subjects that I am curious about. So, I have shortly worked on it. You can use these statistical methods on any kind of data that you want to study. Outline of this case as follows:

    1. Introduction
    2. Data and Method
    3. Exploratory Data Analysis
    4. Linear Regression
    5. Principle Component Analysis
    6. Conclusions

*I will talk a little bit about meteorology since I mainly want to talk about the **R functions** to show how to achieve these statistical moethods.* So, if you want, you can find the whole document [here.](https://github.com/merihbozbura/merihbozbura.github.io/blob/master/files/Merih%20Bozbura.pdf) The document was written using Copernicus **LaTeX** template. [#1]



##### **Introduction**

The North Atlantic Oscillation (NAO) is a large-scale natural climate variability that has important impacts on the weather and climate of the North Atlantic region and surrounding continents, especially Europe. [#2]

Strong positive phase of NAO is associated with lower than normal temperatures over southern Europe and the Middle East and it is related to *lower than normal precipitation* over southern and central Europe.Unlike strong positive phase of NAO , negative phase is related to higher than normal temperature over southern Europe and the Middle East and it is associated with *higher than normal precipitation* over southern and central Europe.

Therefore, NAO is expected to have an impact on Turkey. Weather and climate conditions are controlled by NAO in Mediterranean basin along with Turkey.



##### **Data and Method**

Precipitation data is observation data and it includes all provinces of Turkey between 1970 and 2012. The North Atlantic Oscillation Index data can be found [here.](https://climatedataguide.ucar.edu/climate-data/hurrell-north-atlantic-oscillation-nao-index-pc-based) I merge two dataset into one **.csv** file. So, dataset have 83 variable, one of them is years, the other is NAO Indexes and the remain colums are 81 provinces of Turkey. 

Firstly, exploratory data analysis are applied to understand fundamentals features of precipitation data. Secondly, linear regression is applied to see whether there is a relationship between NAO and precipitation or not. Finally, principle component analysis is applied to understand effect of NAO on precipitation. 



 **Exploratory Data Analysis**

Exploratory data analysis is an approach to analyse a data. [#3] Hypothesis is determined as there is a relationship between precipitation and NAO for this study.

Firstly, the csv file was read and then Shapiro-Wilk normality test is applied the precipitation data. P-values of Marmara, Ege, Karad- eniz, Akdeniz, Ic Anadolu, Dogu Anadolu, and Guneydogu Anadolu regions are respectively 0.001137, 2.65e-15, 2.2e- 16, 1.884e-12, 3.409e-13, 2.2e-16, and 3.668e-06. So, the null hypothesis of Shapiro-Wilk normality test that is the samples come from a normal distribution is rejected.

Csv file was read with **read.csv** and **subset** funciton was used to subset the data. Only processes of Marmara Region was shown as the example below. MarmaraReg variable is a list so before shapiro.test it needs to be **unlist** and then **as.numeric** since we need the numbers. You can check the type of a variable with **typeof()** function.

```r
P<-read.csv("Toplam_Yagis_Nao.csv",header = TRUE, sep=',') # Reads csv file

PPrep<-P[,-1] # Remove first line which is header

marmaraReg<-subset(PPrep, select = c("ckle","edir","ist","tkrd","yalv",
"kirk","blke","blck","brsa","keli","skry")) # subsetting the provinces into regions

shapiro.test(as.numeric(unlist(marmaraReg)))
```
If you uses **View()** function, the read csv file is shown like in this ![image.](https://github.com/merihbozbura/merihbozbura.github.io/blob/master/images/blury.jpg?raw=true)

Histogram of Marmara region has right skewed distribution as it is stated in the ![image.](https://github.com/merihbozbura/merihbozbura.github.io/blob/master/images/Hist_Marmara.jpeg?raw=true) 

A few larger values bring the mean upwards. It is the closest region to normal distribution compared to the other regions and it is expected by looking Shapiro-Wilk normality test results. Also, other reginos are right skewed.[#4]

```r
IQR_marmaraReg = IQR(as.numeric(unlist(marmaraReg))) #interquartile range

c = 2.6 # constant

n_marmaraReg = nrow(marmaraReg)*ncol(marmaraReg)  # number of data
bin_marmaraReg = (c*IQR_marmaraReg)/(n_marmaraReg^(1/3))
min(marmaraReg)   ; max(marmaraReg)

hist(as.numeric(unlist(marmaraReg)), main= "Annual Precipitation for Marmara Region 1970-2012", breaks = seq(min(marmaraReg),(max(marmaraReg)+bin_marmaraReg), by=bin_marmaraReg), col = "grey", xlab = "Annual Precipitation")
```





#### **References**

[#2]: https://www.ncdc.noaa.gov/teleconnections/nao/

[#1]: https://publications.copernicus.org/for_authors/latex_instructions.html

[#3]: https://www.itl.nist.gov/div898/handbook/eda/section1/eda11.htm

**Wilks, D. S.** (2006). Statistical Methods in the Atmospheric Sciences (2nd ed., Vol. 91).








