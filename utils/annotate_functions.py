from django.db.models import Func


def ToCharTZ(expression, timezone, output):
    """
    Custom query to convert timestamp to string in requested time zone.

    Example usage
    queryset.annotate(
        created_date_str=ToCharTZ('created_date', 'GB', 'DD/MM/YYYY HH25:MI')
        )
    """

    class ToCharWithTZ(Func):

        function = "TO_CHAR"
        template = "%(function)s(%(expressions)s AT TIME ZONE '{timezone}', '{output}')".format(
            timezone=timezone, output=output
        )

    return ToCharWithTZ(expression)