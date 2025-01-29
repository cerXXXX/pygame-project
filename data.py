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

ways_data = {1: [(-1, 10), (0, 10), (1, 10), (2, 10), (3, 10), (4, 10), (5, 10), (6, 10), (7, 10), (8, 10), (9, 10),
                 (10, 10), (11, 10), (12, 10), (13, 10), (14, 10), (15, 10), (16, 10), (17, 10), (18, 10), (19, 10)],
             2: [(-1, 10), (0, 10), (1, 10), (2, 10), (3, 10), (4, 10), (5, 10), (6, 10), (7, 10), (8, 10), (9, 10),
                 (10, 10), (11, 10), (12, 10), (13, 10), (14, 10), (15, 10), (16, 10), (17, 10), (18, 10), (19, 10)],
             3: [(0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5), (10, 5), (11, 5),
                 (12, 5), (13, 5), (14, 5), (14, 6), (14, 7), (14, 8), (14, 9), (14, 10), (14, 11), (14, 12), (14, 13),
                 (14, 14), (14, 15), (14, 16), (14, 17), (14, 18), (14, 19)],
             4: [(0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5), (10, 5), (11, 5),
                 (12, 5), (13, 5), (14, 5), (14, 6), (14, 7), (14, 8), (14, 9), (14, 10), (14, 11), (14, 12), (14, 13),
                 (14, 14), (14, 15), (14, 16), (14, 17), (14, 18), (14, 19)],
             5: [(-1, 11), (0, 11), (1, 11), (2, 11), (3, 11), (4, 11), (5, 11), (6, 11), (6, 10), (6, 9), (6, 8),
                 (6, 7), (7, 7), (8, 7), (9, 7), (10, 7),
                 (11, 7), (12, 7), (13, 7), (13, 8), (13, 9),
                 (13, 10), (13, 11), (14, 11), (15, 11), (16, 11),
                 (17, 11), (18, 11), (19, 11)],
             6: [(-1, 11), (0, 11), (1, 11), (2, 11), (3, 11), (4, 11), (5, 11), (6, 11), (6, 10), (6, 9), (6, 8),
                 (6, 7), (7, 7), (8, 7), (9, 7), (10, 7),
                 (11, 7), (12, 7), (13, 7), (13, 8), (13, 9),
                 (13, 10), (13, 11), (14, 11), (15, 11), (16, 11),
                 (17, 11), (18, 11), (19, 11)],

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

waves_data = {
    1: [[Car, Car, Car]],  # 1 волна
    2: [[Car, Car], [Car, Car, Car], [Tank, Car]],  # 3 волны
    3: [[Car, Car, FastCar], [Car, FastCar, Tank], [Tank, Tank, Car, FastCar]],  # 3 волны
    4: [[FastCar, FastCar, FastCar], [Car, Car, Tank, Tank], [Tank, HeavyTank], [FastCar, Tank, HeavyTank]],  # 4 волны
    5: [[Car, Car, FastCar], [FastCar, FastCar, Tank], [Tank, HeavyTank, HeavyTank],
        [Tank, HeavyTank, HeavyTank, FastCar]],  # 4 волны
    6: [[FastCar, FastCar, FastCar, FastCar], [Car, Tank, HeavyTank], [HeavyTank, HeavyTank, HeavyTank, FastCar],
        [FastCar, Tank, Tank], [FastCar, FastCar, Tank]],  # 5 волн
    7: [[Tank, Tank, Tank, HeavyTank], [FastCar, HeavyTank, HeavyTank], [Tank, HeavyTank, HeavyTank, FastCar],
        [FastCar, FastCar, HeavyTank, HeavyTank], [Tank, Tank, Tank, FastCar]],  # 5 волн
    8: [[FastCar, FastCar, Tank, Tank], [Tank, HeavyTank, HeavyTank, FastCar],
        [HeavyTank, HeavyTank, HeavyTank, HeavyTank], [FastCar, FastCar, Tank, Tank],
        [Tank, HeavyTank, HeavyTank, HeavyTank]],  # 5 волн
    9: [[Car, Car, Tank, Tank, Tank], [FastCar, FastCar, Tank, HeavyTank], [HeavyTank, HeavyTank, HeavyTank, FastCar],
        [Tank, HeavyTank, Tank, HeavyTank], [FastCar, FastCar, FastCar, Tank], [HeavyTank, HeavyTank, Tank, Tank]],
    # 6 волн
    10: [[Tank, Tank, Tank, HeavyTank, HeavyTank], [FastCar, FastCar, Tank, HeavyTank],
         [HeavyTank, HeavyTank, HeavyTank, HeavyTank, Tank], [FastCar, FastCar, Tank, HeavyTank],
         [Tank, HeavyTank, HeavyTank, HeavyTank, FastCar], [HeavyTank, HeavyTank, HeavyTank, HeavyTank, Tank]]  # 6 волн
}

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

building_places_data = {1: [(5, 7), (12, 7), (8, 12), (16, 12)],
                        2: [(5, 7), (12, 7), (8, 12), (16, 12)],
                        3: [(7, 2), (2, 7), (10, 8), (10, 14)],
                        4: [(7, 2), (2, 7), (10, 8), (10, 14)],
                        5: [(9, 4), (2, 7), (16, 7), (9, 9)],
                        6: [(9, 4), (2, 7), (16, 7), (9, 9)],
                        7: [(3, 2), (2, 7), (6, 7), (8, 2), (12, 4), (14, 9), (17, 4), (8, 10), (2, 14), (9, 14)],
                        8: [(3, 2), (2, 7), (6, 7), (8, 2), (12, 4), (14, 9), (17, 4), (8, 10), (2, 14), (9, 14)],
                        9: [(3, 2), (2, 7), (6, 7), (8, 2), (12, 4), (14, 9), (17, 4), (8, 10), (2, 14), (9, 14)],
                        10: [(3, 2), (2, 7), (6, 7), (8, 2), (12, 4), (14, 9), (17, 4), (8, 10), (2, 14), (9, 14)]}

super_events_data = {
    1: [],  # Суперсобытий нет на первом уровне
    2: [],  # На втором уровне тоже нет событий
    3: [SuperEvent(0.01, text='ArtilleryStrike', board=None)],  # Частота удвоена (было 0.005)
    4: [SuperEvent(0.04, text='ArtilleryStrike', board=None)],  # Было 0.02
    5: [SuperEvent(0.06, text='ArtilleryStrike', board=None)],  # Было 0.03
    6: [SuperEvent(0.1, text='ArtilleryStrike', board=None),  # Было 0.05
        SuperEvent(0.04, text='Reinforcements', board=None)],
    7: [SuperEvent(0.2, text='ArtilleryStrike', board=None),  # Было 0.1
        SuperEvent(0.1, text='Freeze', board=None)],  # Было 0.05
    8: [SuperEvent(0.3, text='ArtilleryStrike', board=None),  # Было 0.15
        SuperEvent(0.16, text='Freeze', board=None),  # Было 0.08
        SuperEvent(0.04, text='Reinforcements', board=None)],
    9: [SuperEvent(0.4, text='ArtilleryStrike', board=None),  # Было 0.2
        SuperEvent(0.2, text='Freeze', board=None),  # Было 0.1
        SuperEvent(0.06, text='Reinforcements', board=None)],
    10: [SuperEvent(0.5, text='ArtilleryStrike', board=None),  # Было 0.25
         SuperEvent(0.3, text='Freeze', board=None),  # Было 0.15
         SuperEvent(0.1, text='Reinforcements', board=None),
         SuperEvent(0.05, text='ChaosMode', board=None)]
}
