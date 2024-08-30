import streamlit as st
import os
import traceback
import sys
import logging
from batch.utilities.helpers.env_helper import EnvHelper
from batch.utilities.search.search import Search
from batch.utilities.helpers.azure_blob_storage_client import AzureBlobStorageClient

# カレントディレクトリの親ディレクトリをシステムパスに追加
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# 環境ヘルパーとロガーを初期化
env_helper: EnvHelper = EnvHelper()
logger = logging.getLogger(__name__)

# Streamlitのページ設定
st.set_page_config(
    page_title="データ削除",
    page_icon=os.path.join("images", "favicon.ico"),
    layout="wide",
    menu_items=None,
)

# CSSファイルを読み込む関数
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 共通CSSを読み込む
load_css("pages/common.css")

# テーブルの行インデックスを非表示にするCSSを定義
hide_table_row_index = """
    <style>
    thead tr th:first-child {display:none}
    tbody th {display:none}
    </style>
"""
# Markdownを使用してCSSを注入
st.markdown(hide_table_row_index, unsafe_allow_html=True)

try:
    # 選択されたファイルのセッション状態を初期化
    if "selected_files" not in st.session_state:
        st.session_state.selected_files = {}

    # 検索ハンドラーを初期化し、ファイルを取得
    search_handler = Search.get_search_handler(env_helper)
    results = search_handler.get_files()

    # ファイルが見つからない場合の処理
    if results is None or results.get_count() == 0:
        st.info("削除するファイルがありません")
        st.stop()
    else:
        st.write("削除するファイルを選択してください:")

    # 検索結果を表示
    files = search_handler.output_results(results)

    # フォームを作成
    with st.form("delete_form", clear_on_submit=True):
        selections = {
            filename: st.checkbox(filename, False, key=filename)
            for filename in files.keys()
        }
        selected_files = {
            filename: ids for filename, ids in files.items() if selections[filename]
        }

        # フォームの送信ボタンが押された場合の処理
        if st.form_submit_button("削除"):
            with st.spinner("ファイルを削除中..."):
                if len(selected_files) == 0:
                    st.info("選択されたファイルがありません")
                    st.stop()
                else:
                    # ファイルを削除
                    files_to_delete = search_handler.delete_files(selected_files)
                    blob_client = AzureBlobStorageClient()
                    blob_client.delete_files(
                        selected_files,
                        env_helper.AZURE_SEARCH_USE_INTEGRATED_VECTORIZATION,
                    )

                    # 削除成功メッセージを表示
                    if len(files_to_delete) > 0:
                        st.success("削除されたファイル: " + str(files_to_delete))
                        st.rerun()

except Exception:
    logger.error(traceback.format_exc())
    st.error("ファイルの削除中にエラーが発生しました。")
