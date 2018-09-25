from allauth.socialaccount.models import SocialToken
import requests


def st(request):
    global access_t
    access_t = None
    if request.user.is_authenticated and not request.user.is_superuser:
        access_t = SocialToken.objects.get(account__user=request.user, account__provider='vk')
    return {'access_token': access_t}


def friends(request):
    fields = 'order=random&count=5&fields=photo_100'
    url = "https://api.vk.com/method/friends.get?" + fields + "&v=5.84&access_token=" + str(access_t)
    data = requests.get(url, verify=True)
    items = data.json()
    return {"Items": items}
