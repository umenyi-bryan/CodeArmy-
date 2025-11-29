#!/usr/bin/env python3
print("🚀 CodeArmy Quick Start")
print("======================")
print("Choose your method:")
print("1. Full featured chat (codearmy.py)")
print("2. One-liner magic (magic.py)")
print("3. Ultra simple (one-liner-command.py)")
print()
choice = input("Enter choice (1-3): ").strip()

if choice == "1":
    print("Running: python3 codearmy.py")
    exec(open("codearmy.py").read())
elif choice == "2":
    print("Running: python3 magic.py")
    exec(open("magic.py").read())
elif choice == "3":
    print("Running: python3 one-liner-command.py")
    exec(open("one-liner-command.py").read())
else:
    print("Running one-liner command...")
    exec(open("one-liner-command.py").read())
