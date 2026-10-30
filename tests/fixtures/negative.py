from mdutils import MDList, MdUtils, TextUtils
from mdutils.tools.MDList import MDCheckbox

document = MdUtils(file_name=42)
document.new_header(level="first", title=7)
document.new_table(columns=1, rows=1, text=[7], text_align=4)
document.new_list(["parent", [42]])
invalid_items: list[int] = [42]
invalid_nested_tuple: list[str | tuple[str]] = ["parent", ("child",)]
document.new_list(invalid_items)
document.new_checkbox_list(invalid_items)
MDList(invalid_items)
MDCheckbox(invalid_items)
document.new_list(invalid_nested_tuple)
document.new_checkbox_list(invalid_nested_tuple)
MDList(invalid_nested_tuple)
MDCheckbox(invalid_nested_tuple)
TextUtils.text_format(text=42)
