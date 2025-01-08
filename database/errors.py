

class DatabaseLoseConnection(Exception):
    def __init__(self, message: str = "Нет соединения с базой данных."):
        self.message = message
        super().__init__(self.message)


class DatabaseTablesErrors(Exception):
    def __init__(self, message: str = "Внутренние проблемы базы данных. Таблицы."):
        self.message = message
        super().__init__(self.message)


class UserWithTheSameUsernameIsAlreadyExistsError(Exception):
    def __init__(self, message: str = "Пользователь с таким ником уже существует. Придумайте другой."):
        self.message = message
        super().__init__(self.message)


class UserWithTheSameEmailIsAlreadyExistsError(Exception):
    def __init__(self, message: str = "Пользователь с этим адресом электронной почты уже существует."):
        self.message = message
        super().__init__(self.message)


class DatabaseColumnsErrors(Exception):
    def __init__(self, message: str = "Нарушение целостности базы данных. Возможно, вставляются некорректные данные."):
        self.message = message
        super().__init__(self.message)
