'''this file holds the structure for the simulation of a radiology department
authors: '''
import radiology_functions as f


class Job:
    global counter

    def _init_(self):
        counter += 1
        self.ID = counter
        self.time = 0


class Station:
    def _init_(self, servers, distributions):
        self.queue = list()
        self.servers = servers
        self.servers_busy = 0


def simulation(foo1, foo2):
    clock = 0
    simulation_time = 11

    while clock < simulation_time:
        f.arrival()


