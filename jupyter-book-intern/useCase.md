---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.5
kernelspec:
  display_name: Python 3.9.7 64-bit (windows store)
  name: python3
---

# Our use case

### Summary

The goal is to make predictions about the safety of a city/area. Ideally we want to provide a safety index that can be used to rate the safety of a city the user wants to visit. 

#### Data sources

We have a few data sources in mind that can be used to calculate the desired index. We want to start with a few and expand the list of data sources over time. 

- One (or multiple) data sources about criminal data. The API should/could include: Commited crimes (+ date of the crime) as a baseline to the safety of the city, this can be used as dependent variable y
- Weather data, as the weather may affect criminal activity
- Events: For example football games may provide for more crime
- Calendar data. Here we can check whether a given date is a Weekend day or any kind of public holiday
- ... more data sources may be used to further improve the quality of the index 

For the criminal data we found a data source of the police in UK. We need to check whether we can use that as a primary data source. 

#### MLOPS driven

The whole process should be guided by a MLOPS-driven workflow. If we want to add more data to make the index more accurate and therefore more meaningfull it should be easy to rebuild all components in the whole pipeline and redeploy the application that the end user wants to use. Also if we want to change something in the UI it should be possible to only rebuild the UI application and keep the remainder of the stack untouched. 

#### Visualization

The whole data should be visualized in a web application in the browser. Users should be able to view the criminal index on a map and also be able to view the index for a specific area they are looking for. The website must be publicly accessible, authorization will not be part of the website.
