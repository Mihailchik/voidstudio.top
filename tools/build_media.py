#!/usr/bin/env python3
"""Собирает витрину работ из библиотеки Poster_2.0 в статические файлы сайта.

Источник — рабочий проект, который живёт отдельно:
  ~/Trae_PJ/Poster_2.0/library/void-studio/<NNN>/   — файлы работ
  ~/Trae_PJ/Poster_2.0/data/void-studio/*.sqlite3   — названия, тексты, ссылки

Результат — то, что коммитится в этот репозиторий:
  assets/media/<NNN>/thumb.webp  — превью для сетки
  assets/media/<NNN>/full.webp   — картинка для лайтбокса (у работ-картинок)
  assets/media/<NNN>/video.mp4   — видео 540p без звука (у работ-видео)
  data/works.json                — метаданные витрины

Запуск:
  python3 tools/build_media.py --thumbs-only --limit 12   # лёгкий набор под дизайн
  python3 tools/build_media.py                            # полная сборка витрины

Полная сборка весит порядка 34 МБ, поэтому на время работы над дизайном в
репозитории живёт только --thumbs-only: превью по ~25 КБ и никакого видео.

Скрипт идемпотентный: уже собранные файлы пропускаются, если исходник не новее.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE = Path.home() / "Trae_PJ" / "Poster_2.0"

THUMB_WIDTH = 640
FULL_WIDTH = 1200
VIDEO_WIDTH = 540
VIDEO_CRF = 32
WEBP_QUALITY = 74

# Чем раньше в списке, тем выше приоритет как исходника кадра.
IMAGE_CANDIDATES = (
    "original.png", "original.jpg", "original.jpeg", "original.webp",
    "source.png", "source.jpg", "source.jpeg", "source.webp",
    "instagram-post.png", "telegram-post.png", "pikabu-image.png",
)

# Порядок каналов в карточке. Совпадает с тем, как проект их называет.
CHANNEL_ORDER = ("youtube", "instagram", "telegram", "pikabu")
CHANNEL_LABEL = {
    "youtube": "YouTube",
    "instagram": "Instagram",
    "telegram": "Telegram",
    "pikabu": "Pikabu",
}


def run(cmd: list[str]) -> None:
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{cmd[0]} упал: {r.stderr.strip()[:400]}")


def newer(src: Path, dst: Path, force: bool) -> bool:
    """Нужно ли пересобирать dst."""
    if force or not dst.exists():
        return True
    return src.stat().st_mtime > dst.stat().st_mtime


def to_webp(src: Path, dst: Path, width: int) -> None:
    """PNG/JPEG любого размера -> webp фиксированной ширины."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_suffix(".tmp.png")
    run(["ffmpeg", "-y", "-v", "error", "-i", str(src),
         "-vf", f"scale={width}:-2:flags=lanczos", str(tmp)])
    run(["cwebp", "-quiet", "-q", str(WEBP_QUALITY), str(tmp), "-o", str(dst)])
    tmp.unlink(missing_ok=True)


def frame_from_video(src: Path, dst_png: Path) -> None:
    """Кадр для превью: секунда от начала, чтобы не попасть на затемнение."""
    dst_png.parent.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-y", "-v", "error", "-ss", "1", "-i", str(src),
         "-frames:v", "1", str(dst_png)])


def compress_video(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-y", "-v", "error", "-i", str(src),
         "-vf", f"scale={VIDEO_WIDTH}:-2:flags=lanczos",
         "-c:v", "libx264", "-crf", str(VIDEO_CRF), "-preset", "slow",
         "-profile:v", "main", "-pix_fmt", "yuv420p",
         "-movflags", "+faststart", "-an", str(dst)])


def probe_size(path: Path) -> tuple[int, int]:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "csv=p=0:s=x", str(path)],
        capture_output=True, text=True)
    w, _, h = r.stdout.strip().partition("x")
    return int(w), int(h)


def load_metadata(source: Path) -> tuple[dict, dict, dict]:
    """Идеи и ссылки по idea_id + карта «папка библиотеки -> idea_id».

    Карта нужна потому, что manifest.json есть не у всех папок: у работ-картинок
    его нет вовсе, и единственный надёжный мостик — таблица files.
    """
    db_path = source / "data" / "void-studio" / "void-studio.sqlite3"
    db = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    db.row_factory = sqlite3.Row

    ideas = {r["id"]: dict(r) for r in
             db.execute("select id, title, text, status from ideas")}

    links: dict[int, list[dict]] = {}
    rows = db.execute("""
        select f.idea_id as iid, dl.channel as ch, dl.permalink as url
        from delivery_log dl
        join jobs j  on j.id = dl.job_id
        join files f on f.id = j.file_id
        where dl.permalink is not null and dl.status = 'active'
    """)
    for r in rows:
        if r["iid"] is None:
            continue
        bucket = links.setdefault(r["iid"], [])
        # Stories живут сутки — в постоянной витрине им не место.
        if "/stories/" in r["url"]:
            continue
        if any(x["channel"] == r["ch"] for x in bucket):
            continue
        bucket.append({"channel": r["ch"], "url": r["url"]})

    for bucket in links.values():
        bucket.sort(key=lambda x: CHANNEL_ORDER.index(x["channel"])
                    if x["channel"] in CHANNEL_ORDER else 99)

    by_folder: dict[str, int] = {}
    for r in db.execute("select idea_id, path from files where idea_id is not null"):
        parts = Path(r["path"]).parts
        if len(parts) >= 2:
            by_folder.setdefault(parts[-2], r["idea_id"])

    db.close()
    return ideas, links, by_folder


def build(source: Path, force: bool, thumbs_only: bool, limit: int | None) -> None:
    library = source / "library" / "void-studio"
    if not library.is_dir():
        sys.exit(f"Библиотека не найдена: {library}")

    ideas, links, by_folder = load_metadata(source)
    media_root = SITE / "assets" / "media"
    works = []

    folders = sorted((p for p in library.iterdir() if p.is_dir()), reverse=True)
    if limit:
        folders = folders[:limit]

    for folder in folders:
        slug = folder.name
        manifest = folder / "manifest.json"
        idea_id = None
        if manifest.exists():
            idea_id = json.loads(manifest.read_text()).get("idea_id")
        if idea_id is None:
            idea_id = by_folder.get(slug)
        idea = ideas.get(idea_id, {})
        title = (idea.get("title") or "").strip()
        if not title:
            print(f"  пропуск {slug}: нет названия")
            continue

        out = media_root / slug
        video_src = folder / "video.mp4"
        entry = {
            "slug": slug,
            "title": title,
            "text": (idea.get("text") or "").strip(),
            "links": links.get(idea_id, []),
        }

        if video_src.exists():
            # Кадр для сетки: готовый poster.jpg, иначе вытаскиваем из видео.
            poster = folder / "poster.jpg"
            if not poster.exists():
                poster = out / "_frame.png"
                if newer(video_src, poster, force):
                    frame_from_video(video_src, poster)
            if newer(poster, out / "thumb.webp", force):
                to_webp(poster, out / "thumb.webp", THUMB_WIDTH)
            entry["kind"] = "video"
            if thumbs_only:
                (out / "video.mp4").unlink(missing_ok=True)
            else:
                if newer(video_src, out / "video.mp4", force):
                    print(f"  {slug} · видео")
                    compress_video(video_src, out / "video.mp4")
                entry["video"] = f"assets/media/{slug}/video.mp4"
            (out / "_frame.png").unlink(missing_ok=True)
        else:
            picture = next((folder / n for n in IMAGE_CANDIDATES
                            if (folder / n).exists()), None)
            if picture is None:
                print(f"  пропуск {slug}: нет пригодного файла")
                continue
            if newer(picture, out / "thumb.webp", force):
                to_webp(picture, out / "thumb.webp", THUMB_WIDTH)
            entry["kind"] = "image"
            if thumbs_only:
                (out / "full.webp").unlink(missing_ok=True)
            else:
                if newer(picture, out / "full.webp", force):
                    to_webp(picture, out / "full.webp", FULL_WIDTH)
                entry["full"] = f"assets/media/{slug}/full.webp"

        entry["thumb"] = f"assets/media/{slug}/thumb.webp"
        w, h = probe_size(media_root / slug / "thumb.webp")
        entry["ratio"] = round(w / h, 4)
        works.append(entry)

    # Новые работы — сверху.
    works.sort(key=lambda w: w["slug"], reverse=True)

    data_dir = SITE / "data"
    data_dir.mkdir(exist_ok=True)
    (data_dir / "works.json").write_text(
        json.dumps({"works": works}, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")

    # Папки, оставшиеся от удалённых работ, чистим — иначе репозиторий пухнет.
    alive = {w["slug"] for w in works}
    for stale in media_root.iterdir() if media_root.exists() else []:
        if stale.is_dir() and stale.name not in alive:
            shutil.rmtree(stale)
            print(f"  удалено лишнее: {stale.name}")

    size = sum(f.stat().st_size for f in media_root.rglob("*") if f.is_file())
    videos = sum(1 for w in works if w["kind"] == "video")
    print(f"\nГотово: {len(works)} работ ({videos} видео, "
          f"{len(works) - videos} картинок), медиа {size / 2**20:.1f} МБ")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", type=Path, default=DEFAULT_SOURCE,
                    help="каталог Poster_2.0")
    ap.add_argument("--force", action="store_true",
                    help="пересобрать всё, игнорируя даты файлов")
    ap.add_argument("--thumbs-only", action="store_true",
                    help="только превью: без видео и полных картинок")
    ap.add_argument("--limit", type=int,
                    help="взять только N самых свежих работ")
    args = ap.parse_args()
    build(args.source.expanduser(), args.force, args.thumbs_only, args.limit)
