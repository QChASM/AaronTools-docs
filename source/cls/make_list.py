import os, subprocess, sys

from charset_normalizer import from_bytes
from charset_normalizer.models import CliDetectionResult

for cls in os.listdir("../../../AaronTools/bin"):
    cls_path = os.path.join("../../../AaronTools/bin", cls)
    proc = subprocess.run(
        [sys.executable, cls_path, "--help"],
        capture_output=True,
    )
    name, ext = os.path.splitext(cls)
    matches = from_bytes(proc.stdout, threshold=0.2, explain=False)
    # best guess is None if there's no good match
    best_guess = matches.best()
    enc = "utf-8"
    print(30 * "=")
    if not best_guess:
        print(fname, "\tno guess")
    else:
        print(best_guess.encoding)
        enc = best_guess.encoding
    print(30 * "=")
    with open("%s_help.txt" % name, "w", encoding="utf-8") as f:
        f.write(".. code-block:: text \n\n    ")
        # the guessed encoding sucks, Latin_1 works though
        man = proc.stdout.decode("Latin_1")
        # I guess there's two newlines
        f.write(man.replace("\n", "    "))
    
    rst_name = "%s.rst" % name
    if os.path.exists(rst_name):
        continue
    
    with open(rst_name, "w") as f:
        f.write(cls + "\n")
        f.write(len(cls) * "=")
        f.write("\n\n")
        f.write(".. include:: %s" % "%s_help.txt" % name)

    