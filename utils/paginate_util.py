from django.core.paginator import Paginator, EmptyPage


def paginate(request, objects, results):
    page = request.GET.get('page') or 1
    page = int(page)
    paginator = Paginator(objects, results)

    try:
        objects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        objects = paginator.page(page)

    left_index = (page - 4)
    if left_index < 1:
        left_index = 1

    right_index = page + 5

    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)

    return custom_range, objects
