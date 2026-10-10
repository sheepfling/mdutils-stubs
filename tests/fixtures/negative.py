from mdutils import MdUtils, TextUtils

document = MdUtils(file_name=42)
document.new_header(level="first", title=7)
document.new_table(columns=1, rows=1, text=[7], text_align=4)
TextUtils.text_format(text=42)
