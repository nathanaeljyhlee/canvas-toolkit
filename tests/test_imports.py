#!/usr/bin/env python3
"""Validation test - verify all imports work."""

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")

    # Client
    from canvas_toolkit.client import CanvasClient, CanvasAPIError, AuthenticationError
    print("[OK] Client imports successful")

    # Models
    from canvas_toolkit.models import Assignment
    print("[OK] Models imports successful")

    # Writers
    from canvas_toolkit.writers import ExcelWriter, CSVWriter, JSONWriter
    print("[OK] Writers imports successful")

    print("\n[SUCCESS] All imports successful!")

if __name__ == "__main__":
    test_imports()
