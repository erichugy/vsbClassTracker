class SelectOption():
    def __init__(self, text,value) -> None:
        self.text = text
        self.value = value
    def __str__(self) -> str:
        return f'{self.text} - {self.value}'

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, __o: object) -> bool:
        return self.text == __o.text