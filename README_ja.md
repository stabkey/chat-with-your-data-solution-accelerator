---
name: データとチャット - ソリューションアクセラレータ（Python）
description: OpenAIとAI検索を使用してPythonでデータとチャットします。
languages:
- python
- typescript
- bicep
- az
developerproducts:
- azure-openai
- azure-cognitive-search
- azure-app-service
- azure-bot-service
- document-intelligence
- azure-functions
- azure-storage-accounts
- azure-speech
page_type: sample
urlFragment: chat-with-your-data-solution-accelerator
---

<!-- YAML front-matter schema: https://review.learn.microsoft.com/ja-jp/help/contribute/samples/process/onboarding?branch=main#supported-metadata-fields-for-readmemd -->

# Chat with your data - Solution accelerator

 ##### Table of Contents

- [Chat with your data - Solution accelerator](#chat-with-your-data---solution-accelerator)
        - [Table of Contents](#table-of-contents)
  - [User story](#user-story)
    - [About this repo](#about-this-repo)
    - [When should you use this repo?](#when-should-you-use-this-repo)
    - [Key features](#key-features)
    - [Target end users](#target-end-users)
    - [Industry scenario](#industry-scenario)
  - [Deploy](#deploy)
    - [Pre-requisites](#pre-requisites)
    - [Products used](#products-used)
    - [Required licenses](#required-licenses)
    - [Pricing Considerations](#pricing-considerations)
    - [Deploy instructions](#deploy-instructions)
    - [Testing the deployment](#testing-the-deployment)
  - [Supporting documentation](#supporting-documentation)
    - [Resource links](#resource-links)
    - [Licensing](#licensing)
  - [Disclaimers](#disclaimers)

## User story

*データとチャット* ソリューションアクセラレータのリポジトリへようこそ！ *データとチャット* ソリューションアクセラレータは、Azure AI Searchと大規模言語モデル（LLMs）の機能を組み合わせて会話型検索体験を提供する強力なツールです。このソリューションアクセラレータは、Azure OpenAI GPTモデルと、あなたのデータから生成されたAzure AI Searchインデックスを使用し、検索クエリのための自然言語インターフェースを提供するWebアプリケーションに統合されています。また、[音声認識](docs/speech_to_text.md)機能も含まれています。ユーザーはファイルをドラッグ＆ドロップしたり、ストレージを指定したり、技術的なセットアップを行うことでドキュメントを変換できます。すべてがあなた自身のサブスクリプションにデプロイされ、この技術の使用を加速させることができます。

![Solution Architecture - Chat with your data](/docs/images/cwyd-solution-architecture.png)

### About this repo

このリポジトリは、自然言語でデータをクエリしたいユーザーのためのエンドツーエンドソリューションを提供します。複数のファイルタイプに対応した優れたインジェスチョン機構、簡単なデプロイメント、そしてメンテナンスをサポートするチームが含まれています。このアクセラレータは、プッシュまたはプルのインジェスチョンをデモンストレーションし、オーケストレーションの選択（Semantic Kernel、LangChain、OpenAI Functions、または[Prompt Flow](docs/prompt_flow.md)）を提供し、RAGパターンを実装するために必要な最小限のコンポーネントを提供します。実験やデータの評価なしにそのままプロダクション環境で使用することは意図されていません。以下の機能を提供します：

- 自分のデータを使用してAzure OpenAIモデルとチャット
- ドキュメントのアップロードと処理
- 公開ウェブページのインデックス化
- 簡単なプロンプト設定
- 複数のチャンク戦略

### When should you use this repo?

もし [Azure OpenAI on your data](https://learn.microsoft.com/azure/ai-services/openai/concepts/use-your-data) が提供する標準機能以上にシナリオをカスタマイズする必要がある場合は、このリポジトリを使用してください。デフォルトでは、このリポジトリにはチャンクサイズ、オーバーラップ、検索/取得タイプ、システムプロンプトなどの特定のRAG設定が含まれています。プロダクションでこのリポジトリを使用する前に、データに対する検索/取得および回答の生成を評価し、これらの設定を調整することが重要です。RAG評価を理解し実行するための出発点として、[RAG Experiment Accelerator](https://github.com/microsoft/rag-experiment-accelerator) を参照することをお勧めします。

ここで紹介するアクセラレータは、以下のような複数のオプションを提供します：

- データと公開ウェブページの両方を使用してモデルを基盤にする能力
- 「カスタム」および「オン・ユア・データ」[会話フロー](./docs/conversation_flow_options.md) をサポートするバックエンド
- 高度なプロンプトエンジニアリング機能
- データセットを即時にインジェスト、検査、設定するための管理サイト
- データインジェスチョンのプッシュまたはプルモデル：詳細については [統合ベクトル化](./docs/integrated_vectorization.md) のドキュメントを参照
- ローカルでのRAGソリューションの実行

*[ChatGPT + Enterprise data with Azure OpenAI and AI Search demo](https://github.com/Azure-Samples/azure-search-openai-demo) をご覧になりましたか？もし実験したい場合：プロンプトを試したり、RAGパターンの異なる実装アプローチを理解したり、異なる機能がRAGパターンとどう相互作用するかを見たり、RAGデプロイメントのための最適なオプションを選択したりするために、そのリポジトリを参照してください。

ここに、Azureが提供するいくつかの機能、利用可能なGitHubのデモサンプル、このリポジトリの機能を比較した表があります。どれを使用するか決定する際のガイダンスとして役立ちます：

| 名前 | 機能またはサンプル？ | それは何？ | いつ使用する？ |
| --------- | --------- | --------- | --------- |
| ["Chat with your data" ソリューションアクセラレータ](https://aka.ms/ChatWithYourDataSolutionAccelerator) - (このリポジトリ) | Azureサンプル | Azure AI Searchをレトリーバーとして使用するエンドツーエンドのベースラインRAGパターンサンプル。 | Azureが提供するRAGパターン実装がビジネス要件を満たさない場合、開発者はこのサンプルを使用するべきです。このサンプルはソリューションをカスタマイズする手段を提供します。開発者は要件を満たし、各企業のポリシーに従ってベストプラクティスを適用するために独自のコードを追加する必要があります。 |
| [Azure OpenAI on your data](https://learn.microsoft.com/azure/ai-services/openai/concepts/use-your-data) | Azure機能 | Azure OpenAI Serviceが提供する標準機能で、REST APIまたはAzure AI Studioのウェブベースインターフェースを使用して、Azure OpenAI ChatGPTモデルとAzure AI Searchを使用したチャット体験を可能にするソリューションを作成します。 | Azure OpenAI ServiceとAzure AI Searchを使用したエンドツーエンドのソリューションが必要な開発者にとって、最初に検討すべきオプションです。サポートされているデータソース、Azure OpenAI ServiceのChatGPTモデル、およびエンタープライズアプリケーションのニーズを設定するために必要な他のAzureリソースを選択するだけです。 |
| [Azure Machine Learning prompt flow](https://learn.microsoft.com/azure/machine-learning/concept-retrieval-augmented-generation) | Azure機能 | RAGは、Azure OpenAI Serviceとの統合により、Azure Machine Learningで有効化されます。FaissやAzure AI Searchをベクトルストアとしてサポートし、LangChainなどのデータチャンク化のためのオープンソース提供、ツール、およびフレームワークもサポートします。Azure Machine Learning prompt flowは、データ生成をテストし、プロンプト作成を自動化し、プロンプト評価指標を視覚化し、RAGワークフローをMLOpsに統合する機能を提供します。 | LLMベースのAIアプリケーションの開発サイクルに関与するプロセスをより制御したい開発者は、Azure Machine Learning prompt flowを使用して実行可能なフローを作成し、大規模なテストを通じてパフォーマンスを評価するべきです。 |
| [ChatGPT + Enterprise data with Azure OpenAI and AI Search demo](https://github.com/Azure-Samples/azure-search-openai-demo) | Azureサンプル | Azure AI Searchをレトリーバーとして使用するRAGパターンデモ。 | RAGパターンのエンドツーエンドデモを使用または提示したい開発者はこのサンプルを使用するべきです。これには、異なる検索モードのデプロイおよびテスト、ビジネスユースケースをサポートするプロンプトの設定が含まれます。 |
| [RAG Experiment Accelerator](https://github.com/microsoft/rag-experiment-accelerator) | ツール | RAG Experiment Acceleratorは、Azure AI SearchとRAGパターンを使用して実験と評価を行うための多用途なツールです。 | RAG Experiment Acceleratorは、検索クエリとOpenAIからの応答の品質を評価するための実験と評価を迅速に行うためのツールです。このツールは、研究者、データサイエンティスト、および異なる検索およびOpenAI関連のハイパーパラメータのパフォーマンステストを行いたい開発者にとって有用です。 |

### Key features

- **プライベートLLMアクセスでのデータ利用**: プライベートで非構造化データに対するChatGPTの全てのメリットを享受できます。
- **フルデータセットへの単一アプリケーションアクセス**: 社内のナレッジベースにアクセスするためのエンドポイントを最小限に抑えます。同じバックエンドを[Microsoft Teams拡張](docs/teams_extension.md)と再利用できます。
- **非構造化データとの自然言語インタラクション**: 自然言語を使用して必要な回答を迅速に見つけ、補足的な詳細を得るためのフォローアップクエリを行います。[音声認識](docs/speech_to_text.md)も含まれています。
- **クエリ時のソースドキュメントへの簡単なアクセス**: 追加のコンテキストを提供するために、同じチャットウィンドウ内で参照されたドキュメントを確認できます。
- **データアップロード**: [さまざまなファイルタイプ](docs/supported_file_types.md)のドキュメントを一括アップロードできます。
- **アクセス可能なオーケストレーション**: プロンプトとドキュメントの設定（プロンプトエンジニアリング、ドキュメント処理、データ取得）

**注意**: 現在のモデルでは、PDF、テキスト、docxファイルなどの非構造化データに関する質問が可能です。対応している[ファイルタイプ](docs/supported_file_types.md)を参照してください。

### Target end users

社内の非構造化データを調査する必要がある会社の従業員や経営者は、このアクセラレータを利用して、自然言語を使用して迅速に必要な情報を見つけることができます。
このアクセラレータは業界や役割を問わず機能し、社内の非構造化データに対してChatGPTの体験を通じて迅速に回答を得たい従業員に適しています。
技術管理者はこのアクセラレータを使用して、同僚に社内の非構造化データへの簡単なアクセスを提供できます。管理者はシステム構成をカスタマイズして、意図した対象者に合わせた応答を提供することができます。

### Use Case scenarios

#### Financial Advisor Scenario
The sample data illustrates how this accelerator could be used in the financial services industry (FSI).

In this scenario, a financial advisor is preparing for a meeting with a potential client who has expressed interest in Woodgrove Investments’ Emerging Markets Funds. The advisor prepares for the meeting by refreshing their understanding of the emerging markets fund's overall goals and the associated risks.

Now that the financial advisor is more informed about Woodgrove’s Emerging Markets Funds, they're better equipped to respond to questions about this fund from their client.

#### Legal Review and Summarization Assistant scenario
Additionally, we have implemented a Legal Review and Summarization Assistant scenario to demonstrate how this accelerator can be utilized in any industry. The Legal Review and Summarization Assistant helps professionals manage and interact with a large collection of documents efficiently. For more details, refer to the [Legal Review and Summarization Assistant README](docs/contract_assistance.md).

Note: Some of the sample data included with this accelerator was generated using AI and is for illustrative purposes only.

---

![One-click Deploy](/docs/images/oneClickDeploy.png)
## Deploy
### Pre-requisites
- Azure subscription - [Create one for free](https://azure.microsoft.com/free/) with owner access.
- Approval to use Azure OpenAI services with your Azure subcription. To apply for approval, see [here](https://learn.microsoft.com/en-us/azure/ai-services/openai/overview#how-do-i-get-access-to-azure-openai).
- [Enable custom Teams apps and turn on custom app uploading](https://learn.microsoft.com/en-us/microsoftteams/platform/concepts/build-and-test/prepare-your-o365-tenant#enable-custom-teams-apps-and-turn-on-custom-app-uploading) (optional: Teams extension only)

### Products used
- Azure App Service
- Azure Application Insights
- Azure Bot
- Azure OpenAI
- Azure Document Intelligence
- Azure Function App
- Azure Search Service
- Azure Storage Account
- Azure Speech Service
- Teams (optional: Teams extension only)

### Required licenses
- Microsoft 365 (optional: Teams extension only)

### Pricing Considerations

This solution accelerator deploys multiple resources. Evaluate the cost of each component prior to deployment.

The following are links to the pricing details for some of the resources:
- [Azure OpenAI service pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/). GPT and embedding models are charged separately.
- [Azure AI Search pricing](https://azure.microsoft.com/pricing/details/search/). AI Search core service and semantic ranker are charged separately.
- [Azure Blob Storage pricing](https://azure.microsoft.com/pricing/details/storage/blobs/)
- [Azure Functions pricing](https://azure.microsoft.com/pricing/details/functions/)
- [Azure AI Document Intelligence pricing](https://azure.microsoft.com/pricing/details/ai-document-intelligence/)
- [Azure Web App Pricing](https://azure.microsoft.com/pricing/details/app-service/windows/)

### Deploy instructions

There are two choices; the "Deploy to Azure" offers a one click deployment where you don't have to clone the code, alternatively if you would like a developer experience, follow the [Local deployment instructions](./docs/LOCAL_DEPLOYMENT.md).

The demo, which uses containers pre-built from the main branch is available by clicking this button:

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FAzure-Samples%2Fchat-with-your-data-solution-accelerator%2Fmain%2Finfra%2Fmain.json)

**Note**: The default configuration deploys an OpenAI Model "gpt-35-turbo" with version 0613. However, not all
locations support this version. If you're deploying to a location that doesn't support version 0613, you'll need to
switch to a lower version. To find out which versions are supported in different regions, visit the
[GPT-35 Turbo Model Availability](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models#gpt-35-turbo-model-availability) page.

### Testing the deployment
1. Navigate to the admin site, where you can upload documents. It will be located at:

    `https://web-{RESOURCE_TOKEN}-admin.azurewebsites.net/`

    Where `{RESOURCE_TOKEN}` is uniquely generated during deployment. This is a combination of your subscription and the name of the resource group. Then select **Ingest Data** and add your data. You can find sample data in the `/data` directory.

    ![A screenshot of the admin site.](./docs/images/admin-site.png)


2. Navigate to the web app to start chatting on top of your data. The web app can be found at:

    `https://web-{RESOURCE_TOKEN}.azurewebsites.net/`


    ![A screenshot of the chat app.](./docs/images/web-unstructureddata.png)

\
\
![Supporting documentation](/docs/images/supportingDocuments.png)
## Supporting documentation

### Resource links

This solution accelerator deploys the following resources. It's critical to comprehend the functionality of each. Below are the links to their respective documentation:
- [Application Insights overview - Azure Monitor | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview?tabs=net)
- [Azure OpenAI Service - Documentation, quickstarts, API reference - Azure AI services | Microsoft Learn](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/use-your-data)
- [Using your data with Azure OpenAI Service - Azure OpenAI | Microsoft Learn](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/use-your-data)
- [Content Safety documentation - Quickstarts, Tutorials, API Reference - Azure AI services | Microsoft Learn](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/)
- [Document Intelligence documentation - Quickstarts, Tutorials, API Reference - Azure AI services | Microsoft Learn](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/?view=doc-intel-3.1.0)
- [Azure Functions documentation | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-functions/)
- [Azure Cognitive Search documentation | Microsoft Learn](https://learn.microsoft.com/en-us/azure/search/)
- [Speech to text documentation - Tutorials, API Reference - Azure AI services - Azure AI services | Microsoft Learn](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/index-speech-to-text)
- [Bots in Microsoft Teams - Teams | Microsoft Learn](https://learn.microsoft.com/en-us/microsoftteams/platform/bots/what-are-bots) (Optional: Teams extension only)

### Licensing

This repository is licensed under the [MIT License](LICENSE.md).

The data set under the /data folder is licensed under the [CDLA-Permissive-2 License](CDLA-Permissive-2.md).

## Disclaimers

このソフトウェアは、以下に示すような別個のプロプライエタリまたはオープンソースのライセンスによって管理されるサードパーティコンポーネントの使用を必要とし、それぞれの適用されるライセンスの条件に従う必要があります。このライセンスがそのようなサードパーティのプロプライエタリまたはオープンソースのコンポーネントを使用するためのライセンスや他の権利を付与するものではないことを認識し、同意するものとします。

ソフトウェアにMicrosoft製品またはサービス（Microsoft Azure Servicesを含むがこれに限定されない）を使用または派生したコンポーネントやコードが含まれている場合（総称して「Microsoft製品およびサービス」）、そのMicrosoft製品およびサービスに適用される製品条項を遵守する必要があります。ソフトウェアを管理するライセンスがMicrosoft製品およびサービスを使用するためのライセンスや他の権利を付与するものではないことを認識し、同意するものとします。このライセンスまたは本ReadMeファイルのいかなる記載も、Microsoft製品およびサービスに関する製品条項を無効化、修正、終了または変更するものではありません。

ソフトウェアに適用されるすべての国内および国際的な輸出法および規制を遵守する必要があります。これには、目的地、エンドユーザー、およびエンドユースに対する制限が含まれます。輸出制限に関する詳細は、[こちら](https://aka.ms/exporting)を参照してください。

ソフトウェアおよびMicrosoft製品およびサービスが (1) 医療機器として設計、意図、提供されていないこと、(2) 専門的な医療アドバイス、診断、治療、または判断の代替として設計または意図されていないこと、ならびに専門的な医療アドバイス、診断、治療、または判断の代替または置き換えとして使用されるべきではないことを認識し、同意するものとします。顧客は、オンラインサービスの顧客の実装のエンドユーザーに対して適切な同意、警告、免責事項、および確認を表示および取得する責任を単独で負います。

ソフトウェアはSOC 1およびSOC 2のコンプライアンス監査の対象ではないことを認識してください。Microsoftの技術、またはそのコンポーネント技術（ソフトウェアを含む）は、認定された金融サービスの専門家の専門的なアドバイス、意見、または判断の代替として提供または意図されたものではありません。ソフトウェアを使用して専門的な金融アドバイスや判断を置き換える、代替する、または提供するべきではありません。

ソフトウェアにアクセスまたは使用することにより、サービスの中断、欠陥、エラー、またはソフトウェアの他の障害が発生した場合に、人の死や重大な身体傷害、または物理的または環境的損害（総称して「高リスク使用」）を引き起こす可能性がある使用をサポートするように設計または意図されていないことを認識し、同意します。また、ソフトウェアの中断、欠陥、エラー、または他の障害が発生した場合に、人、財産、および環境の安全性が合理的に適切かつ合法的なレベルを下回らないようにすることを保証するものとします。ソフトウェアにアクセスすることにより、高リスク使用の自己責任であることをさらに認識します。
