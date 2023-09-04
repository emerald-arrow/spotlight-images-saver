# Spotlight Images Saver

## About

It is a script that saves lockscreen images provided by Windows Spotlight. The script asks user for a directory where these images should be saved and copies them there. User might choose to copy images with Desktop aspect ratio, Mobile aspect ratio or both types at once. Images with Desktop aspect ratio have "Desktop_" prefix added to their names and images with Mobile aspect ratio are saved with "Mobile_" prefix. The script omitts copying images in case if images with the same file names are already in destination directory. It does not prevent duplicates in 100% of cases but it decreases amount of them.

## How to use

### Basic usage

1. Download latest version from **[Releases](https://github.com/emerald-arrow/spotlight-images-saver/releases)**
2. Run the script
3. Follow instructions given by the script

### Destination path in environment variable

User might skip the script's phase of asking for directory path by setting environment variable named `WALLPAPERS_SAVE_PATH` with desired save location.