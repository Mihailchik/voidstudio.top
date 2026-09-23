#!/usr/bin/env python3
"""Собирает карточку проекта для страницы студии из скриншотов приложения.

Нужен, чтобы при обновлении скриншотов не подбирать смещения руками:
меняешь файлы — прогоняешь команду — карточка пересобрана.

Примеры:
  # два экрана рядом на светлой подложке (как у FitTimer)
  python3 tools/build_project_card.py --out assets/project-fittimer.jpg \\
      ~/Trae_PJ/FL_Timer/docs/FitTimer_Ru2.png ~/Trae_PJ/FL_Timer/docs/FitTimer_Ru3.png

  # один экран крупно, тёмная подложка, со скруглением углов
  python3 tools/build_project_card.py --out assets/card.jpg --layout single \\
      --bg 111111 --radius 48 ~/Trae_PJ/FL_Timer/docs/FitTimer_Ru2.png

Раскладки:
  pair    два экрана рядом, второй чуть ниже
  single  один экран по центру, крупно
  stack   экраны внахлёст, как стопка карточек

Требуется ffmpeg.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

CARD_W, CARD_H = 1600, 1300


def run(cmd: list[str]) -> None:
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"ffmpeg не справился:\n{r.stderr.strip()[:600]}")


def probe(path: Path) -> tuple[int, int]:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "csv=p=0:s=x", str(path)],
        capture_output=True, text=True)
    if r.returncode != 0 or "x" not in r.stdout:
        sys.exit(f"не читается как изображение: {path}")
    w, _, h = r.stdout.strip().partition("x")
    return int(w), int(h)


def rounded(index: int, radius: int) -> str:
    """Скругление углов через geq по альфе. Без него у скриншота острые углы."""
    if radius <= 0:
        return f"[{index}:v]null"
    r = radius
    # Сравнения пишем через lt(): знак «меньше» ffmpeg в выражениях не понимает.
    inside = (f"if(lt(X,{r})*lt(Y,{r}), lt(hypot({r}-X,{r}-Y),{r}),"
              f" if(gt(X,W-{r})*lt(Y,{r}), lt(hypot(X-(W-{r}),{r}-Y),{r}),"
              f" if(lt(X,{r})*gt(Y,H-{r}), lt(hypot({r}-X,Y-(H-{r})),{r}),"
              f" if(gt(X,W-{r})*gt(Y,H-{r}), lt(hypot(X-(W-{r}),Y-(H-{r})),{r}), 1))))")
    return f"[{index}:v]format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*({inside})'"


def build(shots: list[Path], out: Path, layout: str, bg: str, radius: int) -> None:
    if layout == "single" and len(shots) != 1:
        sys.exit("для раскладки single нужен ровно один файл")
    if layout in ("pair", "stack") and len(shots) != 2:
        sys.exit(f"для раскладки {layout} нужно ровно два файла")

    inputs: list[str] = []
    for s in shots:
        inputs += ["-i", str(s)]

    # Высота экрана и его место на холсте — по раскладке.
    if layout == "single":
        plan = [(1, 1150, "(W-w)/2", "(H-h)/2")]
    elif layout == "pair":
        plan = [(1, 1080, "250", "110"), (2, 1080, "850", "110")]
    else:  # stack
        plan = [(1, 1000, "300", "60"), (2, 1000, "760", "230")]

    chains, last = [], "[bg]"
    for n, (idx, height, x, y) in enumerate(plan):
        chains.append(f"{rounded(idx, radius)},scale=-1:{height}:flags=lanczos[s{n}]")
        nxt = f"[v{n}]" if n < len(plan) - 1 else "[out]"
        chains.append(f"{last}[s{n}]overlay={x}:{y}{nxt}")
        last = f"[v{n}]"

    graph = f"color=c=0x{bg}:s={CARD_W}x{CARD_H}[bg];" + ";".join(chains)
    out.parent.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", f"color=c=0x{bg}:s={CARD_W}x{CARD_H}",
         *inputs, "-filter_complex", graph.split(";", 1)[1], "-map", "[out]",
         "-frames:v", "1", "-q:v", "4", str(out)])

    size = out.stat().st_size / 1024
    print(f"готово: {out} — {CARD_W}×{CARD_H}, {size:.0f} КБ, раскладка {layout}")


if __name__ == "__main__":
    if not shutil.which("ffmpeg"):
        sys.exit("нужен ffmpeg")
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("shots", nargs="+", type=Path, help="скриншоты приложения")
    ap.add_argument("--out", type=Path, required=True, help="куда положить карточку")
    ap.add_argument("--layout", choices=("pair", "single", "stack"), default="pair")
    ap.add_argument("--bg", default="ece7f7", help="цвет подложки, hex без решётки")
    ap.add_argument("--radius", type=int, default=0, help="скругление углов экрана, px")
    a = ap.parse_args()
    for s in a.shots:
        if not s.exists():
            sys.exit(f"нет файла: {s}")
        probe(s)
    build(a.shots, a.out, a.layout, a.bg.lstrip("#"), a.radius)
