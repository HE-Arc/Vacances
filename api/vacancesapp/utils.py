from .models import User

# This variable "simulate" the name of the connected user
DEBUG_force_connect_user = "admin" # TODO DEBUG VAR Comment this line when auth is implemented 
# Available users :       admin               (mentionned in "clone project steps")
#   LOCAL TO @Jonas :     samy, MPolo


def get_current_username(request):
    """Get the current usename (connected) from the request context

    Args:
        request (_type_): the request that contains connected user information.

    Returns:
        User: The connected user
        
    Note : If global var "DEBUG_force_connect_user" exists, the connected user will be forced to this value
        instead of the real connected user
    """
    
    if "DEBUG_force_connect_user" in globals():
        print("FORCED 'connected' user to " + DEBUG_force_connect_user)
        return User.objects.get(username=DEBUG_force_connect_user)
    
    user = request.user
    if (user.is_anonymous):
        print("TODO NEED TO HANDLE ANONYMOUS USER") # TODO What we do when the user is anonymous ?
    
    return user