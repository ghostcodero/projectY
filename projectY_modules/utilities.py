import unicodedata
import re

def sanitize_filename(filename):
    """Removes non-ASCII characters and special symbols from filenames."""
    filename = unicodedata.normalize('NFKD', filename).encode('ascii', 'ignore').decode('utf-8')  # Remove non-ASCII
    filename = re.sub(r'[^\w\s-]', '', filename).strip()  # Remove special characters
    filename = re.sub(r'[-\s]+', '-', filename)  # Replace spaces with hyphens
    return filename
