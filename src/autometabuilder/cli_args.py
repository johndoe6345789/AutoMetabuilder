"""CLI argument parsing."""
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="AutoMetabuilder: AI-driven SDLC assistant.")
    parser.add_argument("--dry-run", action="store_true", help="Do not execute state-modifying tools.")
    parser.add_argument("--yolo", action="store_true", help="Execute tools without confirmation.")
    parser.add_argument("--once", action="store_true", help="Run a single full iteration (AI -> Tool -> AI).")
    parser.add_argument("--web", action="store_true", help="Start the Web UI.")
    return parser.parse_args()
