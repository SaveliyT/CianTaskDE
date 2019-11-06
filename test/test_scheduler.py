import unittest
from scheduler.Scheduler import Scheduler
from scheduler.Task import Task
import time


class TestTask1(Task):
    def process(self):
        time.sleep(0.01)
        return time.time()


class TestTask2(Task):
    def process(self):
        time.sleep(0.01)
        return time.time()


class TestTask3(Task):
    def process(self):
        time.sleep(0.01)
        return time.time()


class TestTask4(Task):
    def process(self):
        time.sleep(0.01)
        return time.time()


class TestTask5(Task):
    pass


class SchedulerTestCase(unittest.TestCase):

    def test_scheduler_add_task(self):
        scheduler = Scheduler()
        task1 = TestTask1()

        scheduler.add_task_to_queue(task1)
        self.assertListEqual(scheduler.queue, [task1])

    def test_scheduler_clear_queue(self):
        scheduler = Scheduler()
        task1 = TestTask1()

        scheduler.add_task_to_queue(task1)
        scheduler.clear_queue()
        self.assertListEqual(scheduler.get_queue(), list())

    def test_scheduler_get_queue(self):
        scheduler = Scheduler()
        task1 = TestTask1()

        scheduler.add_task_to_queue(task1)
        self.assertListEqual(scheduler.get_queue(), scheduler.queue)

    def test_add_not_a_task_insance(self):
        scheduler = Scheduler()
        with self.assertRaises(Exception) as exception_context:
            scheduler.add_task_to_queue("task")
        self.assertEqual(str(exception_context.exception),
                         'New task has to be an instance of subclass of Task')


class SchedulerProcessTasksTestCase(unittest.TestCase):

    def test_process_task_with_no_preceding_started(self):
        scheduler = Scheduler()
        task1 = TestTask1()
        task2 = TestTask2()

        task2.add_preceding_task(task1)
        scheduler.add_task_to_queue(task2)
        with self.assertRaises(Exception) as exception_context:
            scheduler.run_tasks()
        self.assertEqual(str(exception_context.exception),
                         'Some tasks were not executed')

    def test_run_scheduler_with_empty_queue(self):
        scheduler = Scheduler()

        with self.assertRaises(Exception) as exception_context:
            scheduler.run_tasks()
        self.assertEqual(str(exception_context.exception), 'Scheduler has no tasks to run')

    def test_process_task_with_not_implemented_process(self):
        scheduler = Scheduler()
        task5 = TestTask5()

        scheduler.add_task_to_queue(task5)
        with self.assertRaises(Exception) as exception_context:
            scheduler.run_tasks()
        self.assertEqual(str(exception_context.exception), 'Method process of task {} did not implemented'
                         .format(task5.get_name()))

    # 1
    def test_process_one_task(self):
        scheduler = Scheduler()
        task1 = TestTask1()

        scheduler.add_task_to_queue(task1)
        scheduler.run_tasks()
        self.assertIn(task1, scheduler._result_map)
        self.assertIsNotNone(scheduler._result_map[task1])

    # 1 -> 2
    def test_process_two_tasks(self):
        scheduler = Scheduler()
        task1 = TestTask1()
        task2 = TestTask2()

        scheduler.clear_queue()
        task1.clear_preceding_tasks()
        task2.clear_preceding_tasks()

        task2.add_preceding_task(task1)
        scheduler.add_task_to_queue(task1)
        scheduler.add_task_to_queue(task2)
        scheduler.run_tasks()

        self.assertIn(task1, scheduler._result_map)
        self.assertIn(task2, scheduler._result_map)
        self.assertGreater(scheduler._result_map[task2], scheduler._result_map[task1])

    # 1 -> 2
    # 1 -> 3
    def test_process_two_tasks_after_same(self):
        scheduler = Scheduler()
        task1 = TestTask1()
        task2 = TestTask2()
        task3 = TestTask3()

        task2.add_preceding_task(task1)
        task3.add_preceding_task(task1)

        scheduler.add_task_to_queue(task1)
        scheduler.add_task_to_queue(task2)
        scheduler.add_task_to_queue(task3)
        scheduler.run_tasks()

        self.assertIn(task1, scheduler._result_map)
        self.assertIn(task2, scheduler._result_map)
        self.assertIn(task3, scheduler._result_map)
        self.assertGreater(scheduler._result_map[task2], scheduler._result_map[task1])
        self.assertGreater(scheduler._result_map[task3], scheduler._result_map[task1])

    # 1 -> 2 -> 4_1
    # 1 -> 3 -> 4_2
    def test_process_tasks_of_one_base_class(self):
        scheduler = Scheduler()
        task1 = TestTask1()
        task2 = TestTask2()
        task3 = TestTask3()
        task4_1 = TestTask4()
        task4_2 = TestTask4()

        task2.add_preceding_task(task1)
        task4_1.add_preceding_tasks([task1, task2])
        task3.add_preceding_task(task1)
        task4_2.add_preceding_tasks([task1, task3])

        scheduler.add_task_to_queue(task1)
        scheduler.add_task_to_queue(task2)
        scheduler.add_task_to_queue(task3)
        scheduler.add_task_to_queue(task4_1)
        scheduler.add_task_to_queue(task4_2)
        scheduler.run_tasks()

        self.assertIn(task1, scheduler._result_map)
        self.assertIn(task2, scheduler._result_map)
        self.assertIn(task3, scheduler._result_map)
        self.assertIn(task4_1, scheduler._result_map)
        self.assertIn(task4_2, scheduler._result_map)
        self.assertGreater(scheduler._result_map[task2], scheduler._result_map[task1])
        self.assertGreater(scheduler._result_map[task3], scheduler._result_map[task1])
        self.assertGreater(scheduler._result_map[task4_1], scheduler._result_map[task2])
        self.assertGreater(scheduler._result_map[task4_2], scheduler._result_map[task3])


if __name__ == '__main__':
    unittest.main()
