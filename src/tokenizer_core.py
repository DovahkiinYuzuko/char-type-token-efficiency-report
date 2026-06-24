# src/tokenizer_core.py
from tokenizers import Tokenizer
from decimal import Decimal, getcontext, ROUND_HALF_UP

class TokenizerCore:
    def __init__(self, model_id):
        # ローカルファイルではなく、Hugging FaceのIDから直接ロードするように変更
        self.tokenizer = Tokenizer.from_pretrained(model_id)
        self.colors = [
            "#1e40af", "#86198f", "#166534", "#991b1b",
            "#115e59", "#3f3f46", "#4c1d95", "#5b21b6"
        ]

    def process(self, text):
        encoded = self.tokenizer.encode(text)
        token_ids = encoded.ids
        
        char_count = len(text)
        token_count = len(token_ids)
        
        if token_count > 0 and char_count > 0:
            getcontext().prec = 4
            chars_per_token = +(Decimal(char_count) / Decimal(token_count))
            getcontext().prec = 28
            percent = (Decimal(token_count) / Decimal(char_count)) * Decimal('100')
            percent = percent.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        else:
            chars_per_token = Decimal('0')
            percent = Decimal('0.00')

        token_html_elements = []
        buffer = []
        color_idx = 0
        
        for token_id in token_ids:
            buffer.append(token_id)
            decoded_str = self.tokenizer.decode(buffer)
            
            if "\ufffd" not in decoded_str and decoded_str != "":
                color = self.colors[color_idx % len(self.colors)]
                safe_str = decoded_str.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
                
                if len(buffer) > 1:
                    display_text = f"{safe_str}({len(buffer)})"
                else:
                    display_text = safe_str
                    
                token_html_elements.append(f'<span class="token" style="background-color: {color};">{display_text}</span>')
                color_idx += 1
                buffer = []
                
        if buffer:
            color = self.colors[color_idx % len(self.colors)]
            fallback_str = self.tokenizer.decode(buffer)
            if fallback_str == "":
                fallback_str = f"[RAW:{buffer}]"
            safe_str = fallback_str.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
            token_html_elements.append(f'<span class="token" style="background-color: {color};">{safe_str}</span>')

        return char_count, token_count, chars_per_token, percent, "\n".join(token_html_elements)