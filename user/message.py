
def Message(user, token):

    return f"""
    Hello {user},

    To Verify your DoomCart Account,
    click the link below:


    https://doomcart.herokuapp.com/verify/{token}/

    If you haven't inisitate this request please contact us 

    http://127.0.0.1:8000/

    Sincerely,

    The DoomCart Team"""
