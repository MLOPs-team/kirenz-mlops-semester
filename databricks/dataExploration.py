# Databricks notebook source
import numpy as np
import pandas as pd
import json

# Read json stop and searches

# Read Raw Data from JSON File, which was acquired in a separate script
rawdf = spark.read.json("/FileStore/shared_uploads/dataForces_2.json")
rawdf.printSchema()
rawdf.show()

# Write the raw data to its target in the delta lake
rawdf.write \
   .format('delta') \
   .mode('overwrite') \
   .save('s3a://delta-lake-mlops/dataForcesRaw')

# COMMAND ----------

# Start to build "Silver Standard" Dataframe
# Delete columns operation and operation_name because they do not hold any valuable data
df_silver = rawdf.drop('operation', 'operation_name')

# COMMAND ----------

# Write the silver dataframe in the delta lake
df_silver.write \
 .format('delta') \
 .mode('overwrite') \
 .save('s3a://delta-lake-mlops/dataForcesSilver')

# COMMAND ----------

# Prepare dataframe for gold status
# Drop all columns that are not needed for our model
df_gold = df_silver.drop('outcome_linked_to_object_of_search', 'datetime', 'removal_of_more_than_outer_clothing', 'outcome_object', 'location')

# COMMAND ----------

# Delete all rows with null values in the following columns
df_gold = df_gold.na.drop(subset=["outcome","age_range","involved_person", "gender","officer_defined_ethnicity","object_of_search","type","legislation", "force", 'self_defined_ethnicity'])

# COMMAND ----------

# Split the DataFrame into noAction = 0 and Action = 1
from pyspark.sql.functions import when, lit

# Introdurce new Column action for usage as a label for the classification later
df_gold = df_gold.withColumn("action", \
                     when((df_gold.outcome == "A no further action disposal"), lit(0)) \
                     .otherwise(lit(1)))
df_gold = df_gold.drop('outcome')

# COMMAND ----------

# Set Self Defined Ethnicity in new column to group people by their ethnicity
# This might be slightly racist, there also might be a more elegant way of doing this but it works
df_gold = df_gold.withColumn("self_defined_ethnicity_white", \
                     when(((df_gold.self_defined_ethnicity == 'White - English/Welsh/Scottish/Northern Irish/British') | \
                           (df_gold.self_defined_ethnicity == 'White - Any other White background') | (df_gold.self_defined_ethnicity=='White - Irish') | \
                           (df_gold.self_defined_ethnicity == 'White - Irish') | (df_gold.self_defined_ethnicity == 'White - Gypsy or Irish Traveller')), lit(1)) \
                     .otherwise(lit(0)))

df_gold = df_gold.withColumn("self_defined_ethnicity_black", \
                    when(((df_gold.self_defined_ethnicity == 'Black/African/Caribbean/Black British - Any other Black/African/Caribbean background') | \
                         (df_gold.self_defined_ethnicity == 'Black/African/Caribbean/Black British - African') | \
                         (df_gold.self_defined_ethnicity == 'Black/African/Caribbean/Black British - Caribbean')), lit(1)) \
                         .otherwise(lit(0)))

df_gold = df_gold.withColumn("self_defined_ethnicity_asian", \
                    when(((df_gold.self_defined_ethnicity == 'Asian/Asian British - Any other Asian background') | \
                         (df_gold.self_defined_ethnicity == 'Asian/Asian British - Pakistani') | \
                         (df_gold.self_defined_ethnicity == 'Asian/Asian British - Bangladeshi') | \
                         (df_gold.self_defined_ethnicity == 'Asian/Asian British - Indian') | \
                         (df_gold.self_defined_ethnicity == 'Asian/Asian British - Chinese')), lit(1)) \
                         .otherwise(lit(0)))

df_gold = df_gold.withColumn("self_defined_ethnicity_other", \
                    when(((df_gold.self_defined_ethnicity == 'Other ethnic group - Not stated') | \
                         (df_gold.self_defined_ethnicity == 'Other ethnic group - Any other ethnic group') | \
                         (df_gold.self_defined_ethnicity == 'Other ethnic group - Arab')), lit(1)) \
                         .otherwise(lit(0)))               

df_gold = df_gold.withColumn("self_defined_ethnicity_mixed", \
                    when(((df_gold.self_defined_ethnicity == 'Mixed/Multiple ethnic groups - Any other Mixed/Multiple ethnic background') | \
                         (df_gold.self_defined_ethnicity == 'Mixed/Multiple ethnic groups - White and Black Caribbean') | \
                          (df_gold.self_defined_ethnicity == 'Mixed/Multiple ethnic groups - White and Black African') | \
                         (df_gold.self_defined_ethnicity == 'Mixed/Multiple ethnic groups - White and Asian')), lit(1)) \
                         .otherwise(lit(0)))          

df_gold = df_gold.drop('self_defined_ethnicity')

# COMMAND ----------

# Encode data for Usage in TensorFlow Model Training
import pandas as pd
import re
from sklearn.preprocessing import LabelEncoder

df_gold_pd = df_gold.toPandas()
df_gold_pd_dummies = pd.get_dummies(df_gold_pd, columns=['force','gender', 'legislation', 'officer_defined_ethnicity', 'type', 'object_of_search'])

labelEncoder = LabelEncoder()

labelEncoder.fit(['10-17', '25-34', 'over 34', '18-24', 'under 10'])
df_gold_pd_dummies.age_range = labelEncoder.fit_transform(df_gold_pd_dummies.age_range)

df_gold_pd_dummies.columns = df_gold_pd_dummies.columns.str.replace(' ', '_', regex=False)
df_gold_pd_dummies.columns = df_gold_pd_dummies.columns.str.replace('.', '', regex=False)
df_gold_pd_dummies.columns = df_gold_pd_dummies.columns.str.replace('(', '_', regex=False)
df_gold_pd_dummies.columns = df_gold_pd_dummies.columns.str.replace(')', '', regex=False)
df_gold_pd_dummies.columns = df_gold_pd_dummies.columns.str.replace('-', '_', regex=False)

df_gold_encoded = spark.createDataFrame(df_gold_pd_dummies)

# COMMAND ----------

from pyspark.sql.types import IntegerType,BooleanType,DateType, FloatType
columns = [
 'age_range',
 'involved_person',
 'action',
 'self_defined_ethnicity_white',
 'self_defined_ethnicity_black',
 'self_defined_ethnicity_asian',
 'self_defined_ethnicity_other',
 'self_defined_ethnicity_mixed',
 'force_avon_and_somerset',
 'force_bedfordshire',
 'force_btp',
 'force_cambridgeshire',
 'force_cheshire',
 'force_city_of_london',
 'force_cleveland',
 'force_cumbria',
 'force_derbyshire',
 'force_devon_and_cornwall',
 'force_dorset',
 'force_durham',
 'force_dyfed_powys',
 'force_essex',
 'force_gloucestershire',
 'force_hampshire',
 'force_hertfordshire',
 'force_humberside',
 'force_kent',
 'force_lancashire',
 'force_leicestershire',
 'force_lincolnshire',
 'force_merseyside',
 'force_metropolitan',
 'force_norfolk',
 'force_north_wales',
 'force_north_yorkshire',
 'force_northamptonshire',
 'force_northumbria',
 'force_nottinghamshire',
 'force_south_yorkshire',
 'force_staffordshire',
 'force_suffolk',
 'force_sussex',
 'force_thames_valley',
 'force_warwickshire',
 'force_west_mercia',
 'force_west_yorkshire',
 'force_wiltshire',
 'gender_Female',
 'gender_Male',
 'gender_Other',
 'legislation_Aviation_Security_Act_1982__section_27_1',
 'legislation_Conservation_of_Seals_Act_1970__section_4',
 'legislation_Criminal_Justice_Act_1988__section_139B',
 'legislation_Criminal_Justice_and_Public_Order_Act_1994__section_60',
 'legislation_Crossbows_Act_1987__section_4',
 'legislation_Customs_and_Excise_Management_Act_1979__section_163',
 'legislation_Deer_Act_1991__section_12',
 'legislation_Environmental_Protection_Act_1990__section_34B_',
 'legislation_Firearms_Act_1968__section_47',
 'legislation_Hunting_Act_2004__section_8',
 'legislation_Misuse_of_Drugs_Act_1971__section_23',
 'legislation_Poaching_Prevention_Act_1862__section_2',
 'legislation_Police_and_Criminal_Evidence_Act_1984__section_1',
 'legislation_Police_and_Criminal_Evidence_Act_1984__section_6',
 'legislation_Protection_of_Badgers_Act_1992__section_11',
 'legislation_Psychoactive_Substances_Act_2016__s36_2',
 'legislation_Psychoactive_Substances_Act_2016__s37_2',
 'legislation_Public_Stores_Act_1875__section_6',
 'legislation_Wildlife_and_Countryside_Act_1981__section_19',
 'officer_defined_ethnicity_Asian',
 'officer_defined_ethnicity_Black',
 'officer_defined_ethnicity_Mixed',
 'officer_defined_ethnicity_Other',
 'officer_defined_ethnicity_White',
 'type_Person_and_Vehicle_search',
 'type_Person_search',
 'type_Vehicle_search',
 'object_of_search_Anything_to_threaten_or_harm_anyone',
 'object_of_search_Article_for_use_in_theft',
 'object_of_search_Articles_for_use_in_criminal_damage',
 'object_of_search_Controlled_drugs',
 'object_of_search_Crossbows',
 'object_of_search_Detailed_object_of_search_unavailable',
 'object_of_search_Evidence_of_offences_under_the_Act',
 'object_of_search_Evidence_of_wildlife_offences',
 'object_of_search_Firearms',
 'object_of_search_Fireworks',
 'object_of_search_Game_or_poaching_equipment',
 'object_of_search_Goods_on_which_duty_has_not_been_paid_etc',
 'object_of_search_Offensive_weapons',
 'object_of_search_Psychoactive_substances',
 'object_of_search_Seals_or_hunting_equipment',
 'object_of_search_Stolen_goods',
 'object_of_search_dog']

for x in columns:
    df_gold_encoded = df_gold_encoded.withColumn(x, df_gold_encoded[x].cast(FloatType()))

df_gold_encoded = df_gold_encoded.withColumn('age_range', df_gold_encoded['age_range'].cast(IntegerType()))

# COMMAND ----------

# Write the Gold Dataframe in the Delta Lake
df_gold_encoded.write \
 .format('delta') \
 .mode('overwrite') \
 .save('s3a://delta-lake-mlops/dataForcesGold')

# COMMAND ----------

df_gold_encoded.dtypes
