black .
isort .

pytest --alluredir=allure-results
allure serve allure-results
