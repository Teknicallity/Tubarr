from drf_link_header_pagination import LinkHeaderPagination


class CustomPagination(LinkHeaderPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
