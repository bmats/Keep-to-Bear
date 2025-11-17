import os
import sys
import re
import base64
import mimetypes

def get_mime_type(filename):
	"""Get MIME type from filename extension."""
	mime_type, _ = mimetypes.guess_type(filename)
	return mime_type or 'application/octet-stream'

def embed_images_in_html(html_file):
	"""Convert linked images to base64 embedded images in HTML file."""
	html_dir = os.path.dirname(html_file)

	with open(html_file, 'r') as f:
		html_content = f.read()

	# Find all img tags with src attributes
	img_pattern = r'<img([^>]*?)src="([^"]+)"([^>]*?)>'

	def replace_image(match):
		before_src = match.group(1)
		img_src = match.group(2)
		after_src = match.group(3)

		# Skip if already a data URI
		if img_src.startswith('data:'):
			return match.group(0)

		# Skip if it's an absolute URL
		if img_src.startswith('http://') or img_src.startswith('https://'):
			return match.group(0)

		# Construct full path to image file
		img_path = os.path.join(html_dir, img_src) if html_dir else img_src

		# Check if image file exists
		if not os.path.exists(img_path):
			print(f"Warning: Image file not found: {img_path}")
			return match.group(0)

		try:
			# Read and encode image
			with open(img_path, 'rb') as img_file:
				img_data = img_file.read()
				img_base64 = base64.b64encode(img_data).decode('utf-8')

			# Get MIME type
			mime_type = get_mime_type(img_path)

			# Create data URI
			data_uri = f'data:{mime_type};base64,{img_base64}'

			# Return modified img tag
			return f'<img{before_src}src="{data_uri}"{after_src}>'

		except Exception as e:
			print(f"Error processing image {img_path}: {e}")
			return match.group(0)

	# Replace all image sources
	html_content = re.sub(img_pattern, replace_image, html_content)

	# Write back to file
	with open(html_file, 'w') as f:
		f.write(html_content)

for arg in sys.argv[1:]:
	if not ".html" in arg:
		continue
	embed_images_in_html(arg)
