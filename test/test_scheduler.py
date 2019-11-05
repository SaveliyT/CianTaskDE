import unittest
from unittest.mock import Mock
from test.SchedulerBaseTestCase import SchedulerBaseTestCase



class SchedulerTestCase(SchedulerBaseTestCase):
    def test_scheduler_add_task(self):
        self.scheduler.add_task_to_queue(self.task1)
        self.assertListEqual(self.scheduler.queue, [self.task1])

    def test_scheduler_clear_queue(self):
        self.scheduler.add_task_to_queue(self.task1)
        self.scheduler.clear_queue()
        self.assertListEqual(self.scheduler.get_queue(), list())

    def test_scheduler_get_queue(self):
        self.scheduler.add_task_to_queue(self.task1)
        self.assertListEqual(self.scheduler.get_queue(), self.scheduler.queue)


# class SchedulerProcessTasksTestCase(SchedulerBaseTestCase):
#     def test_process_one_task(self):
#         self.scheduler.clear_queue()
#
#         mock = Mock()
#         self.scheduler.add_task_to_queue(mock)
#         self.scheduler.run_tasks(mock)
#         self.scheduler.run_tasks = MagicMock()
#         self.scheduler.run_tasks()
#         mock.process.



if __name__ == '__main__':
    unittest.main()
