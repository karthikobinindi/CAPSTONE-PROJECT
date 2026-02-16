*** Settings ***
Library    RequestsLibrary
Library    BuiltIn

*** Variables ***
${BASE_URL}    http://127.0.0.1:5000

*** Test Cases ***
Register User JSON
    ${rand}=    Evaluate    __import__('random').randint(1000,9999)
    Create Session    foodie    ${BASE_URL}
    ${data}=    Create Dictionary    name=RobotUser${rand}    email=robot${rand}@gmail.com    password=12345
    ${res}=    POST On Session    foodie    /api/v1/users/register    json=${data}
    Status Should Be    201    ${res}
