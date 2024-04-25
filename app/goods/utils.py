from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
# from django.db.models import Q

from goods.models import Products


def q_search(query):
    if query.isdigit() and len(query) <= 5:
        return Products.objects.filter(id=int(query))

    vector = SearchVector('name', 'description')
    query = SearchQuery(query)
    return Products.objects.annotate(rank=SearchRank(vector, query)).order_by("-rank")

    # keywords = [word for word in query.split() if len(word) > 2]  # Получение слов без предлогов
    #
    # q_objects = Q()  # Если пользователь введёт како-либо предлог, то ему выдастся весь список,
    # # т.к. эта переменная будет пустая
    #
    # for token in keywords:
    #     q_objects |= Q(description__icontains=token)
    #     q_objects |= Q(name__icontains=token)
    #
    # return Products.objects.filter(q_objects)
