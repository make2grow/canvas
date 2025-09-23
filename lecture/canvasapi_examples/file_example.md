from urllib.parse import urlparse, parse_qs

def get_canvas_image_preview_url(download_url: str, course_id: int) -> str:
    """
    Given a Canvas file download URL and course ID,
    returns the preview URL usable for embedding the image.
    """
    # Parse the URL to extract the file ID
    parsed_url = urlparse(download_url)
    # The file ID is the second path segment in /files/{file_id}/download
    path_parts = parsed_url.path.split('/')
    # path example: ['', 'files', '12716411', 'download']
    if len(path_parts) < 4 or path_parts[1] != 'files':
        raise ValueError("Invalid Canvas file download URL format")
    file_id = path_parts

    # Construct the preview URL
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    preview_url = f"{base_url}/courses/{course_id}/files/{file_id}/preview"

    return preview_url

# Example usage
download_url = "https://nku.instructure.com/files/12716411/download?download_frd=1&verifier=Sgn5X4Jw0Mor5oxxMeQ57ewTOP96eKEmTM1WFJYR"
course_id = 81929

preview_url = get_canvas_image_preview_url(download_url, course_id)
print("Preview URL:", preview_url)
