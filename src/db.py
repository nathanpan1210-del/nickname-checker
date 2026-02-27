import pandas as pd
import os

# 使用绝对路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCEL_PATH = os.path.join(BASE_DIR, 'nicknames.xlsx')

def get_nicknames():
    """获取所有花名列表"""
    if not os.path.exists(EXCEL_PATH):
        return []
    df = pd.read_excel(EXCEL_PATH)
    # 假设有nickname列，取出所有非空花名
    if 'nickname' in df.columns:
        return df['nickname'].dropna().tolist()
    elif '花名' in df.columns:
        return df['花名'].dropna().tolist()
    else:
        # 取第一列
        return df.iloc[:, 0].dropna().tolist()

def check_nickname(input_name):
    """查重逻辑
    - 完全重复: "花名重复，请重新取"
    - 2字以上相似: "花名相似，建议重取"
    - 可用: "花名可用"
    """
    input_name = input_name.strip()
    nicknames = get_nicknames()

    # 完全匹配
    if input_name in nicknames:
        return {
            "status": "duplicate",
            "message": "花名重复，请重新取",
            "input": input_name
        }

    # 模糊匹配：2字及以上重复但不完全一致
    for existing in nicknames:
        if len(input_name) >= 2 and len(existing) >= 2:
            # 检查是否有2个及以上连续或非连续字符相同
            common_chars = set(input_name) & set(existing)
            if len(common_chars) >= 2:
                return {
                    "status": "similar",
                    "message": "花名相似，建议重取",
                    "input": input_name,
                    "similar_to": existing
                }

    return {
        "status": "available",
        "message": "花名可用",
        "input": input_name
    }

def get_all():
    """获取全部花名"""
    if not os.path.exists(EXCEL_PATH):
        return []
    df = pd.read_excel(EXCEL_PATH)
    return df.to_dict('records')