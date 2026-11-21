from django.core.exceptions import ValidationError


class MustRespectDateRanges:
    """A custom validator for movie published year"""
    def __call__(self, published_year):
        if published_year < 1900 or published_year > 2100:
            raise ValidationError("Published year can only be between from 1900 to 2100")

    def get_help_text(self):
        return "Published year can only be between from 1900 to 2100"

    def deconstruct(self):
        return (
            'movies.validators.MustRespectDateRanges', [], {}
        )
