from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from common.response import make_response


class StandardPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response(make_response(
            data=data,
            links={
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            amount=self.page.paginator.count,
            page_count=self.page.paginator.num_pages
        ))
