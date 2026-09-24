from fastapi import status


class AppException(Exception):
    def __init__(
        self,
        status_code: int,
        message: str
    ):
        self.status_code = status_code
        self.message = message

        super().__init__(message)


class BadRequestException(AppException):
    def __init__(self, message: str = "Requisição inválida."):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=message
        )


class NotFoundException(AppException):
    def __init__(self, message: str = "Recurso não encontrado."):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=message
        )