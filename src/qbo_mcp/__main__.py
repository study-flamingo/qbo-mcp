import logging
import sys
from .server import mcp

def main():
  try:
      mcp.run()
  except Exception as e:
      logging.error(f"Configuration Error: {e}")
      sys.exit(1)

# This check ensures the main function runs only when the package is executed directly
if __name__ == "__main__":
    main()