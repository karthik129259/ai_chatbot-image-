def allowed_file(filename):
    """
    Checks if the uploaded file has an allowed extension
    """
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image_url(url):
    """
    Validates if a string is a proper URL format
    """
    return url.startswith(('http://', 'https://'))

def sanitize_input(text):
    """
    Sanitizes user input to prevent injection attacks
    """
    # Basic sanitization - remove HTML tags and trim whitespace
    return text.strip()