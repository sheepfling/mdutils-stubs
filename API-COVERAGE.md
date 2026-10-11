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

## Per-class coverage ledger

The member names below are compared one class at a time against the installed
1.8.1 runtime. `__init__` and `__str__` are included in callable counts.
Public state lists class annotations and instance attributes assigned by the
runtime constructor; enum rows list members instead of state.

- `mdutils.fileutils.fileutils.MarkDownFile`
  - Callables: `__init__`, `append_after_second_line`, `append_end`, `read_file`,
    `rewrite_all_file`.
  - State: `dirname`, `file`, `file_name`.
- `mdutils.mdutils.MdUtils`
  - Callables: `__init__`, `create_md_file`, `create_marker`, `get_md_text`,
    `insert_code`, `new_checkbox_list`, `new_header`, `new_inline_image`,
    `new_inline_link`, `new_line`, `new_list`, `new_paragraph`,
    `new_reference_image`, `new_reference_link`, `new_table`,
    `new_table_array`, `new_table_of_contents`, `place_text_using_marker`,
    `read_md_file`, `write`.
  - State: `author`, `file_data_text`, `file_name`, `image`, `reference`,
    `table_of_contents`, `textUtils`, `title`.
- `mdutils.tools.Header.Header`
  - Callables: `__init__`, `__str__`, `atx`, `choose_header`, `header_anchor`,
    `setext`.
  - State: `header_id`, `level`, `style`, `title`.
- `mdutils.tools.Header.HeaderStyle`
  - Enum members: `ATX`, `SETEXT`.
- `mdutils.tools.Header.AtxHeaderLevel`
  - Enum members: `TITLE`, `HEADING`, `SUBHEADING`, `SUBSUBHEADING`,
    `MINORHEADING`, `LEASTHEADING`.
- `mdutils.tools.Header.SetextHeaderLevel`
  - Enum members: `TITLE`, `HEADING`.
- `mdutils.tools.Html.Html`
  - Callables: `image`, `paragraph`.
- `mdutils.tools.Html.HtmlSize`
  - Callables: `size_to_width_and_height`.
- `mdutils.tools.Html.SizeBadFormat`
  - Callables: `__init__`.
- `mdutils.tools.Image.Image`
  - Callables: `__init__`, `new_inline_image`, `new_reference_image`.
  - State: `reference`.
- `mdutils.tools.Link.Inline`
  - Callables: `new_link`.
- `mdutils.tools.Link.Reference`
  - Callables: `__init__`, `get_references`, `get_references_as_markdown`,
    `new_link`.
  - State: `references`.
- `mdutils.tools.MDList.MDListHelper`
  - Callables: `__init__`.
  - State: `n_tabs`.
- `mdutils.tools.MDList.MDList`
  - Callables: `__init__`, `get_md`.
  - State: `md_list`.
- `mdutils.tools.MDList.MDCheckbox`
  - Callables: `__init__`, `get_md`.
  - State: `checked`, `md_list`.
- `mdutils.tools.Table.Table`
  - Callables: `__init__`, `create_table`, `create_table_array`.
  - State: `columns`, `rows`.
- `mdutils.tools.TableOfContents.TableOfContents`
  - Callables: `create_table_of_contents`.
- `mdutils.tools.TextUtils.TextUtils`
  - Callables: `add_tooltip`, `bold`, `center_text`, `inline_code`,
    `insert_code`, `italics`, `text_color`, `text_external_link`, `text_format`.

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
names, kinds, defaults, and decorators, public attributes, enum members,
initializer aliases, and package exports. It also requires annotations on every
public stub callable, rejects `Any` even through a `typing` alias, and matches
positive-fixture calls to their declaring classes. Counts are pinned at 18
classes, 61 callables, 23 attributes, and 10 enum members so an API change
requires an explicit inventory review. The positive fixture imports every
package-level export and type-checks every public callable; the negative
fixture requires seven expected type diagnostics from both mypy and Pyright,
including rejection of a non-string leaf nested in a list.

Nested list and table-of-contents inputs are checked as recursive structures,
including runtime output for nested lists, checkboxes, and a depth-2 TOC.
Structural matching does not prove that each declared annotation fully models
runtime semantics. The fixtures and runtime checks cover selected behavior,
while strict `stubtest` compares installed stubs against the runtime. These
checks provide different evidence and none is a formal proof of complete
semantic typing. The package dependency and exact test pin stay at 1.8.1 until
the full gate supports a wider range.
