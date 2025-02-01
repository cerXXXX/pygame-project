from enemy import *
from events import *

towers_data = [
    {
        'name': 'Артиллерийская башня',
        'icon': 'assets/tower1.png',
        'rate_of_fire': 2.0,  # Чуть медленнее стреляет
        'damage': 11,  # Снижен урон
        'visibility_zone': 220,
        'cost': 300,
        'armor_piercing': 50,
        'kill_zone': 0
    },
    {
        'name': 'Стрелковая башня',
        'icon': 'assets/tower4.png',
        'rate_of_fire': 5,
        'damage': 2,
        'visibility_zone': 320,
        'cost': 250,
        'armor_piercing': 5,
        'kill_zone': 0
    },
    {
        'name': 'Башня Гатлинга',
        'icon': 'assets/tower1.png',
        'rate_of_fire': 35,  # Чуть снизили скорострельность
        'damage': 0.85,  # Еще меньше урона
        'visibility_zone': 450,
        'cost': 200,
        'armor_piercing': 0,
        'kill_zone': 0
    },
    {
        'name': 'Противотанковая башня',
        'icon': 'assets/tower3.png',
        'rate_of_fire': 0.7,  # Стала еще медленнее
        'damage': 20,  # Чуть меньше урон
        'visibility_zone': 200,
        'cost': 600,
        'armor_piercing': 100,
        'kill_zone': 0
    },
    {
        'name': 'Ракетная установка',
        'icon': 'assets/tower7.png',
        'rate_of_fire': 0.5,  # Еще медленнее
        'damage': 80,  # Чуть меньше урон
        'visibility_zone': 200,
        'cost': 800,
        'armor_piercing': 100,
        'kill_zone': 20  # Уменьшен радиус взрыва
    }
]


ways_data = {1: [(-1, 10), (0, 10), (1, 10), (2, 10), (3, 10), (4, 10), (5, 10), (6, 10), (7, 10), (8, 10), (9, 10),
                 (10, 10), (11, 10), (12, 10), (13, 10), (14, 10), (15, 10), (16, 10), (17, 10), (18, 10), (19, 10),
                 (20, 10)],
             2: [(-1, 10), (0, 10), (1, 10), (2, 10), (3, 10), (4, 10), (5, 10), (6, 10), (7, 10), (8, 10), (9, 10),
                 (10, 10), (11, 10), (12, 10), (13, 10), (14, 10), (15, 10), (16, 10), (17, 10), (18, 10), (19, 10),
                 (20, 10)],
             3: [(-1, 5), (0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5), (10, 5),
                 (11, 5),
                 (12, 5), (13, 5), (14, 5), (14, 6), (14, 7), (14, 8), (14, 9), (14, 10), (14, 11), (14, 12), (14, 13),
                 (14, 14), (14, 15), (14, 16), (14, 17), (14, 18), (14, 19), (14, 20)],
             4: [(-1, 5), (0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5), (10, 5),
                 (11, 5),
                 (12, 5), (13, 5), (14, 5), (14, 6), (14, 7), (14, 8), (14, 9), (14, 10), (14, 11), (14, 12), (14, 13),
                 (14, 14), (14, 15), (14, 16), (14, 17), (14, 18), (14, 19), (14, 20)],

             5: [(-1, 11), (0, 11), (1, 11), (2, 11), (3, 11), (4, 11), (5, 11), (6, 11), (6, 10), (6, 9), (6, 8),
                 (6, 7), (7, 7), (8, 7), (9, 7), (10, 7),
                 (11, 7), (12, 7), (13, 7), (13, 8), (13, 9),
                 (13, 10), (13, 11), (14, 11), (15, 11), (16, 11),
                 (17, 11), (18, 11), (19, 11), (20, 11)],
             6: [(-1, 11), (0, 11), (1, 11), (2, 11), (3, 11), (4, 11), (5, 11), (6, 11), (6, 10), (6, 9), (6, 8),
                 (6, 7), (7, 7), (8, 7), (9, 7), (10, 7),
                 (11, 7), (12, 7), (13, 7), (13, 8), (13, 9),
                 (13, 10), (13, 11), (14, 11), (15, 11), (16, 11),
                 (17, 11), (18, 11), (19, 11), (20, 11)],

             7: [(-1, 4), (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (7, 5), (7, 6), (7, 7),
                 (7, 8), (7, 9),
                 (8, 9), (9, 9), (10, 9), (11, 9), (12, 9), (13, 9), (13, 10), (13, 11), (13, 12), (13, 13), (13, 14),
                 (13, 15), (14, 15), (15, 15), (16, 15), (17, 15), (18, 15), (19, 15), (20, 15)],
             8: [(-1, 4), (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (7, 5), (7, 6), (7, 7),
                 (7, 8), (7, 9),
                 (8, 9), (9, 9), (10, 9), (11, 9), (12, 9), (13, 9), (13, 10), (13, 11), (13, 12), (13, 13), (13, 14),
                 (13, 15), (14, 15), (15, 15), (16, 15), (17, 15), (18, 15), (19, 15), (20, 15)],

             9: [(-1, 10), (0, 10), (1, 10), (2, 10), (3, 10), (4, 10), (4, 11), (4, 12), (4, 13), (4, 14), (5, 14),
                 (6, 14),
                 (7, 14), (8, 14), (8, 13), (8, 12), (8, 11), (8, 10), (8, 9), (8, 8), (9, 8), (10, 8), (11, 8),
                 (12, 8), (13, 8),
                 (13, 9), (13, 10), (13, 11), (13, 12), (14, 12), (15, 12), (16, 12), (17, 12), (18, 12), (18, 11),
                 (18, 10),
                 (18, 9), (18, 8), (18, 7), (19, 7), (20, 7)],
             10: [(-1, 10), (0, 10), (1, 10), (2, 10), (3, 10), (4, 10), (4, 11), (4, 12), (4, 13), (4, 14), (5, 14),
                  (6, 14),
                  (7, 14), (8, 14), (8, 13), (8, 12), (8, 11), (8, 10), (8, 9), (8, 8), (9, 8), (10, 8), (11, 8),
                  (12, 8), (13, 8),
                  (13, 9), (13, 10), (13, 11), (13, 12), (14, 12), (15, 12), (16, 12), (17, 12), (18, 12), (18, 11),
                  (18, 10),
                  (18, 9), (18, 8), (18, 7), (19, 7), (20, 7)]}

waves_data = {
    1: [[Car, Car, Car]],  # 1 волна
    2: [[Car, Car], [Car, Car, Car], [Tank, Car]],  # 3 волны
    3: [[Car, Car, FastCar], [Car, FastCar, Tank], [Tank, Tank, Car, FastCar]],  # 3 волны
    4: [[FastCar, FastCar, FastCar], [Car, Car, Tank, Tank], [Tank, HeavyTank], [FastCar, Tank, HeavyTank]],  # 4 волны
    5: [[Car, Car, Car, Car, Car, Car, Car, Car],  # Увеличено в 2 раза
        [Car, Car, Car, Car, Tank, Tank, Tank],  # В 2 раза больше
        [Tank, HeavyTank, HeavyTank, HeavyTank, HeavyTank, Tank, Tank],  # В 2-2.5 раза больше
        [Tank, Tank, HeavyTank, HeavyTank, HeavyTank, HeavyTank, HeavyTank, Car, Car]],  # В 2.5 раза больше

    6: [[Car, Car, Car, Car, Car, Tank, Tank, Tank],  # В 2 раза больше
        [Car, Car, Car, Tank, Tank, Tank, HeavyTank, HeavyTank],  # В 2-3 раза больше
        [HeavyTank, HeavyTank, HeavyTank, HeavyTank, HeavyTank, HeavyTank, Car, Car],  # В 2.5 раза больше
        [Car, Car, Tank, Tank, Tank, Tank, Tank, Tank],  # В 3 раза больше
        [Car, Car, Car, Car, Car, Car, Tank, Tank, HeavyTank, HeavyTank]],
    # В 2-2.5 раза больше

    7: [[Tank, Tank, Tank, Tank, Tank, HeavyTank, HeavyTank, HeavyTank],  # В 2-2.5 раза больше
        [FastCar, FastCar, FastCar, HeavyTank, HeavyTank, HeavyTank, HeavyTank],  # В 2.5 раза больше
        [Tank, Tank, Tank, HeavyTank, HeavyTank, HeavyTank, HeavyTank, FastCar, FastCar],  # В 2.5 раза больше
        [FastCar, FastCar, FastCar, FastCar, HeavyTank, HeavyTank, HeavyTank, HeavyTank],  # В 3 раза больше
        [Tank, Tank, Tank, Tank, Tank, Tank, FastCar, FastCar]],  # В 2.5 раза больше

    8: [[FastCar, FastCar, FastCar, FastCar, Tank, Tank, Tank, Tank],  # В 2 раза больше
        [Tank, HeavyTank, HeavyTank, HeavyTank, HeavyTank, FastCar, FastCar],  # В 2.5 раза больше
        [HeavyTank, HeavyTank, HeavyTank, HeavyTank, HeavyTank, HeavyTank, HeavyTank, HeavyTank],  # В 2 раза больше
        [FastCar, FastCar, FastCar, FastCar, FastCar, Tank, Tank, Tank, Tank],  # В 3 раза больше
        [Tank, HeavyTank, HeavyTank, HeavyTank, HeavyTank, HeavyTank, HeavyTank, HeavyTank]],  # В 2-2.5 раза больше

    9: [[Car, Car, Car, Car, Tank, Tank, Tank, Tank, Tank, Tank],  # В 2.5 раза больше
        [FastCar, FastCar, FastCar, FastCar, FastCar, Tank, HeavyTank, HeavyTank],  # В 3 раза больше
        [HeavyTank, HeavyTank, HeavyTank, HeavyTank, HeavyTank, HeavyTank, FastCar, FastCar],  # В 2.5 раза больше
        [Tank, Tank, HeavyTank, HeavyTank, HeavyTank, HeavyTank],  # В 2 раза больше
        [FastCar, FastCar, FastCar, FastCar, FastCar, FastCar, Tank, Tank],  # В 3 раза больше
        [HeavyTank, HeavyTank, HeavyTank, HeavyTank, Tank, Tank, Tank, Tank]],  # В 2-2.5 раза больше

    10: [[Tank, Tank, Tank, Tank, Tank, HeavyTank, HeavyTank, HeavyTank, HeavyTank, HeavyTank],  # В 2.5 раза больше
         [FastCar, FastCar, FastCar, FastCar, Tank, HeavyTank, HeavyTank, HeavyTank],  # В 3 раза больше
         [HeavyTank, HeavyTank, HeavyTank, HeavyTank, HeavyTank, HeavyTank, HeavyTank, HeavyTank, Tank, Tank],
         # В 2.5 раза больше
         [FastCar, FastCar, FastCar, FastCar, FastCar, Tank, HeavyTank, HeavyTank, HeavyTank],  # В 3 раза больше
         [Tank, HeavyTank, HeavyTank, HeavyTank, HeavyTank, HeavyTank, HeavyTank, HeavyTank, FastCar, FastCar],
         # В 2.5 раза больше
         [HeavyTank, HeavyTank, HeavyTank, HeavyTank, HeavyTank, HeavyTank, Tank, Tank, Tank, Tank]],
    # В 2-3 раза больше
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
7: [(10, 5), (2, 7), (16, 11), (9, 12)],
8: [(10, 5), (2, 7), (16, 11), (9, 12)],
9: [(1, 7), (15, 9), (10, 10), (1, 12), (6, 16)],
10: [(4, 6), (15, 9), (10, 10), (1, 12), (6, 16)]}

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
