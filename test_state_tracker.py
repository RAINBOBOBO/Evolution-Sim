"""StateTracker class tests"""

import os
from unittest import TestCase
from mainsim import StateTracker, quitgame

def mock_main(counter, runs):
	run = True
	while run:
		print("simulating...");
		counter += 1

		state_tracker.set_state(mock_state_handler(state_tracker.state))

        #if state_tracker = 3, run once, if 4, run 5 times, if 5, run 10 times
		if state_tracker.state == 3:
			state_tracker.run_once()
		elif state_tracker.state == 4:
			state_tracker.run_x_times(5)
		elif state_tracker.state == 5:
			state_tracker.run_x_times(10)

		if (counter >= runs):
			print(counter)
			run = False
	return counter


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

state_tracker = StateTracker()
INITIAL_COUNTER = 0
class StateTrackerTestCase(TestCase):
	""" mock_main -> mock_state_handler -> mock_sh"""

	def test_run_once(self):
		"""Test run_once class method"""
		counter = 0
		print("starting run_once test")
		state_tracker.set_state(3)
		counter = mock_main(INITIAL_COUNTER, 1)
		print("run_once test complete")
		self.assertEqual(counter, 1);

	def test_five_times(self):
		"""Test run_five_times class method"""
		counter = 0
		print("starting run_once test")
		state_tracker.set_state(4)
		counter = mock_main(INITIAL_COUNTER, 5)
		print("run_once test complete")
		self.assertEqual(counter, 5);


	def test_ten_times(self):
		"""Test run_ten_times class method"""
		counter = 0
		print("starting run_once test")
		state_tracker.set_state(5)
		counter = mock_main(INITIAL_COUNTER, 10)
		print("run_once test complete")
		self.assertEqual(counter, 10);


	def test_hundred_times(self):
		"""Test run_hundred_times class method"""
		counter = 0
		print("starting run_once test")
		state_tracker.set_state(5)
		counter = mock_main(INITIAL_COUNTER, 100)
		print("run_once test complete")
		self.assertEqual(counter, 100);
		