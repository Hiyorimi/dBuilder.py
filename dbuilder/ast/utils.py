from types import GenericAlias


def _type_name(type_):
    if isinstance(type_, GenericAlias) and type_.__origin__ == tuple:
        types = map(_type_name, type_.__args__)
        names = ", ".join(types)
        n = "({names})".format(names=names)
        return n
    elif hasattr(type_, "type_name"):
        return type_.type_name()
    elif type_ is None:
        return "()"
    elif type_ == int:
        return "int"
    elif type_ == "var":
        return "var"
    return "_"
