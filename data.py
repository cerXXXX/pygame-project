from enemy import *
from events import *

towers_data = [
    {
        'name': 'Cannon Tower',  # Видимое название
        'icon': 'assets/tower1.png',  # Картинка
        'rate_of_fire': 2,  # Выстрелов в секунду
        'damage': 10,  # Урон
        'visibility_zone': 200,  # Область видимости
        'cost': 200,  # Стоимость
        'armor_piercing': 30,  # Бронепробитие (от 0 до 100)
        'kill_zone': 0  # Радиус поражения (если не 0, то создается BigBullet вместо Bullet)
    },
    {
        'name': 'Archer Tower',
        'icon': 'assets/tower2.png',
        'rate_of_fire': 5,
        'damage': 4,
        'visibility_zone': 300,
        'cost': 150,
        'armor_piercing': 0,
        'kill_zone': 0
    },
    {
        'name': 'Wtf is this tower',
        'icon': 'assets/tower1.png',
        'rate_of_fire': 25,
        'damage': 0.2,
        'visibility_zone': 500,
        'cost': 300,
        'armor_piercing': 0,
        'kill_zone': 0
    },
    {
        'name': 'Armor Piercing Tower',
        'icon': 'assets/tower1.png',
        'rate_of_fire': 1,
        'damage': 50,
        'visibility_zone': 200,
        'cost': 500,
        'armor_piercing': 100,
        'kill_zone': 0
    },
    {
        'name': 'РПГ',
        'icon': 'assets/tower1.png',
        'rate_of_fire': 1,
        'damage': 50,
        'visibility_zone': 200,
        'cost': 500,
        'armor_piercing': 100,
        'kill_zone': 20
    }
]

ways_data = {1: [(-1, 5), (0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5),
                 (9, 6), (9, 7), (10, 7), (11, 7), (12, 7), (12, 8), (12, 9), (12, 10), (12, 11), (12, 12),
                 (12, 13), (11, 13), (10, 13), (9, 13), (8, 13), (7, 13), (6, 13), (5, 13), (5, 14), (5, 15), (5, 16),
                 (5, 17), (6, 17), (7, 17), (8, 17), (9, 17), (10, 17), (11, 17), (12, 17), (13, 17),
                 (14, 17), (15, 17), (16, 17), (17, 17), (18, 17), (19, 17), (20, 17)],
             2: [(0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5),
                 (9, 6), (9, 7), (10, 7), (11, 7), (12, 7), (12, 8), (12, 9), (12, 10), (12, 11), (12, 12),
                 (12, 13), (11, 13), (10, 13), (9, 13), (8, 13), (7, 13), (6, 13), (5, 13), (5, 14), (5, 15), (5, 16),
                 (5, 17), (6, 17), (7, 17), (8, 17), (9, 17), (10, 17), (11, 17), (12, 17), (13, 17),
                 (14, 17), (15, 17), (16, 17), (17, 17), (18, 17), (19, 17)],
             3: [(0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5),
                 (9, 6), (9, 7), (10, 7), (11, 7), (12, 7), (12, 8), (12, 9), (12, 10), (12, 11), (12, 12),
                 (12, 13), (11, 13), (10, 13), (9, 13), (8, 13), (7, 13), (6, 13), (5, 13), (5, 14), (5, 15), (5, 16),
                 (5, 17), (6, 17), (7, 17), (8, 17), (9, 17), (10, 17), (11, 17), (12, 17), (13, 17),
                 (14, 17), (15, 17), (16, 17), (17, 17), (18, 17), (19, 17)],
             4: [(0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5),
                 (9, 6), (9, 7), (10, 7), (11, 7), (12, 7), (12, 8), (12, 9), (12, 10), (12, 11), (12, 12),
                 (12, 13), (11, 13), (10, 13), (9, 13), (8, 13), (7, 13), (6, 13), (5, 13), (5, 14), (5, 15), (5, 16),
                 (5, 17), (6, 17), (7, 17), (8, 17), (9, 17), (10, 17), (11, 17), (12, 17), (13, 17),
                 (14, 17), (15, 17), (16, 17), (17, 17), (18, 17), (19, 17)],
             5: [(0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5),
                 (9, 6), (9, 7), (10, 7), (11, 7), (12, 7), (12, 8), (12, 9), (12, 10), (12, 11), (12, 12),
                 (12, 13), (11, 13), (10, 13), (9, 13), (8, 13), (7, 13), (6, 13), (5, 13), (5, 14), (5, 15), (5, 16),
                 (5, 17), (6, 17), (7, 17), (8, 17), (9, 17), (10, 17), (11, 17), (12, 17), (13, 17),
                 (14, 17), (15, 17), (16, 17), (17, 17), (18, 17), (19, 17)],
             6: [(0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5),
                 (9, 6), (9, 7), (10, 7), (11, 7), (12, 7), (12, 8), (12, 9), (12, 10), (12, 11), (12, 12),
                 (12, 13), (11, 13), (10, 13), (9, 13), (8, 13), (7, 13), (6, 13), (5, 13), (5, 14), (5, 15), (5, 16),
                 (5, 17), (6, 17), (7, 17), (8, 17), (9, 17), (10, 17), (11, 17), (12, 17), (13, 17),
                 (14, 17), (15, 17), (16, 17), (17, 17), (18, 17), (19, 17)],
             7: [(0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5),
                 (9, 6), (9, 7), (10, 7), (11, 7), (12, 7), (12, 8), (12, 9), (12, 10), (12, 11), (12, 12),
                 (12, 13), (11, 13), (10, 13), (9, 13), (8, 13), (7, 13), (6, 13), (5, 13), (5, 14), (5, 15), (5, 16),
                 (5, 17), (6, 17), (7, 17), (8, 17), (9, 17), (10, 17), (11, 17), (12, 17), (13, 17),
                 (14, 17), (15, 17), (16, 17), (17, 17), (18, 17), (19, 17)],
             8: [(0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5),
                 (9, 6), (9, 7), (10, 7), (11, 7), (12, 7), (12, 8), (12, 9), (12, 10), (12, 11), (12, 12),
                 (12, 13), (11, 13), (10, 13), (9, 13), (8, 13), (7, 13), (6, 13), (5, 13), (5, 14), (5, 15), (5, 16),
                 (5, 17), (6, 17), (7, 17), (8, 17), (9, 17), (10, 17), (11, 17), (12, 17), (13, 17),
                 (14, 17), (15, 17), (16, 17), (17, 17), (18, 17), (19, 17)],
             9: [(0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5),
                 (9, 6), (9, 7), (10, 7), (11, 7), (12, 7), (12, 8), (12, 9), (12, 10), (12, 11), (12, 12),
                 (12, 13), (11, 13), (10, 13), (9, 13), (8, 13), (7, 13), (6, 13), (5, 13), (5, 14), (5, 15), (5, 16),
                 (5, 17), (6, 17), (7, 17), (8, 17), (9, 17), (10, 17), (11, 17), (12, 17), (13, 17),
                 (14, 17), (15, 17), (16, 17), (17, 17), (18, 17), (19, 17)],
             10: [(0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5),
                  (9, 6), (9, 7), (10, 7), (11, 7), (12, 7), (12, 8), (12, 9), (12, 10), (12, 11), (12, 12),
                  (12, 13), (11, 13), (10, 13), (9, 13), (8, 13), (7, 13), (6, 13), (5, 13), (5, 14), (5, 15), (5, 16),
                  (5, 17), (6, 17), (7, 17), (8, 17), (9, 17), (10, 17), (11, 17), (12, 17), (13, 17),
                  (14, 17), (15, 17), (16, 17), (17, 17), (18, 17), (19, 17)]}

waves_data = {1: [[Car, Car, Car]],
              2: [[Car], [Car, Car, Car], [Tank, Car]],
              3: [],
              4: [],
              5: [],
              6: [],
              7: [],
              8: [],
              9: [],
              10: []}

background_data = {1: None,
                   2: None,
                   3: None,
                   4: None,
                   5: None,
                   6: None,
                   7: None,
                   8: None,
                   9: None,
                   10: None}

building_places_data = {1: [(3, 2), (2, 7), (6, 7), (8, 2), (12, 4), (14, 9), (17, 4), (8, 10), (2, 14), (9, 14)],
                        2: [(3, 2), (2, 7), (6, 7), (8, 2), (12, 4), (14, 9), (17, 4), (8, 10), (2, 14), (9, 14)],
                        3: [(3, 2), (2, 7), (6, 7), (8, 2), (12, 4), (14, 9), (17, 4), (8, 10), (2, 14), (9, 14)],
                        4: [(3, 2), (2, 7), (6, 7), (8, 2), (12, 4), (14, 9), (17, 4), (8, 10), (2, 14), (9, 14)],
                        5: [(3, 2), (2, 7), (6, 7), (8, 2), (12, 4), (14, 9), (17, 4), (8, 10), (2, 14), (9, 14)],
                        6: [(3, 2), (2, 7), (6, 7), (8, 2), (12, 4), (14, 9), (17, 4), (8, 10), (2, 14), (9, 14)],
                        7: [(3, 2), (2, 7), (6, 7), (8, 2), (12, 4), (14, 9), (17, 4), (8, 10), (2, 14), (9, 14)],
                        8: [(3, 2), (2, 7), (6, 7), (8, 2), (12, 4), (14, 9), (17, 4), (8, 10), (2, 14), (9, 14)],
                        9: [(3, 2), (2, 7), (6, 7), (8, 2), (12, 4), (14, 9), (17, 4), (8, 10), (2, 14), (9, 14)],
                        10: [(3, 2), (2, 7), (6, 7), (8, 2), (12, 4), (14, 9), (17, 4), (8, 10), (2, 14), (9, 14)]}

super_events_data = {1: [],
                     2: [],
                     3: [],
                     4: [SuperEvent(0.1, text='ArtilleryStrike', board=None)],
                     5: [SuperEvent(0.1, text='ArtilleryStrike', board=None)],
                     6: [SuperEvent(0.1, text='ArtilleryStrike', board=None)],
                     7: [SuperEvent(0.1, text='ArtilleryStrike', board=None)],
                     8: [SuperEvent(0.1, text='ArtilleryStrike', board=None)],
                     9: [SuperEvent(0.1, text='ArtilleryStrike', board=None)],
                     10: [SuperEvent(0.1, text='ArtilleryStrike', board=None),
                          SuperEvent(0.4, text='Freeze', board=None)]}
