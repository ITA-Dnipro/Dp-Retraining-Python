import math

from users.models import User


class PaginationPage:
    """Custom pagination page object."""

    def __init__(self, items: list[User], page: int, page_size: int, total: int) -> None:
        self.current_page = page
        self.items = items
        self.previous_page = None
        self.next_page = None

        self.has_previous = page > 1
        if self.has_previous:
            self.previous_page = page - 1

        previous_items = (page - 1) * page_size
        self.has_next = previous_items + len(items) < total
        if self.has_next:
            self.next_page = page + 1

        self.total_pages = int(math.ceil(total / float(page_size)))
