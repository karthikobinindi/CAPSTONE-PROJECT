*** Settings ***
Library    RequestsLibrary
Library    Collections
Library    BuiltIn
Resource   variables.robot

*** Keywords ***
Create API Session
    Create Session    foodie    ${BASE_URL}

Generate Random Name
    ${rand}=    Evaluate    __import__('random').randint(1000,9999)
    RETURN    ${rand}