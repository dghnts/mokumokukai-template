import os
from marp_utils import parse_marp_file, read_file

combined_file_path = "combined/slides/slides.md"
sections_dir = "sections"


def comment_out_marp_settings(file_path, input_file):
    lines = input_file.splitlines(keepends=True)
    if lines[0].strip() == "<!--":
        print(f"{os.path.basename(file_path)}：既に設定はコメントアウトされています")
        return
    else:
        print("まだコメントアウトされていません")

    marp_data = parse_marp_file(input_file)
    marp_settings = marp_data["marp_settings"]
    body = marp_data["body"]

    # Marp設定部分をコメントアウト
    content = "<!--\n" + marp_settings + "-->\n" + body

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(content)
    print(f"{os.path.basename(file_path)}のmarp設定をコメントアウトしました")


if __name__ == "__main__":
    # 統合スライドの設定をコメントアウト
    comment_out_marp_settings(
        combined_file_path, read_file(combined_file_path))
    # sectionsディレクトリ内のmdファイルの削除
    for section in sorted(os.listdir(sections_dir)):
        section_path = os.path.join(sections_dir, section)
        if os.path.isdir(section_path):
            md_file_path = os.path.join(section_path, f"{section}.md")
            if os.path.exists(md_file_path):
                comment_out_marp_settings(
                    md_file_path, read_file(md_file_path))
