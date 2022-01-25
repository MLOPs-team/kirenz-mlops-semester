import json, requests
import os, datetime
import pyspark
#import pandas as pd

#from databricks import koalas as ks
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.types import *
from pyspark.sql.functions import explode, split, col, sum, lit, udf
from pyspark.sql import SparkSession, Row
from pyspark.sql import functions as F
from delta import *
from delta.tables import *
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, ArrayType
from sklearn.preprocessing import LabelEncoder
import pyspark.pandas as ps
import json, shutil


# Clear any previous runs
shutil.rmtree("/tmp/delta-table", ignore_errors=True)

#blablab
sparkClassPath = os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages io.delta:delta-core_2.12:1.1.0 pyspark-shell org.apache.hadoop:hadoop-aws:3.2.0 com.amazonaws:aws-java-sdk-bundle:1.11.375 --conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" --conf "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog" --conf spark.hadoop.fs.s3a.access.key=AKIA25EGWZIMKSJ37HWM'


if __name__ == "__main__":
     # build spark session and enable sql extension & load sample data
    builder = pyspark.sql.SparkSession.builder.appName("NiklasTest") \
    .config("spark.driver.extraClassPath", sparkClassPath) \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") 
    spark = spark = configure_spark_with_delta_pip(builder).getOrCreate()
    sc = spark.sparkContext
    
    """ *- This part is skipped for the moment -*
    #Load Data from UK Police API - Niklas   
    reqForces = requests.get('https://data.police.uk/api/crimes-street-dates')
    jsonForces = reqForces.json()

    #Load Data from UK Police API - Pascal
    dataJson = []
    for month in jsonForces:
        if str(month['date']) > '2021-05':
            print(month['date'])
            for force in month['stop-and-search']:
                reqStopandSearch = requests.get('https://data.police.uk/api/stops-force?force=' + str(force) + '&date=' + str(month['date']))
                print('https://data.police.uk/api/stops-force?force=' + str(force) + '&date=' + str(month['date']))
                if reqStopandSearch.status_code == 200:
                    djson = reqStopandSearch.json()
                    for item in djson:
                        item['force'] = force
                        dataJson.append(item)
    print(dataJson)

    #json_rdd = sc.parallelize([dataJson])          
    #json_rdd = sc.parallelize([jsonForces])

    #data_df= pd.read_json(r.json(), lines=True)
    #print(data_df)
    """

    #labelEncoder = LabelEncoder()
    
    #dataString = '[{"age_range":"10-17","outcome":"Arrest","involved_person":true,"self_defined_ethnicity":"Other ethnic group - Not stated","gender":"Male","legislation":"Police and Criminal Evidence Act 1984 (section 1)","outcome_linked_to_object_of_search":null,"datetime":"2021-10-29T23:03:00+00:00","removal_of_more_than_outer_clothing":false,"outcome_object":{"id":"bu-arrest","name":"Arrest"},"location":null,"operation":null,"officer_defined_ethnicity":"White","type":"Person search","operation_name":null,"object_of_search":"Stolen goods","force":"avon-and-somerset"}]'
    #test="""{ "metadata": { "key": 84896, "value": 54 }}"""
    #rddJson = sc.parallelize([test])
    #print(rddJson)
    #df = ps.read.json(rddJson)
    json_data = '[{"age_range":"10-17","outcome":"Arrest","involved_person":true,"self_defined_ethnicity":"Other ethnic group - Not stated","gender":"Male","legislation":"Police and Criminal Evidence Act 1984 (section 1)","outcome_linked_to_object_of_search":null,"datetime":"2021-10-29T23:03:00+00:00","removal_of_more_than_outer_clothing":false,"outcome_object":{"id":"bu-arrest","name":"Arrest"},"location":null,"operation":null,"officer_defined_ethnicity":"White","type":"Person search","operation_name":null,"object_of_search":"Stolen goods","force":"avon-and-somerset"}]'
    json_rdd = sc.parallelize([json_data])
    #df = json_rdd.toDF()
    df = spark.read.json(json_rdd)
    #df = ps.read_json('[{"age_range":"10-17","outcome":"Arrest","involved_person":true,"self_defined_ethnicity":"Other ethnic group - Not stated","gender":"Male","legislation":"Police and Criminal Evidence Act 1984 (section 1)","outcome_linked_to_object_of_search":null,"datetime":"2021-10-29T23:03:00+00:00","removal_of_more_than_outer_clothing":false,"outcome_object":{"id":"bu-arrest","name":"Arrest"},"location":null,"operation":null,"officer_defined_ethnicity":"White","type":"Person search","operation_name":null,"object_of_search":"Stolen goods","force":"avon-and-somerset"}]', orient='columns')

    """
    # drop columns in dataframe
    def drop_columns(df, columns):
        df = df.drop(columns, axis=1)
        return df

    # enocde column in explicit dataframe
    def encode_column(dfColumn, values):
        labelEncoder.fit(values)
        dfColumn = labelEncoder.fit_transform(dfColumn)
        return dfColumn

    # encode datetime year
    def encode_year(df, column):
        df['year'] = df[column].dt.year
        return df

    # encode datetime month
    def encode_month(df, column):
        df['month'] = df[column].dt.year
        return df

    # encode datetime day
    def encode_day(df, column):
        df['day'] = df[column].dt.year
        return df

    # Normalize data set
    def normalize_dataframe(df):
        column_maxes = df.max()
        df_max = column_maxes.max()
        df_normalized = df / df_max
        return df_normalized


    # delete all rows with null values in the following columns
    df_cleared = df[df.age_range.notna() & df.gender.notna() & df.officer_defined_ethnicity.notna() & df.self_defined_ethnicity.notna() & df.object_of_search.notna() & df.location.notna() & df.legislation.notna()]


    # Split the DataFrame into noAction = 0 and Action = 1
    df_noAction = df_cleared[df_cleared.outcome.isin(['A no further action disposal'])]
    df_noAction.insert(loc=1, column='action', value=0)

    df_Action = df_cleared[df_cleared.outcome.isin(['Arrest', 'Community resolution', 'Summons / charged by post', 'Penalty Notice for Disorder', 'Khat or Cannabis warning', 'Caution (simple or conditional)'])]
    df_Action.insert(loc=1, column='action', value=1)

    df_cleared = ps.concat([df_noAction, df_Action])


    # Create a new column with the locationID
    df_cleared['locationId'] = df_cleared.location.apply(lambda x : x['street']['id'] if isinstance(x, dict) else x)


    # Columns that are not needed in silver status are deleted
    df_cleared = df_cleared.drop(['self_defined_ethnicity','outcome','outcome_linked_to_object_of_search', 'datetime', 'removal_of_more_than_outer_clothing', 'outcome_object',  'operation', 'operation_name', 'location'], axis=1)

    # encode column gender
    df_cleared = encode_column(df_cleared.gender, ['Male','Female', 'Other'])

    # encode column age_range
    df_cleared = encode_column(df_cleared.age_range, ['18-24','25-34', 'over 34', 'under 10'])

    # encode column force
    df_cleared = encode_column(df_cleared.force, ['avon-and-somerset', 'bedfordshire', 'btp', 'cambridgeshire',
        'cheshire', 'city-of-london', 'cleveland', 'cumbria', 'derbyshire',
        'devon-and-cornwall', 'dorset', 'durham', 'dyfed-powys', 'essex',
        'gloucestershire', 'hertfordshire', 'humberside', 'kent',
        'lancashire', 'leicestershire', 'norfolk', 'north-wales',
        'north-yorkshire', 'northamptonshire', 'northumbria',
        'nottinghamshire', 'south-yorkshire', 'staffordshire', 'suffolk',
        'surrey', 'sussex', 'thames-valley', 'warwickshire', 'west-mercia',
        'west-yorkshire', 'hampshire', 'lincolnshire', 'merseyside',
        'metropolitan', 'wiltshire'])


    # encode column object_of_search
    df_cleared = encode_column(df_cleared.object_of_search, ['Articles for use in criminal damage', 'Offensive weapons',
        'Controlled drugs', 'Stolen goods', 'Article for use in theft', 'Firearms', 'Fireworks',
        'Anything to threaten or harm anyone',
        'Evidence of offences under the Act', 'Psychoactive substances',
        'Game or poaching equipment',
        'Detailed object of search unavailable',
        'Evidence of wildlife offences', 'Seals or hunting equipment',
        'Goods on which duty has not been paid etc.', 'dog', 'Crossbows'])

    # encode officer_defined_ethnicit
    df_cleared = encode_column(df_cleared.officer_defined_ethnicit, ['White', 'Asian', 'Mixed', 'Black', 'Other'])

    # encode column self_defined_ethnicity
    df_cleared = encode_column(df_cleared.self_defined_ethnicity, ['White - English/Welsh/Scottish/Northern Irish/British',
        'Other ethnic group - Not stated',
        'White - Any other White background',
        'Black/African/Caribbean/Black British - Any other Black/African/Caribbean background',
        'Other ethnic group - Any other ethnic group',
        'Black/African/Caribbean/Black British - Caribbean',
        'Black/African/Caribbean/Black British - African', 'White - Irish',
        'Mixed/Multiple ethnic groups - White and Asian',
        'Mixed/Multiple ethnic groups - White and Black Caribbean',
        'Mixed/Multiple ethnic groups - Any other Mixed/Multiple ethnic background',
        'Asian/Asian British - Any other Asian background',
        'Asian/Asian British - Pakistani', 'Asian/Asian British - Indian',
        'Other ethnic group - Arab', 'Asian/Asian British - Bangladeshi',
        'Asian/Asian British - Chinese',
        'Mixed/Multiple ethnic groups - White and Black African',
        'White - Gypsy or Irish Traveller'])

    # encode column type
    df_cleared = encode_column(df_cleared.type, ['Person search', 'Person and Vehicle search', 'Vehicle search'])

    # encode column legislation
    df_cleared = encode_column(df_cleared.legislation , ['Police and Criminal Evidence Act 1984 (section 1)',
        'Misuse of Drugs Act 1971 (section 23)',
        'Firearms Act 1968 (section 47)',
        'Psychoactive Substances Act 2016 (s36(2))',
        'Criminal Justice Act 1988 (section 139B)',
        'Poaching Prevention Act 1862 (section 2)',
        'Criminal Justice and Public Order Act 1994 (section 60)',
        'Police and Criminal Evidence Act 1984 (section 6)',
        'Crossbows Act 1987 (section 4)',
        'Customs and Excise Management Act 1979 (section 163)',
        'Hunting Act 2004 (section 8)',
        'Protection of Badgers Act 1992 (section 11)',
        'Deer Act 1991 (section 12)',
        'Aviation Security Act 1982 (section 27(1))',
        'Conservation of Seals Act 1970 (section 4)',
        'Public Stores Act 1875 (section 6)',
        'Wildlife and Countryside Act 1981 (section 19)',
        'Environmental Protection Act 1990 (section 34B )'])

    # encode column involved person
    df_cleared = encode_column(df_cleared.involved_person, [True, False])

    # encode year
    df_cleared = encode_year(df_cleared, 'datetime')

    # encode month
    df_cleared = encode_month(df_cleared, 'datetime')

    #encode day
    df_cleared = encode_day(df_cleared, 'datetime')

    # normalize dataframe
    df_normalized = normalize_dataframe(df_cleared)
    
    #create df from JSON Content of UK Police API
    #df = spark.read.json(json_rdd)
    df.printSchema()
    df.show()
    df.describe()
    
    """
    #Save data as Delta Table
    df.write.format("delta").save("s3a://delta-lake-mlops/test")
    
    #Read out History of Table
    #deltaTable = DeltaTable.forPath(spark,"./delta-table")

    #fullHistoryDF = deltaTable.history()    # get the full history of the table
    #print(fullHistoryDF)
    #lastOperationDF = deltaTable.history(1) # get the last operation
    #print(lastOperationDF)
    

    spark.stop()