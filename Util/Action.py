class Action:

    def __init__(self, name, d_score):
        self.name = name
        self.d_score = d_score

    def __str__(self):
        return self.name

    def get_d_score(self):
        return self.d_score

    def __eq__(self, other):
        return self.name == other.name


NO_ACTION = Action("NO_ACTION", 0)
PASS = Action("PASS", 0)
FAIL = Action("FAIL", 0)
ATTACKING = Action("ATTACKING", 30)
EATING = Action("EATING", 35)
DAMAGING = Action("DAMAGING", -2)
GOING_UP = Action("GOING_UP", -1)
GOING_DOWN = Action("GOING_DOWN", -1)
GOING_RIGHT = Action("GOING_RIGHT", -1)
GOING_LEFT = Action("GOING_LEFT", -1)
