# main.py
import os
import concurrent.futures
from rich.console import Console
from src.tokenizer_core import TokenizerCore
from src.markdown_processor import MarkdownProcessor
from src.html_generator import HTMLGenerator
from src.screenshot_manager import ScreenshotManager

LANGUAGES = ["日本語", "中国語", "英語", "韓国語"]
JP_TITLES = [
    "文章1", "文章2", "文章3",
    "文章1(漢字なしバージョン)", "文章1(ローマ字入力)",
    "文章1(漢字増やしバージョン)", "文章1(エセ中国語風味)"
]

LANG_DISPLAY_MAP = {
    "日本語": "日本語",
    "中国語": "簡体中国語",
    "英語": "英語",
    "韓国語": "韓国語"
}

# フォルダ走査をやめて、Hugging FaceのモデルIDマッピングを直接定義
HF_MODELS = {
    "DeepSeek-V3-Base": "deepseek-ai/DeepSeek-V3-Base",
    "DeepSeek-V4-Pro": "deepseek-ai/DeepSeek-V4-Pro",
    "diffusiongemma-26B-A4B-it": "google/diffusiongemma-26B-A4B-it",
    "gemma-4-31B-it": "google/gemma-4-31B-it",
    "LFM2.5-8B-A1B": "LiquidAI/LFM2.5-8B-A1B",
    "Llama-3-ELYZA-JP-8B": "elyza/Llama-3-ELYZA-JP-8B",
    "Mistral-Medium-3.5-128B": "mistralai/Mistral-Medium-3.5-128B",
    "Qwen2.5-72B-Instruct": "Qwen/Qwen2.5-72B-Instruct",
    "Qwen3.6-27B": "Qwen/Qwen3.6-27B",
    "Rakuten AI 3.0": "Rakuten/RakutenAI-3.0"
}

def process_single_model(selected_model, hf_model_id, base_html_dir, texts_dict):
    try:
        # パスではなくHugging FaceのモデルIDを渡す
        tokenizer_core = TokenizerCore(hf_model_id)
    except Exception as e:
        return selected_model, None, f"読み込みエラー: {e}"

    results = {}
    screenshot_mgr = ScreenshotManager()

    for lang in LANGUAGES:
        if lang not in texts_dict:
            continue
            
        specific_html_dir = os.path.join(base_html_dir, selected_model, lang)
        os.makedirs(specific_html_dir, exist_ok=True)
        
        target_png_dir = os.path.join(lang, selected_model)
        os.makedirs(target_png_dir, exist_ok=True)
        
        if lang not in results:
            results[lang] = {}

        for article_title, text in texts_dict[lang].items():
            char_count, token_count, chars_per_token, percent, token_html = tokenizer_core.process(text)
            
            safe_title = article_title.replace("(", "_").replace(")", "")
            html_filename = f"{selected_model}_{lang}_{safe_title}.html"
            html_path = os.path.join(specific_html_dir, html_filename)
            
            html_code = HTMLGenerator.generate(
                selected_model, lang, article_title, 
                char_count, token_count, chars_per_token, percent, 
                text, token_html
            )
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_code)

            png_filename = screenshot_mgr.capture(html_path, target_png_dir, safe_title)
            img_path = f"./{lang}/{selected_model}/{png_filename}"
            
            results[lang][article_title] = {
                "char_count": char_count,
                "token_count": token_count,
                "chars_per_token": chars_per_token,
                "percent": f"{percent}%",
                "img_path": img_path
            }

    return selected_model, results, None

def main():
    console = Console()
    output_md = "output.md"
    output_csv = "output.csv"
    base_html_dir = "html_output"
    
    md_processor = MarkdownProcessor(LANGUAGES, JP_TITLES, LANG_DISPLAY_MAP)
    
    # 全言語のテキストを事前にメモリにキャッシュ
    texts_dict = {}
    for lang in LANGUAGES:
        lang_file = os.path.join(lang, f"{lang}.md")
        if os.path.exists(lang_file):
            texts_dict[lang] = {}
            with open(lang_file, "r", encoding="utf-8") as f:
                content = f.read()
            chunks = [c.strip() for c in content.split("---")]
            chunks = [c for c in chunks if c]
            for idx, text in enumerate(chunks):
                title = JP_TITLES[idx] if lang == "日本語" and idx < len(JP_TITLES) else f"文章{idx + 1}"
                texts_dict[lang][title] = text
    
    model_names = list(HF_MODELS.keys())

    while True:
        console.print("\n[bold cyan]=== モデル選択 ===[/bold cyan]")
        console.print("0: [bold yellow]プログラムを終了する[/bold yellow]")
        for i, model_name in enumerate(model_names, 1):
            console.print(f"{i}: {model_name}")
            
        user_input = input("\n番号を入力（コンマ区切りで複数選択可 例: 1,3）: ").strip()
        if not user_input:
            continue
            
        choices = [c.strip() for c in user_input.split(",")]
        
        if "0" in choices:
            confirm = input("選択肢の中に「0（プログラム終了）」が含まれています。本当に終了しますか？(y/n): ").strip().lower()
            if confirm == 'y':
                console.print("\n[bold green]プログラムを終了します。[/bold green]")
                break
            else:
                continue
                
        valid_choices = []
        try:
            for c in choices:
                idx = int(c)
                if idx < 1 or idx > len(model_names):
                    raise ValueError
                valid_choices.append(idx)
        except ValueError:
            console.print("[bold red]無効な入力が含まれています。再度入力してください。[/bold red]")
            continue
            
        selected_models = [model_names[idx - 1] for idx in valid_choices]
        console.print("\n[bold cyan]>> 選択されたモデル:[/bold cyan]")
        for sm in selected_models:
            # 選択されたモデル名とHugging FaceのIDを表示
            console.print(f" - {sm} ({HF_MODELS[sm]})")
            
        proceed = input("\nこのまま実行しますか？(y/n): ").strip().lower()
        if proceed != 'y':
            continue

        all_data = md_processor.load_csv(output_csv)

        console.print("\n[dim]マルチスレッドで並列処理を開始します...[/dim]")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            # selected_modelとhf_model_idの両方を渡す
            futures = {executor.submit(process_single_model, sm, HF_MODELS[sm], base_html_dir, texts_dict): sm for sm in selected_models}
            
            for future in concurrent.futures.as_completed(futures):
                sm = futures[future]
                try:
                    model, results, error = future.result()
                    if error or results is None:
                        console.print(f"[bold red]エラー ({model}):[/bold red] {error}")
                    else:
                        for lang, titles in results.items():
                            if lang not in all_data:
                                all_data[lang] = {}
                            for title, stats in titles.items():
                                if title not in all_data[lang]:
                                    all_data[lang][title] = {"models": {}}
                                all_data[lang][title]["models"][model] = stats
                        console.print(f"[bold green]✔ {model} の処理が完了しました。[/bold green]")
                except Exception as e:
                    console.print(f"[bold red]予期せぬエラー ({sm}):[/bold red] {e}")

        md_processor.save(output_md, output_csv, all_data, texts_dict)
        console.print(f"\n[bold magenta]✔ すべてのモデル処理が完了し、ファイル(CSV/MD)を更新しました。[/bold magenta]\n")

if __name__ == "__main__":
    main()