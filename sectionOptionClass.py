from selectOption import SelectOption

class SectionOption(SelectOption):
    def __init__(self, text, value) -> None:
        super().__init__(text, value) # initializes text and value
        
        self.crn = self.value[12:16] if 'ss' not in self.value else None

    def __str__(self):
        return f'{self.text} -> CRN = {self.crn}'
    
    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, __o: object) -> bool:
        return self.crn == __o.crn
            