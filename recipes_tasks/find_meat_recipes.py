import re
from scheduler.Task import Task
from pyspark.sql.functions import lower, col, udf, array
from pyspark.sql.types import StringType

class FindMeatRecipes(Task):
    def __init__(self, spark):
        super().__init__()
        self.spark = spark

    def process(self):
        def convert_to_minutes(time):

            minutes = 0
            minutes_gr = re.search('[\d]+(?=M)', time)
            if minutes_gr is not None:
                minutes = int(minutes_gr.group(0))

            hours = 0
            hours_gr = re.search('[\d]+(?=H)', time)
            if hours_gr is not None:
                hours = int(hours_gr.group(0))

            total_minutes = hours * 60 + minutes
            return total_minutes

        def convert_to_difficulty(times):
            cook_minutes = convert_to_minutes(times[0])
            prep_minutes = convert_to_minutes(times[1])
            sum_minutes = cook_minutes + prep_minutes

            if sum_minutes > 60:
                return 'hard'
            elif sum_minutes < 30:
                return 'easy'
            else:
                return 'medium'

        sc = self.spark.sparkContext
        new_df = self.spark.read.orc("recipes_data/raw/recipes.orc")

        filtered_df = new_df.where(lower(col('ingredients')).contains('beef')
                                   | lower(col('ingredients')).contains('meat'))

        convert_to_difficulty_udf = udf(convert_to_difficulty, StringType())
        final_df = filtered_df.withColumn("difficulty", convert_to_difficulty_udf(array("cookTime", "prepTime")))
        final_df.write.format("orc").mode('overwrite').save("recipes_data/meat/meat_recipes.orc")