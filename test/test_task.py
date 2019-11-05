import unittest

from scheduler.Task import Task


class TestTask1(Task):
    pass


class TestTask2(Task):
    pass


class TestTask3(Task):
    pass


class TaskNameTestCase(unittest.TestCase):
    def test_set_default_name(self):
        task1 = TestTask1()
        self.assertEqual(task1.name, task1.__class__.__name__)

    def test_set_name_by_constructor(self):
        name = "some_name"
        task1 = TestTask1(name=name)
        self.assertEqual(task1.name, name)

    def test_set_name_by_setter(self):
        name = "some_name"
        task1 = TestTask1()
        task1.set_name(name)
        self.assertEqual(task1.name, name)

    def test_get_name(self):
        name = "some_name"
        task1 = TestTask1()
        task1.set_name(name)
        self.assertEqual(task1.name, task1.get_name())


class AddPrecedingTaskTestCase(unittest.TestCase):
    def test_add_preceding_task_to_empty(self):
        task1 = TestTask1()
        task2 = TestTask2()

        task2.add_preceding_task(task1)
        self.assertListEqual(task2.preceding_tasks, [task1])

    def test_add_preceding_task(self):
        task1 = TestTask1()
        task2 = TestTask2()
        task3 = TestTask3()

        task3.add_preceding_task(task1)
        task3.add_preceding_task(task2)

        self.assertListEqual(task3.preceding_tasks, [task1, task2])

    def test_add_not_task_intance(self):
        task1 = TestTask1()

        with self.assertRaises(Exception) as exception_context:
            task1.add_preceding_task(1)
        self.assertEqual(str(exception_context.exception),
                         'Preceding task has to be an instance of subclass of Task class')

    def test_add_task_itself(self):
        task1 = TestTask1()

        with self.assertRaises(Exception) as exception_context:
            task1.add_preceding_task(task1)
        self.assertEqual(str(exception_context.exception), 'Current task cannot be preceding for itself')


class AddPrecedingTasksTestCase(unittest.TestCase):
    def test_add_preceding_tasks_by_constructor(self):
        task1 = TestTask1()
        task2 = TestTask2()

        preceding_tasks = [task1, task2]
        task3 = TestTask3(preceding_tasks=preceding_tasks)

        self.assertListEqual(task3.preceding_tasks, preceding_tasks)

    def test_add_preceding_tasks(self):
        task1 = TestTask1()
        task2 = TestTask2()
        task3 = TestTask3()

        preceding_tasks = [task1, task2]
        task3.add_preceding_tasks(preceding_tasks)
        self.assertListEqual(task3.preceding_tasks, preceding_tasks)

    def test_add_tasks_with_no_task_instance(self):
        task1 = TestTask1()
        task2 = TestTask2()
        task3 = TestTask3()

        preceding_tasks = [task1, [task2]]
        with self.assertRaises(Exception) as exception_context:
            task3.add_preceding_tasks(preceding_tasks)
        self.assertEqual(str(exception_context.exception),
                         'Preceding task has to be an instance of subclass of Task class')

    def test_add_tasks_with_task_itself(self):
        task1 = TestTask1()
        task2 = TestTask2()

        preceding_tasks = [task1, task2]
        with self.assertRaises(Exception) as exception_context:
            task2.add_preceding_tasks(preceding_tasks)
        self.assertEqual(str(exception_context.exception),
                         'Current task cannot be preceding for itself')

    def test_get_preceding_tasks(self):
        task1 = TestTask1()
        task2 = TestTask2()

        preceding_tasks = [task1, task2]
        task3 = TestTask3(preceding_tasks=preceding_tasks)

        self.assertListEqual(task3.preceding_tasks, task3.get_preceding_tasks())

    def test_clear_preceding_tasks(self):
        task1 = TestTask1()
        task2 = TestTask2()

        preceding_tasks = [task1, task2]
        task3 = TestTask3(preceding_tasks=preceding_tasks)
        task3.clear_preceding_tasks()
        self.assertListEqual(task3.get_preceding_tasks(), list())


if __name__ == '__main__':
    unittest.main()
