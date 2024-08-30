"""このモジュールには、「Chat with your data Solution Accelerator」の管理アプリのコードが含まれています。"""
import os
import logging
import sys
import streamlit as st
from azure.monitor.opentelemetry import configure_azure_monitor

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
logging.captureWarnings(True)
logging.basicConfig(level=os.getenv("LOGLEVEL", "INFO").upper())

# AzureのログレベルをWARNに設定しています。ログが多すぎるためです。
# https://github.com/Azure/azure-sdk-for-python/issues/9422
logging.getLogger("azure").setLevel(os.environ.get("LOGLEVEL_AZURE", "WARN").upper())

# ここではEnvHelperを使用できません。アプリケーションインサイトが最初に構成される必要があるためです。
# 計測が正しく機能するようにするためです。
if os.getenv("APPLICATIONINSIGHTS_ENABLED", "false").lower() == "true":
    configure_azure_monitor()

logger = logging.getLogger(__name__)
logger.debug("管理アプリを起動しています")

st.set_page_config(
    page_title="管理",
    page_icon=os.path.join("images", "favicon.ico"),
    layout="wide",
    menu_items=None,
)

def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 共通CSSをロード
load_css("pages/common.css")

col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.image(os.path.join("images", "logo.png"))

st.write("# Chat with your data Solution Accelerator")
st.write(
    """
    * データをインジェスト（PDF、ウェブサイトなど）したい場合は、`データインジェスト`タブを使用してください。
    * データがどのようにチャンクされているかを確認したい場合は、`データ探索`タブを確認してください。
    * 基本的なプロンプト、ログ設定などを適応させたい場合は、`設定`タブを使用してください。
    """
)
