"""
The chromosome is the set of values to optimize, the three parameter values.
"""
class Chromosome:
    def __init__(self, _kp, _td, _ti):
        self.kp = _kp
        self.td = _td
        self.ti = _ti
        self._fitness = None

    def __eq__(self, other): 
        if not isinstance(other, Chromosome):
            return NotImplemented

        return self.kp == other.kp and self.td == other.td and self.ti == other.ti and self._fitness == other._fitness

    @property
    def fitness(self):
        return self._fitness

    @fitness.setter
    def fitness(self, fitness_val):
        self._fitness = fitness_val
