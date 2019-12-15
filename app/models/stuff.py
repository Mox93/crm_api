from . import db, ExtendedDocument
from .reference import Reference


def stuff_builder(ref, fields, parents=tuple()):
    name = ref.name
    fields["meta"] = {"collection":ref.collection}
    thing = type(name, (*parents, ExtendedDocument), fields)
    return thing

