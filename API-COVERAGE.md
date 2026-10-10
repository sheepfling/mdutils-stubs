# API coverage and compatibility notes

This inventory is for the first candidate, based on the official
[`didix21/mdutils` v1.8.1 source tag](https://github.com/didix21/mdutils/tree/v1.8.1)
at commit `170f7d040ea598672c53015a5db4fab868dacba0`. The type declarations
describe API shape only; they do not reimplement mdutils.

## Exported modules and classes

The root `mdutils` package exposes `MdUtils`, the `Header`, `Image`, `Link`,
`Table`, and `TableOfContents` modules, the `fileutils` module, and the
`TextUtils`, `Html`, and `MDList` classes. The `mdutils.tools` package exposes
the upstream module/class aliases, including `TextUtils` as a class. The
`mdutils.fileutils` package exposes `MarkDownFile`.

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

- Runtime-private names beginning with `_` are not declared.
- Only mdutils 1.8.1 is in the supported dependency range. The 1.8.0 source tag
  has matching public signatures, but it is not supported until the complete
  installed-wheel consumer and runtime checks pass against that release.
- Future 1.8.x releases are not presumed compatible. Dependabot raises a bounded
  update proposal; API coverage and metadata are revised only after validation.
- No historical support for 1.6.x or 1.7.x is claimed. Those API lines differ
  from 1.8.1 and need separate evidence and release decisions.
- Python versions below 3.10 are not claimed for this stub distribution.

## Local compatibility gate

The external consumer fixtures exercise the root and submodule imports,
constructors, header options, list/table inputs, alignment `None`, markers,
reference defaults, and return values. The runtime checks and `stubtest` compare
the installed declarations with mdutils 1.8.1. The package dependency and exact
test pin stay at 1.8.1 until the full gate supports a wider range.
