import inspect
from inspect import signature, Parameter, Signature
from argparse import ArgumentParser
from typing import Callable, Any, Tuple


def run(command: Callable[..., Any]):
    parser = ArgumentParser()
    signature: Signature = inspect.signature(command)
    parameters = signature.parameters
    for name in parameters:
        parameter: Parameter = parameters[name]

        default = None
        name = name.replace("_", "-")
        if parameter.default != parameter.empty:
            default = parameter.default
            name = f"--{name}"
        kwargs: dict[str, Any] = dict(type=str, action="store")

        if parameter.annotation != parameter.empty:
            if hasattr(parameter.annotation, "__metadata__"):
                kwargs["type"] = parameter.annotation.__origin__
                metadata = parameter.annotation.__metadata__
            if callable(parameter.annotation):
                kwargs["type"] = parameter.annotation

        if kwargs.get("type", None) == bool:
            kwargs["action"] = "store_false" if default else "store_true"

        if kwargs.get("action", None) in ["store_const", "store_true", "store_false", "help"]:
            kwargs.pop("type", None)

        parser.add_argument(name, default=default, **kwargs)
    command(**vars(parser.parse_args()))
