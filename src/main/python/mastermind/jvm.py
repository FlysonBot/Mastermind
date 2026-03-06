import jpype
import jpype.imports
from pathlib import Path

_JAR = Path(__file__).parents[4] / "target" / "mastermind-solver.jar"

jpype.startJVM(classpath=[str(_JAR)])

from org.mastermind import MastermindSession          # type: ignore
from org.mastermind.codes import ConvertCode          # type: ignore
from org.mastermind.compute import ExpectedSize       # type: ignore
from org.mastermind.compute import Feedback           # type: ignore
