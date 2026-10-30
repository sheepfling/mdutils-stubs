from mdutils import MDList, MdUtils, TextUtils
from mdutils.tools.MDList import MDCheckbox

document = MdUtils(file_name=42)
document.new_header(level="first", title=7)
document.new_table(columns=1, rows=1, text=[7], text_align=4)
document.new_list(["parent", [42]])
invalid_items: list[int] = [42]
document.new_list(invalid_items)
document.new_checkbox_list(invalid_items)
MDList(invalid_items)
MDCheckbox(invalid_items)
TextUtils.text_format(text=42)
