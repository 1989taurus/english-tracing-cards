#!/usr/bin/env python3
"""Convert a tracing-cards HTML worksheet to a visually-identical A4 PDF.

双后端策略：
  1. 优先：系统 Chrome / Chromium（--headless=new --print-to-pdf）
  2. 降级：Playwright（pip install playwright + playwright install chromium）
  3. 都没有：退出码 1，打印平台相关安装提示

PDF 生成成功后，默认把 PDF 送系统打印队列（CUPS `lp`）。
  - 无 `lp` / 无可用打印机 → stderr 软降级通知，不影响退出码。
  - `TRACING_CARDS_AUTO_PRINT=0` 或 `--no-print` 禁用自动打印。
  - `TRACING_CARDS_PRINTER=<name>` 指定打印机（否则用系统默认）。

退出码：
  0  成功
  1  没有可用后端
  2  后端启动但产物无效（尺寸过小 / 文件缺失）
  3  参数或输入错误
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# 最小产物尺寸阈值：低于这个值几乎肯定是静默失败
MIN_PDF_BYTES = 1024

# shutil.which 找不到的 macOS 应用路径
MAC_CHROME_PATHS = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]

# PATH 上的候选二进制名，按优先级
CHROME_BIN_CANDIDATES = [
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
    "chrome",
    "microsoft-edge",
    "msedge",
]


def find_chrome(override: str | None = None) -> str | None:
    """返回 Chrome 家族二进制路径；找不到返回 None。"""
    if override:
        return override if Path(override).exists() else None

    env_override = os.environ.get("TRACING_CARDS_BROWSER")
    if env_override and Path(env_override).exists():
        return env_override

    for name in CHROME_BIN_CANDIDATES:
        path = shutil.which(name)
        if path:
            return path

    if sys.platform == "darwin":
        for path in MAC_CHROME_PATHS:
            if Path(path).exists():
                return path

    return None


def has_color_emoji_font() -> bool:
    """Linux 专用：探测是否装了彩色 emoji 字体。macOS/Windows 默认有。"""
    if sys.platform != "linux":
        return True
    try:
        out = subprocess.run(
            ["fc-list", ":", "family"],
            capture_output=True, text=True, timeout=5,
        ).stdout.lower()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return True  # fc-list 都没有，判断不出来，不要误报
    return any(
        marker in out
        for marker in ("color emoji", "noto color emoji", "apple color emoji")
    )


def is_root() -> bool:
    """Unix 下是否以 root 身份运行（容器场景要加 --no-sandbox）。"""
    return hasattr(os, "geteuid") and os.geteuid() == 0


def render_with_chrome(chrome: str, html_path: Path, pdf_path: Path) -> None:
    """跑 Chrome --headless=new --print-to-pdf。失败 raise RuntimeError。"""
    with tempfile.TemporaryDirectory(prefix="tracing-cards-chrome-") as tmp_udd:
        cmd = [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--no-pdf-header-footer",
            "--hide-scrollbars",
            "--virtual-time-budget=5000",
            f"--user-data-dir={tmp_udd}",
            f"--print-to-pdf={pdf_path}",
            html_path.absolute().as_uri(),
        ]
        if is_root():
            cmd.insert(1, "--no-sandbox")

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            tail = (result.stderr or "")[-800:]
            raise RuntimeError(
                f"chrome exited {result.returncode}\n--- stderr tail ---\n{tail}"
            )


def render_with_playwright(html_path: Path, pdf_path: Path) -> None:
    """Playwright 降级路径。未安装抛 ImportError。"""
    from playwright.sync_api import sync_playwright  # type: ignore

    launch_args = ["--no-sandbox"] if is_root() else []
    with sync_playwright() as p:
        browser = p.chromium.launch(args=launch_args)
        try:
            page = browser.new_page()
            page.goto(html_path.absolute().as_uri(), wait_until="networkidle")
            page.pdf(
                path=str(pdf_path),
                format="A4",
                margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
                print_background=True,
            )
        finally:
            browser.close()


def validate_output(pdf_path: Path) -> None:
    """防 Chrome 静默失败：产物必须存在且非平凡尺寸。"""
    if not pdf_path.exists():
        raise RuntimeError(f"output {pdf_path} was not created")
    size = pdf_path.stat().st_size
    if size < MIN_PDF_BYTES:
        raise RuntimeError(
            f"output {pdf_path} is only {size} bytes (<{MIN_PDF_BYTES}); "
            "conversion likely failed silently"
        )


# 强制 lpstat 走 C locale，避免中文等本地化输出把字串匹配搞歪
_C_LOCALE_ENV = {**os.environ, "LC_ALL": "C", "LANG": "C"}


def get_default_printer() -> str | None:
    """查询 CUPS 默认打印机名；无默认或 lpstat 不可用返回 None。"""
    try:
        result = subprocess.run(
            ["lpstat", "-d"], capture_output=True, text=True, timeout=5,
            env=_C_LOCALE_ENV,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    # 输出形如：`system default destination: HP_LaserJet` 或 `no system default destination`
    for line in result.stdout.splitlines():
        if "default destination:" in line and "no system default" not in line:
            return line.split(":", 1)[1].strip() or None
    return None


def list_available_printers() -> list[str]:
    """列出 CUPS 里"accepting"状态的打印机；lpstat 不可用返回空列表。"""
    try:
        result = subprocess.run(
            ["lpstat", "-p"], capture_output=True, text=True, timeout=5,
            env=_C_LOCALE_ENV,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return []
    printers: list[str] = []
    for line in result.stdout.splitlines():
        # 输出形如：`printer HP_LaserJet is idle.  enabled since ...`
        if line.startswith("printer ") and "disabled" not in line:
            parts = line.split()
            if len(parts) >= 2:
                printers.append(parts[1])
    return printers


def auto_print_pdf(pdf_path: Path, disabled: bool = False) -> None:
    """PDF 成功后送系统打印队列。任何失败仅 stderr 通知，不抛异常。

    跳过条件（按优先级）：
      1. disabled=True（来自 --no-print）
      2. TRACING_CARDS_AUTO_PRINT=0
      3. 系统没有 lp 命令
      4. 没有可用打印机
    """
    if disabled or os.environ.get("TRACING_CARDS_AUTO_PRINT") == "0":
        print("[info] 自动打印已禁用（--no-print 或 TRACING_CARDS_AUTO_PRINT=0）", file=sys.stderr)
        return

    lp = shutil.which("lp")
    if lp is None:
        print("[info] 未找到 CUPS `lp` 命令，跳过自动打印。PDF 已生成可手动打印。", file=sys.stderr)
        return

    printer = os.environ.get("TRACING_CARDS_PRINTER") or get_default_printer()
    if printer is None:
        available = list_available_printers()
        if not available:
            print("[info] 无可用打印机，跳过自动打印。PDF 已生成可手动打印。", file=sys.stderr)
            return
        printer = available[0]

    cmd = [lp, "-d", printer, str(pdf_path)]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    except subprocess.TimeoutExpired:
        print(f"[warn] lp 超时（15s），打印请求未确认。打印机：{printer}", file=sys.stderr)
        return

    if result.returncode == 0:
        job_id = (result.stdout or "").strip() or f"(printer={printer})"
        print(f"[ok] 已送打印机队列：{job_id}", file=sys.stderr)
    else:
        tail = (result.stderr or result.stdout or "")[-400:]
        print(f"[warn] lp 返回码 {result.returncode}，打印可能失败：\n{tail}", file=sys.stderr)


def print_install_hints() -> None:
    """两个后端都缺时的安装提示，打到 stderr。"""
    print("ERROR: no PDF backend available.", file=sys.stderr)
    print("", file=sys.stderr)
    if sys.platform == "darwin":
        print("Option A (recommended) — install Google Chrome:", file=sys.stderr)
        print("    brew install --cask google-chrome", file=sys.stderr)
    elif sys.platform == "linux":
        print("Option A (recommended) — install Chromium or Chrome:", file=sys.stderr)
        print("    sudo apt install chromium-browser       # Debian/Ubuntu", file=sys.stderr)
        print("    sudo dnf install chromium               # Fedora", file=sys.stderr)
    else:
        print("Option A — install Google Chrome from https://www.google.com/chrome/", file=sys.stderr)
    print("", file=sys.stderr)
    print("Option B — Playwright (no sudo required, works in sandboxes):", file=sys.stderr)
    print("    pip install --user playwright", file=sys.stderr)
    print("    python -m playwright install chromium", file=sys.stderr)


def main() -> int:
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8+ required", file=sys.stderr)
        return 3

    parser = argparse.ArgumentParser(
        description="Convert tracing-cards HTML worksheet to A4 PDF.",
    )
    parser.add_argument("input", type=Path, help="Input HTML file")
    parser.add_argument(
        "-o", "--output", type=Path, default=None,
        help="Output PDF path (default: replace .html with .pdf)",
    )
    parser.add_argument(
        "--browser", type=str, default=None,
        help="Override path to Chrome/Chromium binary",
    )
    parser.add_argument(
        "--no-print", action="store_true",
        help="Skip auto-printing to system default printer after PDF is generated",
    )
    args = parser.parse_args()

    if not args.input.exists():
        print(f"ERROR: input file {args.input} not found", file=sys.stderr)
        return 3
    if args.input.suffix.lower() != ".html":
        print(f"ERROR: input must be an .html file, got {args.input.suffix}", file=sys.stderr)
        return 3

    out = args.output or args.input.with_suffix(".pdf")
    out.parent.mkdir(parents=True, exist_ok=True)

    # Linux emoji 字体软警告
    if not has_color_emoji_font():
        print(
            "WARNING: no color emoji font detected on this Linux system. "
            "PDF will render emoji in monochrome outline. "
            "Fix on Debian/Ubuntu: sudo apt install fonts-noto-color-emoji",
            file=sys.stderr,
        )

    chrome = find_chrome(args.browser)

    # 后端 1：系统 Chrome
    if chrome:
        try:
            print(f"Rendering with Chrome: {chrome}", file=sys.stderr)
            render_with_chrome(chrome, args.input, out)
            validate_output(out)
            print(f"wrote {out} ({out.stat().st_size // 1024} KB)", file=sys.stderr)
            auto_print_pdf(out, disabled=args.no_print)
            return 0
        except Exception as e:
            print(f"Chrome backend failed: {e}", file=sys.stderr)
            print("Trying Playwright fallback...", file=sys.stderr)

    # 后端 2：Playwright
    try:
        print("Rendering with Playwright...", file=sys.stderr)
        render_with_playwright(args.input, out)
        validate_output(out)
        print(f"wrote {out} ({out.stat().st_size // 1024} KB)", file=sys.stderr)
        auto_print_pdf(out, disabled=args.no_print)
        return 0
    except ImportError:
        if chrome is None:
            print_install_hints()
            return 1
        # Chrome 试过了但失败；Playwright 也没装 → 无救
        print("Playwright not installed; Chrome backend already failed above.", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Playwright backend failed: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
