# 文字の形態における意味情報圧縮率並びにトークン数の簡易調査レポート

文字の種類（表意文字、表音文字など）による意味情報の圧縮率と、LLMのトークナイザーにおける処理効率の関係を簡易的に調査・可視化したリポジトリです。あくまで個人の趣味レベルの簡易レポートです。参考程度にご覧ください。

## 主なドキュメント

本プロジェクトの調査内容と考察は、以下のファイルにまとめられています。

* **[文字効率レポート.md](./文字効率レポート.md)**
    OpenAIのトークナイザーをベースに、日本語、中国語、英語、韓国語の文字数とトークン数の関係をまとめた初期の検証レポートです。日本語における文字種の混在による影響などについて、感覚論を含めて考察しています。
* **[追加検証.2.md](./追加検証.2.md)**
    主要な10モデルのトークナイザーを用いて、同様の文章を処理した際のトークン数を比較・考察したレポートです。
* **[トークン効率グラフ.png](./トークン効率グラフ.png)**
    各モデルおよび各言語におけるトークン消費率のデータをグラフ化したものです。

---
## 検証対象モデル

本調査の追加検証において、トークナイザー（tokenizer.json）を読み込んで使用したモデルは以下の通りです。

| モデル表示名 | Hugging Face リポジトリリンク |
| :--- | :--- |
| DeepSeek-V3-Base | [deepseek-ai/DeepSeek-V3-Base](https://huggingface.co/deepseek-ai/DeepSeek-V3-Base) |
| DeepSeek-V4-Pro | [deepseek-ai/DeepSeek-V4-Pro](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro) |
| diffusiongemma-26B-A4B-it | [google/diffusiongemma-26B-A4B-it](https://huggingface.co/google/diffusiongemma-26B-A4B-it) |
| gemma-4-31B-it | [google/gemma-4-31B-it](https://huggingface.co/google/gemma-4-31B-it) |
| LFM2.5-8B-A1B | [LiquidAI/LFM2.5-8B-A1B](https://huggingface.co/LiquidAI/LFM2.5-8B-A1B) |
| Llama-3-ELYZA-JP-8B | [elyza/Llama-3-ELYZA-JP-8B](https://huggingface.co/elyza/Llama-3-ELYZA-JP-8B) |
| Mistral-Medium-3.5-128B | [mistralai/Mistral-Medium-3.5-128B](https://huggingface.co/mistralai/Mistral-Medium-3.5-128B) |
| Qwen2.5-72B-Instruct | [Qwen/Qwen2.5-72B-Instruct](https://huggingface.co/Qwen/Qwen2.5-72B-Instruct) |
| Qwen3.6-27B | [Qwen/Qwen3.6-27B](https://huggingface.co/Qwen/Qwen3.6-27B) |
| RakutenAI-3.0 | [Rakuten/RakutenAI-3.0](https://huggingface.co/Rakuten/RakutenAI-3.0) |

---
## スクリプトの概要

本リポジトリには、検証データを取得・可視化するために使用したPythonスクリプトを同梱しています。

* `main.py`: 検証処理を自動化するための実行スクリプトです。
* `src/tokenizer_core.py`: トークン分割の処理およびHTML用の要素生成を行うロジックを搭載しています。
* `src/html_generator.py`: トークンの分割状態を色分けして確認できるHTMLファイルを生成します。
* `src/screenshot_manager.py`: Playwrightを使用し、生成されたHTMLのスクリーンショットを自動でキャプチャします。
* `src/markdown_processor.py`: 既存データのCSV読み込み、および検証結果を反映したCSVファイルとMarkdown用テーブルの生成・保存を行います。

---
## ディレクトリ構造

```text
.
├── .gitignore
├── LICENSE
├── LLMトークン効率グラフ.pdf
├── main.py                 # 実行スクリプト
├── NOTICE.md
├── output.csv              # 検証結果のデータシート
├── README.md               # 本ドキュメント
├── requirements.txt
├── トークン効率グラフ.png  # 比較グラフの画像
├── 文字効率レポート.md    # 初期検証レポート
├── 文字効率レポート.pdf
├── 追加検証.2.md          # 追加検証レポート
├── 追加検証.2.pdf
├── html_output/            # 自動生成された検証用HTMLファイル（モデル別・言語別）
├── src/                    # スクリプトのモジュール
├── 英語/                   # 英語のテキストおよび出力された画像
├── 日本語/                 # 日本語のテキスト（各種バリエーション）および出力された画像
├── 中国語/                 # 中国語のテキストおよび出力された画像
├── 韓国語/                 # 韓国語のテキストおよび出力された画像
└── 参考文献/               # 先行研究のAbstractをまとめたドキュメント（Abstracts.md）
```

---
## 参考文献

本調査において参考にした先行研究の一覧です。詳細は [参考文献/Abstracts.md](./参考文献/Abstracts.md) を参照してください。

1. Andrew Gambardella et al. (2025): "Inconsistent Tokenizations Cause Language Models to be Perplexed by Japanese Grammar"
2. Eugene Jang et al. (2025): "Improbable Bigrams Expose Vulnerabilities of Incomplete Tokens in Byte-Level Tokenizers"
3. Jean Seo et al. (2025): "How does a Language-Specific Tokenizer affect LLMs?"
4. Simiao Ren et al. (2026): "Chinese Language Is Not More Efficient Than English in Vibe Coding: A Preliminary Study on Token Cost and Problem-Solving Rate"

---
## ライセンス

* 本リポジトリのスクリプトおよびレポートは MIT License の元で公開されています。
* 利用している外部ライブラリのライセンスについては、[NOTICE.md](./NOTICE.md) を参照してください。
* 各モデルのトークナイザーの著作権およびライセンスは、それぞれの開発元に帰属します。
