
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

