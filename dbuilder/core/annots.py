from functools import partial

from dbuilder.ast import CallStacks
from dbuilder.ast.types import Expr, Statement
from dbuilder.core.factory import Factory
from dbuilder.core.utils import init_abstract_type


def init_func(func):
    if not hasattr(func, "__pyfunc__"):
        setattr(func, "__pyfunc__", {})
    return func


def method(name=None):
    return partial(method_, name=name)


def method_(func, name=None):
    if is_method(func):
        return func

    def nf(*args, **kwargs):
        slf = args[0]
        if "NO_INTERCEPT" in kwargs:
            kwargs.pop("NO_INTERCEPT")
            return func(*args, **kwargs)
        elif hasattr(slf, "__intercepted__") and getattr(
            slf,
            "__intercepted__",
        ):
            annotations = func.__annotations__
            annotations = annotations if annotations else {}
            ret = annotations.get("return", None)
            e = init_abstract_type(
                ret,
                data=Expr.call_func(
                    func.__name__,
                    *args[1:],
                    annotations=func.__annotations__,
                ),
            )
            setattr(
                e,
                "__expr",
                CallStacks.add_statement(Statement.EXPR, e.data),
            )
            e.has_expr = True
            return e
        else:
            ret = func(*args, **kwargs)
            if isinstance(ret, tuple):
                ret = Factory.build("Tensor", list(ret))
            return ret

    nf = init_func(nf)
    nf.__pyfunc__["type"] = ["method"]
    setattr(nf, "__args__", func.__code__.co_argcount)
    annotations = func.__annotations__
    annotations = annotations or {}
    annotations["_fname"] = name
    setattr(nf, "__annotations__", annotations)
    setattr(
        nf,
        "__names__",
        func.__code__.co_varnames[: func.__code__.co_argcount],
    )

    return nf


def asm(input_order=None, out_order=None, name=None):
    return partial(
        asm_,
        input_order=input_order,
        out_order=out_order,
        name=name,
    )


def asm_(func, input_order=None, out_order=None, name=None):
    if is_asm(func):
        return func

    def nf(*args, **kwargs):
        slf = args[0]
        if "NO_INTERCEPT" in kwargs:
            kwargs.pop("NO_INTERCEPT")
            return func(*args, **kwargs)
        elif hasattr(slf, "__intercepted__") and getattr(
            slf,
            "__intercepted__",
        ):
            annotations = func.__annotations__
            annotations = annotations if annotations else {}
            ret = annotations.get("return", None)
            e = init_abstract_type(
                ret,
                data=Expr.call_func(
                    func.__name__,
                    *args[1:],
                    annotations=func.__annotations__,
                ),
            )
            setattr(
                e,
                "__expr",
                CallStacks.add_statement(Statement.EXPR, e.data),
            )
            e.has_expr = True
            return e
        else:
            ret = func(*args, **kwargs)
            if isinstance(ret, tuple):
                ret = Factory.build("Tensor", list(ret))
            return ret

    nf = init_func(nf)
    nf.__pyfunc__["type"] = ["asm"]
    setattr(nf, "__args__", func.__code__.co_argcount)
    annotations = func.__annotations__
    annotations = annotations or {}
    annotations["_fname"] = name
    setattr(nf, "__annotations__", annotations)
    setattr(
        nf,
        "__asm_annotations__",
        {
            "input_order": input_order,
            "out_order": out_order,
        },
    )
    setattr(
        nf,
        "__names__",
        func.__code__.co_varnames[: func.__code__.co_argcount],
    )
    return nf


def inline_ref(f):
    if is_inline(f):
        raise RuntimeError("the function already has the inline specifier")
    if is_method_id(f):
        raise RuntimeError("the function already has the method-id specifier")
    setattr(f, "__inline_ref__", True)
    return f


def inline(f):
    if is_inline_ref(f):
        raise RuntimeError(
            "the function already has the inline_ref specifier",
        )
    if is_method_id(f):
        raise RuntimeError("the function already has the method-id specifier")
    setattr(f, "__inline__", True)
    return f


def impure(f):
    setattr(f, "__impure__", True)
    return f


def method_id(id=None):
    return partial(method_id_, id=id)


def method_id_(f, id=None):
    if is_inline_ref(f):
        raise RuntimeError(
            "the function already has the inline_ref specifier",
        )
    if is_inline(f):
        raise RuntimeError("the function already has the inline specifier")
    setattr(f, "__method_id__", True)
    setattr(f, "__method_id_val__", id)
    return f


def is_inline(f):
    return hasattr(f, "__inline__") and f.__inline__


def is_impure(f):
    return hasattr(f, "__impure__") and f.__impure__


def is_method_id(f):
    return hasattr(f, "__method_id__") and f.__method_id__


def is_inline_ref(f):
    return hasattr(f, "__inline_ref__") and f.__inline_ref__


def is_method(func):
    if not hasattr(func, "__pyfunc__"):
        return False
    type_ = func.__pyfunc__.get("type", [])
    return "method" in type_


def is_asm(func):
    if not hasattr(func, "__pyfunc__"):
        return False
    type_ = func.__pyfunc__.get("type", [])
    return "asm" in type_
