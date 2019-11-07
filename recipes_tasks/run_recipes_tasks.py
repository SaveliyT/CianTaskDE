import os
import sys
from scheduler.Scheduler import Scheduler
from recipes_tasks.get_recipes import GetRecipes
from recipes_tasks.find_meat_recipes import FindMeatRecipes


# change to corresponding paths
PYSPARK_PYTHON = sys.executable  # venv/bin/python
SPARK_HOME = '/usr/local/spark/'


def main(spark):
    scheduler = Scheduler()

    get_recipes_task = GetRecipes(spark)
    find_meat_task = FindMeatRecipes(spark)
    find_meat_task.add_preceding_task(get_recipes_task)

    scheduler.add_task_to_queue(get_recipes_task)
    scheduler.add_task_to_queue(find_meat_task)

    scheduler.run_tasks()


if __name__ == '__main__':
    os.environ["PYSPARK_SUBMIT_ARGS"] = 'pyspark-shell'
    os.environ["PYSPARK_PYTHON"] = PYSPARK_PYTHON
    os.environ["SPARK_HOME"] = SPARK_HOME

    spark_home = os.environ.get('SPARK_HOME', None)

    sys.path.insert(0, os.path.join(spark_home, 'python'))
    sys.path.insert(0, os.path.join(spark_home, 'python/lib/py4j-0.10.7-src.zip'))
    exec(open(os.path.join(spark_home, 'python/pyspark/shell.py')).read())

    main(spark)
    spark.stop()
