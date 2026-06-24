# src/screenshot_manager.py
import os
import time
from playwright.sync_api import sync_playwright

class ScreenshotManager:
    def capture(self, html_filepath, target_dir, safe_title):
        filename = f"{safe_title}.png"
        output_path = os.path.join(target_dir, filename)

        # ファイルがすでに存在する場合はスキップ
        if os.path.exists(output_path):
            return filename

        file_url = "file:///" + os.path.abspath(html_filepath).replace("\\", "/")

        with sync_playwright() as p:
            browser = p.chromium.launch(channel="chrome", headless=False)
            context = browser.new_context(viewport={"width": 1100, "height": 800})
            page = context.new_page()
            page.goto(file_url)
            
            time.sleep(0.5)
            
            element = page.locator("#capture-area")
            element.screenshot(path=output_path)
            
            browser.close()

        return filename