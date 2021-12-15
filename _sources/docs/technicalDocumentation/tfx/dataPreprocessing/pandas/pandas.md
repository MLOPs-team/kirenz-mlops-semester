# Data Preprocessing with pandas

To examine the data set we used pandas. You can find more detailed information about pandas at this link: [Installation &#8212; pandas 1.3.5 documentation](https://pandas.pydata.org/docs/getting_started/install.html)

Install pandas with the following command :

```bash
conda install pandas
```

## Get Data from API

## Read json and understanding of dataset

First of all we read the json with pandas in a jupyter notebook

```python
import pandas as pd
import json

# Read json stop and searches
# https://data.police.uk/docs/method/stops-force/

filePath = r'C:\Users\Pasca\OneDrive\Desktop\tensorflow\delateExploration\dataPreprocessing\dataByForce.json'

df = pd.read_json(filePath, orient='columns')
```

---



After that, we took a first look at the dataset with the following command

```python
df
```

![](..\..\..\..\..\assets\img\2021-12-14-17-36-11-image.png)

---



To have a look how much columns and rows the dataset has, run the following commmand 

```
df.shape
```

Output: (422520, 17)

Our Dataset has 422520 rows and 17 columns

---



We then took a closer look at the dataset using df.info(). Here we could see well which columns there are in the dataset and of which data type they are. Furthermore we can get an overview how many non-null values there are per column in the dataset.

```python
# Info about the dataframe

df.info()
```

![](..\..\..\..\..\assets\img\2021-12-14-17-36-26-image.png)

---



It't also possible to get the columns an there type with the following command 

```python
# types of the dataset

df.dtypes
```

![](..\..\..\..\..\assets\img\2021-12-14-17-36-38-image.png)

---



After that we checked if there are any null values in each column

```python
df.isnull().any()
```

![](..\..\..\..\..\assets\img\2021-12-14-17-36-54-image.png)

If it's True the column has null values

---



In the command above, we saw that the data set contains null values. For this reason we have examined how many values in each column are null

```python
# number of null values in each column

df.isnull().sum()
```

![](..\..\..\..\..\assets\img\2021-12-14-17-37-06-image.png)

---



The data set contains a number of null values. To get a better sense of how much there is, let's check what percentage of the data has null values per column

```python
# Shows how much % of the data per column is null

df.isnull().sum() / df.shape[0]
```

![](..\..\..\..\..\assets\img\2021-12-14-17-50-35-image.png)

The outcome_linked_to_object_of_search has 70% null values. However, this is not further relevant, since the outcome is listed in the column outcome. Although the dataset has some null values, we still have enough after deleting the null values contained in the dataset

---



Get the Columns of the Dataset with the following comand:

```python
# columns of the dataset 

df.columns
```

![](..\..\..\..\..\assets\img\2021-12-14-17-55-01-image.png)

---



In the next step we check how much In the next step we look at how the gender distribution is in the data set 

```python
# distribution of gender
df['gender'].value_counts()
```

![](..\..\..\..\..\assets\img\2021-12-14-17-56-12-image.png)

As can already be seen in the statistics, significantly more men than women have been stopped. 

---



After that we checked what the distribution of age_range is in the dataset

```python
# age range 

df['age_range'].value_counts()
```

![](..\..\..\..\..\assets\img\2021-12-14-17-59-53-image.png)

As the statistics show, most of the people stopped are between 18 and 24 years old. Only 208 people under the age of 10 were checked. Whether these are relevant for our evaluation must be checked in the next steps.



---



```python
# ethnic categories => The self-defined ethnicity of the person stopped

df['self_defined_ethnicity'].value_counts()
```

![](..\..\..\..\..\assets\img\2021-12-14-18-03-32-image.png)

---



```python
# ethnic categories => The officer-defined ethnicity of the person stopped

df.officer_defined_ethnicity.value_counts()
```

![](..\..\..\..\..\assets\img\2021-12-14-18-04-20-image.png)

---



```python
df['outcome'].value_counts()
```

![](..\..\..\..\..\assets\img\2021-12-14-18-04-53-image.png)

---



```python
# How much % is null => only 1,5%

df.outcome.value_counts() / df.type.notnull().sum()
```

![](..\..\..\..\..\assets\img\2021-12-14-18-06-30-image.png)

---



```python
df['object_of_search'].value_counts()
```

![](..\..\..\..\..\assets\img\2021-12-14-18-07-21-image.png)

---



```python
# shows the forces in the dataframe
# force = county

df['force'].value_counts()
```

![](..\..\..\..\..\assets\img\2021-12-14-18-07-55-image.png)

---

## Cleaning of the dataset

After we have examined the dataset we will clean the dataset in the next step 





```python
# Cleanup of the DataFrame. All null values in the columns are deleted

df_cleared = df[df.age_range.notna() & df.gender.notna() & 
df.officer_defined_ethnicity.notna() & df.self_defined_ethnicity.notna()
 & df.object_of_search.notna() & df.location.notna() & 
df.legislation.notna()]
```
