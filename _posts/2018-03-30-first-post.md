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

*I will talk a little bit about meteorology since I mainly want to talk about the **R functions** to show how to achieve these statistical moethods.* So, if you want, you can find the whole document [here.](https://github.com/merihbozbura/merihbozbura.github.io/blob/master/files/Merih%20Bozbura.pdf) The document was written using Copernicus **LaTeX** template [#1].



#### **1.Introduction**

The North Atlantic Oscillation (NAO) is a large-scale natural climate variability that has important impacts on the weather and climate of the North Atlantic region and surrounding continents, especially Europe [#2].

Strong positive phase of NAO is associated with lower than normal temperatures over southern Europe and the Middle East and it is related to *lower than normal precipitation* over southern and central Europe.Unlike strong positive phase of NAO , negative phase is related to higher than normal temperature over southern Europe and the Middle East and it is associated with *higher than normal precipitation* over southern and central Europe.

Therefore, NAO is expected to have an impact on Turkey. Weather and climate conditions are controlled by NAO in Mediterranean basin along with Turkey.



#### **2.Data and Method**

Precipitation data is annual observation data in millimeters(mm) and it includes all provinces of Turkey between 1970 and 2012. The North Atlantic Oscillation Index data can be found [here.](https://climatedataguide.ucar.edu/climate-data/hurrell-north-atlantic-oscillation-nao-index-pc-based) I merge two dataset into one **.csv** file. So, dataset have 83 variable, one of them is years, the other is NAO Indexes and the remain colums are 81 provinces of Turkey. 

Firstly, exploratory data analysis are applied to understand fundamentals features of precipitation data. Secondly, linear regression is applied to see whether there is a relationship between NAO and precipitation or not. Finally, principle component analysis is applied to understand effect of NAO on precipitation. 



#### **3.Exploratory Data Analysis**

Exploratory data analysis is an approach to analyse a data [#3]. Hypothesis is determined as there is a relationship between precipitation and NAO for this study.

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

Histogram of Marmara region has right skewed distribution. A few larger values bring the mean upwards. It is the closest region to normal distribution compared to the other regions and it is expected by looking Shapiro-Wilk normality test results. Also, other reginos are right skewed.

![marmaraHist.](https://github.com/merihbozbura/merihbozbura.github.io/blob/master/images/Hist_Marmara.jpeg?raw=true) 

Before constructing the histogram we need to split the data into intervals called bins. For all regions the equation below was used for bin width. **h** is bin width, **c** is a constant in the range of 2.0 and 2.6 (2.6 is optimal for Gaussian data), **IQR** is interquartile range, and **n** is number of data.

    h=(c*IQR)/(n^1/3)   (Wilks, 2006, p.34)  

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


#### **4.Linear Regression**

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

    The equation of the model is NAOindex= 7.4118 − 0.0015 ∗ Canakkale + 0.0015 ∗ 
    Edirne − 0.007 * Istanbul + 0.0032 * Tekirdag+0.0063 * Yalova−0.0008 * Kirklareli
    − 0.0019 ∗ Balikesir − 0.0044 * Bilecik − 0.0035 * Bursa + 0.0014 * Kocaeli 
    − 0.0045 ∗ Sakarya.
    
In addition to the Marmara region, Karadeniz and Ege regions are chosen to examine and linear regression is applied between each provinces of these three regions and NAO indexes. Provinces with significant p-values are obtained since they will be compared principle component analysis results to understand that pattern on precipitation belongs to NAO or not. 

Provinces with significant p-values are **Balikesir, Bilecik, Bursa, Canakkale, Edirne, Istanbul, Kocaeli, Sakarya, Tekirdag, Yalova, Kirklareli, Amasya, Kastamonu, Rize, Izmir, Kütahya, and Manisa.**    

Residual is the difference between fitted and actual dependent point. Fitted point is a predicted point by the model. There should be no **discernible pattern** around zero. As it is seen below, residuals and fitted values are almost randomly distributed around the zero line. Therefore, the model is not very good, but it fits the data.



![resiualvsfitted](https://github.com/merihbozbura/merihbozbura.github.io/blob/master/images/Residual_Fitted.jpeg?raw=true)


![Q-Q](https://github.com/merihbozbura/merihbozbura.github.io/blob/master/images/Normal_Q-Q.jpeg?raw=true)

According to Normal Q-Q plot, residuals nearly folow the normal distribution. Also, in the Scale-Location plot, residuals are randomly distributed and there is no discernible pattern.

![scale-loca](https://github.com/merihbozbura/merihbozbura.github.io/blob/master/images/Scale_Location.jpeg?raw=true)

Cook’s distance is used to find dominant points in independent variables. These points are far from the other points. In this case, 29th and 41st points are little away from the other points and 40th point are far from the other points as it is shown below. If the Cook’s distance is greater than 0.5, that point can be influencial, so it is worthy to examine [#4]. Cook’s distance of 40th point is greater than 0.5. If exceeding point equals about two times of average of data, it should be examined [#5]. 40th point is not greater or equal to the two times of average of data. So, it is not *worthy* for investigating.

![Cooks](https://github.com/merihbozbura/merihbozbura.github.io/blob/master/images/Cooks.jpeg?raw=true)


#### **5.Principle Component Analysis**

Principal Component Analysis(PCA) is the oldest and the most famous multivariate statistical technique (Abdi and Williams, 2010). The goal of principal components analysis is to clarify th emaximum amount of variance with less number of principal components. It is used for reducing dimension of very **big datasets** in addition to keep most of the information in the **big dataset**. R function of principle component analysis pulls the data normal distribution with centring and scale arguments. Before applying PCA, precipitation data was scaled and standardized since the scale between NAO indexes and precipitation is large. Marmara region, Karadeniz and Ege regions are chosen to examine. In PCA, a new coordinate system is placed on the dataset, this is shown below. 


![coordinate](https://github.com/merihbozbura/merihbozbura.github.io/blob/master/images/Screen%20Shot%202018-04-01%20at%2013.51.25.png?raw=true){:height="30%" width="30%"}
Source: (Swan and Sandilands, 1995, p.446)



**Firstly**, scree plots or percent variance plots are examined to determine the number of principle components that are enough to explain dataset. According to the Kaiser’s Criterion, if eigenvalues are greater than 1, these PCs can be taken [#6]. **Secondly**, interpreting how much do variables contribute to the principle components by looking the loadings. **Finally**, interpreting and understanding distribution of the variables in this classification by examining the scores.

As it is mentioned above, *center* substracts the mean from each data point and *scale* divides each data point to standard deviation, after that **prcomp** function calculates the eigenvalues, loadings and scores. There is another function to do PCA which is **princomp()** in R that I haven't tried yet. 

The *eigenvalues* are the amount of variation along new axes kept by each PC. *Loadings* are the correlations between the variables and PCs. *Scores* are the positions of each data point in this new coordinate system. After obtainig eigenvalues, the variances is turned to percentage to plot. You can see summation of percent variances reach 100 % with cumulative summation **(cumsum)** function. **Percent variances** was plotted with *barplot* function with a red horizontal line on it as it is seen below. This horizontal red line is that if each variable devoted equally, they would devote 2.8% to the total variance since there are thirty six variables(number of provinces). **Fisrt fourteen** PCs represent 77.37% of the data. 

![percent](https://github.com/merihbozbura/merihbozbura.github.io/blob/master/images/Percent_Stand.jpeg?raw=true)

```r
pca <- prcomp(mar_kar_ege_s, center = TRUE, scale. = TRUE)

pca_sd <- pca$sdev  
loadings_pca <- pca$rotation
scores_pca <- pca$x

var_pca <- pca_sd^2  # Eigenvalues
var.percent_pca <- var_pca/sum(var_pca) * 100 # Explained variation by PCs.

cumvar <- cumsum(var.percent_pca) # Cumulative variance

barplot(var.percent_pca, xlab="PC", ylab="Percent Variance", names.arg=1:length(var.percent_pca), las=1, ylim=c(0,max(var.percent_pca)), col="gray", main = "Percent Variance for Scaled Data")
abline(h=1/ncol(mar_kar_ege_s)*100, col="red")

screeplot(pca, type = "lines", main = "Variances of PCs of Scaled Precipitation Data") 
# another function to plot variation of variance
abline(h = 1,lty = 3, col = "red")

loadings_pca

dev.new(height=7, width=7)
biplot(scores_pca[,1:14],loadings_pca[,1:14], cex = 0.8, main = "Distance Biplot of Scaled Precipitation") 
```

Also, there is another method to determine the number of principal components which is **scree plot** as it is shown below. According to Kaiser’s Criterion mentioned above, if eigenvalues are greater than 1, these PCs can be taken. So, blue dashed line shows that first fourteen PCs can be taken and they represent 77.37% of the dataset. To plot this graphic, **screeplot**
function was used as it seen from the code.


![scree](https://github.com/merihbozbura/merihbozbura.github.io/blob/master/images/Scree_Stand.jpeg?raw=true){:height="40%" width="40%"}

The distribution of the data points(rotation of original data points) in this new coordinate system is represented with **biplot** using scores(positions) and loadings(rotations). Biplot pops up in the screen like new window instead of appearing in R Studio's plot section with **dev.new** function and biplot is plotted with **biplot** function.


![biplot](https://github.com/merihbozbura/merihbozbura.github.io/blob/master/images/Stan_Biplot.jpeg?raw=true){:height="50%" width="50%"}
 
*According to biplot above*, Istanbul, Balikesir, Kirklareli, Manisa, Kastamonu, Canakkale are near each other and Bursa, Tekirdag, Gumushane, Yalova, Sakarya, and Izmir are near each other and Amasya, Bilecik, Kutahya, Bolu are near each other and Edirne, Kocaeli, and Rize are near each other. **These provinces are the provinces with significant p-values.** 

Also, Zonguldak, Giresun, Trabzon, Bartın, and Bayburt are near each other and Düzce, Afyon, Aydın are near each other and Tokat and Samsun are near each other. **These provinces are not the provinces with significant p-values.** 

Istanbul, Balıkesir, Kırklareli, Manisa, Kastamonu, Canakkale are near each other, so they can be used **interchangeably.**
Therefore, dimension can be reduced. Reducing dimension can be applied for **all the groups of provinces** that mentioned above.

Besides, principle component analysis was applied to the scaled precipitaiton data and you can read it in the [document](https://github.com/merihbozbura/merihbozbura.github.io/blob/master/files/Merih%20Bozbura.pdf) if you want. 

In this PC Analysis, Kutahya, Manisa, Izmir, Edirne, Kirklareli are near each other and Bolu, Yalova, Bursa, Istanbul, Balikesir, Canakkale, Tekirdag, Kastamonu, Bilecik, Sakarya, and Kocaeli are near each other. **These provinces are the provinces with significant p-values.** 

Also, Bartin, Zongudak, Karabuk, Gumushane, Tokat, Sinop, Trabzon, Giresun, Artvin, Samsun, Bayburt, and Ordu are near each other and Duzce, Afyon, Aydın are near each other and **these provinces are not the provinces with significant p-values.** Kütahya, Manisa, Izmir,Edirne, Kırklareli are near each other, so they can be used **interchangeably.**


#### **6.Conclusions**

* Exploratory data analysis is applied to understand the datasets and linear regression analysis is applied to find out whether there is a relationship or not between precipitation and NAO index datasets. 

* Only, Marmara region rejects the null hypothesis is found out and to investigate NAO’s effect, Ege and Karadeniz regions are choosen in addition to Marmara region. 

* Principle component analysis are applied to three region which contains *thirty six* provinces. As it is seen in section 4 and section 5, the provinces with **significant p-values** and **grouped provinces** that are obtained from **principle component analysis** are nearly same except few provinces. Also, Marmara region has significant p-value. In the light of these informations, **precipitation is affected by North Atlantic Oscillation can be said.**


If you want to see position of provinces, you can check it out [here.](http://cografyaharita.com/haritalarim/4lturkiye-mulki-idare-sistemleri-haritasi1.png)




### **References**

[#2]: https://www.ncdc.noaa.gov/teleconnections/nao/

[#1]: https://publications.copernicus.org/for_authors/latex_instructions.html

[#3]: https://www.itl.nist.gov/div898/handbook/eda/section1/eda11.htm

[#4]: https://onlinecourses.science.psu.edu/stat501/node/340

[#5]: http://polisci.msu.edu/jacoby/icpsr/regress3/lectures/week3/11.Outliers.pdf

[#6]: http://people.stat.sc.edu/habing/courses/530EFA.pdf

**Wilks, D. S.** (2006). Statistical Methods in the Atmospheric Sciences (2nd ed., Vol. 91).

**Abdi, H. and Williams, L. J.** Principal component analysis, Wiley 45 Interdisciplinary Reviews: Computational Statistics, 2, 433–459, doi:10.1002/wics.101, 2010.

**Swan, A.R.H., and M. Sandilands**, 1995. Introduction to Geological Data Analysis. Blackwell Science: Oxford, 446 p.





