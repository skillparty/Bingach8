import os
import sys
import pygame
import argparse

# Parse command line arguments for resolution testing
parser = argparse.ArgumentParser(description='Test Bingacho at different resolutions')
parser.add_argument('--width', type=int, default=1024, help='Screen width')
parser.add_argument('--height', type=int, default=768, help='Screen height')
args = parser.parse_args()

# Modify config.py temporarily for testing
import config as cfg

# Store original values
original_width = cfg.WIDTH
original_height = cfg.HEIGHT

# Set new resolution for testing
cfg.WIDTH = args.width
cfg.HEIGHT = args.height

# Import main game with modified config
import main

# After game exits, restore original values
# Note: This won't actually run because main.py calls sys.exit()
cfg.WIDTH = original_width
cfg.HEIGHT = original_height
