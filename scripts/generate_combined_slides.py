import os
import re
from marp_utils import parse_marp_file, read_file

sections_dir = "sections"
output_file = "combined/slides/slides.md"

comment_start = "<!--\n"
comment_end = "\n-->"


def parse_existing_sections(body):
    """既存スライドからセクション情報を解析"""
    sections = {}
    for match in re.finditer(r"(?<=\n---\n)(.*?)(?=\n---\n|$)", body, re.S):
        section_content = match.group(1).strip()
        section_name = re.search(r"^#\s+(.*?)$", section_content, re.M)
        if section_name:
            sections[section_name.group(1)] = section_content
    return sections


def sync_section(md_file_path, existing_sections):
    """セクションを処理し、差分確認を行う"""
    content = read_file(md_file_path)

    marp_data = parse_marp_file(content)
    body = marp_data["body"]
    section_header = re.search(r"^#\s+(.*?)$", body, re.M)
    section_name = section_header.group(
        1) if section_header else os.path.basename(md_file_path)
    if section_name in existing_sections and existing_sections[section_name].strip() == body.strip():
        return None  # 差分がない場合は何もしない
    return f"\n{body.strip()}"


def save_combined_slides(filepath, combined_content):
    """結合スライドを保存"""
    output = "".join(combined_content)
    # セクションタイトルを抜き出してプレビュー
    section_titles = [
        re.search(r"^#\s+(.*?)$", section, re.M).group(1)
        for section in combined_content if re.search(r"^#\s+(.*?)$", section, re.M)
    ]
    print("生成されたスライドのセクションタイトル:\n", section_titles)
    with open(filepath, "w", encoding="utf-8") as file:
        file.writelines(output)
    print(f"Slides successfully saved to {filepath}")


def generate_combined_slides():
    """セクションを結合して統合スライドを生成"""
    try:
        # 既存のslides.mdを読み取る
        marp_data = parse_marp_file(read_file(output_file))
        marp_settings = marp_data["marp_settings"]
        body = marp_data["body"]

        # 統合結果を保持
        combined_content = []

        combined_content.append(marp_settings)

        existing_sections = parse_existing_sections(body)

        for section in sorted(os.listdir(sections_dir)):
            section_path = os.path.join(sections_dir, section)
            if os.path.isdir(section_path):
                md_file_path = os.path.join(section_path, f"{section}.md")
                if os.path.exists(md_file_path):
                    try:
                        section_content = sync_section(
                            md_file_path, existing_sections)
                        if section_content:
                            combined_content.append(section_content)
                    except ValueError as e:
                        print(f"Error: セクション '{section}' ({
                              md_file_path}) の処理中にエラーが発生しました: {e}")
                        raise

        # 統合されたスライドを保存
        save_combined_slides(output_file, combined_content)
        print(f"統合スライドを生成しました: {output_file}")
    except Exception as e:
        print(f"重大なエラーが発生しました: {e}")


if __name__ == "__main__":
    generate_combined_slides()
