[Back to *Chat with your data* README](../README.md)

# Local setup

**macOS 開発者向けの注意事項**：Apple Silicon（ARM64）で macOS を使用している場合、DevContainer は**動作しません**。これは Azure Functions Core Tools の制限によるものです（詳しくは [こちら](https://github.com/Azure/azure-functions-core-tools/issues/3112) を参照）。ローカルでアクセラレータを実行するには、[Non DevContainer Setup](./NON_DEVCONTAINER_SETUP.md) の手順を使用することを推奨します。
このアクセラレータを実行する最も簡単な方法は、VS Code Dev Containers を使用することです。この方法では、[Dev Containers 拡張機能](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) を使用して、ローカルの VS Code でプロジェクトを開きます。

1. Docker Desktop を起動します（インストールされていない場合はインストールしてください）。
1. プロジェクトを開きます：
    [![Open in Dev Containers](https://img.shields.io/static/v1?style=for-the-badge&label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/azure-samples/chat-with-your-data-solution-accelerator)
1. 開いた VS Code ウィンドウで、プロジェクトファイルが表示されるまで待ちます（数分かかることがあります）。表示されたらターミナルウィンドウを開きます。
1. `azd auth login` を実行します。
1. `azd env set AZURE_APP_SERVICE_HOSTING_MODEL code` を実行します - これは、環境を公開コンテナに頼らずにコードをデプロイする設定にします（"Deploy to Azure" ボタンのように）。
1. `azd up` を実行します - これにより、Azure リソースがプロビジョニングされ、そのリソースにアクセラレータがデプロイされます。

    * **重要**: このコマンドで作成されるリソースは即座に費用が発生することに注意してください。特に AI Search リソースからの費用が主な原因です。コマンドを完全に実行し終える前に中断した場合でも、これらのリソースは費用が発生する可能性があります。不要な支出を避けるために `azd down` を実行するか、手動でリソースを削除してください。
    * サブスクリプションとロケーションを選択するように求められます。そのロケーションリストは [OpenAI モデルの利用可能性テーブル](https://learn.microsoft.com/azure/cognitive-services/openai/concepts/models#model-summary-table-and-region-availability) に基づいており、利用可能な地域が変わると更新される場合があります。
    * 間違ったロケーションを選んでしまった場合は、`azd down` を実行するか、リソースグループを削除して、デプロイメントがこのリソースグループのロケーションに基づいていることを確認してください。
1. アプリケーションが正常にデプロイされた後、コンソールに URL が表示されます。その URL をクリックして、ブラウザでアプリケーションと対話します。

> **注意**: アプリケーションが完全にデプロイされるまでに最大で1時間かかる場合があります。"Python Developer" のウェルカム画面やエラーページが表示された場合は、少し待ってページをリフレッシュしてください。
> **注意**: デフォルトの認証タイプは Azure Keyvault に保存されているキーを使用します。RBAC ベースの認証（よりセキュア）を使用したい場合は、デプロイする前に次のコマンドを実行してください：

```bash
azd env set AZURE_AUTH_TYPE rbac
azd env set USE_KEY_VAULT false
```

また、[RBAC 認証のセットアップ](#authenticate-using-rbac) セクションも参照してください。

## Detailed Development Container setup instructions

このソリューションには、アクセラレータを開発およびデプロイするために必要なツールがすべて含まれた [開発コンテナ](https://code.visualstudio.com/docs/remote/containers) が含まれています。提供された開発コンテナを使用して Chat With Your Data アクセラレータをデプロイするには、以下も必要です：

* [Visual Studio Code](https://code.visualstudio.com)
* [Visual Studio Code 用リモートコンテナ拡張機能](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

Windows でこれを実行する場合は、このリポジトリを [WSL](https://code.visualstudio.com/docs/remote/wsl) にクローンすることをお勧めします。

```cmd
git clone https://github.com/Azure-Samples/chat-with-your-data-solution-accelerator
```

クローンしたリポジトリを Visual Studio Code で開き、開発コンテナに接続します。

```cmd
code .
```

!!! tip
    Visual Studio Code は利用可能な開発コンテナを認識し、それを使用してフォルダーを開くように求めてくるはずです。リモートコンテナへの接続に関する詳細は、[既存のフォルダーをコンテナで開く](https://code.visualstudio.com/docs/remote/containers#_quick-start-open-an-existing-folder-in-a-container)クイックスタートを参照してください。

開発コンテナを初めて起動するとき、コンテナがビルドされます。通常、これには数分かかります。**すべての次のステップについては、開発コンテナを使用してください。**

開発コンテナ用のファイルは `/.devcontainer/` フォルダーにあります。

## Local debugging

アクセラレータをカスタマイズしたりローカルで実行するには、ターミナルで `azd provision` を実行して Azure リソースをプロビジョニングする必要があります。これにより `.env` ファイルが生成され、「実行とデバッグ」（Ctrl + Shift + D）コマンドを使用してアクセラレータのどの部分を実行するか選択できます。以下に[環境変数の値の表](#environment-variables)があります。

ソリューションが RBAC で保護されている場合にアクセラレータをローカルで実行するには、プリンシパル ID にいくつかのロールを割り当てる必要があります。これを手動またはプログラムで行うことができます。

### Manually assign roles

以下のロールを `PRINCIPALID` に割り当てる必要があります（'principal id' は Microsoft Entra ID から取得できます）：

| Role | GUID |
|----|----|
|  Cognitive Services OpenAI Contributor | a001fd3d-188f-4b5d-821b-7da978bf7442 |
| Search Service Contributor | 7ca78c08-252a-4471-8644-bb5ff32d4ba0 |
| Search Index Data Contributor | 8ebe5a00-799e-43f5-93ac-243d3dce84a7 |
| Storage Blob Data Reader | 2a2b9908-6ea1-4ae2-8e65-a410df84e7d1 |
| Reader | acdd72a7-3385-48ef-bd42-f606fba81ae7 |

### Programatically assign roles

`main.bicep` ファイル内の `principalId` 値を自分の principalId に更新することもできます。

### Authenticate using RBAC

API キーを使用して認証するには、`AZURE_AUTH_TYPE` の値を keys に更新します。`rbac` を使用してアクセスするには、以下の手順に従って手動で変更を行います：

1. [このページ](https://techcommunity.microsoft.com/t5/ai-azure-ai-services-blog/eliminate-dependency-on-key-based-authentication-in-azure/ba-p/3821880)に記載されているロールの割り当てが作成されていることを確認します。
2. Azure ポータルで検索サービスに移動します。
3. 設定の下で、`キー` を選択します。
4. `ロールベースのアクセス制御` または `両方` を選択します。
5. Azure ポータルで App サービスに移動します。
6. 設定の下で、`構成` を選択します。
7. `AZURE_AUTH_TYPE` 設定の値を `rbac` に設定します。
8. アプリケーションを再起動します。

### Deploy services manually

以下のコマンドを使用して、ローカルから完全なソリューションをデプロイできます：`azd deploy`。また、個別にサービスをデプロイすることもできます。

| Service               | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| `azd deploy web`      | データの上でチャットできる Python アプリケーション。                             |
| `azd deploy adminweb` | データのアップロードと探索ができる "admin" サイトのための Streamlit アプリケーション。 |
| `azd deploy function` | リクエストを処理する Python 関数アプリケーション。                               |

### Running All Services Locally Using Docker Compose

Docker Compose を使用してすべてのアプリケーションを実行するには、まずプロビジョニングされたリソースの設定を含む `.env` ファイルが必要です。このファイルはプロジェクトのルートに手動で作成することができます。あるいは、リソースが `azd provision` または `azd up` を使用してプロビジョニングされた場合、`.env` ファイルは自動的に `.azure/<env-name>/.env` ファイルに生成されます。`<env-name>` を取得するには、`azd env list` を実行してどの環境がデフォルトか確認します。

`AzureWebJobsStorage` を `.env` ファイルに手動で追加する必要があります。これは Azure ポータルから関数の設定で取得できます。

サービスを開始するには、以下のいずれかのコマンドを使用します：

- `make docker-compose-up`
- `cd docker && AZD_ENV_FILE=<path-to-env-file> docker-compose up`

**注意:** デフォルトでは、これらのコマンドはメインブランチからビルドされた最新の Docker イメージを実行します。別のイメージを使用したい場合は、`docker/docker-compose.yml` ファイルを適宜変更する必要があります。

### Develop & run the frontend locally

より迅速な開発のために、フロントエンドの Typescript React UI アプリと Python Flask API アプリを開発モードで実行することができます。これにより、アプリは「ホットリロード」され、変更が自動的にアプリに反映されるため、ローカルサーバーをリフレッシュまたは再起動する必要がありません。

これらは VS Code からローカルで起動することができます (Ctrl+Shift+D を押して)、「Launch Frontend (api)」および「Launch Frontend (UI)」を選択します。コード内にブレークポイントを配置することも可能です。これにより、Node と Python の依存関係が自動的にインストールされます。

#### Starting the Flask app in dev mode from the command line (optional)

この手順は、VSCode の Launch 構成を使用できない場合に含まれます。ターミナルを開き、以下のコマンドを入力します：

```shell
cd code
poetry run flask run
```

#### Starting the Typescript React app in dev mode (optional)

この手順は、VSCode の Launch 構成を使用できない場合に含まれます。新しいターミナルをそれぞれ開き、以下のコマンドを入力します：

```shell
cd code\frontend
npm install
npm run dev
```

ローカルの Vite サーバーは、チャットインターフェースにローカルでアクセスするための URL を返します。たとえば、`http://localhost:5174/` のようになります。

### Develop & run the admin app

管理アプリは VSCode からローカルで起動することができます (Ctrl+Shift+D を押して)、「Launch Admin site」を選択します。必要に応じて、Python コードにブレークポイントを配置することも可能です。

これにより、自動的に `http://localhost:8501/` が開き、管理インターフェースが表示されるはずです。

### Develop & run the batch processing functions

バッチ処理機能のコンテナをローカルで開発および実行したい場合は、以下のコマンドを使用してください。

#### Running the batch processing locally

First, install [Azure Functions Core Tools](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Cportal%2Cv2%2Cbash&pivots=programming-language-python).

```shell
cd code\backend\batch
poetry run func start
```

Or use the [Azure Functions VS Code extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions).

#### Debugging the batch processing functions locally
Rename the file `local.settings.json.sample` in the `batch` folder to `local.settings.json` and update the `AzureWebJobsStorage` value with the storage account connection string.

Copy the .env file from [previous section](#local-debugging) to the `batch` folder.

Execute the above [shell command](#L81) to run the function locally. You may need to stop the deployed function on the portal so that all requests are debugged locally. To trigger the function, you can click on the corresponding URL that will be printed to the terminal.

## Environment variables

| App Setting | Value | Note |
| --- | --- | ------------- |
|AZURE_SEARCH_SERVICE||The URL of your Azure AI Search resource. e.g. https://<search-service>.search.windows.net|
|AZURE_SEARCH_INDEX||The name of your Azure AI Search Index|
|AZURE_SEARCH_KEY||An **admin key** for your Azure AI Search resource|
|AZURE_SEARCH_USE_SEMANTIC_SEARCH|False|Whether or not to use semantic search|
|AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG|default|The name of the semantic search configuration to use if using semantic search.|
|AZURE_SEARCH_TOP_K|5|The number of documents to retrieve from Azure AI Search.|
|AZURE_SEARCH_ENABLE_IN_DOMAIN|True|Limits responses to only queries relating to your data.|
|AZURE_SEARCH_CONTENT_COLUMN||List of fields in your Azure AI Search index that contains the text content of your documents to use when formulating a bot response. Represent these as a string joined with "|", e.g. `"product_description|product_manual"`|
|AZURE_SEARCH_CONTENT_VECTOR_COLUMN||Field from your Azure AI Search index for storing the content's Vector embeddings|
|AZURE_SEARCH_DIMENSIONS|1536| Azure OpenAI Embeddings dimensions. 1536 for `text-embedding-ada-002`. A full list of dimensions can be found [here](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models#embeddings-models). |
|AZURE_SEARCH_FIELDS_ID|id|`AZURE_SEARCH_FIELDS_ID`: Field from your Azure AI Search index that gives a unique idenitfier of the document chunk. `id` if you don't have a specific requirement.|
|AZURE_SEARCH_FILENAME_COLUMN||`AZURE_SEARCH_FILENAME_COLUMN`: Field from your Azure AI Search index that gives a unique idenitfier of the source of your data to display in the UI.|
|AZURE_SEARCH_TITLE_COLUMN||Field from your Azure AI Search index that gives a relevant title or header for your data content to display in the UI.|
|AZURE_SEARCH_URL_COLUMN||Field from your Azure AI Search index that contains a URL for the document, e.g. an Azure Blob Storage URI. This value is not currently used.|
|AZURE_SEARCH_FIELDS_TAG|tag|Field from your Azure AI Search index that contains tags for the document. `tag` if you don't have a specific requirement.|
|AZURE_SEARCH_FIELDS_METADATA|metadata|Field from your Azure AI Search index that contains metadata for the document. `metadata` if you don't have a specific requirement.|
|AZURE_SEARCH_FILTER||Filter to apply to search queries.|
|AZURE_SEARCH_USE_INTEGRATED_VECTORIZATION ||Whether to use [Integrated Vectorization](https://learn.microsoft.com/en-us/azure/search/vector-search-integrated-vectorization)|
|AZURE_OPENAI_RESOURCE||the name of your Azure OpenAI resource|
|AZURE_OPENAI_MODEL||The name of your model deployment|
|AZURE_OPENAI_MODEL_NAME|gpt-35-turbo|The name of the model|
|AZURE_OPENAI_MODEL_VERSION|0613|The version of the model to use|
|AZURE_OPENAI_API_KEY||One of the API keys of your Azure OpenAI resource|
|AZURE_OPENAI_EMBEDDING_MODEL|text-embedding-ada-002|The name of your Azure OpenAI embeddings model deployment|
|AZURE_OPENAI_EMBEDDING_MODEL_NAME|text-embedding-ada-002|The name of the embeddings model (can be found in Azure AI Studio)|
|AZURE_OPENAI_EMBEDDING_MODEL_VERSION|2|The version of the embeddings model to use (can be found in Azure AI Studio)|
|AZURE_OPENAI_TEMPERATURE|0|What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. A value of 0 is recommended when using your data.|
|AZURE_OPENAI_TOP_P|1.0|An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. We recommend setting this to 1.0 when using your data.|
|AZURE_OPENAI_MAX_TOKENS|1000|The maximum number of tokens allowed for the generated answer.|
|AZURE_OPENAI_STOP_SEQUENCE||Up to 4 sequences where the API will stop generating further tokens. Represent these as a string joined with "|", e.g. `"stop1|stop2|stop3"`|
|AZURE_OPENAI_SYSTEM_MESSAGE|You are an AI assistant that helps people find information.|A brief description of the role and tone the model should use|
|AZURE_OPENAI_API_VERSION|2024-02-01|API version when using Azure OpenAI on your data|
|AzureWebJobsStorage||The connection string to the Azure Blob Storage for the Azure Functions Batch processing|
|BACKEND_URL||The URL for the Backend Batch Azure Function. Use http://localhost:7071 for local execution|
|DOCUMENT_PROCESSING_QUEUE_NAME|doc-processing|The name of the Azure Queue to handle the Batch processing|
|AZURE_BLOB_ACCOUNT_NAME||The name of the Azure Blob Storage for storing the original documents to be processed|
|AZURE_BLOB_ACCOUNT_KEY||The key of the Azure Blob Storage for storing the original documents to be processed|
|AZURE_BLOB_CONTAINER_NAME||The name of the Container in the Azure Blob Storage for storing the original documents to be processed|
|AZURE_FORM_RECOGNIZER_ENDPOINT||The name of the Azure Form Recognizer for extracting the text from the documents|
|AZURE_FORM_RECOGNIZER_KEY||The key of the Azure Form Recognizer for extracting the text from the documents|
|APPLICATIONINSIGHTS_CONNECTION_STRING||The Application Insights connection string to store the application logs|
|ORCHESTRATION_STRATEGY | openai_function | Orchestration strategy. Use Azure OpenAI Functions (openai_function), Semantic Kernel (semantic_kernel),  LangChain (langchain) or Prompt Flow (prompt_flow) for messages orchestration. If you are using a new model version 0613 select any strategy, if you are using a 0314 model version select "langchain". Note that both `openai_function` and `semantic_kernel` use OpenAI function calling. Prompt Flow option is still in development and does not support RBAC or integrated vectorization as of yet.|
|AZURE_CONTENT_SAFETY_ENDPOINT | | The endpoint of the Azure AI Content Safety service |
|AZURE_CONTENT_SAFETY_KEY | | The key of the Azure AI Content Safety service|
|AZURE_SPEECH_SERVICE_KEY | | The key of the Azure Speech service|
|AZURE_SPEECH_SERVICE_REGION | | The region (location) of the Azure Speech service|
|AZURE_AUTH_TYPE | keys | The default is to use API keys. Change the value to 'rbac' to authenticate using Role Based Access Control. For more information refer to section [Authenticate using RBAC](#authenticate-using-rbac)

## Bicep

A [Bicep file](./infra/main.bicep) is used to generate the [ARM template](./infra/main.json). You can deploy this accelerator by the following command if you do not want to use `azd`.

```sh
az deployment sub create --template-file ./infra/main.bicep --subscription {your_azure_subscription_id} --location {search_location}
 ```
