*** Settings ***
Library    RequestsLibrary
Library    BuiltIn

*** Variables ***
${BASE_URL}    http://127.0.0.1:5000

*** Test Cases ***
Give Rating JSON
    Create Session    foodie    ${BASE_URL}

    # Place Order First
    ${order_data}=    Create Dictionary    user_id=1    restaurant_id=1    dishes=["Idly"]
    ${order_res}=    POST On Session    foodie    /api/v1/orders    json=${order_data}
    Status Should Be    201    ${order_res}

    ${order_json}=    Set Variable    ${order_res.json()}
    ${order_id}=      Set Variable    ${order_json["id"]}

    # Give Rating
    ${rating_data}=    Create Dictionary    order_id=${order_id}    rating=5    comment=Excellent
    ${rating_res}=     POST On Session    foodie    /api/v1/ratings    json=${rating_data}
    Status Should Be    201    ${rating_res}
