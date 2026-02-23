*** Settings ***
Library     RequestsLibrary
Library     Collections
Library     DateTime
Resource    ../resources/common_keywords.robot

Suite Setup       Run Keywords    Backup Original Data    AND    Clear Data For Tests    AND    Create Foodie Session    AND    Setup Order Suite
Suite Teardown    Run Keywords    Delete Foodie Session    AND    Restore Original Data

*** Test Cases ***

REQ-17 View Orders By Restaurant
    [Documentation]    GET /api/v1/restaurants/{restaurant_id}/orders — View orders by restaurant.
    [Tags]    order    GET
    ${response}=    Get Restaurant Orders    ${SUITE_REST_ID}
    Response Status Should Be    ${response}    200
    ${orders}=    Evaluate    $response.json()
    Should Be True    isinstance($orders, list)
    ${ids}=    Evaluate    [o['order_id'] for o in $orders]
    Should Contain    ${ids}    ${SUITE_ORDER_ID}

REQ-18 View Orders By User
    [Documentation]    GET /api/v1/users/{user_id}/orders — View orders by user.
    [Tags]    order    GET
    ${response}=    Get User Orders    ${SUITE_USER_ID}
    Response Status Should Be    ${response}    200
    ${orders}=    Evaluate    $response.json()
    Should Be True    isinstance($orders, list)
    ${ids}=    Evaluate    [o['order_id'] for o in $orders]
    Should Contain    ${ids}    ${SUITE_ORDER_ID}


*** Keywords ***

Setup Order Suite
    ${rname}=    Unique Name    RF_OrderSuite
    ${reg}=    Register Restaurant    ${rname}    Indian    Chennai    5000000001
    ${rid}=    Extract Field From Response    ${reg}    restaurant_id
    Admin Approve Restaurant    ${rid}
    &{dp}=    Create Dictionary    name=Order Dish    type=Veg    price=${120}
    ${dr}=    Add Dish    ${rid}    ${dp}
    ${did}=    Extract Field From Response    ${dr}    dish_id
    ${uemail}=    Unique Name    rforder
    ${ur}=    Register User    Order User    ${uemail}@example.com    Order@123
    ${uid}=    Extract Field From Response    ${ur}    user_id
    @{dishes}=    Create List    ${did}
    ${or}=    Place Order    ${uid}    ${rid}    ${dishes}
    ${oid}=    Extract Field From Response    ${or}    order_id
    Set Suite Variable    ${SUITE_REST_ID}    ${rid}
    Set Suite Variable    ${SUITE_USER_ID}    ${uid}
    Set Suite Variable    ${SUITE_ORDER_ID}    ${oid}
