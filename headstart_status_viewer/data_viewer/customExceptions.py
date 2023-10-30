class DataNotFoundError(Exception):
    
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class DataFormatError(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)