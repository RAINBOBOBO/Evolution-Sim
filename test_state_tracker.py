"""StateTracker class tests"""

import os
from unittest import TestCase
from mainsim import StateTracker, quitgame


def mock_main():
	run = True
	while run:
		print("simulating...");

		state_tracker.set_state(mock_state_handler(state_tracker.state))

        #if state_tracker = 3, run once, if 4, run 5 times, if 5, run 10 times
		if state_tracker.state == 3:
			state_tracker.run_once()
		elif state_tracker.state == 4:
			state_tracker.run_x_times(5)
		elif state_tracker.state == 5:
			state_tracker.run_x_times(10)

def mock_menu():
	return 2

def mock_show_matrix():
	# next generation:
	return 3
	# 5 generations
	# return 4
	# 10 generations
	# return 5

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

state_tracker = StateTracker(3)
class StateTrackerTestCase(TestCase):

	def test_run_once(self):
		"""Test run_once class method"""
		print("starting run_once test")
		mock_main()
		print("run_once test complete")



		