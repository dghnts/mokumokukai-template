import re
import os

combined_file_path = "combined/slides/slides.md"
sections_dir = "sections"


def uncomment_marp_settings(file_path):
    '''
    Marp設定部分をコメントアウト解除する

    Args:
        file_path (str): Markdownファイルのパス
    '''

    # 与えられたパスが存在する確認する
    if not os.path.exists(file_path):
        print(f"{os.path.basename(file_path)}が存在しません")
        return

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    uncommented_content = re.sub(
        r"<!--\n(.*?)-->", r"\1", content, flags=re.DOTALL)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(uncommented_content)

    print(f"{os.path.basename(file_path)}のMarp設定のコメントアウトを解除しました")


if __name__ == "__main__":
    # 統合スライドの設定をコメントアウト
    uncomment_marp_settings(combined_file_path)
    # sectionsディレクトリ内のmdファイルの削除
    for section in sorted(os.listdir(sections_dir)):
        section_path = os.path.join(sections_dir, section)
        if os.path.isdir(section_path):
            md_file_path = os.path.join(section_path, f"{section}.md")
            if os.path.exists(md_file_path):
                uncomment_marp_settings(md_file_path)
