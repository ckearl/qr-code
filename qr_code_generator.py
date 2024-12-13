import qrcode
import svgwrite
import cairosvg
import os
import sys

def print_help():
    """Print detailed information about script parameters."""
    help_info = [
        "QR Code Generator Parameters:",
        "1. Filename/Path (required) - Output file for QR code (.svg or .png)",
        "2. URL (required) - The web address to encode in the QR code",
        "3. Color (optional) - Hex color code for QR code dots (default: #000000)",
        "4. Shape (optional) - QR code dot shape. Options:",
        "   - square (default)",
        "   - circle",
        "   - dot",
        "",
        "Usage Examples:",
        "qr-code myqr.png https://example.com",
        "qr-code myqr.svg https://example.com '#FF0000' circle",
        "qr-code ~/Downloads/myqr.png https://example.com",
    ]
    print("\n".join(help_info))

def generate_qr_code(filename, url, color='#000000', shape='square'):
    """
    Generate a QR code with a transparent background and custom dot style.
    
    :param filename: Output filename/path for the QR code
    :param url: URL to encode in the QR code
    :param color: Hex color code for QR code dots
    :param shape: Shape of QR code modules
    """
    # Validate shape input
    if shape not in ['square', 'circle', 'dot']:
        raise ValueError("Shape must be 'square', 'circle', or 'dot'")
    
    # Resolve full path if a directory is provided
    if os.path.isdir(filename):
        # Use current timestamp to create unique filename
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Determine file extension
        ext = '.png' if filename.endswith('.png') else '.svg'
        filename = os.path.join(filename, f"qr_{timestamp}{ext}")
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
    
    # Create QR code instance
    qr = qrcode.QRCode(
        version=None,  # Auto-size
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Add URL data
    qr.add_data(url)
    qr.make(fit=True)
    
    # Get the matrix
    matrix = qr.get_matrix()
    matrix_size = len(matrix)
    
    # Create SVG image with transparent background
    svg = svgwrite.Drawing('temp.svg', size=(matrix_size * 10, matrix_size * 10))
    svg.add(svg.rect(insert=(0, 0), size=('100%', '100%'), fill='none'))
    
    # Draw QR code modules
    for row in range(matrix_size):
        for col in range(matrix_size):
            if matrix[row][col]:
                x = col * 10
                y = row * 10
                
                if shape == 'square':
                    svg.add(svg.rect(insert=(x, y), size=(10, 10), fill=color))
                elif shape == 'circle':
                    svg.add(svg.circle(center=(x+5, y+5), r=5, fill=color))
                elif shape == 'dot':
                    svg.add(svg.circle(center=(x+5, y+5), r=3, fill=color))
    
    # Save the SVG
    svg.save()
    
    # Convert to PNG if requested
    if filename.lower().endswith('.png'):
        cairosvg.svg2png(url='temp.svg', write_to=filename)
        os.remove('temp.svg')
    else:
        os.rename('temp.svg', filename)
    
    print(f"QR Code saved to {filename}")

def main():
    # Check for info flag
    if len(sys.argv) == 2 and sys.argv[1] == '-i':
        print_help()
        sys.exit(0)
    
    # Check if correct number of arguments are provided
    if len(sys.argv) < 3 or len(sys.argv) > 5:
        print("Error: Incorrect number of arguments.")
        print_help()
        sys.exit(1)
    
    # Default values
    filename = sys.argv[1]
    url = sys.argv[2]
    color = sys.argv[3] if len(sys.argv) > 3 else '#000000'
    shape = sys.argv[4] if len(sys.argv) > 4 else 'square'
    
    # Generate QR Code
    generate_qr_code(filename, url, color, shape)

if __name__ == "__main__":
    main()
