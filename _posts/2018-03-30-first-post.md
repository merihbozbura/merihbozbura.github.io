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



##### ** 1.Introduction**

The North Atlantic Oscillation (NAO) is a large-scale natural climate variability that has important impacts on the weather and climate of the North Atlantic region and surrounding continents, especially Europe. [#2]

Strong positive phase of NAO is associated with lower than normal temperatures over southern Europe and the Middle East and it is related to *lower than normal precipitation* over southern and central Europe.Unlike strong positive phase of NAO , negative phase is related to higher than normal temperature over southern Europe and the Middle East and it is associated with *higher than normal precipitation* over southern and central Europe.

Therefore, NAO is expected to have an impact on Turkey. Weather and climate conditions are controlled by NAO in Mediterranean basin along with Turkey.



##### ** 2.Data and Method**

Precipitation data is observation data and it includes all provinces of Turkey between 1970 and 2012. The North Atlantic Oscillation Index data can be found [here.](https://climatedataguide.ucar.edu/climate-data/hurrell-north-atlantic-oscillation-nao-index-pc-based) I merge two dataset into one **.csv** file. So, dataset have 83 variable, one of them is years, the other is NAO Indexes and the remain colums are 81 provinces of Turkey. 

Firstly, exploratory data analysis are applied to understand fundamentals features of precipitation data. Secondly, linear regression is applied to see whether there is a relationship between NAO and precipitation or not. Finally, principle component analysis is applied to understand effect of NAO on precipitation. 



 ##### ** 3.Exploratory Data Analysis**

Exploratory data analysis is an approach to analyse a data. [#3] Hypothesis is determined as there is a relationship between precipitation and NAO for this study.

Firstly, the csv file was read and then Shapiro-Wilk normality test is applied the precipitation data. P-values of Marmara, Ege, Karad- eniz, Akdeniz, Ic Anadolu, Dogu Anadolu, and Guneydogu Anadolu regions are respectively 0.001137, 2.65e-15, 2.2e- 16, 1.884e-12, 3.409e-13, 2.2e-16, and 3.668e-06. So, the null hypothesis of Shapiro-Wilk normality test that is the samples come from a normal distribution is rejected.

Csv file was read with **read.csv** and **subset** funciton was used to subset the data. Only processes of Marmara Region was shown as the example below. MarmaraReg variable is a list so before shapiro.test it needs to be **unlist** and then **as.numeric** since we need the numbers. You can check the type of a variable with **typeof()** function.

```r
P<-read.csv("Toplam_Yagis_Nao.csv",header = TRUE, sep=',') # Reads csv file

PPrep<-P[,-1] # Remove first line which is header

marmaraReg<-subset(PPrep, select = c("ckle","edir","ist","tkrd","yalv","kirk"
,"blke","blck","brsa","keli","skry")) # subsetting the provinces into regions

shapiro.test(as.numeric(unlist(marmaraReg)))
```

If you uses **View()** function, the read csv file is shown like in this image. ![blury.](https://github.com/merihbozbura/merihbozbura.github.io/blob/master/images/blury.jpg?raw=true)

Histogram of Marmara region has right skewed distribution. A few larger values bring the mean upwards. It is the closest region to normal distribution compared to the other regions and it is expected by looking Shapiro-Wilk normality test results. Also, other reginos are right skewed.[#4]

![marmaraHist.](https://github.com/merihbozbura/merihbozbura.github.io/blob/master/images/Hist_Marmara.jpeg?raw=true) 

Before constructing the histogram we need to split the data into intervals called bins. For all regions the equation below was used for bin width. **h** is bin width, **c** is a constant in the range of 2.0 and 2.6 (2.6 is optimal for Gaussian data), **IQR** is interquartile range, and **n** is number of data.

    h=(c*IQR)/(n1/3)    

```r
IQR_marmaraReg = IQR(as.numeric(unlist(marmaraReg))) #interquartile range

c = 2.6 # constant

n_marmaraReg = nrow(marmaraReg)*ncol(marmaraReg)  # number of data
bin_marmaraReg = (c*IQR_marmaraReg)/(n_marmaraReg^(1/3))
min(marmaraReg)   ; max(marmaraReg)

hist(as.numeric(unlist(marmaraReg)), main= "Annual Precipitation for Marmara 
Region 1970-2012", breaks = seq(min(marmaraReg),(max(marmaraReg)+bin_marmaraReg)
, by=bin_marmaraReg), col = "grey", xlab = "Annual Precipitation")

barplot(colMeans(as.matrix(PPrep[,1:81])), cex.names = .5,width = .835, xaxt = "n",col=rep(c("darkseagreen","coral1","thistle"),27), ylim = c(0,2800), main = 
"Mean Precipitation between 1970 and 2012", xlab = "Provinces", ylab = "Precipitation")

axis(1,at=1:81,tcl = -0.4)

meanofprep= mean(colMeans(as.matrix(PPrep[,1:81])))

abline(h=meanofprep , col="darkred")
```

As it is seen from above, **IQR** function directly calculates interquartile range. So, bin width for Marmara Region is calculated and histogram is plotted with **hist**. The maximum value is reached by adding the bin width to the minimum value, so the intervals of the histogram was formed. 

Also, a barplot was plotted with **barplot** to see is there any oddness in the data. For example, we know that Rize is the wettest province in Turkey and its annual precipitation is about 2000 mm. If Rize has 3000 mm precipitation in the barplot, we must suspect about the data whether it is accurate or not. Also, average value of Turkey's precipitation is drawn with **abline** on the barplot.

![barplot](https://github.com/merihbozbura/merihbozbura.github.io/blob/master/images/Barplot.jpeg?raw=true)


 ##### ** 4.Linear Regression**

Turkey has seven regions and linear regression is applied between each region and NAO index with **lm** function. P-values of Marmara, Ege, Karadeniz, Akdeniz, Ic Anadolu, Dogu Anadolu, and Guneydogu Anadolu regions are respectively 0.003816, 0.1888, 0.05551, 0.4469, 0.7868, 0.9588, and 0.7791. Only, Marmara region rejects the null hypothesis which is there is no relationship between precipitation and NAO. However other regions do not reject the null hypothesis. With **plot(fit_marmaraReg,which=1:4)**, Residual vs Fitted, Normal Q-Q, Scale Location, and Cook’s distance were plotted.


```r

fit_marmaraReg <- lm(PPrep[,82]~., data = marmaraReg)

summary(fit_marmaraReg)    

plot(fit_marmaraReg,which=1:4)

(colMeans(PPrep) - PPrep[41,] )== (2*colMeans(PPrep)) ### Rule of Thumb 

```

The **summary** of the linear model between Marmara region and NAO index is shown below.

![summary](https://github.com/merihbozbura/merihbozbura.github.io/blob/master/images/t.jpg?raw=true)

Marmara region is the independent variable and NAO index is the dependent variable in this linear model. 

    The equation of the model is NAOindex= 7.4118 − 0.0015 ∗ Canakkale + 0.0015 ∗ Edirne − 0.007 ∗ Istanbul+0.0032∗Tekirdag+0.0063∗Y alova−0.0008∗ 20 Kßrklareli − 0.0019 ∗ Balßkesir − 0.0044 ∗ Bilecik − 0.0035 ∗ Bursa + 0.0014 ∗ Kocaeli − 0.0045 ∗ Sakarya.
    
In addition to the Marmara region, Karadeniz and Ege regions are chosen to examine and linear regression is applied between each provinces of these three regions and NAO indexes. Provinces with significant p-values are obtained since they will be compared principle component analysis results to understand that pattern on precipitation belongs to NAO or not. 

Provinces with significant p-values are **Balıkesir, Bilecik, Bursa, Canakkale, Edirne, Istanbul, Kocaeli, Sakarya, Tekirdag, Yalova, Kırklareli, Amasya,Kastamonu,Rize,Izmir,Kütahya,andManisa.**    

Residual is the difference between fitted and actual dependent point. Fitted point is a predicted point by the model. There should be no **discernible pattern** around zero. As it is seen below, residuals and fitted values are almost randomly distributed around the zero line. Therefore, the model is not very good, but it fits the data.

![resiualvsfitted](https://github.com/merihbozbura/merihbozbura.github.io/blob/master/images/Residual_Fitted.jpeg?raw=true)

According to Normal Q-Q plot, residuals nearly folow the normal distribution.  

![Q-Q](https://github.com/merihbozbura/merihbozbura.github.io/blob/master/images/Normal_Q-Q.jpeg?raw=true)







#### **References**

[#2]: https://www.ncdc.noaa.gov/teleconnections/nao/

[#1]: https://publications.copernicus.org/for_authors/latex_instructions.html

[#3]: https://www.itl.nist.gov/div898/handbook/eda/section1/eda11.htm

**Wilks, D. S.** (2006). Statistical Methods in the Atmospheric Sciences (2nd ed., Vol. 91).








