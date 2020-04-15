import os
import shutil
if os.path.exists("test.db"):
    os.remove("test.db")
else:
    print("The file does not exist")

shutil.rmtree("__pycache__")