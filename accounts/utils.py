def detectUser(user):
    if user.role == 1:
        redirectUrl = 'venDashbord'
        return redirectUrl
    elif user.role == 2:
        redirectUrl = 'cusDashbord'
        return redirectUrl
    elif user.role == None and user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl