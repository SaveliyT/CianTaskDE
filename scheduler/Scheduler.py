from scheduler.Task import Task
from collections import OrderedDict


class Scheduler(object):
    def __init__(self):
        self.queue = list()
        self.preceding_task_map = dict()
        self._result_map = dict()  # need only for tests

    def add_task_to_queue(self, task):
        if not isinstance(task, Task):
            raise Exception('New task has to be an instance of subclass of Task')

        self.queue.append(task)

    def get_queue(self):
        return self.queue

    def run_tasks(self):
        # check that queue is not empty
        if len(self.queue) != 0:
            self._result_map = dict()

            # make map index task in queue <-> preceding tasks of this task
            for index, task in enumerate(self.queue):
                self.preceding_task_map[index] = task.get_preceding_tasks()
            # sort to make less iterations
            ordered_map = OrderedDict(sorted(self.preceding_task_map.items(), key=lambda x: len(x[1])))

            # iterate over map
            while len(ordered_map) > 0:
                print(ordered_map.items())
                task_executed = False
                key_to_remove = 0
                for item in ordered_map.items():
                    # check if task has no preceding tasks
                    if len(item[1]) == 0:
                        key_to_remove = item[0]
                        task_executed = True
                        # get instance of task by index from queue and execute
                        task = self.queue[item[0]]
                        print("executing task {}".format(task.name))
                        self._result_map[task] = task.process()

                        # remove executed task from preceding tasks list for other tasks
                        for value in ordered_map.values():
                            if task in value:
                                value.remove(task)
                        break

                # remove from map
                if task_executed:
                    ordered_map.pop(key_to_remove)
                # if map does not contain task with empty preceding tasks list throw an error
                else:
                    raise Exception("Some tasks were not executed")

        else:
            raise Exception('Scheduler has no tasks to run')

    def clear_queue(self):
        self.queue = list()
        self._result_map = dict()
