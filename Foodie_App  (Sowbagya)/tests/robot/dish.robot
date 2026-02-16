*** Settings ***
Library    RequestsLibrary
Library    BuiltIn

*** Variables ***
${BASE_URL}    http://127.0.0.1:5000

*** Test Cases ***

Add Dish JSON
    Create Session    foodie    ${BASE_URL}

    # Add Dish for Restaurant ID = 1 (Change if needed)
    ${dish_data}=    Create Dictionary    name=Robot Dish    type=Lunch    price=120    available_time=Afternoon
    ${res}=    POST On Session    foodie    /api/v1/restaurants/1/dishes    json=${dish_data}
    Status Should Be    201    ${res}

Update Dish JSON
    Create Session    foodie    ${BASE_URL}

    # First Add Dish
    ${dish_data}=    Create Dictionary    name=Robot Dish2    type=Dinner    price=150    available_time=Evening
    ${res}=    POST On Session    foodie    /api/v1/restaurants/1/dishes    json=${dish_data}
    Status Should Be    201    ${res}

    ${dish_json}=    Set Variable    ${res.json()}
    ${dish_id}=      Set Variable    ${dish_json["id"]}

    # Update Dish
    ${update_data}=    Create Dictionary    name=Robot Dish Updated    price=200
    ${update_res}=     PUT On Session    foodie    /api/v1/dishes/${dish_id}    json=${update_data}
    Status Should Be    200    ${update_res}

Disable Dish JSON
    Create Session    foodie    ${BASE_URL}

    # Add Dish
    ${dish_data}=    Create Dictionary    name=Robot Dish3    type=Snack    price=80    available_time=Evening
    ${res}=    POST On Session    foodie    /api/v1/restaurants/1/dishes    json=${dish_data}
    Status Should Be    201    ${res}

    ${dish_json}=    Set Variable    ${res.json()}
    ${dish_id}=      Set Variable    ${dish_json["id"]}

    # Disable Dish
    ${status_data}=    Create Dictionary    enabled=${False}
    ${status_res}=     PUT On Session    foodie    /api/v1/dishes/${dish_id}/status    json=${status_data}
    Status Should Be    200    ${status_res}

Enable Dish JSON
    Create Session    foodie    ${BASE_URL}

    # Add Dish
    ${dish_data}=    Create Dictionary    name=Robot Dish4    type=Breakfast    price=60    available_time=Morning
    ${res}=    POST On Session    foodie    /api/v1/restaurants/1/dishes    json=${dish_data}
    Status Should Be    201    ${res}

    ${dish_json}=    Set Variable    ${res.json()}
    ${dish_id}=      Set Variable    ${dish_json["id"]}

    # Enable Dish
    ${status_data}=    Create Dictionary    enabled=${True}
    ${status_res}=     PUT On Session    foodie    /api/v1/dishes/${dish_id}/status    json=${status_data}
    Status Should Be    200    ${status_res}

Delete Dish JSON
    Create Session    foodie    ${BASE_URL}

    # Add Dish
    ${dish_data}=    Create Dictionary    name=Robot Dish5    type=Fast Food    price=99    available_time=All Day
    ${res}=    POST On Session    foodie    /api/v1/restaurants/1/dishes    json=${dish_data}
    Status Should Be    201    ${res}

    ${dish_json}=    Set Variable    ${res.json()}
    ${dish_id}=      Set Variable    ${dish_json["id"]}

    # Delete Dish
    ${delete_res}=    DELETE On Session    foodie    /api/v1/dishes/${dish_id}
    Status Should Be    200    ${delete_res}