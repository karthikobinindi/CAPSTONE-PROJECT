*** Settings ***
Resource    ../resources/keywords.robot
Resource    ../resources/variables.robot

*** Test Cases ***
Register User
    Create API Session
    ${rand}=    Generate Random Name
    ${email}=    Set Variable    user_${rand}@test.com

    ${payload}=    Create Dictionary
    ...    name=RobotUser
    ...    email=${email}
    ...    password=1234

    ${response}=    POST On Session    foodie    /api/v1/users/register    json=${payload}
    Status Should Be    201    ${response}