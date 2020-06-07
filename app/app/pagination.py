from rest_framework import pagination


# PageNumberPagination):
class BlogsPagination(pagination.LimitOffsetPagination):
    page_size = 10
    default_limit = 5
    max_limit = 20
    #limit_query_param = 'lim'
