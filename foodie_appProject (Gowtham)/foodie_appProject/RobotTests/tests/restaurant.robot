*** Settings ***
Resource    ../resources/keywords.robot
Resource    ../resources/variables.robot

*** Test Cases ***
Register Restaurant
    Create API Session
    ${rand}=    Generate Random Name
    ${name}=    Set Variable    Restaurant_${rand}

    ${payload}=    Create Dictionary
    ...    name=${name}
    ...    category=Veg
    ...    location=Hyderabad

    ${response}=    POST On Session    foodie    /api/v1/restaurants    json=${payload}
    Status Should Be    201    ${response}