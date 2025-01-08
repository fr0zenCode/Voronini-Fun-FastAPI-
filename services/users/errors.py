

class IncorrectCredentialsError(Exception):
    def __init__(self, message: str = "Неверный логин или пароль."):
        self.message = message
        super().__init__(message)


class UserNotAuthorizedError(Exception):
    def __init__(self, message: str = "Для совершения этого действия необходимо авторизоваться на сайте."):
        self.message = message
        super().__init__(message)
