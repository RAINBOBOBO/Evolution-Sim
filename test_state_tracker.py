"""StateTracker class tests"""

import os
from unittest import TestCase
from mainsim import StateTracker


def mock_main():
	pass

def mock_state_handler():
	pass


class StateTrackerTestCase(TestCase):
	
	def setUp(self):
		"""Create a StateTracker instance"""
		state_tracker = StateTracker()


	def test_run_once(self):
		"""Test run_once class method"""



		