*** Settings ***
Library    RequestsLibrary
Library    Collections

*** Variables ***
${BASE_URL}    http://127.0.0.1:5000/api/v1/admin

*** Test Cases ***

Approve Restaurant
    Create Session    admin    ${BASE_URL}
    ${response}=    PUT On Session    admin    /restaurants/1/approve
    Should Be True    ${response.status_code} == 200 or ${response.status_code} == 404

Disable Restaurant
    Create Session    admin    ${BASE_URL}
    ${response}=    PUT On Session    admin    /restaurants/1/disable
    Should Be True    ${response.status_code} == 200 or ${response.status_code} == 404

View Feedback
    Create Session    admin    ${BASE_URL}
    ${response}=    GET On Session    admin    /feedback
    Should Be Equal As Integers    ${response.status_code}    200
    ${data}=    Set Variable    ${response.json()}
    Should Not Be Empty    ${data}

View Orders
    Create Session    admin    ${BASE_URL}
    ${response}=    GET On Session    admin    /orders
    Should Be Equal As Integers    ${response.status_code}    200
    ${data}=    Set Variable    ${response.json()}
    Should Not Be Empty    ${data}