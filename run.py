"""Wrapper to fix Windows symlink and encoding issues with HuggingFace Hub."""
import os
import sys
import shutil

os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'

# Fix Windows console encoding for emoji output
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Patch huggingface_hub to use copies instead of symlinks on Windows
import huggingface_hub.file_download as fd

original_create_symlink = fd._create_symlink

def _patched_create_symlink(src, dst, new_blob=False):
    try:
        original_create_symlink(src, dst, new_blob)
    except OSError:
        dst_dir = os.path.dirname(dst)
        os.makedirs(dst_dir, exist_ok=True)
        if os.path.exists(dst):
            os.remove(dst)
        shutil.copy2(src, dst)

fd._create_symlink = _patched_create_symlink

# Now import and run main
import runpy
runpy.run_path('main.py', run_name='__main__')
