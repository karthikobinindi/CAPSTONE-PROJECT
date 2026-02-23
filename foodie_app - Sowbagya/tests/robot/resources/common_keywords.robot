*** Settings ***
Library     RequestsLibrary
Library     Collections
Library     OperatingSystem
Library     DateTime
Library     String


*** Variables ***
${BASE_URL}         http://localhost:5000
${SESSION_ALIAS}    foodie
&{COMMON_HEADERS}   Content-Type=application/json


*** Keywords ***

# ─── Setup / Teardown ────────────────────────────────────────────────────────

Create Foodie Session
    Create Session    ${SESSION_ALIAS}    ${BASE_URL}    headers=&{COMMON_HEADERS}

Delete Foodie Session
    Delete All Sessions

Get Data Dir
    ${root}=    Normalize Path    ${CURDIR}${/}..${/}..${/}..
    RETURN    ${root}${/}data

Backup Original Data
    [Documentation]    Save original JSON file contents before tests run.
    ${data_dir}=    Get Data Dir
    ${r}=    Get File    ${data_dir}${/}restaurants.json
    ${d}=    Get File    ${data_dir}${/}dishes.json
    ${u}=    Get File    ${data_dir}${/}users.json
    ${o}=    Get File    ${data_dir}${/}orders.json
    ${rt}=   Get File    ${data_dir}${/}ratings.json
    Set Suite Variable    ${BACKUP_RESTAURANTS}    ${r}
    Set Suite Variable    ${BACKUP_DISHES}         ${d}
    Set Suite Variable    ${BACKUP_USERS}          ${u}
    Set Suite Variable    ${BACKUP_ORDERS}         ${o}
    Set Suite Variable    ${BACKUP_RATINGS}        ${rt}


Restore Original Data
    [Documentation]    Restore original JSON files after saving test data.
    ${data_dir}=    Get Data Dir
    Create File    ${data_dir}${/}restaurants.json    ${BACKUP_RESTAURANTS}
    Create File    ${data_dir}${/}dishes.json         ${BACKUP_DISHES}
    Create File    ${data_dir}${/}users.json          ${BACKUP_USERS}
    Create File    ${data_dir}${/}orders.json         ${BACKUP_ORDERS}
    Create File    ${data_dir}${/}ratings.json        ${BACKUP_RATINGS}

Clear Data For Tests
    [Documentation]    Temporarily clear JSON files so tests run on clean data.
    ${data_dir}=    Get Data Dir
    Create File    ${data_dir}${/}restaurants.json    {"restaurants": []}
    Create File    ${data_dir}${/}dishes.json         {"dishes": []}
    Create File    ${data_dir}${/}users.json          {"users": []}
    Create File    ${data_dir}${/}orders.json         {"orders": []}
    Create File    ${data_dir}${/}ratings.json        {"ratings": []}

Unique Name
    [Arguments]    ${prefix}
    ${ts}=    Get Current Date    result_format=%H%M%S%f
    RETURN    ${prefix}_${ts}


# ─── Restaurant Keywords ──────────────────────────────────────────────────────

Register Restaurant
    [Arguments]    ${name}    ${category}    ${location}    ${contact}
    &{payload}=    Create Dictionary
    ...    name=${name}    category=${category}
    ...    location=${location}    contact=${contact}
    ${response}=    POST On Session    ${SESSION_ALIAS}    /api/v1/restaurants
    ...    json=${payload}    expected_status=any
    RETURN    ${response}

Get Restaurant
    [Arguments]    ${restaurant_id}
    ${response}=    GET On Session    ${SESSION_ALIAS}
    ...    /api/v1/restaurants/${restaurant_id}    expected_status=any
    RETURN    ${response}

Update Restaurant
    [Arguments]    ${restaurant_id}    ${payload}
    ${response}=    PUT On Session    ${SESSION_ALIAS}
    ...    /api/v1/restaurants/${restaurant_id}
    ...    json=${payload}    expected_status=any
    RETURN    ${response}

Disable Restaurant
    [Arguments]    ${restaurant_id}
    ${response}=    PUT On Session    ${SESSION_ALIAS}
    ...    /api/v1/restaurants/${restaurant_id}/disable    expected_status=any
    RETURN    ${response}

Search Restaurants
    [Arguments]    ${params}
    ${response}=    GET On Session    ${SESSION_ALIAS}
    ...    /api/v1/restaurants/search    params=${params}    expected_status=any
    RETURN    ${response}


# ─── Dish Keywords ────────────────────────────────────────────────────────────

Add Dish
    [Arguments]    ${restaurant_id}    ${payload}
    ${response}=    POST On Session    ${SESSION_ALIAS}
    ...    /api/v1/restaurants/${restaurant_id}/dishes
    ...    json=${payload}    expected_status=any
    RETURN    ${response}

Update Dish
    [Arguments]    ${dish_id}    ${payload}
    ${response}=    PUT On Session    ${SESSION_ALIAS}
    ...    /api/v1/dishes/${dish_id}
    ...    json=${payload}    expected_status=any
    RETURN    ${response}

Set Dish Status
    [Arguments]    ${dish_id}    ${enabled}
    &{payload}=    Create Dictionary    enabled=${enabled}
    ${response}=    PUT On Session    ${SESSION_ALIAS}
    ...    /api/v1/dishes/${dish_id}/status
    ...    json=${payload}    expected_status=any
    RETURN    ${response}

Delete Dish
    [Arguments]    ${dish_id}
    ${response}=    DELETE On Session    ${SESSION_ALIAS}
    ...    /api/v1/dishes/${dish_id}    expected_status=any
    RETURN    ${response}


# ─── Admin Keywords ───────────────────────────────────────────────────────────

Admin Approve Restaurant
    [Arguments]    ${restaurant_id}
    ${response}=    PUT On Session    ${SESSION_ALIAS}
    ...    /api/v1/admin/restaurants/${restaurant_id}/approve    expected_status=any
    RETURN    ${response}

Admin Disable Restaurant
    [Arguments]    ${restaurant_id}
    ${response}=    PUT On Session    ${SESSION_ALIAS}
    ...    /api/v1/admin/restaurants/${restaurant_id}/disable    expected_status=any
    RETURN    ${response}

Admin Get All Feedback
    ${response}=    GET On Session    ${SESSION_ALIAS}
    ...    /api/v1/admin/feedback    expected_status=any
    RETURN    ${response}

Admin Get All Orders
    ${response}=    GET On Session    ${SESSION_ALIAS}
    ...    /api/v1/admin/orders    expected_status=any
    RETURN    ${response}


# ─── User Keywords ────────────────────────────────────────────────────────────

Register User
    [Arguments]    ${name}    ${email}    ${password}
    &{payload}=    Create Dictionary
    ...    name=${name}    email=${email}    password=${password}
    ${response}=    POST On Session    ${SESSION_ALIAS}    /api/v1/users/register
    ...    json=${payload}    expected_status=any
    RETURN    ${response}

Get User Orders
    [Arguments]    ${user_id}
    ${response}=    GET On Session    ${SESSION_ALIAS}
    ...    /api/v1/users/${user_id}/orders    expected_status=any
    RETURN    ${response}


# ─── Order Keywords ───────────────────────────────────────────────────────────

Place Order
    [Arguments]    ${user_id}    ${restaurant_id}    ${dishes}
    &{payload}=    Create Dictionary
    ...    user_id=${user_id}    restaurant_id=${restaurant_id}    dishes=${dishes}
    ${response}=    POST On Session    ${SESSION_ALIAS}    /api/v1/orders
    ...    json=${payload}    expected_status=any
    RETURN    ${response}

Get Restaurant Orders
    [Arguments]    ${restaurant_id}
    ${response}=    GET On Session    ${SESSION_ALIAS}
    ...    /api/v1/restaurants/${restaurant_id}/orders    expected_status=any
    RETURN    ${response}


# ─── Rating Keywords ──────────────────────────────────────────────────────────

Give Rating
    [Arguments]    ${order_id}    ${rating}    ${comment}
    &{payload}=    Create Dictionary
    ...    order_id=${order_id}    rating=${rating}    comment=${comment}
    ${response}=    POST On Session    ${SESSION_ALIAS}    /api/v1/ratings
    ...    json=${payload}    expected_status=any
    RETURN    ${response}


# ─── Assertion & Extraction Helpers ──────────────────────────────────────────

Response Status Should Be
    [Arguments]    ${response}    ${expected_status}
    Should Be Equal As Integers    ${response.status_code}    ${expected_status}

Get Response Body
    [Arguments]    ${response}
    ${body}=    Evaluate    $response.json()
    RETURN    ${body}

Response Should Contain Key
    [Arguments]    ${response}    ${key}
    ${body}=    Get Response Body    ${response}
    Dictionary Should Contain Key    ${body}    ${key}

Extract Field From Response
    [Arguments]    ${response}    ${field}
    ${body}=    Get Response Body    ${response}
    Dictionary Should Contain Key    ${body}    ${field}
    ${value}=    Get From Dictionary    ${body}    ${field}
    RETURN    ${value}

Response List Should Not Be Empty
    [Arguments]    ${response}
    ${body}=    Evaluate    $response.json()
    Should Not Be Empty    ${body}
