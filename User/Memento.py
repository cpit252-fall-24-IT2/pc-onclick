class Memento:
    def __init__(self, pc_state):
        self._pc_state = pc_state

    def get_pc_state(self):
        return self._pc_state

