import unittest

import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
from task_track import get_parser


class TestGetParser(unittest.TestCase):
    
    def test_add_task(self):
        parser = get_parser()
        args = parser.parse_args(['add', 'task1', '--description', 'description1', '--priority', 'high', '--status', 'pending'])
        self.assertEqual(args.subcommamd, 'add')
        self.assertEqual(args.task, 'task1')
        self.assertEqual(args.description, 'description1')
        self.assertEqual(args.priority, 'high')
        self.assertEqual(args.status, 'pending')

    
    def test_delete_task(self):
        parser = get_parser()
        args = parser.parse_args(['delete', '1'])
        self.assertEqual(args.subcommamd, 'delete')
        self.assertEqual(args.task_id, '1')

    
    def test_update_task(self):
        parser = get_parser()
        args = parser.parse_args(['update', '1', '--task', 'task1', '--description', 'description1', '--priority', 'high', '--status', 'pending'])
        self.assertEqual(args.subcommamd, 'update')
        self.assertEqual(args.task_id, '1')
        self.assertEqual(args.task, 'task1')
        self.assertEqual(args.description, 'description1')
        self.assertEqual(args.priority, 'high')
        self.assertEqual(args.status, 'pending')

    
    def test_list_tasks(self):
        parser = get_parser()
        args = parser.parse_args(['list', '-s', 'pending'])
        self.assertEqual(args.subcommamd, 'list')
        self.assertFalse(args.all)
        self.assertEqual(args.status, 'pending')
        self.assertIsNone(args.priority)

    
    def test_mark_done_task(self):
        parser = get_parser()
        args = parser.parse_args(['mark_done', '1'])
        self.assertEqual(args.subcommamd, 'mark_done')
        self.assertEqual(args.task_id, '1')

    
    def test_mark_pending_task(self):
        parser = get_parser()
        args = parser.parse_args(['mark_pending', '1'])
        self.assertEqual(args.subcommamd, 'mark_pending')
        self.assertEqual(args.task_id, '1')
    
    
if __name__ == "__main__":
    unittest.main()
        