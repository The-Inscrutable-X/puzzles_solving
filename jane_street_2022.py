from __future__ import annotations
from copy import deepcopy

class Dice():
    data: list = [0, 1, 2, 3, 4, 5]
    TIP_MAPPINGS = {"S": [(3, 0), (0, 1), (1, 2), (2, 3)], "W": [(5, 0), (0, 4), (4, 2), (2, 5)]}
    TIP_MAPPINGS["E"] = [(0, 5), (5, 2), (2, 4), (4, 0)]
    TIP_MAPPINGS["N"] = [(0, 3), (3, 2), (2, 1), (1, 0)]
    step: int
    location: tuple  # In the format of y, x
    LOCATION_MAPPINGS = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}
    score: int
    DIRECTION_TO_DATA_MAPPINGS = {"S": 3, "W": 5, "N": 1, "E": 4}
    # top: int
    # down: int
    # front: int
    # back: int
    # left: int
    # right: int
    # adjacencies: dict[str, list[int]]

    def __init__(self, data = None, location = (5, 0), step = 0, score = 0):
        # self.top = self.data[0]
        # self.down = self.data[2]
        # self.front = self.data[1]
        # self.back = self.data[3]
        # self.left = self.data[4]
        # self.right = self.data[5]
        if data != None:
            self.data = data
        self.location = location
        self.step = step
        self.score = score
    
    def tip(self, direction: str) -> None:
        """Tip/roll the cube in one of the cardinal directions. Currently supporting N and E for a Naive recursion."""
        print("Mapping", self.TIP_MAPPINGS[direction])
        print("before", self)
        temp = None
        for a, b in self.TIP_MAPPINGS[direction]:  # shifts data by one, wraps around.
            print(self.data)
            if temp != None:
                print("propar")
                temp2 = self.data[b]
                self.data[b] = temp
                temp = temp2
            else:
                print("nano")
                temp = self.data[b]
                self.data[b] = self.data[a]
            print(self.data)
        loc_transform = self.LOCATION_MAPPINGS[direction]
        # print(direction, "old loc" , self.location, end = "; ")
        self.location = (self.location[0] + loc_transform[0], self.location[1] + loc_transform[1])
        # print(direction, "new loc" , self.location)
        self.step += 1
        print("after", self)

    def new_face(self, datum) -> None:
        """Replaces current upwards facing face's value."""
        self.data[0] = datum

    def copy(self) -> Dice:
        """Create new copy of the Dice."""
        new = Dice(deepcopy(self.data), self.location, self.step, self.score)
        return new

    def inc_score(self) -> None:
        """Increases the score after a succeeseful 'tip' or move."""
        self.score += self.data[0] * self.step

    def get_face_value(self, direction) -> float:
        """"""
        return self.data[self.DIRECTION_TO_DATA_MAPPINGS[direction]]

    def __str__(self) -> None:
        """Prints a surface unwrap of a dice cube."""
        a = f"""
        __|{self.data[3]}|__
        |{self.data[4]}|{self.data[0]}|{self.data[5]}|
        __|{self.data[1]}|__
        __|{self.data[2]}|__
        {self.location} {self.step}
        """
        return a


class Grid():

    grid = [
    [57, 33, 132, 268, 492, 732],
    [81, 123, 240, 443, 353, 508],
    [186, 42, 195, 704, 452, 228],
    [-7, 2, 357, 452, 317, 395],
    [5, 23, -4, 592, 445, 620],
    [0, 77, 32, 403, 337, 452]
    ]
    path = []

    def __init__(self, goal = (0, 5), start = (5, 0), grid = None):
        """"""
        if grid is None:
            pass
        else:
            self.grid = grid
        self.goal = goal
        self.start = start

    def grid_sum(self):
        """"""
        # new_list = []
        # for sub in self.grid:
        #     for j in sub:
        #         new_list.append(j)
        return sum([j for sub in self.grid for j in sub])

    def simulate(self):
        """"""
        start_die = Dice([0, 0, 0, 0, 0, 0], self.start)
        path = self.RecursiveAdvance([], start_die)
        print("mypath", path)
        print("catched path", self.path)
        return path

    def RecursiveAdvance(self, inp_path: list, inp_cube: Dice) -> list:
        """"""
        print(inp_cube)
        childs = []
        # print("cube loc", inp_cube.location, "step", inp_cube.step, "scorechange", inp_cube.step*inp_cube.data[0], "score", inp_cube.score, "id", id(inp_cube))
        if inp_cube.location == self.goal:
            self.path = inp_path
            print("HORYA", inp_path)
            print("Dice used", inp_cube)
            return inp_path
        
        for direction in ["N", "E", "S", "W"]:  
            print(inp_cube.location, "|", inp_cube.location[0] + inp_cube.LOCATION_MAPPINGS[direction][0],
                inp_cube.location[1] + inp_cube.LOCATION_MAPPINGS[direction][1])
            cube = inp_cube.copy()
            path = deepcopy(inp_path)

            try:
                grid_score = self.grid\
                    [cube.location[0]+cube.LOCATION_MAPPINGS[direction][0]]\
                    [cube.location[1]+cube.LOCATION_MAPPINGS[direction][1]]
            except IndexError:
                continue

            if cube.location[0]+cube.LOCATION_MAPPINGS[direction][0] < 0 or \
                cube.location[1]+cube.LOCATION_MAPPINGS[direction][1] < 0:
                continue

            if cube.get_face_value(direction) == 0:
                cube.tip(direction)
                cube.new_face((grid_score-cube.score)/cube.step)

            elif cube.get_face_value(direction) != 0:
                if ((grid_score - cube.score) / (cube.step + 1)) == cube.get_face_value(direction):
                    print("grid score", grid_score, "expected face", (grid_score - cube.score) / (cube.step + 1), "actual face", cube.get_face_value(direction))
                    print("Good Match")
                    cube.tip(direction)
                    print(cube)
                    
                else:
                    print("expected face", (grid_score - cube.score) / (cube.step + 1), "actual face", cube.get_face_value(direction))
                    continue

            cube.inc_score()
            path.append(grid_score)
            childs.append((path, cube))
        # return [self.RecursiveAdvance(childs[index][0], childs[index][1]) for index in range(len(childs))]
        if len(childs) == 0:
            return []
        else:
            # print("CHILD", childs)
            return max([self.RecursiveAdvance(childs[index][0], childs[index][1]) for index in range(len(childs))])


def path_uniques(input_path: list) -> list:
    new_list = []
    for i in input_path:
        if i in new_list:
            pass
        else:
            new_list.append(i)
    return new_list


myGrid = Grid()
final_path = myGrid.simulate()
print(final_path)
final_path_uniques = path_uniques(final_path)
print([j for sub in myGrid.grid for j in sub])
print(final_path_uniques)
unvisited_squares_sum = 0
unvisited_squares = []
for i in [j for sub in myGrid.grid for j in sub]:
    if i not in final_path_uniques:
        unvisited_squares_sum += i
        unvisited_squares.append(i)
print(unvisited_squares)
print(unvisited_squares_sum)