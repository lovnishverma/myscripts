import qrcode

def generate_qr_code(url, file_name):
    """Generate a QR code for a given URL and save it as an image file.

    Args:
        url (str): The URL to encode in the QR code.
        file_name (str): The name of the output file (e.g., 'qrcode.png').
    """
    # Create a QR code object
    qr = qrcode.QRCode(
        version=1,  # Controls the size of the QR code (1 is the smallest)
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
        box_size=10,  # Size of each box in the QR code grid
        border=4,  # Thickness of the border (minimum is 4)
    )

    # Add data to the QR code
    qr.add_data(url)
    qr.make(fit=True)

    # Create an image of the QR code
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image to a file
    img.save(file_name)
    print(f"QR code saved as {file_name}")

# Example usage
if __name__ == "__main__":
    url_to_encode = "https://google.com/"
    output_file = "qrcode.png"
    generate_qr_code(url_to_encode, output_file)
