import datetime as dt
import time
from courseClass import *

def is_seq_not_str(seq):
    return type(seq) in (list,tuple, dict)

class VSB:
    
    def __init__(self) -> None:
        self.driver = VSB.open_vsb()
        
        self.term = None
        self.term_year = dt.date.today().year

        self.course_id_to_num = {} # 1-indexed
        self.course_id_to_objs = {}


    @staticmethod
    def open_vsb() -> Window:
        #open page
        driver = Window("https://vsb.mcgill.ca/vsb/welcome.jsp")

        #First continue of vsb
        driver.click_button_xpath('/html/body/div[2]/div/input')

        print('Set Up Complete')
        return driver
    #opens the driver window
    

    def select_term(self, term:int|str = None) -> None:
        """ 
        term: str (i've allowed the numeric months as well cuz i'm lazy)
            Defines the term that you are interested in finding classes for.
            Possible Inputs: ('s', "summer", "f", 'fall', 'w', 'winter',5,9,1)
            If None, then the next one will be used
        """
        today = dt.date.today()

        if type(term) == str:
            term = term.lower()
        
        possible_terms = ('s', "summer", 5, "f", 'fall', 9, 'w', 'winter',1)
        #validate term or set term
        if term == None:
            if today.month <= 2 or today.month > 10:
                term = 'w'
            elif today.month <= 5:
                term = 's'
            else:
                term = 'f'
        elif term not in possible_terms:
            raise ValueError(f'Term: {term} is not a valid input. Choose from {possible_terms}.')

        
        #determine year: only add 1 to year if looking at winter
        
        add_year = 1 if (term in ('w', 'winter',1) and today.month > 2) else 0
        self.term_year = today.year + add_year

        term_conversions  = {
            's': '05', 
            "summer": '05',
            5: '05',
            "f":'09', 
            'fall':'09', 
            9:'09',
            'w':'01',
            'winter':'01',
            1:'01'
        }

        term = term_conversions[term]

        id_name = f'term_{self.term_year}{term}'

        self.driver.click_button_id(id_name)
        self.term = term


    def open(self,course_id):
        if course_id in self.course_id_to_objs: #decided to re initiate each course because of the number resetting bug
            del self.course_id_to_objs[course_id]

        self.driver.fill_out_id('code_number', course_id)
        time.sleep(1) #need to wait for it to load
        course = Course(self.term, self.term_year, course_id, self.driver)
                
        self.course_id_to_objs[course_id] = course

    def close(self, course_id):
        """
        Clicks the deselect button
        """
        course = self.course_id_to_objs[course_id]

        assert course.open == True
        course.open = False

        deselect_xpath = course.deselect_xpath
        self.driver.click_button_xpath(deselect_xpath)
        time.sleep(1)


    def validate_course_id(self,course_id: str) -> str:
        try:
            c = course_id.upper()
        except TypeError as e:
            print(f'{e} thrown due to {c}')
        assert c in self.course_id_to_objs , f'Course ID {c} is not a course you are taking.'
        return c

        
    def get_all_lecture_seats(self, course_ids:str|list, semester:str|int=None):
        """
        gets the information on multiple or one course. Making sure to deselect each course as you get the information
        """
        
        self.select_term(semester)
        
        if is_seq_not_str(course_ids):
            for i in course_ids:
                self.open(i)
                self.close(i)
        elif type(course_ids) == str:#if one course is entered
            self.open(course_ids)
            self.close(course_ids)
        else:
            raise TypeError(f"Course_ids {course_ids} input is the wrong type")
    
    def print_seats(self,course_ids,semester=None):
        self.get_all_lecture_seats(course_ids,semester)

        if is_seq_not_str(course_ids):
            for i in course_ids:
                print(f"{i} -> {self.course_id_to_objs[i].lec_seats}")
        else:
            print(f"{i} -> {self.course_id_to_objs[i].lec_seats}")



def main(course_ids,semester=None):
    vsb = VSB()
    vsb.print_seats(course_ids,semester)
        

if __name__ == '__main__':
    main(['FINE 342', 'MATH 240','MGCR 271','COMP 250','comp 206'],1)
