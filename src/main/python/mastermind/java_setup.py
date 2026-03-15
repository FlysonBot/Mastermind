"""
Ensures the JRE and JAR are available before the program starts.
Returns (jre_path, jar_path) — jre_path is None on Android (system JDK used directly).

On Android (Termux): requires openjdk-21 via `pkg install openjdk-21`.
On other platforms:  uses the bundled JRE zip if available, else downloads a JDK
                     and builds a trimmed JRE into target/mastermind-jre.
"""

import platform
import shutil
import subprocess
import sys
import time
import zipfile
from pathlib import Path

from mastermind.ui import console

# --- Paths ---

_PKG = Path(__file__).parent
_ROOT = _PKG.parents[3]  # repo root, only valid in dev (not in installed package)
_SRC_JAVA = _ROOT / "src" / "main" / "java"
_CLASSES = _ROOT / "target" / "classes"
_JDK = _ROOT / "target" / "java-jdk"
_BUNDLED_JAR = _PKG / "mastermind-solver.jar"
_BUNDLED_JRE = _PKG / "jre"
_CACHED_JRE = _PKG / "mastermind-jre"

# --- Platform config ---

_PLATFORM_MAP = {
    ("linux", "x86_64"): "linux-x64",
    ("linux", "amd64"): "linux-x64",
    ("windows", "amd64"): "windows-x64",
    ("windows", "x86_64"): "windows-x64",
    ("darwin", "x86_64"): "mac-x64",
    ("darwin", "amd64"): "mac-x64",
    ("darwin", "arm64"): "mac-aarch64",
    ("darwin", "aarch64"): "mac-aarch64",
}


# --- Public API ---


def ensure_ready():
    """Return (jre_path, jar_path), setting up whatever is missing."""
    if platform.system().lower() == "android":
        return _ensure_android()
    return _ensure_desktop()


# --- Platform-specific setup ---


def _ensure_android():
    """On Android/Termux, verify the system JDK is present and return (None, jar)."""
    if not shutil.which("java"):
        console.print("[red]Java is not installed.[/red] Please run:")
        console.print("    [cyan]pkg install openjdk-21[/cyan]")
        sys.exit(1)

    if not _BUNDLED_JAR.exists():
        console.print(
            "[red]Bundled JAR not found.[/red] Please re-clone or re-download the repository."
        )
        sys.exit(1)

    console.print(
        "[yellow]Note:[/yellow] You're currently running this application on Android. "
        "openjdk-21 has a known bug on this platform that may cause occasional pointer tag "
        "crashes. This is not a bug in this application and cannot be fixed. If it happens, "
        "simply restart the app."
    )

    return None, _BUNDLED_JAR


def _ensure_desktop():
    """Return (jre, jar), extracting or building the JRE/JAR as needed."""
    jre_path = _resolve_jre()
    jar_path = _BUNDLED_JAR if _BUNDLED_JAR.exists() else None

    if jre_path and jar_path:
        return jre_path, jar_path

    # Fallback: download a JDK to build whatever is missing
    _download_jdk()
    try:
        if not jre_path:
            _build_jre()
            jre_path = _CACHED_JRE

        if not jar_path:
            _build_jar()
            jar_path = _BUNDLED_JAR
    finally:
        shutil.rmtree(_JDK, ignore_errors=True)

    return jre_path, jar_path


def _resolve_jre():
    """Return the JRE path if ready, extracting the bundled zip if needed."""
    if _CACHED_JRE.exists():
        return _CACHED_JRE

    os_name = platform.system().lower()
    arch = platform.machine().lower()
    name = _PLATFORM_MAP.get((os_name, arch))

    if name:
        zip_path = _BUNDLED_JRE / f"{name}.zip"
        if zip_path.exists():
            _extract_jre(zip_path)
            return _CACHED_JRE

    return None


# --- JRE extraction ---


def _extract_jre(zip_path: Path):
    t = time.time()
    with console.status(f"Extracting JRE from [cyan]{zip_path.name}[/cyan]..."):
        _CACHED_JRE.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(_CACHED_JRE)

        # Restore execute permissions on binaries (lost during zip on Unix)
        for f in (_CACHED_JRE / "bin").iterdir():
            f.chmod(f.stat().st_mode | 0o111)

    console.print(f"[green]✓[/green] JRE extracted. ({time.time() - t:.1f}s)")


# --- Fallback: build from downloaded JDK ---


def _download_jdk():
    import jdk  # install-jdk library

    t = time.time()
    with console.status("Downloading JDK..."):
        jdk.install(version="21", path=str(_JDK))
    size_mb = (
        sum(f.stat().st_size for f in _JDK.rglob("*") if f.is_file()) / 1024 / 1024
    )
    console.print(
        f"[green]✓[/green] JDK ready. ({time.time() - t:.1f}s, {size_mb:.0f} MB)"
    )


def _build_jre():
    jlink = next(_JDK.rglob("jlink"), None)
    if not jlink:
        raise RuntimeError("jlink not found in downloaded JDK")

    t = time.time()
    with console.status("Building trimmed JRE..."):
        subprocess.run(
            [
                str(jlink),
                "--add-modules",
                "java.base",
                "--output",
                str(_CACHED_JRE),
                "--strip-debug",
                "--no-header-files",
                "--no-man-pages",
            ],
            check=True,
        )
    console.print(f"[green]✓[/green] JRE ready. ({time.time() - t:.1f}s)")


def _build_jar():
    javac = next(_JDK.rglob("javac"), None)
    jar_tool = next(_JDK.rglob("jar"), None)
    if not javac:
        raise RuntimeError("javac not found in downloaded JDK")
    if not jar_tool:
        raise RuntimeError("jar not found in downloaded JDK")

    sources = [str(p) for p in _SRC_JAVA.rglob("*.java")]
    _CLASSES.mkdir(parents=True, exist_ok=True)
    _BUNDLED_JAR.parent.mkdir(parents=True, exist_ok=True)

    t = time.time()
    with console.status("Compiling Java sources..."):
        subprocess.run([str(javac), "-d", str(_CLASSES)] + sources, check=True)
        subprocess.run(
            [
                str(jar_tool),
                "--create",
                "--file",
                str(_BUNDLED_JAR),
                "-C",
                str(_CLASSES),
                ".",
            ],
            check=True,
        )
    console.print(f"[green]✓[/green] JAR ready. ({time.time() - t:.1f}s)")


if __name__ == "__main__":
    jre, jar = ensure_ready()
    console.print(f"JRE: {jre}")
    console.print(f"JAR: {jar}")
