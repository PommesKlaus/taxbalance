from django.db.models.fields.related import ManyToManyField

def to_dict(instance):
    """ Returns a provided Django Model Instance as python dictionary. """
    opts = instance._meta
    data = {}
    for f in opts.concrete_fields + opts.many_to_many:
        if isinstance(f, ManyToManyField):
            if instance.pk is None:
                data[f.name] = []
            else:
                data[f.name] = []
                # Following line eventually not working; To check if m2m-Relationship is required.
                # data[f.name] = list(f.value_from_object(instance).values_list('pk', flat=True))
        else:
            data[f.name] = getattr(instance, f.name)
    if "id" in data:
        data["pk"] = data["id"]
    return data
