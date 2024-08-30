from os import path
import streamlit as st
import traceback
import requests
import urllib.parse
import sys
import logging
from batch.utilities.helpers.config.config_helper import ConfigHelper
from batch.utilities.helpers.env_helper import EnvHelper
from batch.utilities.helpers.azure_blob_storage_client import AzureBlobStorageClient

sys.path.append(path.join(path.dirname(__file__), ".."))
env_helper: EnvHelper = EnvHelper()
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="データインジェスト",
    page_icon=path.join("images", "favicon.ico"),
    layout="wide",
    menu_items=None,
)

def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 共通CSSをロード
load_css("pages/common.css")

def reprocess_all():
    backend_url = urllib.parse.urljoin(
        env_helper.BACKEND_URL, "/api/BatchStartProcessing"
    )
    params = {}
    if env_helper.FUNCTION_KEY is not None:
        params["code"] = env_helper.FUNCTION_KEY
        params["clientId"] = "clientKey"

    try:
        response = requests.post(backend_url, params=params)
        if response.status_code == 200:
            st.success(
                f"{response.text}\nこれは非同期プロセスであり、完了するまでに数分かかる場合があります。"
            )
        else:
            st.error(f"エラー: {response.text}")
    except Exception:
        st.error(traceback.format_exc())

def add_urls():
    urls = st.session_state["urls"].split("\n")
    add_url_embeddings(urls)

def add_url_embeddings(urls: list[str]):
    params = {}
    if env_helper.FUNCTION_KEY is not None:
        params["code"] = env_helper.FUNCTION_KEY
        params["clientId"] = "clientKey"
    for url in urls:
        body = {"url": url}
        backend_url = urllib.parse.urljoin(
            env_helper.BACKEND_URL, "/api/AddURLEmbeddings"
        )
        r = requests.post(url=backend_url, params=params, json=body)
        if not r.ok:
            raise ValueError(f"エラー {r.status_code}: {r.text}")
        else:
            st.success(f"{url} の埋め込みが正常に追加されました")

try:
    with st.expander("バッチでドキュメントを追加", expanded=True):
        config = ConfigHelper.get_active_config_or_default()
        file_type = [
            processor.document_type for processor in config.document_processors
        ]
        uploaded_files = st.file_uploader(
            "ドキュメントをアップロードしてAzure Storage Accountに追加し、埋め込みを計算してAzure AI Searchインデックスに追加します。利用可能なドキュメントプロセッサの構成を確認してください。",
            type=file_type,
            accept_multiple_files=True,
        )
        blob_client = AzureBlobStorageClient()
        if uploaded_files is not None:
            for up in uploaded_files:
                # ファイルをバイトとして読み取る
                bytes_data = up.getvalue()
                if st.session_state.get("filename", "") != up.name:
                    # 新しいファイルをアップロード
                    st.session_state["filename"] = up.name
                    st.session_state["file_url"] = blob_client.upload_file(
                        bytes_data, up.name, metadata={"title": up.name}
                    )
            if len(uploaded_files) > 0:
                st.success(
                    f"{len(uploaded_files)} 件のドキュメントがアップロードされました。埋め込み計算が進行中です。\nこれは非同期プロセスであり、完了するまでに数分かかる場合があります。\n詳細については、Azure Functionのログを確認してください。"
                )
        col1, col2, col3 = st.columns([2, 1, 2])
        with col3:
            st.button(
                "Azure Storageアカウント内のすべてのドキュメントを再処理",
                on_click=reprocess_all,
            )
    with st.expander("ナレッジベースにURLを追加", expanded=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.text_area(
                "URLを追加してから「埋め込みを計算」をクリックしてください",
                placeholder="URLをここに改行で区切って入力してください",
                height=100,
                key="urls",
            )
        with col2:
            st.selectbox(
                "埋め込みモデル",
                [env_helper.AZURE_OPENAI_EMBEDDING_MODEL],
                disabled=True,
            )
            st.button(
                "ウェブページを処理してインジェスト",
                on_click=add_urls,
                key="add_url",
            )
except Exception:
    st.error(traceback.format_exc())
