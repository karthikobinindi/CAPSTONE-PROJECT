*** Settings ***
Library     RequestsLibrary
Library     Collections
Library     DateTime
Resource    ../resources/common_keywords.robot

Suite Setup       Run Keywords    Backup Original Data    AND    Clear Data For Tests    AND    Create Foodie Session
Suite Teardown    Run Keywords    Delete Foodie Session    AND    Restore Original Data

*** Test Cases ***

REQ-1 Register Restaurant
    [Documentation]    POST /api/v1/restaurants — Register a new restaurant.
    [Tags]    restaurant    POST
    &{payload}=    Create Dictionary
    ...    name=Spice Garden    category=Indian
    ...    location=Chennai    contact=9876543210
    ${response}=    POST On Session    foodie    /api/v1/restaurants
    ...    json=${payload}    expected_status=any
    Response Status Should Be    ${response}    201
    Response Should Contain Key    ${response}    restaurant_id
    ${status}=    Extract Field From Response    ${response}    status
    Should Be Equal    ${status}    pending

REQ-2 Update Restaurant
    [Documentation]    PUT /api/v1/restaurants/{restaurant_id} — Update restaurant details.
    [Tags]    restaurant    PUT
    ${name}=    Unique Name    RF_Update
    ${reg}=    Register Restaurant    ${name}    Fast Food    Mumbai    9000000001
    ${rid}=    Extract Field From Response    ${reg}    restaurant_id
    &{upd}=    Create Dictionary    name=Updated Name    contact=9000000099
    ${response}=    Update Restaurant    ${rid}    ${upd}
    Response Status Should Be    ${response}    200
    ${updated}=    Extract Field From Response    ${response}    name
    Should Be Equal    ${updated}    Updated Name

REQ-3 Disable Restaurant
    [Documentation]    PUT /api/v1/restaurants/{restaurant_id}/disable — Disable a restaurant.
    [Tags]    restaurant    PUT
    ${name}=    Unique Name    RF_Disable
    ${reg}=    Register Restaurant    ${name}    Cafe    Delhi    9000000002
    ${rid}=    Extract Field From Response    ${reg}    restaurant_id
    ${response}=    Disable Restaurant    ${rid}
    Response Status Should Be    ${response}    200
    ${msg}=    Extract Field From Response    ${response}    message
    Should Be Equal    ${msg}    Restaurant disabled

REQ-4 View Restaurant Profile
    [Documentation]    GET /api/v1/restaurants/{restaurant_id} — View restaurant profile.
    [Tags]    restaurant    GET
    ${name}=    Unique Name    RF_View
    ${reg}=    Register Restaurant    ${name}    Pizza    Bangalore    9000000003
    ${rid}=    Extract Field From Response    ${reg}    restaurant_id
    ${response}=    Get Restaurant    ${rid}
    Response Status Should Be    ${response}    200
    ${returned_id}=    Extract Field From Response    ${response}    restaurant_id
    Should Be Equal    ${returned_id}    ${rid}
