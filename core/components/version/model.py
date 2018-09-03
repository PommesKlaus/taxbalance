from django.db import models


class Version(models.Model):
    shortname = models.CharField(max_length=30)
    reporting_date = models.DateField()
    company = models.ForeignKey(
        'Company',
        related_name='versions',
        on_delete=models.CASCADE
        )
    compare_version = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_name="compared_in",
        on_delete=models.PROTECT
        )
    matching_version = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_name="matching_in",
        on_delete=models.PROTECT
        )
    copy_version = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_name="copied_in",
        on_delete=models.SET_NULL
        )
    description = models.CharField(max_length=150, blank=True, default="")
    archived = models.BooleanField(default=False)
    locked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{0} > {1}".format(self.reporting_date, self.shortname)

    def partial_update(self, save_update=True, **kwargs):
        """Updates the specified model instance using the keyword arguments as the model
        property attributes and values.
        """
        cls = type(self)
        foreign_key_fields = []
        for attr, val in kwargs.items():
            # Check if attr in model
            if hasattr(self, attr):
                # If model-attr is a Foreign_Key field:
                # Add "_id"-suffix to provided attr-name
                if cls._meta.get_field(attr).is_relation:
                    setattr(self, attr + "_id", val)
                    foreign_key_fields.append(attr)
                else:
                    setattr(self, attr, val)
            else:
                raise KeyError("Failed to update non existing attribute {}.{}".format(str(cls), attr))
        if save_update:
            self.save()
            # partial_update modifies Foreign-Key-Fields directly by their _id-Attribute
            # Problem: The "real" related field doesn't get updated; therefore resulting
            # in a difference between fk_field_id and fk_field.id
            # Solution: Remember all Foreign-Key-Fields which are updated and perform
            # a refresh from db for these fields.
            self.refresh_from_db(fields=foreign_key_fields)
