*** Settings ***
Library     RequestsLibrary
Library     Collections
Library     DateTime
Resource    ../resources/common_keywords.robot

Suite Setup       Run Keywords    Backup Original Data    AND    Clear Data For Tests    AND    Create Foodie Session    AND    Setup User Suite
Suite Teardown    Run Keywords    Delete Foodie Session    AND    Restore Original Data


*** Test Cases ***

REQ-13 User Registration
    [Documentation]    POST /api/v1/users/register — Register a new user.
    [Tags]    user    POST
    ${email}=    Unique Name    rfuser
    ${response}=    Register User    Arjun Kumar    ${email}@example.com    Arjun@123
    Response Status Should Be    ${response}    201
    Response Should Contain Key    ${response}    user_id
    ${body}=    Get Response Body    ${response}
    Dictionary Should Not Contain Key    ${body}    password

REQ-14 Search Restaurants
    [Documentation]    GET /api/v1/restaurants/search — Search restaurants.
    [Tags]    user    GET
    &{params}=    Create Dictionary    name=${SUITE_REST_NAME}
    ${response}=    Search Restaurants    ${params}
    Response Status Should Be    ${response}    200
    ${body}=    Evaluate    $response.json()
    Should Not Be Empty    ${body}

REQ-15 Place Order
    [Documentation]    POST /api/v1/orders — Place an order.
    [Tags]    user    POST
    @{dishes}=    Create List    ${SUITE_DISH_ID}
    ${response}=    Place Order    ${SUITE_USER_ID}    ${SUITE_REST_ID}    ${dishes}
    Response Status Should Be    ${response}    201
    Response Should Contain Key    ${response}    order_id
    ${status}=    Extract Field From Response    ${response}    status
    Should Be Equal    ${status}    placed

REQ-16 Give Rating
    [Documentation]    POST /api/v1/ratings — Give a rating for a placed order.
    [Tags]    user    POST
    @{dishes}=    Create List    ${SUITE_DISH_ID}
    ${order}=    Place Order    ${SUITE_USER_ID}    ${SUITE_REST_ID}    ${dishes}
    ${oid}=    Extract Field From Response    ${order}    order_id
    ${response}=    Give Rating    ${oid}    ${5}    Excellent food and fast delivery!
    Response Status Should Be    ${response}    201
    Response Should Contain Key    ${response}    rating_id
    ${rating}=    Extract Field From Response    ${response}    rating
    Should Be Equal As Integers    ${rating}    5


*** Keywords ***

Setup User Suite
    ${rname}=    Unique Name    RF_UserSuite
    ${reg}=    Register Restaurant    ${rname}    Indian    Chennai    6000000001
    ${rid}=    Extract Field From Response    ${reg}    restaurant_id
    Admin Approve Restaurant    ${rid}
    &{dp}=    Create Dictionary    name=Suite Dish    type=Veg    price=${150}
    ${dr}=    Add Dish    ${rid}    ${dp}
    ${did}=    Extract Field From Response    ${dr}    dish_id
    ${uemail}=    Unique Name    rfsuite
    ${ur}=    Register User    Suite User    ${uemail}@example.com    Suite@123
    ${uid}=    Extract Field From Response    ${ur}    user_id
    Set Suite Variable    ${SUITE_REST_ID}    ${rid}
    Set Suite Variable    ${SUITE_REST_NAME}    ${rname}
    Set Suite Variable    ${SUITE_DISH_ID}    ${did}
    Set Suite Variable    ${SUITE_USER_ID}    ${uid}
