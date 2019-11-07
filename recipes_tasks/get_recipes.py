from urllib.request import urlopen
from scheduler.Task import Task
from pyspark.sql import SQLContext


class GetRecipes(Task):

    def __init__(self, spark):
        super().__init__()
        self.sc = spark.sparkContext

    def process(self):

        url = 'https://s3-eu-west-1.amazonaws.com/dwh-test-resources/recipes.json'
        response = urlopen(url)
        data = response.read().decode()
        lines = data.split('\n')

        rdd = self.sc.parallelize(lines)
        sqlContext = SQLContext(self.sc)
        df = sqlContext.read.json(rdd)

        df.write.format("orc").mode('overwrite').save("recipes_data/raw/recipes.orc")