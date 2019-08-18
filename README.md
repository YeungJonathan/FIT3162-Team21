
# Project FAQ

### Overview
Species observations are entered by volunteers though an online application (https://www.environment.vic.gov.au/biodiversity/victorian-biodiversity-atlas/vba-go) that assures data completeness. New tools and citizen science contributions mean the number of observations contributed are rapidly growing. This is placing a burden on the expert verification processes as data validity currently needs to be confirmed by species experts before the data is stored in the observations repository known as Victorian Biodiversity Atlas (VBA)  

### The goal
The main goal of this project is to develop a predictive model that sorts new observations into high and low reliability categories with the intention of keeping the Victorian Biodiversity Atlas as up to date as possible. The categorisation will guide how DELWP best uses their experts’ time. The second goal is to identify predictors (variables) that have the most impact on successful categorisation.  

### Dataset
The DELWP Biodiversity Division is providing verified datasets of species observations with location, high and low reliability labels and collection method attributes for several selected species. HOWEVER it does not have any environmental data associated with the locations

### How to replicate expert reviewer
Using the environmental variables tied to each location, we need to model based on previously accepted records the determining features of the landscape that predict if it is likely the species will occur there and if not flag the observaton as an outlier.

### The problem
The dataset we are given does not contain environmental variables. Thus, we need to extract environmental variables from long, lat locations using raster data that has been provided to us.

# Steps
1. Get VBA data containing long, lat (location) for each species

# Before running:
```
brew install graphviz
pip install pandas
pip install sklearn
```

# Visualised Decision Tree
- execute main.py
- visualised tree in vba.pdf

# Potential errors
Do you have the following errors when running our project?  
Error 1: ImportError: Install xlrd >= 0.9.0 for Excel support  
Solution: pip install xlrd

# Not to the developers:
Please do not commit and push the raster data files to git. (for example vegtype3_4)
Just add it to your local as the size of it is too big. 

# ToDo
- Separate decision trees based on different species
- Handle raster data with QGIS
