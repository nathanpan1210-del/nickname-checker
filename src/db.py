import pandas as pd
import os

EXCEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'names.xlsx')

def load_data():
    """加载全部数据"""
    df = pd.read_excel(EXCEL_PATH)
    return df.to_dict('records')

def add_person(name):
    """添加人员"""
    df = pd.read_excel(EXCEL_PATH)
    new_id = int(df['ID'].max()) + 1 if not df.empty else 1
    new_row = {'ID': new_id, '姓名': name}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_excel(EXCEL_PATH, index=False)
    return new_row

def search_by_name(name):
    """按姓名搜索"""
    df = pd.read_excel(EXCEL_PATH)
    results = df[df['姓名'].str.contains(name, na=False)]
    return results.to_dict('records')

def delete_by_id(person_id):
    """按ID删除"""
    df = pd.read_excel(EXCEL_PATH)
    df = df[df['ID'] != person_id]
    df.to_excel(EXCEL_PATH, index=False)