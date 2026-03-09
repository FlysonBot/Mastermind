export PATH := $(HOME)/.local/bin:$(PATH)

.PHONY: build-jar build-jre build

# Build the JAR without Maven: downloads a JDK, compiles Java sources,
# and copies the result to src/main/mastermind-solver.jar
build-jar:
	uv run python src/build.py jar

# Cross-compile trimmed JREs for linux-x64, windows-x64, mac-x64, and mac-aarch64,
# compress each with LZMA, and place them under src/main/jre/<platform>.zip.
# These are committed to the repo so end users don't have to download a JDK themselves.
build-jre:
	uv run python src/build.py jre

# Full release build: builds the JAR and all JREs
build: build-jar build-jre
