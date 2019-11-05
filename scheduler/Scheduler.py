from scheduler.Task import Task
from collections import OrderedDict


class Scheduler(object):
    def __init__(self):
        self.queue = list()
        self.preceding_task_map = dict()

    def add_task_to_queue(self, task):
        if not isinstance(task, Task):
            raise Exception('New task has to be an instance of subclass of Task')
        # preceding_tasks = task.get_preceding_tasks()
        # if len(preceding_tasks) != len(self.queue):
        #     print("prev_tasks : {} \t qeuue: {}".format(preceding_tasks, self.queue))
        #     raise Exception('New task preceding tasks and scheduler queue must be identical')
        # for preceding_task, queued_task in zip(preceding_tasks, self.queue):
        #     if preceding_task != queued_task:
        #         raise Exception('Already queued tasks do not match with new task preceding tasks')
        self.queue.append(task)

    def get_queue(self):
        return self.queue

    def run_tasks(self):
        if len(self.queue) != 0:
            for index, task in enumerate(self.queue):
                self.preceding_task_map[index] = task.get_preceding_tasks()
            ordered_map = OrderedDict(sorted(self.preceding_task_map.items(), key=lambda x: len(x[1])))

            while len(ordered_map) > 0:
                print(ordered_map.items())
                task_executed = False
                key_to_remove = 0
                for item in ordered_map.items():
                    if len(item[1]) == 0:
                        key_to_remove = item[0]
                        task_executed = True
                        task = self.queue[item[0]]
                        print("executing task {}".format(task.name))
                        task.process()

                        for value in ordered_map.values():
                            if task in value:
                                value.remove(task)
                        break
                if task_executed:
                    ordered_map.pop(key_to_remove)
                else:
                    Exception("Some tasks were not executed but queue is not empty")

        else:
            raise Exception('Scheduler has no tasks to run')

    def clear_queue(self):
        self.queue = list()
