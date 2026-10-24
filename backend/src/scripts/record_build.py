"""Hash the tested code/configuration without reading secrets or runtime data."""

import hashlib
import json
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parents[3]
    paths: set[Path] = set()
    for folder in (
        "backend/src",
        "backend/data",
        "backend/tests",
        "backend/scripts",
        "backend/migrations",
        "frontend/app",
        "frontend/tests",
        "frontend/scripts",
    ):
        paths.update(
            path
            for path in (root / folder).rglob("*")
            if path.is_file()
            and path.suffix in {".py", ".ts", ".tsx", ".mjs", ".css", ".json", ".pdf"}
        )
    for name in (
        "backend/pyproject.toml",
        "backend/uv.lock",
        "backend/Dockerfile",
        "backend/.dockerignore",
        "backend/alembic.ini",
        "frontend/package.json",
        "frontend/Dockerfile",
        "frontend/.dockerignore",
        "docker-compose.yml",
        "frontend/package-lock.json",
        "frontend/tsconfig.json",
        "frontend/next.config.ts",
        "frontend/playwright.config.ts",
        ".github/workflows/ci.yml",
    ):
        paths.add(root / name)
    files = {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(paths)
    }
    fingerprint = hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()
    target = root / "docs/event/BUILD_MANIFEST.json"
    target.write_text(
        json.dumps(
            {
                "scope": "code/configuration only; no credentials or runtime data",
                "sha256": fingerprint,
                "files": files,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Build fingerprint: {fingerprint}")


if __name__ == "__main__":
    main()
