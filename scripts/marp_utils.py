import os
from typing import Dict, Optional


def parse_marp_file(file_path: str) -> Dict[str, str]:
    content = read_file(file_path)
    lines = content.splitlines(keepends=True)

    if not lines[0].strip() == "---":
        raise ValueError("Error: ファイルの先頭に有効なMarp設定が見つかりません。'---' で始まる設定が必要です。")

    for i, line in enumerate(lines[1:], 1):
        if line.strip() == "---":  # 設定部分の終端を検出
            return {
                "marp_settings": "".join(lines[:i+1]),  # 設定部分
                "body": "".join(lines[i+1:])  # 本文部分
            }
    raise ValueError("Error: 設定部分が閉じられていません。2つ目の '---' が必要です。")


def read_file(file_path: str) -> Optional[str]:
    """既存のslides.mdを読み取る"""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            if not content.strip():
                raise ValueError("Error: ファイルが空です。")
            return file.read()
    raise FileNotFoundError(f"Error: {os.path.basename(file_path)} が存在しません")
