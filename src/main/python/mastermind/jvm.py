import jpype
import jpype.imports
from pathlib import Path

_JAR = Path(__file__).parents[5] / "target" / "mastermind-solver.jar"

jpype.startJVM(classpath=[str(_JAR)])

from org.mastermind import MastermindSession  # noqa: E402
from org.mastermind.codes import ConvertCode  # noqa: E402
