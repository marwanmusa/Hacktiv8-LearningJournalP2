# -*- coding: utf-8 -*-
"""spark_example.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mIceuyJdUYLTQ2DrCIWhWfm-FkO11exb

# Spark Example

PySpark applications start with initializing SparkSession which is the entry point of PySpark as below. In case of running it in PySpark shell via pyspark executable, the shell automatically creates the session in the variable spark for users.
"""

from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

"""## DataFrame Creation

A PySpark DataFrame can be created via pyspark.sql.SparkSession.createDataFrame typically by passing a list of lists, tuples, dictionaries and pyspark.sql.Rows, a pandas DataFrame and an RDD consisting of such a list. pyspark.sql.SparkSession.createDataFrame takes the schema argument to specify the schema of the DataFrame. When it is omitted, PySpark infers the corresponding schema by taking a sample from the data.

Firstly, you can create a PySpark DataFrame from a list of rows
"""

from datetime import datetime, date
import pandas as pd
from pyspark.sql import Row

df = spark.createDataFrame([
    Row(a=1, b=2., c='string1', d=date(2000, 1, 1), e=datetime(2000, 1, 1, 12, 0)),
    Row(a=2, b=3., c='string2', d=date(2000, 2, 1), e=datetime(2000, 1, 2, 12, 0)),
    Row(a=4, b=5., c='string3', d=date(2000, 3, 1), e=datetime(2000, 1, 3, 12, 0))
])
df

"""Create a PySpark DataFrame with an explicit schema."""

df = spark.createDataFrame([
    (1, 2., 'string1', date(2000, 1, 1), datetime(2000, 1, 1, 12, 0)),
    (2, 3., 'string2', date(2000, 2, 1), datetime(2000, 1, 2, 12, 0)),
    (3, 4., 'string3', date(2000, 3, 1), datetime(2000, 1, 3, 12, 0))
], schema='a long, b double, c string, d date, e timestamp')
df

"""Create a PySpark DataFrame from a pandas DataFrame"""

pandas_df = pd.DataFrame({
    'a': [1, 2, 3],
    'b': [2., 3., 4.],
    'c': ['string1', 'string2', 'string3'],
    'd': [date(2000, 1, 1), date(2000, 2, 1), date(2000, 3, 1)],
    'e': [datetime(2000, 1, 1, 12, 0), datetime(2000, 1, 2, 12, 0), datetime(2000, 1, 3, 12, 0)]
})
df = spark.createDataFrame(pandas_df)
df

"""Create a PySpark DataFrame from an RDD consisting of a list of tuples."""

rdd = spark.sparkContext.parallelize([
    (1, 2., 'string1', date(2000, 1, 1), datetime(2000, 1, 1, 12, 0)),
    (2, 3., 'string2', date(2000, 2, 1), datetime(2000, 1, 2, 12, 0)),
    (3, 4., 'string3', date(2000, 3, 1), datetime(2000, 1, 3, 12, 0))
])
df = spark.createDataFrame(rdd, schema=['a', 'b', 'c', 'd', 'e'])
df

"""The DataFrames created above all have the same results and schema."""

# All DataFrames above result same.
df.show()
df.printSchema()

"""## Viewing Data

The top rows of a DataFrame can be displayed using DataFrame.show().
"""

df.show(1)

"""Alternatively, you can enable spark.sql.repl.eagerEval.enabled configuration for the eager evaluation of PySpark DataFrame in notebooks such as Jupyter. The number of rows to show can be controlled via spark.sql.repl.eagerEval.maxNumRows configuration."""

spark.conf.set('spark.sql.repl.eagerEval.enabled', True)
df

"""The rows can also be shown vertically. This is useful when rows are too long to show horizontally."""

df.show(1, vertical=True)

"""You can see the DataFrame’s schema and column names as follows:"""

df.columns

df.printSchema()

"""Show the summary of the DataFrame"""

df.select("a", "b", "c").describe().show()

"""DataFrame.collect() collects the distributed data to the driver side as the local data in Python. Note that this can throw an out-of-memory error when the dataset is too large to fit in the driver side because it collects all the data from executors to the driver side."""

df.collect()

"""In order to avoid throwing an out-of-memory exception, use DataFrame.take() or DataFrame.tail()."""

df.take(1)

"""PySpark DataFrame also provides the conversion back to a pandas DataFrame to leverage pandas APIs. Note that toPandas also collects all data into the driver side that can easily cause an out-of-memory-error when the data is too large to fit into the driver side."""

df.toPandas()

"""## Selecting and Accessing Data

PySpark DataFrame is lazily evaluated and simply selecting a column does not trigger the computation but it returns a Column instance.
"""

df.a

from pyspark.sql import Column
from pyspark.sql.functions import upper

type(df.c) == type(upper(df.c)) == type(df.c.isNull())

"""These Columns can be used to select the columns from a DataFrame. For example, DataFrame.select() takes the Column instances that returns another DataFrame."""

df.select(df.c).show()

"""Assign new Column instance."""

df.withColumn('upper_c', upper(df.c)).show()

"""To select a subset of rows, use DataFrame.filter()."""

df.filter(df.a == 1).show()

"""## Applying a Function

PySpark supports various UDFs and APIs to allow users to execute Python native functions. See also the latest Pandas UDFs and Pandas Function APIs. For instance, the example below allows users to directly use the APIs in a pandas Series within Python native function.
"""

import pandas
from pyspark.sql.functions import pandas_udf

@pandas_udf('long')
def pandas_plus_one(series: pd.Series) -> pd.Series:
    # Simply plus one by using pandas Series.
    return series + 1

df.select(pandas_plus_one(df.a)).show()

"""Another example is DataFrame.mapInPandas which allows users directly use the APIs in a pandas DataFrame without any restrictions such as the result length."""

def pandas_filter_func(iterator):
    for pandas_df in iterator:
        yield pandas_df[pandas_df.a == 1]

df.mapInPandas(pandas_filter_func, schema=df.schema).show()

"""## Grouping Data

PySpark DataFrame also provides a way of handling grouped data by using the common approach, split-apply-combine strategy. It groups the data by a certain condition applies a function to each group and then combines them back to the DataFrame.
"""

df = spark.createDataFrame([
    ['red', 'banana', 1, 10], ['blue', 'banana', 2, 20], ['red', 'carrot', 3, 30],
    ['blue', 'grape', 4, 40], ['red', 'carrot', 5, 50], ['black', 'carrot', 6, 60],
    ['red', 'banana', 7, 70], ['red', 'grape', 8, 80]], schema=['color', 'fruit', 'v1', 'v2'])
df.show()

"""Grouping and then applying the avg() function to the resulting groups."""

df.groupby('color').avg().show()

"""You can also apply a Python native function against each group by using pandas APIs."""

def plus_mean(pandas_df):
    return pandas_df.assign(v1=pandas_df.v1 - pandas_df.v1.mean())

df.groupby('color').applyInPandas(plus_mean, schema=df.schema).show()

"""Co-grouping and applying a function."""

df1 = spark.createDataFrame(
    [(20000101, 1, 1.0), (20000101, 2, 2.0), (20000102, 1, 3.0), (20000102, 2, 4.0)],
    ('time', 'id', 'v1'))

df2 = spark.createDataFrame(
    [(20000101, 1, 'x'), (20000101, 2, 'y')],
    ('time', 'id', 'v2'))

def asof_join(l, r):
    return pd.merge_asof(l, r, on='time', by='id')

df1.groupby('id').cogroup(df2.groupby('id')).applyInPandas(
    asof_join, schema='time int, id int, v1 double, v2 string').show()

"""## Getting Data in/out

CSV is straightforward and easy to use. Parquet and ORC are efficient and compact file formats to read and write faster.

There are many other data sources available in PySpark such as JDBC, text, binaryFile, Avro, etc. See also the latest Spark SQL, DataFrames and Datasets Guide in Apache Spark documentation.
"""

df.write.csv('ftds.csv', header=True)
spark.read.csv('ftds.csv', header=True).show()

"""## Working with SQL

DataFrame and Spark SQL share the same execution engine so they can be interchangeably used seamlessly. For example, you can register the DataFrame as a table and run a SQL easily as below:
"""

df.createOrReplaceTempView("tableA")
spark.sql("SELECT count(*) from tableA").show()

"""In addition, UDFs can be registered and invoked in SQL out of the box:"""

import pandas
from pyspark.sql.functions import pandas_udf

@pandas_udf("integer")
def add_one(s: pd.Series) -> pd.Series:
    return s + 1

spark.udf.register("add_one", add_one)
spark.sql("SELECT add_one(v1) FROM tableA").show()

"""These SQL expressions can directly be mixed and used as PySpark columns."""

from pyspark.sql.functions import expr

df.selectExpr('add_one(v1)').show()
df.select(expr('count(*)') > 0).show()

"""## Spark Data Practice"""

import pandas as pd
from pyspark.sql import SparkSession
from pyspark.context import SparkContext
from pyspark.sql.functions import *
from pyspark.sql.types import *
from datetime import date, timedelta, datetime
import time

"""First of all, a Spark session needs to be initialized. With the help of SparkSession, DataFrame can be created and registered as tables. Moreover, SQL tables are executed, tables can be cached, and parquet/JSON/CSV/Avro data formatted files can be read."""

sc = SparkSession.builder.appName("PysparkFTDS")\
.config ("spark.sql.shuffle.partitions", "50")\
.config("spark.driver.maxResultSize","5g")\
.config ("spark.sql.execution.arrow.enabled", "true")\
.getOrCreate()

"""### Creating DataFrame

dataset [here](https://www.kaggle.com/cmenca/new-york-times-hardcover-fiction-best-sellers)

DataFrames can be created by reading text, CSV, JSON, and Parquet file formats. In our example, we will be using a .json formatted file. You can also find and read text, CSV, and Parquet file formats by using the related read functions as shown below.
"""

#Creates a spark data frame called as raw_data.

#JSON
dataframe = sc.read.json('nyt2.json')

#TXT FILES
# dataframe_txt = sc.read.text('text_data.txt')

#CSV FILES
# dataframe_csv = sc.read.csv('csv_data.csv')

#PARQUET FILES
# dataframe_parquet = sc.read.load('parquet_data.parquet')

"""### Duplicates"""

dataframe.show(10)

"""Duplicate values in a table can be eliminated by using dropDuplicates() function."""

dataframe_dropdup = dataframe.dropDuplicates()
dataframe_dropdup.show(10)

"""### Queries

"Select" Operation

It is possible to obtain columns by attribute `("author")` or by indexing `(dataframe['author'])`.
"""

#Show all entries in title column
dataframe.select("author").show(10)

#Show all entries in title, author, rank, price columns
dataframe.select("author", "title", "rank", "price").show(10)

"""The 'title' column is selected and a condition is added with a 'when' condition."""

# Show title and assign 0 or 1 depending on title
dataframe.select("title", when(dataframe.title != 'ODD HOURS', 1).otherwise(0)).show(10)

"""The “isin” operation is applied instead of “when” which can be also used to define some conditions to rows."""

# Show rows with specified authors if in the given options

dataframe [dataframe.author.isin("John Sandford", "Emily Giffin")].show(5)

"""In the brackets of the “Like” function, the % character is used to filter out all titles having the “ THE ” word. If the condition we are looking for is the exact match, then no % character shall be used."""

# Show author and title is TRUE if title has " THE " word in titles

dataframe.select("author", "title", dataframe.title.like("% THE %")).show(15)

"""StartsWith scans from the beginning of word/content with specified criteria in the brackets. In parallel, EndsWith processes the word/content starting from the end. Both of the functions are case-sensitive."""

dataframe.select("author", "title", dataframe.title.startswith("THE")).show(5)

dataframe.select("author", "title", dataframe.title.endswith("NT")).show(5)

"""Substring functions to extract the text between specified indexes. In the following examples, texts are extracted from the index numbers (1, 3), (3, 6), and (1, 6)."""

dataframe.select(dataframe.author.substr(1, 3).alias("title")).show(5)
dataframe.select(dataframe.author.substr(3, 6).alias("title")).show(5)
dataframe.select(dataframe.author.substr(1, 6).alias("title")).show(5)

"""Adding Columns"""

# Lit() is required while we are creating columns with exact values.

dataframe = dataframe.withColumn('new_column', lit('This is a new column'))

dataframe.show(5)

"""Updating Columns"""

dataframe = dataframe.withColumnRenamed('amazon_product_url', 'URL')

dataframe.show(5)

"""Removing Columns"""

dataframe_remove = dataframe.drop("publisher", "published_date").show(5)

dataframe_remove2 = dataframe.drop(dataframe.publisher).drop(dataframe.published_date).show(5)

"""### Inspect Data"""

# Returns dataframe column names and data types
dataframe.dtypes

# Displays the content of dataframe
dataframe.show()

# Return first n rows
dataframe.head()

# Returns first row
dataframe.first()

# Return first n rows
dataframe.take(5)

# Computes summary statistics
dataframe.describe().show()

# Returns columns of dataframe
dataframe.columns

# Counts the number of rows in dataframe
dataframe.count()

# Counts the number of distinct rows in dataframe
dataframe.distinct().count()

# Prints plans including physical and logical
dataframe.explain()

"""### GroupBy"""

# Group by author, count the books of the authors in the groups

dataframe.groupBy("author").count().show(10)

"""### Filter"""

# Filtering entries of title
# Only keeps records having value 'THE HOST'

dataframe.filter(dataframe["title"] == 'THE HOST').show(5)

"""### Missing & Replacing Values"""

# Replace null values
dataframe.na.fill(50).show(5)

# Return new dataframe restricting rows with null values
dataframe.na.drop().show(5)

# Return new dataframe replacing one value with another
dataframe.na.replace(10, 20).show(5)

"""### Repartitioning

It is possible to increase or decrease the existing level of partitioning in RDD Increasing can be actualized by using the repartition(self, numPartitions) function which results in a new RDD that obtains the higher number of partitions. Decreasing can be processed with coalesce(self, numPartitions, shuffle=False) function that results in a new RDD with a reduced number of partitions to a specified number.
"""

# Dataframe with 10 partitions
dataframe.repartition(10).rdd.getNumPartitions()

# Dataframe with 1 partition
dataframe.coalesce(1).rdd.getNumPartitions()

"""### Running SQL Queries Programmatically

Raw SQL queries can also be used by enabling the “sql” operation on our SparkSession to run SQL queries programmatically and return the result sets as DataFrame structures.
"""

# Registering a table
dataframe.registerTempTable("df")

sc.sql("select * from df").show(3)


sc.sql("select \
               CASE WHEN description LIKE '%love%' THEN 'Love_Theme' \
               WHEN description LIKE '%hate%' THEN 'Hate_Theme' \
               WHEN description LIKE '%happy%' THEN 'Happiness_Theme' \
               WHEN description LIKE '%anger%' THEN 'Anger_Theme' \
               WHEN description LIKE '%horror%' THEN 'Horror_Theme' \
               WHEN description LIKE '%death%' THEN 'Criminal_Theme' \
               WHEN description LIKE '%detective%' THEN 'Mystery_Theme' \
               ELSE 'Other_Themes' \
               END Themes \
       from df").groupBy('Themes').count().show()

"""### Output"""

# Converting dataframe into an RDD
rdd_convert = dataframe.rdd

# Converting dataframe into a RDD of string
dataframe.toJSON().first()

# Obtaining contents of df as Pandas dataFrame
dataframe.toPandas()

# Write & Save File in .parquet format
dataframe.select("author", "title", "rank", "description")\
.write \
.save("Rankings_Descriptions.parquet")

# Write & Save File in .json format
dataframe.select("author", "title") \
.write \
.save("Authors_Titles.json",format="json")

# End Spark Session 
sc.stop()

"""## Multiclass Text Classifications

Loading a CSV file dataset [here](https://www.kaggle.com/kaggle/san-francisco-crime-classification?select=train.csv)
"""

from pyspark.sql import SQLContext

data = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load('train.csv')

"""Remove the columns we do not need and have a look the first five rows:"""

drop_list = ['Dates', 'DayOfWeek', 'PdDistrict', 'Resolution', 'Address', 'X', 'Y']
data = data.select([column for column in data.columns if column not in drop_list])
data.show(5)

"""Apply printSchema() on the data which will print the schema in a tree format:"""

data.printSchema()

"""Top 20 crime categories:"""

from pyspark.sql.functions import col
data.groupBy("Category") \
    .count() \
    .orderBy(col("count").desc()) \
    .show()

"""Top 20 crime descriptions:"""

data.groupBy("Descript") \
    .count() \
    .orderBy(col("count").desc()) \
    .show()

"""Model Pipeline

Spark Machine Learning Pipelines API is similar to Scikit-Learn. Spark pipeline includes three steps:

- regexTokenizer: Tokenization (with Regular Expression)
- stopwordsRemover: Remove Stop Words
- countVectors: Count vectors (“document-term vectors”)
"""

from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, CountVectorizer
from pyspark.ml.classification import LogisticRegression

# regular expression tokenizer
regexTokenizer = RegexTokenizer(inputCol="Descript", outputCol="words", pattern="\\W")

# stop words
add_stopwords = ["http","https","amp","rt","t","c","the"] 
stopwordsRemover = StopWordsRemover(inputCol="words", outputCol="filtered").setStopWords(add_stopwords)

# bag of words count
countVectors = CountVectorizer(inputCol="filtered", outputCol="features", vocabSize=10000, minDF=5)

"""StringIndexer

StringIndexer encodes a string column of labels to a column of label indices. The indices are in `(0, numLabels)`, ordered by label frequencies, so the most frequent label gets index `0`.

In our case, the label column (Category) will be encoded to label indices, from 0 to 32; the most frequent label (LARCENY/THEFT) will be indexed as 0.
"""

from pyspark.ml import Pipeline
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler
label_stringIdx = StringIndexer(inputCol = "Category", outputCol = "label")
pipeline = Pipeline(stages=[regexTokenizer, stopwordsRemover, countVectors, label_stringIdx])

# Fit the pipeline to training documents.
pipelineFit = pipeline.fit(data)
dataset = pipelineFit.transform(data)
dataset.show(5)

"""Partition Training & Test sets"""

# set seed for reproducibility
(trainingData, testData) = dataset.randomSplit([0.7, 0.3], seed = 100)

print("Training Dataset Count: " + str(trainingData.count()))
print("Test Dataset Count: " + str(testData.count()))

"""Model Training and Evaluation

Logistic Regression using Count Vector Features

Our model will make predictions and score on the test set; we then look at the top 10 predictions from the highest probability
"""

lr = LogisticRegression(maxIter=20, regParam=0.3, elasticNetParam=0)
lrModel = lr.fit(trainingData)

predictions = lrModel.transform(testData)
predictions.filter(predictions['prediction'] == 0) \
    .select("Descript","Category","probability","label","prediction") \
    .orderBy("probability", ascending=False) \
    .show(n = 10, truncate = 30)

from pyspark.ml.evaluation import MulticlassClassificationEvaluator

evaluator = MulticlassClassificationEvaluator(predictionCol="prediction")
evaluator.evaluate(predictions)

"""Logistic Regression using TF-IDF Features"""

from pyspark.ml.feature import HashingTF, IDF

hashingTF = HashingTF(inputCol="filtered", outputCol="rawFeatures", numFeatures=10000)

idf = IDF(inputCol="rawFeatures", outputCol="features", minDocFreq=5) #minDocFreq: remove sparse terms

pipeline = Pipeline(stages=[regexTokenizer, stopwordsRemover, hashingTF, idf, label_stringIdx])
pipelineFit = pipeline.fit(data)
dataset = pipelineFit.transform(data)

(trainingData, testData) = dataset.randomSplit([0.7, 0.3], seed = 100)

lr = LogisticRegression(maxIter=20, regParam=0.3, elasticNetParam=0)
lrModel = lr.fit(trainingData)

predictions = lrModel.transform(testData)
predictions.filter(predictions['prediction'] == 0) \
    .select("Descript","Category","probability","label","prediction") \
    .orderBy("probability", ascending=False) \
    .show(n = 10, truncate = 30)

evaluator = MulticlassClassificationEvaluator(predictionCol="prediction")
evaluator.evaluate(predictions)

"""Cross-Validation"""

pipeline = Pipeline(stages=[regexTokenizer, stopwordsRemover, countVectors, label_stringIdx])
pipelineFit = pipeline.fit(data)
dataset = pipelineFit.transform(data)
(trainingData, testData) = dataset.randomSplit([0.7, 0.3], seed = 100)
lr = LogisticRegression(maxIter=20, regParam=0.3, elasticNetParam=0)

from pyspark.ml.tuning import ParamGridBuilder, CrossValidator

# Create ParamGrid for Cross Validation
paramGrid = (ParamGridBuilder()
             .addGrid(lr.regParam, [0.1, 0.3, 0.5]) # regularization parameter
             .addGrid(lr.elasticNetParam, [0.0, 0.1, 0.2]) # Elastic Net Parameter (Ridge = 0)
#            .addGrid(model.maxIter, [10, 20, 50]) #Number of iterations
#            .addGrid(idf.numFeatures, [10, 100, 1000]) # Number of features
             .build())

# Create 5-fold CrossValidator
cv = CrossValidator(estimator=lr, \
                    estimatorParamMaps=paramGrid, \
                    evaluator=evaluator, \
                    numFolds=5)
cvModel = cv.fit(trainingData)

predictions = cvModel.transform(testData)

# Evaluate best model
evaluator = MulticlassClassificationEvaluator(predictionCol="prediction")
evaluator.evaluate(predictions)

"""Naive Bayes"""

from pyspark.ml.classification import NaiveBayes

nb = NaiveBayes(smoothing=1)
model = nb.fit(trainingData)

predictions = model.transform(testData)
predictions.filter(predictions['prediction'] == 0) \
    .select("Descript","Category","probability","label","prediction") \
    .orderBy("probability", ascending=False) \
    .show(n = 10, truncate = 30)

evaluator = MulticlassClassificationEvaluator(predictionCol="prediction")
evaluator.evaluate(predictions)

"""Random Forest"""

from pyspark.ml.classification import RandomForestClassifier

rf = RandomForestClassifier(labelCol="label", \
                            featuresCol="features", \
                            numTrees = 100, \
                            maxDepth = 4, \
                            maxBins = 32)

# Train model with Training Data
rfModel = rf.fit(trainingData)

predictions = rfModel.transform(testData)
predictions.filter(predictions['prediction'] == 0) \
    .select("Descript","Category","probability","label","prediction") \
    .orderBy("probability", ascending=False) \
    .show(n = 10, truncate = 30)

evaluator = MulticlassClassificationEvaluator(predictionCol="prediction")
evaluator.evaluate(predictions)