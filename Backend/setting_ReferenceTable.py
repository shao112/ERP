
#時津
def get_sleep_json():

    data = [
    [0, 0.5, 1, 1.5, 2, 2, 2, 2.5, 3, 4, 4.5, 5, 6],
    [0.5, 0, 0.5, 1, 1.5, 2, 2, 2, 2.5, 3, 4, 4.5, 5],
    [1, 0.5, 0, 0.5, 1, 1.5, 2, 2, 2, 2.5, 3, 4, 4.5],
    [1.5, 1, 0.5, 0, 0.5, 1, 1.5, 2, 2, 2, 2.5, 3, 4],
    [2, 1.5, 1, 0.5, 0, 0.5, 1, 1.5, 2, 2, 2, 2.5, 3],
    [2, 2, 1.5, 1, 0.5, 0, 0.5, 1, 1.5, 2, 2, 2, 2.5],
    [2, 2, 2, 1.5, 1, 0.5, 0, 0.5, 1, 1.5, 2, 2, 2],
    [2.5, 2, 2, 2, 1.5, 1, 0.5, 0, 0.5, 1, 1.5, 2, 2],
    [3, 2.5, 2, 2, 2, 1.5, 1, 0.5, 0, 0.5, 1, 2, 2],
    [4, 3, 2.5, 2, 2, 2, 1.5, 1, 0.5, 0, 0.5, 1, 2],
    [4.5, 4, 3, 2.5, 2, 2, 2, 1.5, 1, 0.5, 0, 0.5, 1],
    [5, 4.5, 4, 3, 2.5, 2, 2, 2, 2, 1, 0.5, 0, 1],
    [6, 5, 4.5, 4, 3, 2.5, 2, 2, 2, 2, 1, 1, 0],
    [5, 6, 7, 7, 6, 5, 5, 5, 5, 5, 4, 3, 2],
    [2, 3, 3, 3, 4, 4, 5, 5, 6, 7, 6, 5, 4]
]

    start_points = ["宜蘭", "北北基", "桃園", "新竹", "苗栗", "台中", "南投", "彰化", "雲林", "嘉義", "台南", "高雄", "屏東"]
    business_trip_destinations = ["宜蘭", "北北基", "桃園", "新竹", "苗栗", "台中", "南投", "彰化", "雲林", "嘉義", "台南", "高雄", "屏東", "台東", "花蓮"]

    # 生成 JSON 数据
    matrix = []

    for i in range(len(start_points)):
        for j in range(len(business_trip_destinations)):
            print(start_points[i],business_trip_destinations[j])
            matrix.append({
                "location_city_residence": start_points[i],
                "location_city_business_trip": business_trip_destinations[j],
                "amount": data[j][i],
                "name": "車程津貼"
            })
            print("--")

    
    for entry in matrix:
        ReferenceTable.objects.create(
            location_city_residence=entry["location_city_residence"],
            location_city_business_trip=entry["location_city_business_trip"],
            amount=entry["amount"],
            name=entry["name"]
        )


# 出差津貼
def get_json():
    data = [
            [250, 250, 250, 250, 250, 350, 350, 350, 450, 450, 450, 550, 550],
            [250, 250, 250, 250, 250, 250, 350, 350, 350, 450, 450, 450, 550],
            [250, 250, 250, 250, 250, 250, 250, 350, 350, 350, 450, 450, 450],
            [250, 250, 250, 250, 250, 250, 250, 250, 350, 350, 350, 450, 450],
            [250, 250, 250, 250, 250, 250, 250, 250, 250, 350, 350, 350, 450],
            [350, 250, 250, 250, 250, 250, 250, 250, 250, 250, 350, 350, 350],
            [350, 350, 250, 250, 250, 250, 250, 250, 250, 250, 250, 350, 350],
            [350, 350, 350, 250, 250, 250, 250, 250, 250, 250, 250, 250, 350],
            [450, 350, 350, 350, 250, 250, 250, 250, 250, 250, 250, 250, 250],
            [450, 450, 350, 350, 350, 250, 250, 250, 250, 250, 250, 250, 250],
            [450, 450, 450, 350, 350, 350, 250, 250, 250, 250, 250, 250, 250],
            [550, 450, 450, 450, 350, 350, 350, 250, 250, 250, 250, 250, 250],
            [550, 550, 450, 450, 450, 350, 350, 350, 250, 250, 250, 250, 250],
            [550, 550, 550, 550, 550, 550, 550, 550, 550, 550, 550, 550, 550],
            [550, 550, 550, 550, 550, 550, 550, 550, 550, 550, 550, 550, 550]
        ]

    city_names = [
        "宜蘭", "北北基", "桃園", "新竹", "苗栗", "台中", "南投", "彰化", "雲林",
        "嘉義", "台南", "高雄", "屏東"
    ]

    location_city = []

    for i in range(len(city_names)):
        for j in range(len(city_names)):
            location_city.append({
                "location_city_residence": city_names[i],
                "location_city_business_trip": city_names[j],
                "amount": data[i][j],
                "name": "出差津貼"
            })

    for i in range(len(city_names)):
        location_city.append({
            "location_city_residence": city_names[i],
            "location_city_business_trip": "花蓮",
            "amount": 550,
            "name": "出差津貼"
        })
        location_city.append({
            "location_city_residence": "花蓮",
            "location_city_business_trip": city_names[i],
            "amount": 550,
            "name": "出差津貼"
        })
        location_city.append({
            "location_city_residence": city_names[i],
            "location_city_business_trip":"台東" ,
            "amount": 550,
            "name": "出差津貼"
        })
        location_city.append({
            "location_city_residence": "台東",
            "location_city_business_trip": city_names[i],
            "amount": 550,
            "name": "出差津貼"
        })

    location_city.append({
            "location_city_residence": "台東",
            "location_city_business_trip": "花蓮",
            "amount": 550,
            "name": "出差津貼"
        })
    location_city.append({
            "location_city_residence": "花蓮",
            "location_city_business_trip": "台東",
            "amount": 550,
            "name": "出差津貼"
        })

    # print(location_city)


    for entry in location_city:
        ReferenceTable.objects.create(
            location_city_residence=entry["location_city_residence"],
            location_city_business_trip=entry["location_city_business_trip"],
            amount=entry["amount"],
            name=entry["name"]
        )
        
# 派工-伙食津貼
def get_p_allowance_json():
    data = [
        [150, 150, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300],
        [150, 150, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300],
        [300, 300, 150, 150, 150, 150, 150, 150, 150, 300, 300, 300, 300, 300, 300],
        [300, 300, 150, 150, 150, 150, 150, 150, 150, 300, 300, 300, 300, 300, 300],
        [300, 300, 150, 150, 150, 150, 150, 150, 150, 300, 300, 300, 300, 300, 300],
        [300, 300, 150, 150, 150, 150, 150, 150, 150, 300, 300, 300, 300, 300, 300],
        [300, 300, 150, 150, 150, 150, 150, 150, 150, 300, 300, 300, 300, 300, 300],
        [300, 300, 150, 150, 150, 150, 150, 150, 150, 300, 300, 300, 300, 300, 300],
        [300, 300, 150, 150, 150, 150, 150, 150, 150, 300, 300, 300, 300, 300, 300],
        [300, 300, 300, 300, 300, 300, 300, 300, 300, 150, 150, 150, 150, 150, 150],
        [300, 300, 300, 300, 300, 300, 300, 300, 300, 150, 150, 150, 150, 150, 150],
        [300, 300, 300, 300, 300, 300, 300, 300, 300, 150, 150, 150, 150, 150, 150],
        [300, 300, 300, 300, 300, 300, 300, 300, 300, 150, 150, 150, 150, 150, 150],
        [300, 300, 300, 300, 300, 300, 300, 300, 300, 150, 150, 150, 150, 150, 150],
        [300, 300, 300, 300, 300, 300, 300, 300, 300, 150, 150, 150, 150, 150, 150]
    ]

    start_points = ["花蓮", "台東", "宜蘭", "北北基", "桃園", "新竹", "苗栗", "台中", "南投", "彰化", "雲林", "嘉義", "台南", "高雄", "屏東"]
    business_trip_destinations = ["花蓮", "台東", "宜蘭", "北北基", "桃園", "新竹", "苗栗", "台中", "南投", "彰化", "雲林", "嘉義", "台南", "高雄", "屏東"]

    matrix = []

    for i in range(len(start_points)):
        for j in range(len(business_trip_destinations)):
            matrix.append({
                "location_city_residence": start_points[i],
                "location_city_business_trip": business_trip_destinations[j],
                "amount": data[j][i],
                "name": "派工-伙食津貼"
            })

    for entry in matrix:
        ReferenceTable.objects.create(
            location_city_residence=entry["location_city_residence"],
            location_city_business_trip=entry["location_city_business_trip"],
            amount=entry["amount"],
            name=entry["name"]
        )

#建立勞健保
def labor_health():
    data = [
    (1, 1500, 266, 933, 90, 409, 1286),
    (1501, 3000, 266, 933, 180, 409, 1286),
    (3001, 4500, 266, 933, 270, 409, 1286),
    (4501, 6000, 266, 933, 360, 409, 1286),
    (6001, 7500, 266, 933, 450, 409, 1286),
    (7501, 8700, 266, 933, 522, 409, 1286),
    (8701, 9900, 266, 933, 594, 409, 1286),
    (9901, 11100, 266, 933, 666, 409, 1286),
    (11101, 12540, 301, 1054, 752, 409, 1286),
    (12541, 13500, 324, 1135, 810, 409, 1286),
    (13501, 15840, 380, 1331, 950, 409, 1286),
    (15841, 16500, 396, 1387, 990, 409, 1286),
    (16501, 17280, 415, 1452, 1037, 409, 1286),
    (17281, 17880, 429, 1502, 1073, 409, 1286),
    (17881, 19047, 457, 1600, 1143, 409, 1286),
    (19048, 20008, 480, 1681, 1200, 409, 1286),
    (20009, 21009, 504, 1765, 1261, 409, 1286),
    (21010, 22000, 528, 1848, 1320, 409, 1286),
    (22001, 23100, 554, 1941, 1386, 409, 1286),
    (23101, 24000, 576, 2016, 1440, 409, 1286),
    (24001, 25250, 607, 2121, 1515, 409, 1286),
    (25251, 26400, 634, 2218, 1584, 409, 1286),
    (26401, 27600, 662, 2318, 1656, 428, 1344),
    (27601, 28800, 692, 2420, 1728, 447, 1403),
    (28801, 30300, 728, 2545, 1818, 470, 1476),
    (30301, 31800, 764, 2672, 1908, 493, 1549),
    (31801, 33300, 800, 2797, 1998, 516, 1622),
    (33301, 34800, 836, 2924, 2088, 540, 1695),
    (34801, 36300, 872, 3049, 2178, 563, 1768),
    (36301, 38200, 916, 3208, 2292, 592, 1860),
    (38201, 40100, 962, 3369, 2406, 622, 1953),
    (40101, 42000, 1008, 3528, 2520, 651, 2045),
    (42001, 43900, 1054, 3687, 2634, 681, 2138),
    (43901, 45800, 1100, 3848, 2748, 710, 2231),
    (45801, 48200, 1100, 3848, 2892, 748, 2347),
    (48201, 50600, 1100, 3848, 3036, 785, 2464),
    (50601, 53000, 1100, 3848, 3180, 822, 2581),
    (53001, 55400, 1100, 3848, 3324, 859, 2698),
    (55401, 57800, 1100, 3848, 3468, 896, 2815),
    (57801, 60800, 1100, 3848, 3648, 943, 2961),
    (60801, 63800, 1100, 3848, 3828, 990, 3107),
    (63801, 66800, 1100, 3848, 4008, 1036, 3253),
    (66801, 69800, 1100, 3848, 4188, 1083, 3399),
    (69801, 72800, 1100, 3848, 4368, 1129, 3545),
    (72801, 76500, 1100, 3848, 4590, 1187, 3726),
    (76501, 80200, 1100, 3848, 4812, 1244, 3906),
(80201, 83900, 1100, 3848, 5034, 1301, 4086),
(83901, 87600, 1100, 3848, 5256, 1359, 4266),
(87601, 92100, 1100, 3848, 5526, 1428, 4485),
(92101, 96600, 1100, 3848, 5796, 1498, 4705),
(96601, 101100, 1100, 3848, 6066, 1568, 4924),
(101101, 105600, 1100, 3848, 6336, 1638, 5143),
(105601, 110100, 1100, 3848, 6606, 1708, 5362),
(110101, 115500, 1100, 3848, 6930, 1791, 5625),
(115501, 120900, 1100, 3848, 7254, 1875, 5888),
(120901, 126300, 1100, 3848, 7578, 1959, 6151),
(126301, 131700, 1100, 3848, 7902, 2043, 6414),
(131701, 137100, 1100, 3848, 8226, 2126, 6677),
(137101, 142500, 1100, 3848, 8550, 2210, 6940),
(142501, 147900, 1100, 3848, 8874, 2294, 7203),
(147901, 150000, 1100, 3848, 9000, 2327, 7305),
(150001, 156400, 1100, 3848, 9000, 2426, 7617),
(156401, 162800, 1100, 3848, 9000, 2525, 7929),
(162801, 169200, 1100, 3848, 9000, 2624, 8240),
(169201, 175600, 1100, 3848, 9000, 2724, 8552),
(175601, 182000, 1100, 3848, 9000, 2823, 8864),
(182001, 189500, 1100, 3848, 9000, 2939, 9229),
(189501, 197000, 1100, 3848, 9000, 3055, 9594),
(197001, 204500, 1100, 3848, 9000, 3172, 9959),
(204501, 212000, 1100, 3848, 9000, 3288, 10325),
(212001, 219500, 1100, 3848, 9000, 3404, 10690)

]
    for item in data:
        salary_info = LaborHealthInfo(
            salary_low=item[0],
            salary_high=item[1],
            labor_insurance_personal=item[2],
            labor_insurance_employer=item[3],
            health_insurance_personal=item[5],
            health_insurance_employer=item[6],
            retirement_benefit=item[4]
        )
        salary_info.save()

# 非派工-伙食津貼
def get_nonp_allowance_json():
    data = [
        [0, 150, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300],
        [150, 0, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300],
        [300, 300, 0, 150, 150, 150, 150, 150, 150, 300, 300, 300, 300, 300, 300],
        [300, 300, 150, 0, 150, 150, 150, 150, 150, 300, 300, 300, 300, 300, 300],
        [300, 300, 150, 150, 0, 150, 150, 150, 150, 300, 300, 300, 300, 300, 300],
        [300, 300, 150, 150, 150, 0, 150, 150, 150, 300, 300, 300, 300, 300, 300],
        [300, 300, 150, 150, 150, 150, 0, 150, 150, 300, 300, 300, 300, 300, 300],
        [300, 300, 150, 150, 150, 150, 150, 0, 150, 300, 300, 300, 300, 300, 300],
        [300, 300, 150, 150, 150, 150, 150, 150, 0, 300, 300, 300, 300, 300, 300],
        [300, 300, 300, 300, 300, 300, 300, 300, 300, 0, 150, 150, 150, 150, 150],
        [300, 300, 300, 300, 300, 300, 300, 300, 300, 150, 0, 150, 150, 150, 150],
        [300, 300, 300, 300, 300, 300, 300, 300, 300, 150, 150, 0, 150, 150, 150],
        [300, 300, 300, 300, 300, 300, 300, 300, 300, 150, 150, 150, 0, 150, 150],
        [300, 300, 300, 300, 300, 300, 300, 300, 300, 150, 150, 150, 150, 0, 150],
        [300, 300, 300, 300, 300, 300, 300, 300, 300, 150, 150, 150, 150, 150, 0]
    ]

    start_points = ["花蓮", "台東", "宜蘭", "北北基", "桃園", "新竹", "苗栗", "台中", "南投", "彰化", "雲林", "嘉義", "台南", "高雄", "屏東"]
    business_trip_destinations = ["花蓮", "台東", "宜蘭", "北北基", "桃園", "新竹", "苗栗", "台中", "南投", "彰化", "雲林", "嘉義", "台南", "高雄", "屏東"]

    matrix = []

    for i in range(len(start_points)):
        for j in range(len(business_trip_destinations)):
            matrix.append({
                "location_city_residence": start_points[i],
                "location_city_business_trip": business_trip_destinations[j],
                "amount": data[j][i],
                "name": "非派工-伙食津貼"
            })

    for entry in matrix:
        ReferenceTable.objects.create(
            location_city_residence=entry["location_city_residence"],
            location_city_business_trip=entry["location_city_business_trip"],
            amount=entry["amount"],
            name=entry["name"]
        )

