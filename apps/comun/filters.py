import django_filters
from django.forms import HiddenInput

from apps.comun.filter_fields import CommaSeparatedFilter

# The `AbstractFilter` class in Python is a Django filter set that customizes filter fields and

class AbstractFilter(django_filters.FilterSet):
    # id = CommaSeparatedFilter(field_name="id")

    # The class `Meta` in Python contains abstract attributes and a dictionary for fields.
    class Meta:
        abstract = True
        fields_dict = {}

    def __init__(self, *args, **kwargs):
        """
        The function initializes filters for fields in a Django model form, setting labels, attributes,
        and input types based on field types.
        """
        super().__init__(*args, **kwargs)

        fields_dict = self.Meta.fields_dict

        for field_name in self.get_fields():
            label = fields_dict[field_name]["label"]
            self.filters[field_name].label = label
            self.filters[field_name].field.widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": fields_dict[field_name].get("placeholder", label),
                },
            )

            # If it's an input field, change it so that it uses contains
            if self.filters[field_name].__class__.__name__ == "CharFilter":
                self.filters[field_name].lookup_expr = "icontains"

            elif self.filters[field_name].__class__.__name__ == "DateFilter":
                self.filters[field_name].field.widget.input_type = "date"

            elif self.filters[field_name].__class__.__name__ == "DateTimeFilter":
                self.filters[field_name].field.widget.input_type = "datetime-local"

            elif self.filters[field_name].__class__.__name__ == "TimeFilter":
                self.filters[field_name].field.widget.input_type = "time"

            elif "ChoiceFilter" in self.filters[field_name].__class__.__name__:
                self.filters[field_name].field.widget.attrs.update(
                    {"class": "select form-select"},
                )

        if not "id" in fields_dict:
            pass
            # self.filters["id"].field.widget = HiddenInput()

        elif fields_dict["id"].get("hidden", True):
            print("Hidden id field")
            # self.filters["id"].field.widget = HiddenInput()
