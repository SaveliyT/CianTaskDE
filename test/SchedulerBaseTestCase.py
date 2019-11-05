from unittest import TestCase
from scheduler.Scheduler import Scheduler
from scheduler.Task import Task


class TestTask1(Task):
    def process(self):
        pass


class TestTask2(Task):
    def process(self):
        pass


class TestTask3(Task):
    def process(self):
        pass


class TestTask4(Task):
    def process(self):
        pass


class SchedulerBaseTestCase(TestCase):
    scheduler = Scheduler()
    task1 = TestTask1()
    task2 = TestTask2()
    task3 = TestTask3()
    task4 = TestTask4()
