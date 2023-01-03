import inspect
from logging import INFO, WARNING, getLogger
from typing import Any, Callable, ParamSpec, TypeVar, get_type_hints, overload

from django.core.exceptions import ObjectDoesNotExist

from core.seedwork.domain_layer import DomainError

logger = getLogger("usecase")

T = TypeVar("T")


class Findable:
    def __init__(self, func):
        self.__func = func

    def __call__(self, *args, **kwargs):
        return self.__func(*args, **kwargs)


def find(func: Callable[[Any, Any], T]) -> T:
    # The use case wrapper calls this function and makes this function return T

    return Findable(func)  # type: ignore


class UseCaseError(Exception):
    def __init__(self, message):
        self.message = message


class UseCaseInputError(Exception):
    def __init__(self, message):
        self.message = message


P1 = ParamSpec("P1")


def finder_function(function: Callable[P1, Any]) -> Callable[P1, Any]:
    def decorator(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except ObjectDoesNotExist:
            message = "The object could not be found."
            raise UseCaseInputError(message)

    return decorator


__all__ = [
    "use_case",
    "find",
    "UseCaseError",
    "UseCaseInputError",
]


def __check_actor(args, kwargs, func_code, type_hints):
    if len(func_code.co_varnames) == 0 or "__actor" not in func_code.co_varnames:
        raise ValueError("The use case function needs to have '__actor' as input.")

    if "__actor" not in type_hints:
        raise ValueError("The usecase needs a type hint to '__actor'.")

    if "__actor" in kwargs:
        actor = kwargs["__actor"]
    elif len(args) > 0:
        index = func_code.co_varnames.index("__actor")
        actor = args[index]
    else:
        raise ValueError(
            "You need to submit an '__actor' when you call a use case function."
        )

    usecase_actor_type = type_hints["__actor"]
    if not isinstance(actor, usecase_actor_type):
        raise TypeError(
            "The submitted use case '__actor' type is '{}' but should be '{}'.".format(
                type(actor), usecase_actor_type
            )
        )

    return actor


def __check_type(value, type_hint):
    value_type = type(value)
    if value_type != type_hint:
        raise TypeError(
            "The type of '{}' is '{}' but should be '{}'.".format(
                value, value_type, type_hint
            )
        )


def __update_parameters(args, kwargs, func, actor):
    args = list(args)

    signature = inspect.signature(func)
    data = {k: v.default for k, v in signature.parameters.items()}

    for index, (key, value) in enumerate(data.items()):
        if isinstance(value, Findable):

            try:
                if index < len(args):
                    old_value = args[index]
                else:
                    old_value = kwargs[key]
            except (IndexError, KeyError):
                raise ValueError("You need to submit '{}'.".format(key))

            try:
                new_value = value(actor, old_value)
            except ObjectDoesNotExist as e:
                message = "The object with identifier '{}' could not be found.".format(
                    old_value
                )
                raise UseCaseInputError(message) from e

            if index < len(args):
                args[index] = new_value
            else:
                kwargs[key] = new_value

    return args, kwargs


def __check_permissions(actor, permissions):
    for permission in permissions:
        if not actor.has_permission(permission):
            message = "You need the permission '{}' to do this.".format(permission)
            raise UseCaseError(message)


Param = ParamSpec("Param")
RetType = TypeVar("RetType")


@overload
def use_case(
    func: Callable[Param, RetType],
    *,
    permissions: None = ...,
) -> Callable[Param, RetType]:
    ...


@overload
def use_case(
    func: None = ...,
    *,
    permissions: list[str] | None = ...,
) -> Callable[[Callable[Param, RetType]], Callable[Param, RetType]]:
    ...


def use_case(
    func: Callable[Param, RetType] | None = None,
    *,
    permissions: list[str] | None = None,
) -> Callable[Param, RetType] | Callable[
    [Callable[Param, RetType]], Callable[Param, RetType]
]:
    if permissions is None:
        permissions = []

    def decorator(usecase_func: Callable[Param, RetType]) -> Callable[Param, RetType]:
        type_hints = get_type_hints(usecase_func)

        def wrapper(*args, **kwargs) -> RetType:
            func_code = usecase_func.__code__
            func_name = func_code.co_name

            actor = __check_actor(args, kwargs, func_code, type_hints)

            __check_permissions(actor, permissions)

            args, kwargs = __update_parameters(args, kwargs, usecase_func, actor)

            try:
                ret = usecase_func(*args, **kwargs)
                msg = "SUCCESS: '{}' called '{}'.".format(str(actor), func_name)
                logger.log(INFO, msg)
                return ret
            except (UseCaseError, DomainError) as e:
                msg = "ERROR: '{}' called '{}' and '{}' happened.".format(
                    str(actor), func_name, str(e)
                )
                logger.log(WARNING, msg)
                raise e

        return wrapper

    if func:
        # this happens when use_case is used like @use_case instead of @use_case()
        return decorator(func)

    return decorator
