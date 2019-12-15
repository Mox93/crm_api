from models.field import FieldModel
from .utils import DBInterface
from graphene import (ObjectType, Mutation, InputObjectType,
                      String, Int, Boolean, ID, List, Field, InputField)


class CommonAttributes(object):
    question = String()
    description = String()
    required = Boolean()
    input_type = String()


class FieldInterface(CommonAttributes, DBInterface):
    # _id = ID()
    pass


class FieldType(ObjectType):
    class Meta:
        name = "Field"
        description = "..."
        interfaces = (FieldInterface,)

    # creation_date = DateTime()
    # modified_date = DateTime()

    name = String()


class FieldInput(CommonAttributes, InputObjectType):
    name = String()


class CreateField(InputObjectType):
    field_data = InputField(FieldInput, required=True)


class UpdateField(InputObjectType):
    field_id = ID()
    field_data = InputField(FieldInput, required=True)


class DeleteField(InputObjectType):
    field_id = ID()


class FieldOps(Mutation):
    class Meta:
        name = "FieldOps"
        description = "..."

    class Arguments:
        create = CreateField()
        update = UpdateField()
        delete = DeleteField()

    ok = Boolean()
    ops = List(String)
    field = Field(lambda: FieldType)

    @staticmethod
    def mutate(root, info, create=None, update=None, delete=None):
        ops = []
        ok = False
        field = None

        if create:
            ops.append("create")
            field = FieldModel(**create.field_data)

            try:
                field.save()
                ok = True
            except Exception as e:
                print(str(e))
                ok = False

        if update:
            ops.append("update")
            field = FieldModel.find_by_id(update.field_id)

            try:
                for key, val in update.field_data.items():
                    if hasattr(field, key):
                        setattr(field, key, val)
                field.save()
                ok = True
            except Exception as e:
                print(str(e))
                ok = False

        if delete:
            ops.append("delete")
            field = FieldModel.find_by_id(delete.field_id)

            try:
                field.delete()
                ok = True
            except Exception as e:
                print(str(e))
                ok = False

            return FieldOps(ok=ok, ops=ops)

        return FieldOps(ok=ok, field=field, ops=ops)


class EmbeddedFieldType(ObjectType):
    class Meta:
        name = "EmbeddedField"
        description = "..."
        interfaces = (FieldInterface,)

    index = Int()
    collection = ID()


class EmbeddedFieldInput(CommonAttributes, InputObjectType):
    index = Int()
    collection = ID()


class AddField(InputObjectType):
    form_id = ID(required=True)
    field_data = InputField(EmbeddedFieldInput, required=True)


class EditField(InputObjectType):
    form_id = ID(required=True)
    field_id = ID(required=True)
    field_data = InputField(EmbeddedFieldInput, required=True)


class RemoveField(InputObjectType):
    form_id = ID()
    field_id = ID(required=True)

