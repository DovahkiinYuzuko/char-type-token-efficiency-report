# src/markdown_processor.py
import os
import csv

class MarkdownProcessor:
    def __init__(self, languages, jp_titles, lang_map):
        self.languages = languages
        self.jp_titles = jp_titles
        self.lang_map = lang_map

    def load_csv(self, csv_filepath):
        data = {}
        if not os.path.exists(csv_filepath):
            return data
            
        with open(csv_filepath, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                lang = row["言語"]
                title = row["文章名"]
                model = row["モデル名"]
                
                if lang not in data:
                    data[lang] = {}
                if title not in data[lang]:
                    data[lang][title] = {"models": {}}
                    
                data[lang][title]["models"][model] = {
                    "char_count": row["文字数"],
                    "token_count": row["トークン数"],
                    "chars_per_token": row["文字数目安(有効桁4)"],
                    "percent": row["トークン消費[%]"],
                    "img_path": row["画像パス"]
                }
        return data

    def save(self, md_filepath, csv_filepath, data, texts_dict):
        # 1. CSVの保存
        with open(csv_filepath, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["言語", "文章名", "モデル名", "文字数", "トークン数", "文字数目安(有効桁4)", "トークン消費[%]", "画像パス"])
            
            for lang in self.languages:
                if lang not in data: continue
                
                titles = [t for t in self.jp_titles if t in data[lang]] if lang == "日本語" else sorted(data[lang].keys())
                titles += [t for t in sorted(data[lang].keys()) if t not in titles]
                
                for title in titles:
                    if title not in data[lang]: continue
                    for model in sorted(data[lang][title]["models"].keys()):
                        mdata = data[lang][title]["models"][model]
                        writer.writerow([
                            lang, title, model,
                            mdata["char_count"], mdata["token_count"],
                            mdata["chars_per_token"], mdata["percent"],
                            mdata["img_path"]
                        ])

        # 2. Markdown(テーブル構造)の保存
        with open(md_filepath, "w", encoding="utf-8") as f:
            f.write("## 追加検証.2\n他アーキテクチャによるトークナイザー効率可視化ならびに日本語ボトルネック検証\n\n")
            
            first_lang = True
            for lang in self.languages:
                if lang not in data: continue
                
                if not first_lang:
                    f.write("\n---\n")
                first_lang = False
                
                display_lang = self.lang_map.get(lang, lang)
                f.write(f"### {display_lang}\n")
                
                titles = [t for t in self.jp_titles if t in data[lang]] if lang == "日本語" else sorted(data[lang].keys())
                titles += [t for t in sorted(data[lang].keys()) if t not in titles]
                
                for title in titles:
                    f.write(f"#### {title}\n")
                    text = texts_dict.get(lang, {}).get(title, "")
                    if text:
                        f.write(f"```markdown\n{text}\n```\n\n")
                        
                    f.write("| モデル名（クリックで可視化） | 文字数 | トークン数 | 文字数目安 (有効桁4) | トークン消費 [%] |\n")
                    f.write("| :--- | :---: | :---: | :---: | :---: |\n")
                    
                    for model in sorted(data[lang][title]["models"].keys()):
                        mdata = data[lang][title]["models"][model]
                        f.write(f"| [{model}]({mdata['img_path']}) | {mdata['char_count']} | {mdata['token_count']} | {mdata['chars_per_token']} | {mdata['percent']} |\n")
                    f.write("\n")