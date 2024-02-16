from rest_framework.exceptions import APIException


class InvalidAccounts(APIException):

    status_code = 400
    default_detail = "Invalid accounts"
    default_code = 'invalid_accounts'

# :D
class YouAreBadBakhtError(APIException):

    status_code = 400
    default_detail = "Not enough money"
    default_code = 'not_enough_money'