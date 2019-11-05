class Task(object):
    def __init__(self, name=None, preceding_tasks=None):
        self.preceding_tasks = list()
        if preceding_tasks is not None:
            self.add_preceding_tasks(preceding_tasks)
        # else:
        #     self.preceding_tasks = list()

        if name is not None:
            self.name = str(name)
        else:
            self.name = self.__class__.__name__

    def process(self):
        raise NotImplementedError("Method process of task {} did not implemented".format(self.name))

    def get_preceding_tasks(self):
        return self.preceding_tasks

    def add_preceding_task(self, task):
        if not isinstance(task, Task):
            raise Exception('Preceding task has to be an instance of subclass of Task class')
        if task.__class__ == self.__class__:
            raise Exception("Current task cannot be preceding for itself")
        self.preceding_tasks.append(task)

    def add_preceding_tasks(self, tasks):
        for task in tasks:
            if not isinstance(task, Task):
                raise Exception('Preceding task has to be an instance of subclass of Task class')
            if task.__class__ == self.__class__:
                raise Exception("Current task cannot be preceding for itself")

        self.preceding_tasks.extend(list(tasks))

    def set_name(self, name):
        self.name = str(name)

    def get_name(self):
        return self.name

    def clear_preceding_tasks(self):
        self.preceding_tasks = list()
