from home.models import Vote
from accounts.models import User


def user_like(user):
    user_like = Vote.objects.filter(user=user)
    if user_like is not None:
        can_like = [b.post.id for b in user_like ]
    else :
        can_like=[]
    return can_like

def user_save(user):
    pass 