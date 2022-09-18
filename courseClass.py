from windowClass import *
from sectionOptionClass import SectionOption
from selenium.common.exceptions import NoSuchElementException


class Course:
    NUM = 0
    def __init__(self, term:str|int, term_year, course_id:str, driver):
        Course.NUM += 1 #used for the bd 1 bc1 thing
        """
        
        """
        num = Course.NUM
        self.term = term
        self.term_year = term_year
        self.course_id = course_id
        self.open = True

        #xpaths
        self.reset_xpaths()

        
        #objects
        self.driver = driver
        self.select = self.get_select()
        self.course_options = {} #{SelectOption}

        #lists
        #lectures
        #select_options
        #crns
        self.sections = []
        self.options = []
        self.crn = []

        #dictionaries
        #lec -> crn
        #lec -> option obj
        #crn -> lec
        #crn -> option obj
        #crn -> seats_xpath
        self.lec_to_crn = {}
        self.lec_to_obj = {}
        self.crn_to_lec = {}
        self.crn_to_obj = {}
        self.crn_to_seats_xpath = {}

        #initiate course
        self.get_select_options()

        #extra dict| needs to be initiated after crns
        

        #seats
        #lec -> seats
        #crn -> seats
        self.lec_seats = {}
        self.crn_seats = {}
        
        for section in self.sections:
            self.set_section_seats(section)
        
    def __str__(self) -> str:
        return f"{self.course_id} has {self.lec_to_crn}"
    def __repr__(self) -> str:
        return self.__str__()
    

    def reset_xpaths(self):
        num = Course.NUM
        self.course_xpath = f'courseDiv bc{num} bd{num}'
        self.course_block_xpath = f'course_header bc{num} bh{num} bclock'
        self.select_xpath = f"//div[@class='{self.course_xpath}']//child::select"
        self.deselect_xpath = f"//div[@class='{self.course_xpath}']//div[2]//a[@title='Remove this course from the Search']"

    #initiate course
    def get_select(self) -> Select:
        attempts = 1
        while attempts < 10:
            try:
                select = Select(self.driver.find_element(By.XPATH,self.select_xpath))
                break
            except NoSuchElementException:
                Course.NUM = attempts
                self.reset_xpaths()
                attempts +=1
        return select


    def get_select_options(self) -> list:
        """
        Gets the dropdown box text and values. Returns a list of SelectOption
        """
        
        for option in self.select.options:
            option_obj = SectionOption(option.text, option.get_attribute("value"))


            if 'Lec' in option_obj.text:
                lec = option_obj.text
                crn = option_obj.crn
                obj = option_obj

                self.sections.append(lec)
                self.options.append(obj)
                self.crn.append(crn)

                #dictionaries
                self.lec_to_crn[lec] = crn
                self.lec_to_obj[lec] = obj
                self.crn_to_lec[crn] = lec
                self.crn_to_obj[crn] = obj
                self.crn_to_seats_xpath[crn] = self.seats_xpath(crn)


    #methods
    def lec_string(self, section:str|int) -> str:
        if type(section) == int: section = str(section)
        if 'Lec' in section: return section
        
        zeros = "0"*(3-len(section))
        s = f'Lec {zeros}{section}'

        if s in self.sections:
            return s
        elif s + ' (Full)' in self.sections:
            return s + ' (Full)'
        else:
            raise ValueError(f"The section string {s} still doesn't line up with any Select Options")
    #gets the lecture string


    def select_section(self,section):
        section = str(section)
        lecture = self.lec_string(section)
        
        self.select.select_by_visible_text(lecture)

    
    #get_seats
    def seats_xpath(self, crn:str):
        for_text = f'rad_--{self.term_year}{self.term}_{crn}--'
        return f"//label[@for = '{for_text}']//following-sibling::span[contains(@title, 'seats')]"
    
    def see_seats(self,seats_xpath):
        attempts = 0
        while attempts < 2:
            try:
                element = self.driver.find_element(By.XPATH, seats_xpath)
                title = element.get_attribute('title')
                break
            except exceptions.StaleElementReferenceException:
                attempts += 1
        
        
        num = [int(word) for word in title.split() if word.isdigit()]
        if len(num) == 0: #No available seats
            return 0
        else:
            assert len(num) < 2
            return num[0] 
        #returns the number of seats

    def set_section_seats(self,section):
        section = self.lec_string(section)  
        crn = self.lec_to_crn[section]

        #make sure you select the section so that you can find it's xpath
        self.select_section(section)

        #get seats for course
        seats_xpath = self.crn_to_seats_xpath[crn]
        
        #get the number of seats
        seats = self.see_seats(seats_xpath)

        #set seats
        self.lec_seats[section] = seats
        self.crn_seats[crn] = seats



    
