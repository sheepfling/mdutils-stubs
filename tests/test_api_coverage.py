"""Structural inventory checks against the installed mdutils runtime source.

These checks compare names and call signatures. They intentionally do not claim
to infer whether each declared type captures the runtime's full semantics; the
external consumer fixtures cover selected positive and negative typing cases.
"""

from __future__ import annotations

import ast
import importlib
import importlib.util
import unittest
from collections import Counter
from importlib import metadata
from pathlib import Path

RUNTIME_MODULES = frozenset(
    {
        "__init__",
        "fileutils/__init__",
        "fileutils/fileutils",
        "mdutils",
        "tools/Header",
        "tools/Html",
        "tools/Image",
        "tools/Link",
        "tools/MDList",
        "tools/Table",
        "tools/TableOfContents",
        "tools/TextUtils",
        "tools/__init__",
    }
)

PACKAGE_EXPORTS = {
    "mdutils": frozenset(
        {
            "Header",
            "Html",
            "Image",
            "Link",
            "MDList",
            "MdUtils",
            "Table",
            "TableOfContents",
            "TextUtils",
            "fileutils",
            "mdutils",
            "tools",
        }
    ),
    "mdutils.fileutils": frozenset({"MarkDownFile", "fileutils"}),
    "mdutils.tools": frozenset(
        {
            "Header",
            "Html",
            "Image",
            "Inline",
            "Link",
            "MDCheckbox",
            "MDList",
            "SizeBadFormat",
            "Table",
            "TableOfContents",
            "TextUtils",
        }
    ),
}

# The normalized source module and imported name used by each stub package
# initializer. This protects aliases whose runtime package attribute shadows
# the package object with a nested module of the same name.
PACKAGE_STUB_IMPORTS = {
    "mdutils": {
        "Header": ("mdutils.tools", "Header"),
        "Html": ("mdutils.tools", "Html"),
        "Image": ("mdutils.tools", "Image"),
        "Link": ("mdutils.tools", "Link"),
        "MDList": ("mdutils.tools", "MDList"),
        "MdUtils": ("mdutils.mdutils", "MdUtils"),
        "Table": ("mdutils.tools", "Table"),
        "TableOfContents": ("mdutils.tools", "TableOfContents"),
        "TextUtils": ("mdutils.tools", "TextUtils"),
        "fileutils": ("mdutils.fileutils", "fileutils"),
        "mdutils": ("mdutils", "mdutils"),
        "tools": ("mdutils", "tools"),
    },
    "mdutils.fileutils": {
        "MarkDownFile": ("mdutils.fileutils.fileutils", "MarkDownFile"),
        "fileutils": ("mdutils.fileutils", "fileutils"),
    },
    "mdutils.tools": {
        "Header": ("mdutils.tools", "Header"),
        "Html": ("mdutils.tools.Html", "Html"),
        "Image": ("mdutils.tools", "Image"),
        "Inline": ("mdutils.tools.Link", "Inline"),
        "Link": ("mdutils.tools", "Link"),
        "MDCheckbox": ("mdutils.tools.MDList", "MDCheckbox"),
        "MDList": ("mdutils.tools.MDList", "MDList"),
        "SizeBadFormat": ("mdutils.tools.Html", "SizeBadFormat"),
        "Table": ("mdutils.tools", "Table"),
        "TableOfContents": ("mdutils.tools", "TableOfContents"),
        "TextUtils": ("mdutils.tools.TextUtils", "TextUtils"),
    },
}

EXPORT_TARGETS = {
    "mdutils": {
        "Header": ("mdutils.tools.Header", None),
        "Html": ("mdutils.tools.Html", "Html"),
        "Image": ("mdutils.tools.Image", None),
        "Link": ("mdutils.tools.Link", None),
        "MDList": ("mdutils.tools.MDList", "MDList"),
        "MdUtils": ("mdutils.mdutils", "MdUtils"),
        "Table": ("mdutils.tools.Table", None),
        "TableOfContents": ("mdutils.tools.TableOfContents", None),
        "TextUtils": ("mdutils.tools.TextUtils", "TextUtils"),
        "fileutils": ("mdutils.fileutils.fileutils", None),
        "mdutils": ("mdutils.mdutils", None),
        "tools": ("mdutils.tools", None),
    },
    "mdutils.fileutils": {
        "MarkDownFile": ("mdutils.fileutils.fileutils", "MarkDownFile"),
        "fileutils": ("mdutils.fileutils.fileutils", None),
    },
    "mdutils.tools": {
        "Header": ("mdutils.tools.Header", None),
        "Html": ("mdutils.tools.Html", "Html"),
        "Image": ("mdutils.tools.Image", None),
        "Inline": ("mdutils.tools.Link", "Inline"),
        "Link": ("mdutils.tools.Link", None),
        "MDCheckbox": ("mdutils.tools.MDList", "MDCheckbox"),
        "MDList": ("mdutils.tools.MDList", "MDList"),
        "SizeBadFormat": ("mdutils.tools.Html", "SizeBadFormat"),
        "Table": ("mdutils.tools.Table", None),
        "TableOfContents": ("mdutils.tools.TableOfContents", None),
        "TextUtils": ("mdutils.tools.TextUtils", "TextUtils"),
    },
}


def _is_public(name: str) -> bool:
    return not name.startswith("_") or (name.startswith("__") and name.endswith("__"))


def _defined_names(tree: ast.Module) -> set[str]:
    return {
        node.name
        for node in tree.body
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
        and _is_public(node.name)
    }


def _class_nodes(tree: ast.Module) -> dict[str, ast.ClassDef]:
    return {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.ClassDef) and _is_public(node.name)
    }


def _method_nodes(class_node: ast.ClassDef) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    return {
        node.name: node
        for node in class_node.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and _is_public(node.name)
    }


def _default_key(value: ast.expr | None) -> str | None:
    return None if value is None else ast.dump(value, include_attributes=False)


def _signature_shape(
    function: ast.FunctionDef | ast.AsyncFunctionDef,
) -> tuple[tuple[str, str, str | None], ...]:
    args = function.args
    positional = [*args.posonlyargs, *args.args]
    positional_defaults: dict[str, ast.expr] = dict(
        zip(
            (arg.arg for arg in positional[-len(args.defaults) :]) if args.defaults else (),
            args.defaults,
        )
    )
    result = [
        (
            arg.arg,
            "positional_only" if index < len(args.posonlyargs) else "positional_or_keyword",
            _default_key(positional_defaults.get(arg.arg)),
        )
        for index, arg in enumerate(positional)
    ]
    if args.vararg is not None:
        result.append((args.vararg.arg, "var_positional", None))
    result.extend(
        (arg.arg, "keyword_only", _default_key(default))
        for arg, default in zip(args.kwonlyargs, args.kw_defaults)
    )
    if args.kwarg is not None:
        result.append((args.kwarg.arg, "var_keyword", None))
    return tuple(result)


def _decorator_kinds(function: ast.FunctionDef | ast.AsyncFunctionDef) -> frozenset[str]:
    kinds = set()
    for decorator in function.decorator_list:
        if isinstance(decorator, ast.Name) and decorator.id in {
            "staticmethod",
            "classmethod",
            "property",
        }:
            kinds.add(decorator.id)
        elif isinstance(decorator, ast.Attribute) and decorator.attr in {"setter", "deleter"}:
            kinds.add(decorator.attr)
    return frozenset(kinds)


def _expression_name(expression: ast.expr) -> str:
    if isinstance(expression, ast.Name):
        return expression.id
    if isinstance(expression, ast.Attribute):
        return f"{_expression_name(expression.value)}.{expression.attr}"
    return ast.dump(expression, include_attributes=False)


def _class_bases(class_node: ast.ClassDef) -> tuple[str, ...]:
    if not class_node.bases:
        return ("object",)
    return tuple(_expression_name(base) for base in class_node.bases)


def _target_names(target: ast.expr) -> set[str]:
    if isinstance(target, ast.Name) and _is_public(target.id):
        return {target.id}
    if isinstance(target, (ast.Tuple, ast.List)):
        return set().union(*(_target_names(item) for item in target.elts))
    return set()


def _class_attributes(class_node: ast.ClassDef) -> set[str]:
    attributes: set[str] = set()
    for node in class_node.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                attributes.update(_target_names(target))
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if "property" in _decorator_kinds(node):
                attributes.add(node.name)
            parameters = [*node.args.posonlyargs, *node.args.args]
            if parameters:
                receiver = parameters[0].arg
                for child in ast.walk(node):
                    if isinstance(child, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
                        targets = child.targets if isinstance(child, ast.Assign) else [child.target]
                        for target in targets:
                            if (
                                isinstance(target, ast.Attribute)
                                and isinstance(target.value, ast.Name)
                                and target.value.id == receiver
                                and _is_public(target.attr)
                            ):
                                attributes.add(target.attr)
    return attributes


def _enum_members(class_node: ast.ClassDef) -> set[str]:
    if not any(
        _expression_name(base).split(".")[-1] in {"Enum", "IntEnum", "StrEnum"}
        for base in class_node.bases
    ):
        return set()
    members: set[str] = set()
    for node in class_node.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                members.update(_target_names(target))
    return members


def _stub_import_bindings(package: str, tree: ast.Module) -> dict[str, tuple[str, str]]:
    bindings: dict[str, tuple[str, str]] = {}
    for node in tree.body:
        if not isinstance(node, ast.ImportFrom):
            continue
        if node.level:
            relative = "." * node.level + (node.module or "")
            module = importlib.util.resolve_name(relative, package)
        else:
            module = node.module or ""
        for alias in node.names:
            exported = alias.asname or alias.name
            bindings[exported] = (module, alias.name)
    return bindings


def _runtime_package_root() -> Path:
    spec = importlib.util.find_spec("mdutils")
    if spec is None or spec.origin is None:
        raise AssertionError("The mdutils runtime dependency is not installed")
    return Path(spec.origin).parent


class PublicApiCoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.runtime_root = _runtime_package_root()
        cls.stub_root = Path(__file__).parents[1] / "mdutils-stubs"
        runtime_version = metadata.version("mdutils")
        if runtime_version != "1.8.1":
            raise AssertionError(
                f"API inventory is pinned to mdutils 1.8.1, found {runtime_version}"
            )

    def test_runtime_modules_have_one_to_one_stub_files(self) -> None:
        runtime_modules = {
            path.relative_to(self.runtime_root).with_suffix("").as_posix()
            for path in self.runtime_root.rglob("*.py")
        }
        stub_modules = {
            path.relative_to(self.stub_root).with_suffix("").as_posix()
            for path in self.stub_root.rglob("*.pyi")
        }
        self.assertEqual(runtime_modules, RUNTIME_MODULES)
        self.assertEqual(stub_modules, RUNTIME_MODULES)

    def test_public_definitions_and_class_shapes_match(self) -> None:
        class_count = 0
        method_count = 0
        attribute_count = 0
        enum_member_count = 0
        for relative in sorted(RUNTIME_MODULES):
            runtime_path = self.runtime_root / f"{relative}.py"
            stub_path = self.stub_root / f"{relative}.pyi"
            runtime_tree = ast.parse(runtime_path.read_text(encoding="utf-8"))
            stub_tree = ast.parse(stub_path.read_text(encoding="utf-8"))
            self.assertEqual(_defined_names(runtime_tree), _defined_names(stub_tree), relative)
            runtime_classes = _class_nodes(runtime_tree)
            stub_classes = _class_nodes(stub_tree)
            self.assertEqual(runtime_classes.keys(), stub_classes.keys(), relative)
            for class_name, runtime_class in runtime_classes.items():
                class_count += 1
                stub_class = stub_classes[class_name]
                self.assertEqual(
                    _class_bases(runtime_class),
                    _class_bases(stub_class),
                    f"{relative}:{class_name} bases",
                )
                runtime_methods = _method_nodes(runtime_class)
                stub_methods = _method_nodes(stub_class)
                self.assertEqual(
                    runtime_methods.keys(), stub_methods.keys(), f"{relative}:{class_name} methods"
                )
                for method_name, runtime_method in runtime_methods.items():
                    stub_method = stub_methods[method_name]
                    self.assertEqual(
                        _signature_shape(runtime_method),
                        _signature_shape(stub_method),
                        f"{relative}:{class_name}.{method_name} parameters/defaults",
                    )
                    self.assertEqual(
                        _decorator_kinds(runtime_method),
                        _decorator_kinds(stub_method),
                        f"{relative}:{class_name}.{method_name} decorators",
                    )
                    method_count += 1
                runtime_attributes = _class_attributes(runtime_class)
                stub_attributes = _class_attributes(stub_class)
                self.assertEqual(
                    runtime_attributes,
                    stub_attributes,
                    f"{relative}:{class_name} public attributes",
                )
                runtime_enum = _enum_members(runtime_class)
                stub_enum = _enum_members(stub_class)
                self.assertEqual(runtime_enum, stub_enum, f"{relative}:{class_name} enum members")
                attribute_count += len(runtime_attributes - runtime_enum)
                enum_member_count += len(runtime_enum)

        self.assertEqual(class_count, 18)
        self.assertEqual(method_count, 61)
        self.assertEqual(attribute_count, 23)
        self.assertEqual(enum_member_count, 10)

    def test_initializer_exports_match_runtime_aliases_and_typing_fixture(self) -> None:
        fixture_path = Path(__file__).parent / "fixtures" / "positive.py"
        fixture_tree = ast.parse(fixture_path.read_text(encoding="utf-8"))
        fixture_imports: dict[str, set[str]] = {name: set() for name in PACKAGE_EXPORTS}
        for node in fixture_tree.body:
            if isinstance(node, ast.ImportFrom) and node.module in fixture_imports:
                fixture_imports[node.module].update(alias.name for alias in node.names)

        for package, expected_names in PACKAGE_EXPORTS.items():
            runtime_package = importlib.import_module(package)
            runtime_names = {name for name in vars(runtime_package) if not name.startswith("_")}
            self.assertEqual(runtime_names, expected_names, f"{package} runtime exports")
            self.assertEqual(fixture_imports[package], expected_names, f"{package} fixture imports")

            relative = package.removeprefix("mdutils").lstrip(".")
            stub_init = (
                self.stub_root / relative / "__init__.pyi"
                if relative
                else self.stub_root / "__init__.pyi"
            )
            stub_tree = ast.parse(stub_init.read_text(encoding="utf-8"))
            stub_names = {
                alias.asname or alias.name
                for node in stub_tree.body
                if isinstance(node, ast.ImportFrom)
                for alias in node.names
            }
            self.assertEqual(stub_names, expected_names, f"{package} stub exports")
            self.assertEqual(
                _stub_import_bindings(package, stub_tree),
                PACKAGE_STUB_IMPORTS[package],
                f"{package} stub import targets",
            )

            for export, (target_module, target_name) in EXPORT_TARGETS[package].items():
                target = importlib.import_module(target_module)
                expected = target if target_name is None else getattr(target, target_name)
                self.assertIs(
                    getattr(runtime_package, export), expected, f"{package}.{export} runtime alias"
                )

    def test_consumer_fixture_probes_every_public_callable(self) -> None:
        fixture_path = Path(__file__).parent / "fixtures" / "positive.py"
        fixture_tree = ast.parse(fixture_path.read_text(encoding="utf-8"))
        method_probes: Counter[str] = Counter(
            node.func.attr
            for node in ast.walk(fixture_tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
        )
        constructor_probes: set[str] = set()
        expected_methods: Counter[str] = Counter()
        expected_constructors: set[str] = set()
        expected_str_methods = 0
        for relative in RUNTIME_MODULES:
            tree = ast.parse((self.runtime_root / f"{relative}.py").read_text(encoding="utf-8"))
            for class_name, class_node in _class_nodes(tree).items():
                for method_name in _method_nodes(class_node):
                    if method_name == "__init__":
                        expected_constructors.add(class_name)
                    elif method_name == "__str__":
                        expected_str_methods += 1
                    else:
                        expected_methods[method_name] += 1

        imported_names: dict[str, str] = {}
        for node in fixture_tree.body:
            if isinstance(node, ast.ImportFrom):
                imported_names.update(
                    {alias.asname or alias.name: alias.name for alias in node.names}
                )
        constructor_probes = {
            imported_names.get(node.func.id, node.func.id)
            for node in ast.walk(fixture_tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and imported_names.get(node.func.id, node.func.id) in expected_constructors
        }

        self.assertEqual(method_probes, expected_methods, "typed method call inventory")
        self.assertEqual(constructor_probes, expected_constructors, "constructor call inventory")
        self.assertEqual(
            sum(
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "str"
                for node in ast.walk(fixture_tree)
            ),
            expected_str_methods,
            "protocol __str__ call inventory",
        )

        parents = {
            child: parent
            for parent in ast.walk(fixture_tree)
            for child in ast.iter_child_nodes(parent)
        }
        for node in ast.walk(fixture_tree):
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
                continue
            parent = parents.get(node)
            while parent is not None:
                if (
                    isinstance(parent, ast.Call)
                    and isinstance(parent.func, ast.Name)
                    and parent.func.id == "assert_type"
                ):
                    break
                parent = parents.get(parent)
            self.assertIsNotNone(parent, f"{node.func.attr} call must assert its result type")

    def test_runtime_has_no_unmodeled_dynamic_api_hooks_or_any_annotations(self) -> None:
        forbidden = {"__getattr__", "__getattribute__", "__dir__", "setattr", "exec", "eval"}
        for root in (self.runtime_root, self.stub_root):
            for path in root.rglob("*.py" if root == self.runtime_root else "*.pyi"):
                source = path.read_text(encoding="utf-8")
                tree = ast.parse(source)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Name):
                        self.assertNotIn(node.id, forbidden, f"{path}: dynamic API hook {node.id}")
                    if isinstance(node, ast.Name) and node.id == "Any":
                        self.fail(f"{path}: Any weakens this stub candidate")


if __name__ == "__main__":
    unittest.main()
