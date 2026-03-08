import jpype
from pathlib import Path

_JAR = Path(__file__).parents[4] / "target" / "mastermind-solver.jar"

jpype.startJVM(classpath=[str(_JAR)])

MastermindSession = jpype.JClass("org.mastermind.MastermindSession")
ConvertCode = jpype.JClass("org.mastermind.codes.ConvertCode")
ExpectedSize = jpype.JClass("org.mastermind.compute.ExpectedSize")
Feedback = jpype.JClass("org.mastermind.compute.Feedback")
