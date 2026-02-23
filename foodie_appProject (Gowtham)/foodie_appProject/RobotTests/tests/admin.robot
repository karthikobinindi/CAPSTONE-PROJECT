*** Settings ***
Resource    ../resources/keywords.robot
Resource    ../resources/variables.robot

*** Test Cases ***
View Admin Feedback
    Create API Session
    ${response}=    GET On Session    foodie    /api/v1/admin/feedback
    Status Should Be    200    ${response}