"""
AST Transformer.

Patches the contract AST to capture the assignments, wrap the returns
Wouldn't be possible without:
https://gist.github.com/RyanKung/4830d6c8474e6bcefa4edd13f122b4df
"""

import ast

from dbuilder.ast.patchers import (
    AssertPatcher,
    AssignPatcher,
    IfPatcher,
    RaisePatcher,
    ReturnPatcher,
    WhilePatcher,
)


def patch(node):
    transformers = [
        AssertPatcher(),
        AssignPatcher(),
        IfPatcher(),
        RaisePatcher(),
        ReturnPatcher(),
        WhilePatcher(),
    ]
    for t in transformers:
        new_node = t.visit(node)
        ast.fix_missing_locations(new_node)
    return new_node
