"""
Build script for the Java side of Mastermind.
Called by the Makefile targets build-jar and build-jre.
Does not require Maven — uses install-jdk to obtain a JDK on the fly.

Usage:
    python src/build.py jar   -- compile Java sources and copy JAR to src/main/
    python src/build.py jre   -- cross-compile trimmed JREs for all supported platforms
                                 and place them under src/main/jre/<platform>.zip
"""

import platform
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile
from pathlib import Path

import jdk as install_jdk
from jdk.enums import Architecture, OperatingSystem
from rich.console import Console

console = Console()

# --- Paths ---

_ROOT = Path(__file__).parents[1]
_SRC_JAVA = _ROOT / "src" / "main" / "java"
_CLASSES = _ROOT / "target" / "classes"
_OUT_JAR = _ROOT / "src" / "main" / "mastermind-solver.jar"
_OUT_JRE = _ROOT / "src" / "main" / "jre"

# JDKs are cached in the system temp dir: persists across builds, auto-cleaned by the OS
_JDK_CACHE = Path(tempfile.gettempdir()) / "mastermind-jdk"

# --- Platform config ---

# Supported target platforms: (name, OperatingSystem, Architecture)
_PLATFORMS = [
    ("linux-x64", OperatingSystem.LINUX, Architecture.X64),
    ("windows-x64", OperatingSystem.WINDOWS, Architecture.X64),
    ("mac-x64", OperatingSystem.MAC, Architecture.X64),
    ("mac-aarch64", OperatingSystem.MAC, Architecture.AARCH64),
]

# Maps (os, arch) as reported by Python to a platform name
_HOST_PLATFORM_MAP = {
    ("linux", "x86_64"): "linux-x64",
    ("linux", "amd64"): "linux-x64",
    ("windows", "amd64"): "windows-x64",
    ("windows", "x86_64"): "windows-x64",
    ("darwin", "x86_64"): "mac-x64",
    ("darwin", "amd64"): "mac-x64",
    ("darwin", "arm64"): "mac-aarch64",
    ("darwin", "aarch64"): "mac-aarch64",
}


def _host_platform():
    return _HOST_PLATFORM_MAP.get(
        (platform.system().lower(), platform.machine().lower())
    )


# --- JAR build ---


def build_jar():
    """Compile Java sources into a JAR and copy it to src/main/.
    Uses system javac/jar if available, otherwise downloads a JDK."""
    javac, jar_tool = _resolve_javac_and_jar()
    try:
        _compile(javac, jar_tool)
    finally:
        shutil.rmtree(_CLASSES, ignore_errors=True)


def _resolve_javac_and_jar():
    """Return (javac, jar) paths — from system if available, else from cached/downloaded JDK."""
    javac = shutil.which("javac")
    jar_tool = shutil.which("jar")

    if javac and jar_tool:
        console.print(f"Using system javac: [cyan]{javac}[/cyan]")
        return Path(javac), Path(jar_tool)

    if not _JDK_CACHE.exists():
        _download_jdk(_JDK_CACHE)

    javac = next(_JDK_CACHE.rglob("javac"), None)
    jar_tool = next(_JDK_CACHE.rglob("jar"), None)

    if not javac:
        raise RuntimeError("javac not found in downloaded JDK")

    if not jar_tool:
        raise RuntimeError("jar not found in downloaded JDK")

    return javac, jar_tool


def _compile(javac: Path, jar_tool: Path):
    sources = [str(p) for p in _SRC_JAVA.rglob("*.java")]
    _CLASSES.mkdir(parents=True, exist_ok=True)

    t = time.time()
    with console.status("Compiling Java sources..."):
        subprocess.run([str(javac), "-d", str(_CLASSES)] + sources, check=True)

    tmp_jar = _ROOT / "target" / "mastermind-solver.jar"
    tmp_jar.parent.mkdir(parents=True, exist_ok=True)

    with console.status("Packaging JAR..."):
        subprocess.run(
            [
                str(jar_tool),
                "--create",
                "--file",
                str(tmp_jar),
                "-C",
                str(_CLASSES),
                ".",
            ],
            check=True,
        )
    console.print(f"[green]✓[/green] JAR built. ({time.time() - t:.1f}s)")

    _OUT_JAR.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(tmp_jar, _OUT_JAR)
    console.print(
        f"[green]✓[/green] JAR copied to [cyan]{_OUT_JAR.relative_to(_ROOT)}[/cyan]"
    )


# --- JRE build ---


def build_jre():
    """Cross-compile trimmed JREs for all supported platforms.
    Each JRE is compressed with LZMA into src/main/jre/<platform>.zip.
    Skips platforms whose zip already exists."""
    _OUT_JRE.mkdir(parents=True, exist_ok=True)
    jlink = _resolve_jlink()

    for platform_name, os_enum, arch_enum in _PLATFORMS:
        _build_platform_jre(platform_name, os_enum, arch_enum, jlink)


def _resolve_jlink():
    """Return a jlink Path — from system if available, else from a cached/downloaded JDK.
    Prefers the host platform's JDK (downloaded naturally during its JRE build) to avoid
    an extra download. Falls back to a standalone host JDK only if necessary."""
    system_jlink = shutil.which("jlink")
    if system_jlink:
        console.print(f"Using system jlink: [cyan]{system_jlink}[/cyan]")
        return Path(system_jlink)

    host = _host_platform()
    needs_build = [
        name
        for name, _, _ in _PLATFORMS
        if not (_OUT_JRE / f"{name}.zip").exists() and not (_OUT_JRE / name).exists()
    ]

    if needs_build and not any(name == host for name in needs_build):
        # Host platform's JDK won't be downloaded during the loop — fetch jlink now
        if not _JDK_CACHE.exists():
            _download_jdk(_JDK_CACHE)

        jlink = next(_JDK_CACHE.rglob("jlink"), None)
        if not jlink:
            raise RuntimeError("jlink not found in host JDK")

        return jlink

    return None  # will be set from the host platform's JDK during the loop


def _build_platform_jre(platform_name, os_enum, arch_enum, jlink):
    """Build, compress, and cache the JRE for a single target platform."""
    target_jdk = Path(tempfile.gettempdir()) / f"mastermind-jdk-{platform_name}"
    out_jre = _OUT_JRE / platform_name
    out_zip = _OUT_JRE / f"{platform_name}.zip"

    if out_zip.exists():
        console.print(
            f"[dim]Skipping {platform_name} — {out_zip.relative_to(_ROOT)} already exists[/dim]"
        )
        return

    console.print(f"\n[bold]Building JRE for {platform_name}[/bold]")

    # Compress and clean up a leftover raw folder from a previous interrupted run
    if out_jre.exists():
        console.print("Found existing raw JRE folder, compressing...")
        _compress_jre(out_jre, out_zip)
        shutil.rmtree(out_jre)
        return

    # Download this platform's JDK if not cached
    if not target_jdk.exists():
        _download_jdk(target_jdk, os=os_enum, arch=arch_enum, label=platform_name)

    # If this is the host platform and we don't have jlink yet, grab it from this JDK
    if jlink is None and platform_name == _host_platform():
        jlink = next(target_jdk.rglob("jlink"), None)

    if jlink is None:
        raise RuntimeError("No jlink available — this should not happen")

    _jlink_jre(jlink, target_jdk, out_jre, platform_name)
    _compress_jre(out_jre, out_zip)
    shutil.rmtree(out_jre)


def _jlink_jre(jlink: Path, target_jdk: Path, out_jre: Path, platform_name: str):
    """Run jlink to produce a trimmed JRE from the target platform's JDK."""
    jmods = next(target_jdk.rglob("jmods"), None)
    if not jmods:
        raise RuntimeError(f"jmods directory not found in {platform_name} JDK")

    t = time.time()
    with console.status("Linking trimmed JRE..."):
        proc = subprocess.run(
            [
                str(jlink),
                "--module-path",
                str(jmods),
                "--add-modules",
                "java.base",
                "--output",
                str(out_jre),
                "--strip-debug",
                "--no-header-files",
                "--no-man-pages",
            ],
            capture_output=True,
            text=True,
        )
    # objcopy errors appear when cross-compiling between OS families (e.g. Linux→Mac)
    # because objcopy doesn't understand the foreign binary format. Safe to suppress —
    # the JRE still works; only debug symbol stripping is skipped for affected binaries.
    for line in proc.stderr.splitlines():
        if "objcopy" not in line and "strip-native-debug-symbols" not in line:
            print(line, file=sys.stderr)

    if proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode, proc.args)

    raw_mb = (
        sum(f.stat().st_size for f in out_jre.rglob("*") if f.is_file()) / 1024 / 1024
    )
    console.print(
        f"[green]✓[/green] JRE linked. ({time.time() - t:.1f}s, {raw_mb:.0f} MB uncompressed)"
    )


def _compress_jre(jre_dir: Path, out_zip: Path):
    """Zip a JRE directory using LZMA compression."""
    t = time.time()
    with console.status(f"Compressing to [cyan]{out_zip.relative_to(_ROOT)}[/cyan]..."):
        with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_LZMA) as zf:
            for file in jre_dir.rglob("*"):
                zf.write(file, file.relative_to(jre_dir))

    size_mb = out_zip.stat().st_size / 1024 / 1024
    console.print(
        f"[green]✓[/green] Compressed. ({time.time() - t:.1f}s, {size_mb:.1f} MB)"
    )


# --- JDK download ---


def _download_jdk(path: Path, os=None, arch=None, label="host"):
    kwargs = {"version": "21", "path": str(path)}
    if os is not None:
        kwargs["operating_system"] = os
    if arch is not None:
        kwargs["arch"] = arch

    t = time.time()
    with console.status(f"Downloading [cyan]{label}[/cyan] JDK..."):
        install_jdk.install(**kwargs)
    size_mb = (
        sum(f.stat().st_size for f in path.rglob("*") if f.is_file()) / 1024 / 1024
    )
    console.print(
        f"[green]✓[/green] {label} JDK ready. ({time.time() - t:.1f}s, {size_mb:.0f} MB)"
    )


# --- Entry point ---

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("jar", "jre"):
        console.print(__doc__)
        sys.exit(1)

    if sys.argv[1] == "jar":
        build_jar()

    elif sys.argv[1] == "jre":
        build_jre()
