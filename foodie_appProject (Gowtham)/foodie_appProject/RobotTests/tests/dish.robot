*** Settings ***
Resource    ../resources/keywords.robot
Resource    ../resources/variables.robot

*** Test Cases ***
Add Dish
    Create API Session
    ${rand}=    Generate Random Name
    ${rname}=    Set Variable    DishRest_${rand}

    ${restaurant}=    Create Dictionary
    ...    name=${rname}
    ...    category=Veg
    ...    location=Hyderabad

    ${r_resp}=    POST On Session    foodie    /api/v1/restaurants    json=${restaurant}
    ${r_json}=    Set Variable    ${r_resp.json()}
    ${restaurant_id}=    Set Variable    ${r_json["id"]}

    ${dish}=    Create Dictionary
    ...    name=Paneer Biryani
    ...    price=250

    ${d_resp}=    POST On Session    foodie    /api/v1/restaurants/${restaurant_id}/dishes    json=${dish}
    Status Should Be    201    ${d_resp}