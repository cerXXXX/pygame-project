class Level:
    def __init__(self, way, waves, background, building_places: list[tuple[int, int]]):
        self.way = way
        self.waves = waves
        self.background = background
        self.building_places = building_places
