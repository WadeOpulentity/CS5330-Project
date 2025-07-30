from flask import flash
#This is just helpful for us to know its working
def flash_success(message):
    """runs the success message for Flask"""
    flash(message, 'success')

def flash_error(message):
    """runs the error message for Flask"""
    flash(message, 'error')

def flash_info(message):
    """runs the info message for Flask"""
    flash(message, 'info')
