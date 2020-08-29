"""StateTracker class tests"""

import os
from unittest import TestCase
from mainsim import StateTracker


def mock_main():
	pass

def mock_menu():
	return 2

def mock_show_matrix():
	pass

def mock_state_handler(defaultState = 1):
	done = False
    state = defaultState
    while done == False:
        if state == 1:
            state = mock_menu()
        elif state == 2:
            state = mock_show_matrix()
        elif state == 3 or state == 4 or state == 5:
            done = True
    return state


class StateTrackerTestCase(TestCase):
	
	def setUp(self):
		"""Create a StateTracker instance"""
		state_tracker = StateTracker()


	def test_run_once(self):
		"""Test run_once class method"""



		