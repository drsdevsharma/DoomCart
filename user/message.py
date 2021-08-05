
def Message(user, token):

    return f"""
    Hello {user},

    To Verify your DoomCart Account,
    click the link below:


    http://127.0.0.1:8000/verify/{token}/

    If you haven't inisitate this request please contact us 

    http://127.0.0.1:8000/

    Sincerely,

    The DoomCart Team"""
