import jpype
from mastermind.java_setup import ensure_ready

jre, jar = ensure_ready()

if jre is None:
    # Android/Termux: use the system JDK's libjvm directly
    import glob

    matches = glob.glob(
        "/data/data/com.termux/files/usr/lib/jvm/java-21-openjdk*/lib/server/libjvm.so"
    )
    if not matches:
        raise RuntimeError("libjvm.so not found. Is openjdk-21 installed via pkg?")

    jvmpath = matches[0]

else:
    jvmpath = str(jre / "lib" / "server" / "libjvm.so")

jpype.startJVM(
    "-Xlog:os+container=off",
    jvmpath=jvmpath,
    classpath=[str(jar)],
    convertStrings=False,
)

MastermindSession = jpype.JClass("org.mastermind.MastermindSession")
ConvertCode = jpype.JClass("org.mastermind.codes.ConvertCode")
ExpectedSize = jpype.JClass("org.mastermind.compute.ExpectedSize")
Feedback = jpype.JClass("org.mastermind.compute.Feedback")
