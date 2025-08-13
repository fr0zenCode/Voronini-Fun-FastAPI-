from typing import Final


#core
ENCODING_TYPE: Final[str] = "UTF-8"
SESSION_KEY_IN_COOKIES: Final[str] = "session"
USERNAME_VALIDATION_REGEXP: Final[str] = "^[a-zA-Z]{3,10}$"


#invalid input data from user
INCORRECT_EMAIL_OR_PASSWORD_ALIAS: Final[str] = "Неверный email или пароль."
INVALID_USERNAME: Final[str] = ("Некорректно задан username. Используйте только латинские буквы. "
                                "Минимальная длина - 3 символа. Максимальная - 10.")
INVALID_EMAIL: Final[str] = "Некорректно задан email."
EMAIL_ALREADY_TAKEN_ALIAS: Final[str] = "Пользователь с таким email уже существует."
USERNAME_ALREADY_TAKEN_ALIAS: Final[str] = "Этот username уже занят, попробуйте выбрать другой."
TOO_LONG_TEXT_ALIAS: Final[str] = "Превышен допустимый лимит символов, попробуйте сократить сообщение."


#http exceptions texts
UNAUTHORIZED_ALIAS: Final[str] = "Для выполнения этого действия необходимо авторизоваться."
POST_ID_NON_EXIST_ALIAS: Final[str] = "Пост с указанным ID не существует. Возможно он был удален или скрыт автором."
YOU_CANT_DO_IT_ALIAS: Final[str] = "У вас недостаточно прав для совершения этого действия."
STOP_POSTING_SPAM_ALIAS: Final[str] = "Новые посты можно создавать не чаще, чем раз в 5 минут."
