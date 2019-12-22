# Простой планировщик задач

## Описание

Для работы планировщика необходимо:
 * Создать классы, наследующиеся от класса `Task` и реализовать метод `process` в каждом из них.
 * Проинициализировать объекты этих классов и с помощью метода `add_preceding_task()`
 добавить таски, которые необходимо выполнить до того, как выполнить данную таску
 (Как минимум для одной таски этого делать не нужно, чтобы с неё начать выполнение)
 * Проинициализировать объект класса `Scheduler` и добавить все объекты тасок в очередь 
 с помощью метода `add_task_to_queue()`
 * Запустить выполнение тасок при помощи метода `run_tasks()`
 
 ## Пример
 
 ```python
from scheduler.Scheduler import Scheduler
from scheduler.Task import Task

class SomeTask1(Task):
    def process(self):
        print("Task1")


class SomeTask2(Task):
    def process(self):
        print("Task2")

scheduler = Scheduler()
task1 = SomeTask1()
task2 = SomeTask2()

task2.add_preceding_task(task1)

scheduler.add_task_to_queue(task1)
scheduler.add_task_to_queue(task2)
scheduler.run_tasks()

```

## Мини ETL для рецептов
Для запуска небольшого скрипта в качестве примера, который сохраняет [данные рецептов] (https://s3-eu-west-1.amazonaws.com/dwh-test-resources/recipes.json) в orc файлы необходимо указать в файле 
`run_recipes_tasks.py` путь для $SPARK_HOME и запустить его

После выполнения ETL данные будут находиться по пути
* `recipes_data/raw/recipes.orc` - для необработанных данных 
* `recipes_data/meat/meat_recipes.orc` - для мясных рецептов со столбцом сложности
