import sys
from os import fdopen

from clients.submarine_captain_client import SubmarineCaptain

class ManualSubmarineCaptain(SubmarineCaptain):
	def __init__(self, name, fd):
		super(ManualSubmarineCaptain, self).__init__(name=name)
		sys.stdin = fdopen(fd)

	def your_algorithm(self, times_probed):
		return int(input(f"You have been probed {times_probed} times. What move would you like to make [-1,1]? "))