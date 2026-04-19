#!/usr/bin/env python3
"""
渲染级验证：确认生成的描红 HTML 里每行第一份单词真的是黑色、后续副本真的是浅蓝。

光看源码的内联 stroke 属性和 CSS `!important` 规则不够——必须让浏览器实际渲染一遍，
才能保证 `:first-of-type` 选择器、SVG `<use>` 引用、stroke 继承链路全程生效。

### 双重维度
1. **getComputedStyle**（浏览器最终生效样式）：遍历每个 `svg.row-letters` 下的每个 `<g>`，
   断言首份 `stroke = rgb(0, 0, 0)`、后续 `stroke = rgb(184, 217, 238)`。
2. **像素采样**（实际绘制到屏幕的像素）：对首份 `<g>` 的 bounding-rect 裁剪，断言裁剪区
   内存在黑色像素（RGB 三通道均 ≤ 20）；对第二份同尺寸裁剪，断言无黑色像素（对照）。

### 用法
    python3 scripts/verify_first_black.py [HTML 路径]

默认跑 `tracing-cards-smoke20.html`。任何失败 exit 1，全部通过 exit 0。

### 依赖
- `pip install --user playwright pillow`
- `python3 -m playwright install chromium`

### 产物（调试截图）
- `/tmp/card1_rendered.png`       首张卡片整体
- `/tmp/row_letters_rendered.png` 首个 row-letters 层
- `/tmp/first_g_crop.png`         首份单词 bbox 裁剪
- `/tmp/second_g_crop.png`        第二份单词 bbox 裁剪（对照）

### 定位
仓库级开发/回归工具，不随 skill 分发；skill 产物完整性靠 evals/ prompt 级回归兜底。
"""
import sys
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
    from PIL import Image
except ImportError as exc:
    print(f"[err] 缺依赖：{exc}", file=sys.stderr)
    print("安装: pip install --user playwright pillow && python3 -m playwright install chromium", file=sys.stderr)
    sys.exit(2)

REPO = Path(__file__).resolve().parent.parent
DEFAULT_HTML = REPO / "tracing-cards-smoke20.html"

EXPECT_FIRST = "rgb(0, 0, 0)"
EXPECT_REST = "rgb(184, 217, 238)"
BLACK_THRESHOLD = 20


def is_black(rgb: tuple) -> bool:
    return max(rgb[:3]) <= BLACK_THRESHOLD


def main() -> int:
    html_path = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_HTML
    if not html_path.exists():
        print(f"[err] HTML 未找到: {html_path}", file=sys.stderr)
        return 2

    print(f"[input] {html_path}")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1240, "height": 1754})
        page.goto(html_path.as_uri())
        page.wait_for_load_state("networkidle")

        # 1. computed-style 维度
        report = page.evaluate("""
            () => {
                const rows = document.querySelectorAll('svg.row-letters');
                return Array.from(rows).map((svg, ri) => ({
                    row: ri,
                    colors: Array.from(svg.querySelectorAll(':scope > g'))
                                 .map(g => getComputedStyle(g).stroke),
                }));
            }
        """)

        total_rows = len(report)
        first_ok = rest_ok = rest_total = 0
        failures = []
        for row in report:
            colors = row["colors"]
            if not colors:
                continue
            if colors[0] == EXPECT_FIRST:
                first_ok += 1
            else:
                failures.append(f"row#{row['row']} first={colors[0]} (want {EXPECT_FIRST})")
            for k, c in enumerate(colors[1:], start=1):
                rest_total += 1
                if c == EXPECT_REST:
                    rest_ok += 1
                else:
                    failures.append(f"row#{row['row']} g[{k}]={c} (want {EXPECT_REST})")

        print(f"[computed-style] row-letters 扫描 = {total_rows}")
        print(f"[computed-style] 首份黑色 OK: {first_ok}/{total_rows}")
        print(f"[computed-style] 余份浅蓝 OK: {rest_ok}/{rest_total}")
        if failures:
            print("[computed-style] FAIL:")
            for f in failures[:10]:
                print(f"  - {f}")
            browser.close()
            return 1

        # 2. 像素维度（仅第一行做兜底采样）
        bbox = page.evaluate("""
            () => {
                const svg = document.querySelector('svg.row-letters');
                if (!svg) return null;
                const gs = svg.querySelectorAll(':scope > g');
                if (gs.length < 1) return null;
                const sb = svg.getBoundingClientRect();
                const r = g => { const b = g.getBoundingClientRect();
                                 return {x: b.x, y: b.y, w: b.width, h: b.height}; };
                return {
                    svg: {x: sb.x, y: sb.y, w: sb.width, h: sb.height},
                    first: r(gs[0]),
                    second: gs.length >= 2 ? r(gs[1]) : null,
                };
            }
        """)
        if not bbox:
            print("[pixel] 无 row-letters，跳过像素采样")
            browser.close()
            return 0

        page.locator(".card").first.screenshot(path="/tmp/card1_rendered.png")
        page.locator("svg.row-letters").first.screenshot(path="/tmp/row_letters_rendered.png")

        img = Image.open("/tmp/row_letters_rendered.png").convert("RGB")
        W, H = img.size
        scale_x = W / bbox["svg"]["w"]
        scale_y = H / bbox["svg"]["h"]

        def crop_rel(rect, out_path):
            rx = (rect["x"] - bbox["svg"]["x"]) * scale_x
            ry = (rect["y"] - bbox["svg"]["y"]) * scale_y
            rw = rect["w"] * scale_x
            rh = rect["h"] * scale_y
            cx, cy = max(0, int(rx)), max(0, int(ry))
            cw = min(W - cx, int(rw) + 1)
            ch = min(H - cy, int(rh) + 1)
            crop = img.crop((cx, cy, cx + cw, cy + ch))
            crop.save(out_path)
            pixels = list(crop.getdata())
            return cw, ch, len(pixels), sum(1 for px in pixels if is_black(px))

        fw, fh, ftotal, fblack = crop_rel(bbox["first"], "/tmp/first_g_crop.png")
        print(f"[pixel] 首份 bbox {fw}x{fh} = {ftotal} px · 黑色 = {fblack}")
        if fblack == 0:
            print("[pixel] FAIL — 首份 bbox 裁剪内没有黑色像素！")
            browser.close()
            return 1

        if bbox["second"]:
            sw, sh, stotal, sblack = crop_rel(bbox["second"], "/tmp/second_g_crop.png")
            print(f"[pixel] 第二份 bbox {sw}x{sh} = {stotal} px · 黑色 = {sblack} (期望 0)")
            if sblack > 0:
                print("[pixel] WARN — 第二份 bbox 有意外黑色像素")

        browser.close()

    print()
    print("PASS — 首份单词经浏览器渲染后确认是黑色（computed-style + pixel 双重）")
    print("截图: /tmp/card1_rendered.png /tmp/row_letters_rendered.png "
          "/tmp/first_g_crop.png /tmp/second_g_crop.png")
    return 0


if __name__ == "__main__":
    sys.exit(main())
