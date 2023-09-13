# тест выполняет проверку заданий airflow
# для успешного прохождения теста необходимо выполнить пример docs\examples\airflow\dag_BashOperator.py

import unittest
from airflow.models import DagBag

class TestCheckForNewFilesDAG(unittest.TestCase):
    """Проверка заданий"""

    dag_id="example_EmptyOperator"
    task_id="emptyTask"

    def setUp(self):
        self.dagbag = DagBag()

    def test_task_count(self):
        """Проверка количества заданий"""        
        dag = self.dagbag.get_dag(self.dag_id)
        self.assertEqual(len(dag.tasks), 1)

    def test_contain_tasks(self):
        """Проверка наличия задач"""
        dag = self.dagbag.get_dag(self.dag_id)
        tasks = dag.tasks
        task_ids = list(map(lambda task: task.task_id, tasks))
        self.assertListEqual(task_ids, [self.task_id])

    def test_dependencies_of_task(self):
        """Проверка конкретной задачи"""
        dag = self.dagbag.get_dag(self.dag_id)
        task = dag.get_task(self.task_id)
        
        # to be use in case you have upstream task
        upstream_task_ids = list(map(lambda task: task.task_id, 
                                     task.upstream_list))
        self.assertListEqual(upstream_task_ids, [])
        
        downstream_task_ids = list(map(lambda task: task.task_id, 
                                       task.downstream_list))
        self.assertListEqual(downstream_task_ids, [])

if __name__ == '__main__':
    unittest.main(verbosity=2)