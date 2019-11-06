class Task(object):
    """
    Parent class for task instances

    :param name: task's name
    :type name: str, optional
    :param preceding_tasks: List or iterable for tasks that must be run before the task
    :type preceding_tasks: list, optional
    """

    def __init__(self, name=None, preceding_tasks=None):
        self.preceding_tasks = list()
        if preceding_tasks is not None:
            self.add_preceding_tasks(preceding_tasks)

        if name is not None:
            self.name = str(name)
        else:
            self.name = self.__class__.__name__

    def process(self):
        """
        Main execution body of task. Must be implemented in child class.

        :raises NotImplementedError:
        """

        raise NotImplementedError("Method process of task {} did not implemented".format(self.name))

    def get_preceding_tasks(self):
        """
        Returns list of preceding tasks

        :returns: preceding_tasks
        :rtype: list
        """

        return self.preceding_tasks

    def add_preceding_task(self, task):
        """
        Add a task to list of preceding tasks

        :param task:
        :type task: Task
        :return:
        """

        if not isinstance(task, Task):
            raise Exception('Preceding task has to be an instance of subclass of Task class')
        if task.__class__ == self.__class__:
            raise Exception("Current task cannot be preceding for itself")
        self.preceding_tasks.append(task)

    def add_preceding_tasks(self, tasks):
        """
        Add a tasks to list of preceding tasks

        :param tasks:
        :type tasks: list
        :return:
        """

        for task in tasks:
            if not isinstance(task, Task):
                raise Exception('Preceding task has to be an instance of subclass of Task class')
            if task.__class__ == self.__class__:
                raise Exception("Current task cannot be preceding for itself")

        self.preceding_tasks.extend(list(tasks))

    def set_name(self, name):
        """
        Sets name for the task

        :param name:
        :type name: str
        :return:
        """

        self.name = str(name)

    def get_name(self):
        """
        Returns name of the task

        :return: Name
        :rtype: str
        """

        return self.name

    def clear_preceding_tasks(self):
        """Clear preceding tasks of the task"""
        self.preceding_tasks = list()
