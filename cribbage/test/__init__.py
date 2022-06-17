# per https://docs.pytest.org/en/7.1.x/explanation/goodpractices.html#goodpractices
# pytest --pyargs cribbage
# will cause pytest to find mypkg wherever it's installed and collect tests from there

# But the above isn't how I actually run things - to run from the cmd line, see the comment
# I added to the README.md. To run from VS Code, using its test infrastructure, I have to 
# do the following, which I learned about at https://stackoverflow.com/questions/57273945/imports-break-vscode-testing-with-pytest

import sys
from pathlib import Path
sys.path.insert(0, str(Path('cribbage/').resolve()))
