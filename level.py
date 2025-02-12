from data import ways_data, waves_data, background_data, building_places_data, super_events_data


class Level:
    """Класс уровня"""

    def __init__(self, way, waves, background, building_places: list[tuple[int, int]], super_events=None):
        self.way = way
        self.waves = waves
        self.background = background
        self.building_places = building_places
        self.super_events = super_events if super_events else []


class DefaultLevel(Level):
    """Класс уровня по умолчанию (вся информация берется из data.py)"""

    levels = {1: Level(ways_data[1], waves_data[1], background_data[1], building_places_data[1], super_events_data[1]),
              2: Level(ways_data[2], waves_data[2], background_data[2], building_places_data[2], super_events_data[2]),
              3: Level(ways_data[3], waves_data[3], background_data[3], building_places_data[3], super_events_data[3]),
              4: Level(ways_data[4], waves_data[4], background_data[4], building_places_data[4], super_events_data[4]),
              5: Level(ways_data[5], waves_data[5], background_data[5], building_places_data[5], super_events_data[5]),
              6: Level(ways_data[6], waves_data[6], background_data[6], building_places_data[6], super_events_data[6]),
              7: Level(ways_data[7], waves_data[7], background_data[7], building_places_data[7], super_events_data[7]),
              8: Level(ways_data[8], waves_data[8], background_data[8], building_places_data[8], super_events_data[8]),
              9: Level(ways_data[9], waves_data[9], background_data[9], building_places_data[9], super_events_data[9]),
              10: Level(ways_data[10], waves_data[10], background_data[10], building_places_data[10],
                        super_events_data[10])}

    def __init__(self, num):
        super().__init__(self.levels[num].way, self.levels[num].waves, self.levels[num].background,
                         self.levels[num].building_places, self.levels[num].super_events)
