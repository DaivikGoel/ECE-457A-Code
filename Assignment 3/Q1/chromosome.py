"""
The chromosome is the set of values to optimize, the three parameter values.
"""
class Chromosome:
    def __init__(self, _kp, _td, _ti):
        self.kp = _kp
        self.td = _td
        self.ti = _ti
        self._fitness = None

    @property
    def fitness(self):
        return self._fitness

    @fitness.setter
    def fitness(self, fitness_val):
        self._fitness = fitness_val
