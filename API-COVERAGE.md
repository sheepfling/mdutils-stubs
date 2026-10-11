# API coverage and compatibility notes

This inventory is for the first candidate, based on the official
[`didix21/mdutils` v1.8.1 source tag](https://github.com/didix21/mdutils/tree/v1.8.1)
at commit `170f7d040ea598672c53015a5db4fab868dacba0`. The type declarations
describe API shape only; they do not reimplement mdutils.

## Exported modules and classes

The inventory covers 13 runtime modules and their matching `.pyi` files. The
root `mdutils` package exposes 12 names: `MdUtils`; the `Header`, `Image`,
`Link`, `Table`, and `TableOfContents` modules; the `fileutils`, `mdutils`, and
`tools` modules; and the `TextUtils`, `Html`, and `MDList` classes. The
`mdutils.fileutils` package exposes `MarkDownFile` and its `fileutils`
submodule. The `mdutils.tools` package exposes 11 names, preserving upstream's
module/class aliases (including `TextUtils` as a class).

One runtime name needs special care: `mdutils.fileutils` at the root package
attribute resolves to the inner `mdutils.fileutils.fileutils` module, while
the importable `mdutils.fileutils` package has its own `fileutils` submodule
alias. The declarations and alias tests preserve both paths.

## Declared public surface

- `mdutils.mdutils.MdUtils`: constructor, public state (`file_name`, `author`,
  `textUtils`, `title`, `table_of_contents`, `file_data_text`, `reference`, and
  `image`), and every public method: `create_md_file`, `get_md_text`,
  `read_md_file`, `new_header`, `new_table_of_contents`, `new_table`,
  `new_table_array`, `new_paragraph`, `new_line`, `write`, `insert_code`,
  `create_marker`, `place_text_using_marker`, `new_inline_link`,
  `new_reference_link`, `new_inline_image`, `new_reference_image`, `new_list`,
  and `new_checkbox_list`.
- `mdutils.fileutils.fileutils.MarkDownFile`: constructor, file metadata, write
  and append methods, and static `read_file`.
- `mdutils.tools.Header`: `Header`, `HeaderStyle`, `AtxHeaderLevel`, and
  `SetextHeaderLevel`, including all enum members and public constructors,
  formatters, and anchor helpers.
- `mdutils.tools.Html`: `Html`, `HtmlSize`, and `SizeBadFormat`, including
  paragraph/image formatting and size conversion.
- `mdutils.tools.Image`: constructor and inline/reference image methods.
- `mdutils.tools.Link`: `Inline` and `Reference`, including reference lookup,
  Markdown formatting, and link creation.
- `mdutils.tools.MDList`: `MDListHelper`, `MDList`, and `MDCheckbox`, including
  list state and Markdown output.
- `mdutils.tools.Table`: `Table`, its row/column state, and both table builders.
- `mdutils.tools.TableOfContents`: recursive heading-tree input and table of
  contents generation.
- `mdutils.tools.TextUtils`: every public static text-formatting helper.

## Deliberate gaps

- Private names beginning with `_` are not declared; protocol dunders such as
  `__init__` and `__str__` are part of the checked callable surface.
- Only mdutils 1.8.1 is in the supported dependency range. The 1.8.0 source tag
  has matching public signatures, but it is not supported until the complete
  installed-wheel consumer and runtime checks pass against that release.
- Future 1.8.x releases are not presumed compatible. Dependabot raises a bounded
  update proposal; API coverage and metadata are revised only after validation.
- No historical support for 1.6.x or 1.7.x is claimed. Those API lines differ
  from 1.8.1 and need separate evidence and release decisions.
- Python versions below 3.10 are not claimed for this stub distribution.

## Local compatibility gate

`tests/test_api_coverage.py` compares runtime and stub module inventories,
public class/function names, class bases, every public callable's parameter
names, parameter kinds, defaults, and decorators, public attributes, enum
members, initializer aliases, and package exports. Counts are pinned at 18
classes, 61 callables, 23 attributes, and 10 enum members so an API change
requires an explicit inventory review. The positive consumer fixture imports
every package-level export and type-checks the public members; the negative
fixture requires six expected type diagnostics from both mypy and Pyright.

Structural matching does not prove that each declared annotation fully models
runtime semantics. The positive/negative fixtures and runtime behavior checks
cover representative use, while strict `stubtest` checks installed stubs
against the runtime. These checks provide different evidence and none is a
formal proof of complete semantic typing. The package dependency and exact test
pin stay at 1.8.1 until the full gate supports a wider range.
