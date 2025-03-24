import django_filters


class CommaSeparatedFilter(django_filters.Filter):
    def filter(self, qs, value):
        if not value:
            return qs
        values = value.split(",")
        return qs.filter(id__in=values)
    
