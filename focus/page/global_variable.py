from ..models import PostType
def settings(request):
    types=PostType.objects.all()
    content={'types':types}
    return content
