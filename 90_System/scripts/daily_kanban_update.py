#!/usr/bin/env python3
"""Scheduled dashboard update. Reads the vault and publishes only live data."""
from research_publisher import publish

if __name__ == "__main__":
    publish()
