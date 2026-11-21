import os
import tempfile
from pathlib import Path

# this file creates a excalibur database that is not the one at ~/excalibur/ 🧠 - which you probably don't want the tests overwriting

# Set before any test module imports excalibur. Configuration reads these
# at import time and would otherwise use ~/excalibur.
_HOME = Path(tempfile.mkdtemp(prefix="excalibur-tests-"))
os.environ["EXCALIBUR_HOME"] = str(_HOME)
os.environ["EXCALIBUR_CONFIG"] = str(_HOME / "excalibur.cfg")
