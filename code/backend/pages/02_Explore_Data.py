import streamlit as st
import os
import traceback
import sys
import pandas as pd
from batch.utilities.helpers.env_helper import EnvHelper
from batch.utilities.search.search import Search

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

env_helper: EnvHelper = EnvHelper()

st.set_page_config(
    page_title="データの探索",
    page_icon=os.path.join("images", "favicon.ico"),
    layout="wide",
    menu_items=None,
)

# CSSを文字列として注入
hide_table_row_index = """
    <style>
    thead tr th:first-child {display:none}
    tbody th {display:none}
    </style>
"""

# マークダウンでCSSを注入
st.markdown(hide_table_row_index, unsafe_allow_html=True)

def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 共通CSSを読み込む
load_css("pages/common.css")

try:
    search_handler = Search.get_search_handler(env_helper)
    results = search_handler.search_with_facets("*", "title", facet_count=0)
    unique_files = search_handler.get_unique_files(results, "title")
    filename = st.selectbox("ファイルを選択してください:", unique_files)
    st.write("表示するチャンク:", filename)

    results = search_handler.perform_search(filename)
    data = search_handler.process_results(results)
    df = pd.DataFrame(data, columns=("チャンク", "内容")).sort_values(by=["チャンク"])
    st.table(df)

except Exception:
    st.error(traceback.format_exc())
