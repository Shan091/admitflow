"""Download only local PDF layout/table assets; no OCR, generation or document inputs."""

import argparse
import hashlib
import json
import logging
import os
from importlib import import_module
from importlib.metadata import version
from pathlib import Path


def prepare(target: Path) -> None:
    import_module("cv2")  # TableFormer's headless image runtime must exist before setup succeeds.
    import_module("rtree")
    os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
    os.environ["HF_HUB_DISABLE_IMPLICIT_TOKEN"] = "1"
    from docling.utils.model_downloader import download_models

    target.mkdir(parents=True, exist_ok=True)
    download_models(
        output_dir=target,
        with_layout=True,
        with_tableformer=True,
        with_code_formula=False,
        with_picture_classifier=False,
        with_rapidocr=False,
        progress=False,
    )
    files = {
        path.relative_to(target).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in target.rglob("*")
        if path.is_file()
        and not any(part.startswith(".") for part in path.relative_to(target).parts)
    }
    if not files:
        raise RuntimeError("Document model download produced no assets")
    marker = target / ".ready.json.tmp"
    marker.write_text(
        json.dumps({"package": version("docling-slim"), "files": files}, indent=2), encoding="utf-8"
    )
    marker.replace(target / ".ready.json")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--assets", type=Path, default=Path(".runtime/document-models"))
    args = parser.parse_args()
    logging.basicConfig(level=logging.ERROR)
    try:
        prepare(args.assets.resolve())
    except Exception as error:
        print(
            f"Document model preparation failed: {type(error).__name__}; no document was processed."
        )
        raise SystemExit(1) from None
    print("Local layout and table assets are ready. OCR and generation models were not downloaded.")


if __name__ == "__main__":
    main()
