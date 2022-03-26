from unittest import TestCase
import os
import time
from mido import MidiFile
from b2b_ai.utils.midi import in_range, next_file, normalize_data, \
    play_song, get_project_root, create_dir_if_not_exists

class TestMidiUtils(TestCase):
    """
    Test midi utils functions
    """
    def setUp(self) -> None:
        self.root = get_project_root()
        os.chdir(self.root)
        return super().setUp()

    def test_in_range(self):
        self.assertTrue(in_range(0,0,0))
        self.assertTrue(in_range(1,0,2))
        self.assertFalse(in_range(0,1,2))
        self.assertFalse(in_range(1,2,0))
        self.assertFalse(in_range(2,0,1))

    def test_play_song(self):
        root = get_project_root()
        os.chdir(root)
        mid = MidiFile('test_data/test.mid')
        curr_time = time.time()
        play_song(mid)
        passed_time = time.time() - curr_time
        self.assertAlmostEqual(passed_time, mid.length, places=0)

    def test_next_file(self):
        self.assertEqual(next_file('./data/1.mid'), './data/2.mid')

    def test_normalize_data(self):
        normalize_data('bass', 'test_data')
        os.chdir(self.root)
        self.assertTrue(os.path.exists('test_data/bass-8bar'))
        mid_1 = MidiFile('test_data/bass-8bar/1.mid')
        mid_2 = MidiFile('test_data/bass-8bar/2.mid')
        mid_3 = MidiFile('test_data/bass-8bar/3.mid')
        self.assertAlmostEqual(mid_1.length, mid_2.length, places=0)
        self.assertAlmostEqual(mid_2.length, mid_3.length, places=0)

    def test_create_dir(self):
        self.assertFalse(os.path.exists('test'))
        create_dir_if_not_exists('test')
        self.assertTrue(os.path.exists('test'))
        os.removedirs('test')
        self.assertFalse(os.path.exists('test'))
