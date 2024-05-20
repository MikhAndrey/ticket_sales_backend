from django.core.paginator import Page, Paginator


class Response:
    def __init__(self, model=None, message=None, errors=None):
        self.model = model
        self.message = message
        self.errors = errors

    def to_dict(self):
        return {
            "model": self.model,
            "message": self.message,
            "errors": self.errors
        }


class PageResponse:
    def __init__(self, model, message, page_obj: Page, paginator: Paginator, errors=None):
        self.model = model
        self.message = message
        self.errors = errors
        self.page_number = page_obj.number
        self.total_pages = paginator.num_pages
        self.total_items = paginator.count
        self.has_next = page_obj.has_next()
        self.has_previous = page_obj.has_previous()

    def to_dict(self):
        return {
            "model": self.model,
            "message": self.message,
            "errors": self.errors,
            "page_number": self.page_number,
            "total_pages": self.total_pages,
            "total_items": self.total_items,
            "has_next": self.has_next,
            "has_previous": self.has_previous
        }
