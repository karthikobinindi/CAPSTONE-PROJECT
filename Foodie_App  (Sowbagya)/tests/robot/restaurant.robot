*** Settings ***
Library    RequestsLibrary
Library    BuiltIn

*** Variables ***
${BASE_URL}    http://127.0.0.1:5000

*** Test Cases ***
Register Restaurant JSON
    ${rand}=    Evaluate    __import__('random').randint(1000,9999)
    Create Session    foodie    ${BASE_URL}
    ${data}=    Create Dictionary    name=RobotRest${rand}    category=Veg    location=Chennai    contact=9876543210
    ${res}=    POST On Session    foodie    /api/v1/restaurants    json=${data}
    Status Should Be    201    ${res}
