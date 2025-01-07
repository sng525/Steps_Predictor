# https://docs.python.org/3/library/exceptions.html

import sys 
from src.logger import logging

# custom ex exception handling: https://docs.python.org/3/tutorial/errors.html

# Define a function to get detailed error messages
def error_message_detail(error, error_detail: sys):

    # Extract the traceback object from the current exception
    #exception traceback: info on where exception occurred
    _, _, exc_tb = error_detail.exc_info()
    
    # Get the filename where the exception occurred
    file_name = exc_tb.tb_frame.f_code.co_filename 
    
    # Format the error message with the filename, line number, and error message
    error_message = (
        "Error occurred in python script name [{0}] line number [{1}] error message [{2}]"
        .format(file_name, exc_tb.tb_lineno, str(error))
    )

    return error_message
    

# Custom exception class inheriting from the base Exception class
class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys):
            
            detailed_error_message = error_message_detail(error_message, error_detail)
            
            # Initialize the base Exception class with the error message
            super().__init__(detailed_error_message) 
            
            # Generate a detailed error message using the provided function
            self.error_message=detailed_error_message

    def __str__(self):
         # Return the detailed error message when the exception is printed
         return self.error_message
    
    
if __name__=="__main__":
         
    try:
           a=1/0
    except Exception as e:
        logging.info("Divide by Zero Error")
        raise CustomException(e, sys)
