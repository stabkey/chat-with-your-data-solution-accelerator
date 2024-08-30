import os
import sys
import traceback
import json
import jsonschema
import streamlit as st
from batch.utilities.helpers.env_helper import EnvHelper
from batch.utilities.helpers.config.config_helper import ConfigHelper
from azure.core.exceptions import ResourceNotFoundError
from batch.utilities.helpers.config.assistant_strategy import AssistantStrategy

# カレントディレクトリの親ディレクトリをシステムパスに追加
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# 環境ヘルパーを初期化
env_helper: EnvHelper = EnvHelper()

# Streamlitのページ設定
st.set_page_config(
    page_title="プロンプト設定",
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

# 設定を取得
config = ConfigHelper.get_active_config_or_default()

# 設定値をセッションステートに初期化
if "answering_system_prompt" not in st.session_state:
    st.session_state["answering_system_prompt"] = config.prompts.answering_system_prompt
if "answering_user_prompt" not in st.session_state:
    st.session_state["answering_user_prompt"] = config.prompts.answering_user_prompt
if "use_on_your_data_format" not in st.session_state:
    st.session_state["use_on_your_data_format"] = config.prompts.use_on_your_data_format
if "post_answering_prompt" not in st.session_state:
    st.session_state["post_answering_prompt"] = config.prompts.post_answering_prompt
if "enable_post_answering_prompt" not in st.session_state:
    st.session_state["enable_post_answering_prompt"] = config.prompts.enable_post_answering_prompt
if "post_answering_filter_message" not in st.session_state:
    st.session_state["post_answering_filter_message"] = config.messages.post_answering_filter
if "enable_content_safety" not in st.session_state:
    st.session_state["enable_content_safety"] = config.prompts.enable_content_safety
if "example_documents" not in st.session_state:
    st.session_state["example_documents"] = config.example.documents
if "example_user_question" not in st.session_state:
    st.session_state["example_user_question"] = config.example.user_question
if "example_answer" not in st.session_state:
    st.session_state["example_answer"] = config.example.answer
if "log_user_interactions" not in st.session_state:
    st.session_state["log_user_interactions"] = config.logging.log_user_interactions
if "log_tokens" not in st.session_state:
    st.session_state["log_tokens"] = config.logging.log_tokens
if "orchestrator_strategy" not in st.session_state:
    st.session_state["orchestrator_strategy"] = config.orchestrator.strategy.value
if "ai_assistant_type" not in st.session_state:
    st.session_state["ai_assistant_type"] = config.prompts.ai_assistant_type

# Azure Searchの統合ベクトル化が有効な場合の設定
if env_helper.AZURE_SEARCH_USE_INTEGRATED_VECTORIZATION:
    if "max_page_length" not in st.session_state:
        st.session_state["max_page_length"] = config.integrated_vectorization_config.max_page_length
    if "page_overlap_length" not in st.session_state:
        st.session_state["page_overlap_length"] = config.integrated_vectorization_config.page_overlap_length

# ユーザープロンプトのバリデーション関数
def validate_answering_user_prompt():
    if "{sources}" not in st.session_state.answering_user_prompt:
        st.warning("ユーザープロンプトに `{sources}` 変数が含まれていません")
    if "{question}" not in st.session_state.answering_user_prompt:
        st.warning("ユーザープロンプトに `{question}` 変数が含まれていません")

# アシスタントのプロンプトを設定する関数
def config_contract_assistant_prompt():
    if st.session_state["ai_assistant_type"] == AssistantStrategy.CONTRACT_ASSISTANT.value:
        st.success("契約アシスタントのプロンプト")
        st.session_state["answering_user_prompt"] = ConfigHelper.get_default_contract_assistant()
    else:
        st.success("デフォルトアシスタントのプロンプト")
        st.session_state["answering_user_prompt"] = ConfigHelper.get_default_assistant_prompt()

# ポストアンサープロンプトのバリデーション関数
def validate_post_answering_prompt():
    if "post_answering_prompt" not in st.session_state or len(st.session_state.post_answering_prompt) == 0:
        pass
    if "{sources}" not in st.session_state.post_answering_prompt:
        st.warning("ポストアンサープロンプトに `{sources}` 変数が含まれていません")
    if "{question}" not in st.session_state.post_answering_prompt:
        st.warning("ポストアンサープロンプトに `{question}` 変数が含まれていません")
    if "{answer}" not in st.session_state.post_answering_prompt:
        st.warning("ポストアンサープロンプトに `{answer}` 変数が含まれていません")

# ドキュメントのバリデーション関数
def validate_documents():
    documents_schema = {
        "type": "object",
        "required": ["retrieved_documents"],
        "additionalProperties": False,
        "properties": {
            "retrieved_documents": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "patternProperties": {
                        r"^\[doc\d+\]$": {
                            "type": "object",
                            "required": ["content"],
                            "additionalProperties": False,
                            "properties": {"content": {"type": "string"}},
                        }
                    },
                },
            }
        },
    }
    documents_string = st.session_state.example_documents
    if not documents_string:
        return
    try:
        documents = json.loads(documents_string)
    except json.JSONDecodeError:
        st.warning("ドキュメント: 無効なJSONオブジェクト")
        return
    try:
        jsonschema.validate(documents, documents_schema)
    except jsonschema.ValidationError as e:
        st.warning(f"ドキュメント: {e.message}")

try:
    # オーケストレータ設定のエクスパンダー
    with st.expander("オーケストレータ設定", expanded=True):
        cols = st.columns([2, 4])
        with cols[0]:
            st.selectbox(
                "オーケストレータ戦略",
                key="orchestrator_strategy",
                options=config.get_available_orchestration_strategies(),
            )

    # アシスタントタイプ設定のエクスパンダー
    with st.expander("アシスタントタイプ設定", expanded=True):
        cols = st.columns([2, 4])
        with cols[0]:
            st.selectbox(
                "アシスタントタイプ",
                key="ai_assistant_type",
                on_change=config_contract_assistant_prompt,
                options=config.get_available_ai_assistant_types(),
                help="デフォルトユーザープロンプトまたは契約アシスタントユーザープロンプトを使用するかどうかを選択します。詳細は契約アシスタンスREADMEを参照してください。",
            )

    # プロンプト設定のエクスパンダー
    with st.expander("プロンプト設定", expanded=True):
        st.checkbox(
            "Azure OpenAI On Your Dataプロンプト形式を使用",
            key="use_on_your_data_format",
            help="Azure OpenAI On Your Dataと同様のプロンプト形式を使用するかどうかを選択します。これには、システムおよびユーザーのメッセージと数ショットの例が含まれます。",
        )
        st.text_area(
            "ユーザープロンプト",
            key="answering_user_prompt",
            on_change=validate_answering_user_prompt,
            help="ナレッジベースから取得したソースを使用してユーザーの質問に答えるためのユーザープロンプト。Azure OpenAI On Your Dataプロンプト形式を使用する場合は、シンプルに保つことをお勧めします。",
            height=400,
        )
        st.text_area(
            "システムプロンプト",
            key="answering_system_prompt",
            help="ユーザーの質問に答えるためのシステムプロンプト。Azure OpenAI On Your Dataプロンプト形式が有効な場合にのみ使用されます。",
            height=400,
            disabled=not st.session_state["use_on_your_data_format"],
        )
        st.text_area(
            "ポストアンサープロンプト",
            key="post_answering_prompt",
            on_change=validate_post_answering_prompt,
            help="ソース、質問、および回答をもとに事実確認や回答処理を行うためのポストプロンプトを設定できます。このプロンプトは `True` または `False` を返す必要があります。",
            height=200,
        )
        st.checkbox("ポストアンサープロンプトを有効にする", key="enable_post_answering_prompt")
        st.text_area(
            "ポストアンサーのフィルターメッセージ",
            key="post_answering_filter_message",
            help="ポストアンサープロンプトが返されたときにユーザーに返されるメッセージ。",
            height=200,
        )
        st.checkbox("Azure AI Content Safetyを有効にする", key="enable_content_safety")

    # フューショット例設定のエクスパンダー
    with st.expander("フューショット例", expanded=True):
        st.write(
            "以下は、アンサープロンプトで使用するフューショット例を設定するために使用できます。Azure OpenAI On Your Dataプロンプト形式が有効な場合にのみ使用されます。\n"
            "この設定はオプションですが、有効にするには3つのオプションすべてを提供する必要があります。"
        )
        st.text_area(
            "ドキュメント",
            key="example_documents",
            help="ナレッジベースから取得したドキュメントを含むJSONオブジェクト。",
            on_change=validate_documents,
            height=200,
            disabled=not st.session_state["use_on_your_data_format"],
        )
        st.text_area(
            "ユーザーの質問",
            key="example_user_question",
            help="例としてのユーザーの質問。",
            disabled=not st.session_state["use_on_your_data_format"],
        )
        st.text_area(
            "ユーザーの回答",
            key="example_answer",
            help="期待される回答。",
            disabled=not st.session_state["use_on_your_data_format"],
        )

    # ドキュメントプロセッサの設定
    document_processors = list(
        map(
            lambda x: {
                "document_type": x.document_type,
                "chunking_strategy": x.chunking.chunking_strategy.value if x.chunking else None,
                "chunking_size": x.chunking.chunk_size if x.chunking else None,
                "chunking_overlap": x.chunking.chunk_overlap if x.chunking else None,
                "loading_strategy": x.loading.loading_strategy.value if x.loading else None,
                "use_advanced_image_processing": x.use_advanced_image_processing,
            },
            config.document_processors,
        )
    )

    # 統合ベクトル化の設定
    if env_helper.AZURE_SEARCH_USE_INTEGRATED_VECTORIZATION:
        with st.expander("統合ベクトル化設定", expanded=True):
            st.text_input("最大ページ長", key="max_page_length")
            st.text_input("ページ重なり長", key="page_overlap_length")
            integrated_vectorization_config = {
                "max_page_length": st.session_state["max_page_length"],
                "page_overlap_length": st.session_state["page_overlap_length"],
            }
    else:
        with st.expander("ドキュメント処理設定", expanded=True):
            edited_document_processors = st.data_editor(
                data=document_processors,
                use_container_width=True,
                num_rows="dynamic",
                column_config={
                    "document_type": st.column_config.SelectboxColumn(
                        options=config.get_available_document_types()
                    ),
                    "chunking_strategy": st.column_config.SelectboxColumn(
                        options=[cs for cs in config.get_available_chunking_strategies()]
                    ),
                    "loading_strategy": st.column_config.SelectboxColumn(
                        options=[ls for ls in config.get_available_loading_strategies()]
                    ),
                },
            )

    # ロギング設定のエクスパンダー
    with st.expander("ロギング設定", expanded=True):
        st.checkbox(
            "ユーザーの入力と出力（質問、回答、チャット履歴、ソース）をログに記録",
            key="log_user_interactions",
        )
        st.checkbox("トークンをログに記録", key="log_tokens")

    # 設定を保存するボタン
    if st.button("設定を保存"):
        document_processors = (
            list(
                map(
                    lambda x: {
                        "document_type": x["document_type"],
                        "chunking": {
                            "strategy": x["chunking_strategy"],
                            "size": x["chunking_size"],
                            "overlap": x["chunking_overlap"],
                        },
                        "loading": {
                            "strategy": x["loading_strategy"],
                        },
                        "use_advanced_image_processing": x["use_advanced_image_processing"],
                    },
                    edited_document_processors,
                )
            )
            if env_helper.AZURE_SEARCH_USE_INTEGRATED_VECTORIZATION is False
            else []
        )
        current_config = {
            "prompts": {
                "condense_question_prompt": "",  # st.session_state['condense_question_prompt'],
                "answering_system_prompt": st.session_state["answering_system_prompt"],
                "answering_user_prompt": st.session_state["answering_user_prompt"],
                "use_on_your_data_format": st.session_state["use_on_your_data_format"],
                "post_answering_prompt": st.session_state["post_answering_prompt"],
                "enable_post_answering_prompt": st.session_state["enable_post_answering_prompt"],
                "enable_content_safety": st.session_state["enable_content_safety"],
                "ai_assistant_type": st.session_state["ai_assistant_type"],
            },
            "messages": {
                "post_answering_filter": st.session_state["post_answering_filter_message"]
            },
            "example": {
                "documents": st.session_state["example_documents"],
                "user_question": st.session_state["example_user_question"],
                "answer": st.session_state["example_answer"],
            },
            "document_processors": document_processors,
            "logging": {
                "log_user_interactions": st.session_state["log_user_interactions"],
                "log_tokens": st.session_state["log_tokens"],
            },
            "orchestrator": {"strategy": st.session_state["orchestrator_strategy"]},
            "integrated_vectorization_config": (
                integrated_vectorization_config
                if env_helper.AZURE_SEARCH_USE_INTEGRATED_VECTORIZATION
                else None
            ),
        }
        ConfigHelper.save_config_as_active(current_config)
        st.success(
            "設定が正常に保存されました！これらの変更を有効にするには、チャットサービスを再起動してください。"
        )

    # 設定をデフォルトにリセットするポップオーバー
    with st.popover(":red[設定をデフォルトにリセット]"):
        # カスタムクラスを持つ閉じるボタン
        if st.button("X", key="close_popup", help="ポップアップを閉じる"):
            st.session_state["popup_open"] = False
            st.rerun()
        st.write("**設定のリセットは元に戻せません。注意して進めてください！**")
        st.text_input('進めるには "reset" と入力してください', key="reset_configuration")
        if st.button(":red[リセット]", disabled=st.session_state["reset_configuration"] != "reset"):
            try:
                ConfigHelper.delete_config()
            except ResourceNotFoundError:
                pass
            for key in st.session_state:
                del st.session_state[key]
            st.session_state["reset"] = True
            st.session_state["reset_configuration"] = ""
            st.rerun()
        if st.session_state.get("reset") is True:
            st.success("設定が正常にリセットされました！")
            del st.session_state["reset"]
            del st.session_state["reset_configuration"]

except Exception:
    st.error(traceback.format_exc())
