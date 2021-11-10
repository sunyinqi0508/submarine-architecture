import sys
from os import fdopen

from clients.trench_manager_client import TrenchManager

class ManualTrenchManager(TrenchManager):
	def __init__(self, name, fd):
		super(ManualTrenchManager, self).__init__(name=name)
		sys.stdin = fdopen(fd)

	def send_probes(self):
		return [int(i) for i in input('What probes would you like to send (separated by spaces, 0-99)? ').split(' ')]

	def choose_alert(self, sent_probes, results):
		return input(f"You sent probes {sent_probes} with results {results}. What alert do you want to send ('red', 'yellow')? ")