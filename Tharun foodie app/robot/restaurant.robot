*** Settings ***
Library    RequestsLibrary
Library    Collections

*** Variables ***
${BASE_URL}    http://localhost:5001

*** Test Cases ***
Add Restaurant
    Create Session    foodie    ${BASE_URL}

    ${body}=    Create Dictionary    name=Robot Hotel
    ${headers}=    Create Dictionary    Content-Type=application/json

    ${response}=    POST On Session    foodie    /api/v1/restaurants
    ...    json=${body}
    ...    headers=${headers}

    Log    ${response.text}
    Should Be Equal As Integers    ${response.status_code}    201