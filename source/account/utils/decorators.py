def required_login(func):
    """ Decorator to check if user is logged. """
    def inner(request):
        if not request.user.is_authenticated:
            return redirect('account:login')

        ret = func(request)
        return ret
    
    return inner
