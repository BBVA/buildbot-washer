"""
Launch washer worker.

"""
import invoke  # import invoke to force nuitka to include it in bundle
from washer.worker import main

main()
