*** Settings ***
Resource    ../resources/keywords.robot
Resource    ../resources/variables.robot

*** Test Cases ***
Give Rating
    Create API Session
    ${rand}=    Generate Random Name

    ${restaurant}=    Create Dictionary
    ...    name=RatingRest_${rand}
    ...    category=Veg
    ...    location=Hyderabad

    ${r_resp}=    POST On Session    foodie    /api/v1/restaurants    json=${restaurant}
    ${r_json}=    Set Variable    ${r_resp.json()}
    ${restaurant_id}=    Set Variable    ${r_json["id"]}

    ${email}=    Set Variable    user_${rand}@test.com
    ${user}=    Create Dictionary
    ...    name=RatingUser
    ...    email=${email}
    ...    password=1234

    ${u_resp}=    POST On Session    foodie    /api/v1/users/register    json=${user}
    ${u_json}=    Set Variable    ${u_resp.json()}
    ${user_id}=    Set Variable    ${u_json["user_id"]}

    ${order}=    Create Dictionary
    ...    user_id=${user_id}
    ...    restaurant_id=${restaurant_id}

    ${o_resp}=    POST On Session    foodie    /api/v1/orders    json=${order}
    ${o_json}=    Set Variable    ${o_resp.json()}
    ${order_id}=    Set Variable    ${o_json["order_id"]}

    ${rating}=    Create Dictionary
    ...    order_id=${order_id}
    ...    rating=5
    ...    comment=Excellent

    ${rating_resp}=    POST On Session    foodie    /api/v1/ratings    json=${rating}
    Status Should Be    201    ${rating_resp}