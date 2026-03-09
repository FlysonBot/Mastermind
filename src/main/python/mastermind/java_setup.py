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

# --- Paths ---

_ROOT         = Path(__file__).parents[4]
_SRC_JAVA     = _ROOT / "src" / "main" / "java"
_CLASSES      = _ROOT / "target" / "classes"
_JDK          = _ROOT / "target" / "java-jdk"
_BUNDLED_JAR  = _ROOT / "src" / "main" / "mastermind-solver.jar"
_BUNDLED_JRE  = _ROOT / "src" / "main" / "jre"
_CACHED_JRE   = _ROOT / "target" / "mastermind-jre"

# --- Platform config ---

_PLATFORM_MAP = {
    ("linux",   "x86_64"):  "linux-x64",
    ("linux",   "amd64"):   "linux-x64",
    ("windows", "amd64"):   "windows-x64",
    ("windows", "x86_64"):  "windows-x64",
    ("darwin",  "x86_64"):  "mac-x64",
    ("darwin",  "amd64"):   "mac-x64",
    ("darwin",  "arm64"):   "mac-aarch64",
    ("darwin",  "aarch64"): "mac-aarch64",
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
        print("Java is not installed. Please run:")
        print("    pkg install openjdk-21")
        sys.exit(1)
    if not _BUNDLED_JAR.exists():
        print("Bundled JAR not found. Please re-clone or re-download the repository.")
        sys.exit(1)
    return None, _BUNDLED_JAR


def _ensure_desktop():
    """Return (jre, jar), extracting or building the JRE/JAR as needed."""
    jre = _resolve_jre()
    jar = _BUNDLED_JAR if _BUNDLED_JAR.exists() else None

    if jre and jar:
        return jre, jar

    # Fallback: download a JDK to build whatever is missing
    _download_jdk()
    try:
        if not jre:
            _build_jre()
            jre = _CACHED_JRE
        if not jar:
            _build_jar()
            jar = _BUNDLED_JAR
    finally:
        shutil.rmtree(_JDK, ignore_errors=True)

    return jre, jar


def _resolve_jre():
    """Return the JRE path if ready, extracting the bundled zip if needed."""
    if _CACHED_JRE.exists():
        return _CACHED_JRE

    os_name = platform.system().lower()
    arch    = platform.machine().lower()
    name    = _PLATFORM_MAP.get((os_name, arch))
    if name:
        zip_path = _BUNDLED_JRE / f"{name}.zip"
        if zip_path.exists():
            _extract_jre(zip_path)
            return _CACHED_JRE

    return None


# --- JRE extraction ---

def _extract_jre(zip_path: Path):
    print(f"Extracting JRE from {zip_path.name}...")
    t = time.time()
    _CACHED_JRE.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(_CACHED_JRE)
    # Restore execute permissions on binaries (lost during zip on Unix)
    for f in (_CACHED_JRE / "bin").iterdir():
        f.chmod(f.stat().st_mode | 0o111)
    print(f"JRE extracted. ({time.time() - t:.1f}s)")

# --- Fallback: build from downloaded JDK ---

def _download_jdk():
    import jdk  # install-jdk library
    print("Downloading JDK...")
    t = time.time()
    jdk.install(version="21", path=str(_JDK))
    size_mb = sum(f.stat().st_size for f in _JDK.rglob("*") if f.is_file()) / 1024 / 1024
    print(f"JDK ready. ({time.time() - t:.1f}s, {size_mb:.0f} MB)")


def _build_jre():
    jlink = next(_JDK.rglob("jlink"), None)
    if not jlink:
        raise RuntimeError("jlink not found in downloaded JDK")
    print("Building trimmed JRE...")
    t = time.time()
    subprocess.run(
        [str(jlink), "--add-modules", "java.base", "--output", str(_CACHED_JRE),
         "--strip-debug", "--no-header-files", "--no-man-pages"],
        check=True,
    )
    print(f"JRE ready. ({time.time() - t:.1f}s)")


def _build_jar():
    javac    = next(_JDK.rglob("javac"), None)
    jar_tool = next(_JDK.rglob("jar"),   None)
    if not javac:    raise RuntimeError("javac not found in downloaded JDK")
    if not jar_tool: raise RuntimeError("jar not found in downloaded JDK")

    sources = [str(p) for p in _SRC_JAVA.rglob("*.java")]
    _CLASSES.mkdir(parents=True, exist_ok=True)
    _BUNDLED_JAR.parent.mkdir(parents=True, exist_ok=True)

    print("Compiling Java sources...")
    t = time.time()
    subprocess.run([str(javac), "-d", str(_CLASSES)] + sources, check=True)
    subprocess.run(
        [str(jar_tool), "--create", "--file", str(_BUNDLED_JAR), "-C", str(_CLASSES), "."],
        check=True,
    )
    print(f"JAR ready. ({time.time() - t:.1f}s)")


if __name__ == "__main__":
    jre, jar = ensure_ready()
    print(f"JRE: {jre}")
    print(f"JAR: {jar}")
