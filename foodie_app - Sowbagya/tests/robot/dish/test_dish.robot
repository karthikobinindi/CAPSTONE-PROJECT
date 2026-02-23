*** Settings ***
Library     RequestsLibrary
Library     Collections
Library     DateTime
Resource    ../resources/common_keywords.robot

Suite Setup       Run Keywords    Backup Original Data    AND    Clear Data For Tests    AND    Create Foodie Session    AND    Setup Dish Suite
Suite Teardown    Run Keywords    Delete Foodie Session    AND    Restore Original Data

*** Test Cases ***

REQ-5 Add Dish
    [Documentation]    POST /api/v1/restaurants/{restaurant_id}/dishes — Add a dish.
    [Tags]    dish    POST
    &{payload}=    Create Dictionary
    ...    name=Butter Chicken    type=Non-Veg
    ...    price=${320}    available_time=11:00-23:00    image=butter.jpg
    ${response}=    Add Dish    ${SUITE_RESTAURANT_ID}    ${payload}
    Response Status Should Be    ${response}    201
    Response Should Contain Key    ${response}    dish_id
    ${name}=    Extract Field From Response    ${response}    name
    Should Be Equal    ${name}    Butter Chicken

REQ-6 Update Dish
    [Documentation]    PUT /api/v1/dishes/{dish_id} — Update dish details.
    [Tags]    dish    PUT
    &{add}=    Create Dictionary    name=Old Dish    type=Veg    price=${100}
    ${add_resp}=    Add Dish    ${SUITE_RESTAURANT_ID}    ${add}
    ${did}=    Extract Field From Response    ${add_resp}    dish_id
    &{upd}=    Create Dictionary    name=New Dish    price=${150}
    ${response}=    Update Dish    ${did}    ${upd}
    Response Status Should Be    ${response}    200
    ${name}=    Extract Field From Response    ${response}    name
    Should Be Equal    ${name}    New Dish

REQ-7 Enable Disable Dish
    [Documentation]    PUT /api/v1/dishes/{dish_id}/status — Enable or disable a dish.
    [Tags]    dish    PUT
    &{add}=    Create Dictionary    name=Toggle Dish    type=Veg    price=${80}
    ${add_resp}=    Add Dish    ${SUITE_RESTAURANT_ID}    ${add}
    ${did}=    Extract Field From Response    ${add_resp}    dish_id
    ${response}=    Set Dish Status    ${did}    ${False}
    Response Status Should Be    ${response}    200
    Response Should Contain Key    ${response}    message

REQ-8 Delete Dish
    [Documentation]    DELETE /api/v1/dishes/{dish_id} — Delete a dish.
    [Tags]    dish    DELETE
    &{add}=    Create Dictionary    name=Delete Me    type=Veg    price=${60}
    ${add_resp}=    Add Dish    ${SUITE_RESTAURANT_ID}    ${add}
    ${did}=    Extract Field From Response    ${add_resp}    dish_id
    ${response}=    Delete Dish    ${did}
    Response Status Should Be    ${response}    200
    ${msg}=    Extract Field From Response    ${response}    message
    Should Be Equal    ${msg}    Dish deleted


*** Keywords ***

Setup Dish Suite
    ${name}=    Unique Name    RF_DishSuite
    ${reg}=    Register Restaurant    ${name}    Indian    Chennai    8000000001
    ${rid}=    Extract Field From Response    ${reg}    restaurant_id
    Admin Approve Restaurant    ${rid}
    Set Suite Variable    ${SUITE_RESTAURANT_ID}    ${rid}
