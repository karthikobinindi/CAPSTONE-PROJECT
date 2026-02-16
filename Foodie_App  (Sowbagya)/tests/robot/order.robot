*** Settings ***
Library    RequestsLibrary

*** Variables ***
${BASE_URL}    http://127.0.0.1:5000

*** Test Cases ***
Place Order JSON
    Create Session    foodie    ${BASE_URL}
    ${data}=    Create Dictionary    user_id=1    restaurant_id=1    dishes=["Idly","Dosa"]
    ${res}=    POST On Session    foodie    /api/v1/orders    json=${data}
    Status Should Be    201    ${res}
