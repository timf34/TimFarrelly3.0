#!/usr/bin/env python3
"""
Geometric Overlay Generator

Creates subtle geometric construction lines over images,
inspired by classical proportional geometry and compositional guides.
"""

from PIL import Image, ImageDraw
import math
import argparse
from pathlib import Path


def golden_ratio_spiral(draw, width, height, color, line_width):
    """Draw a golden ratio spiral with construction rectangles."""
    phi = (1 + math.sqrt(5)) / 2  # Golden ratio ≈ 1.618
    
    # Draw the golden rectangle divisions
    x, y = 0, 0
    w, h = width, height
    
    # Ensure we're working with golden proportions
    squares = []
    for i in range(8):  # 8 iterations of the spiral
        if w > h:
            square_size = h
            squares.append((x, y, square_size, 'h'))
            x += square_size
            w -= square_size
        else:
            square_size = w
            squares.append((x, y, square_size, 'v'))
            y += square_size
            h -= square_size
        
        if w < 10 or h < 10:
            break
    
    # Draw the spiral using quarter circles
    for i, (sx, sy, size, orientation) in enumerate(squares):
        # Draw the square division line
        if orientation == 'h':
            draw.line([(sx + size, sy), (sx + size, sy + size)], fill=color, width=line_width)
        else:
            draw.line([(sx, sy + size), (sx + size, sy + size)], fill=color, width=line_width)
        
        # Draw quarter circle arc (approximated with line segments)
        segments = 20
        for j in range(segments):
            angle1 = (math.pi / 2) * (j / segments)
            angle2 = (math.pi / 2) * ((j + 1) / segments)
            
            # Adjust center and start angle based on position in spiral
            if i % 4 == 0:
                cx, cy = sx + size, sy + size
                a1, a2 = math.pi + angle1, math.pi + angle2
            elif i % 4 == 1:
                cx, cy = sx, sy + size
                a1, a2 = 1.5 * math.pi + angle1, 1.5 * math.pi + angle2
            elif i % 4 == 2:
                cx, cy = sx, sy
                a1, a2 = angle1, angle2
            else:
                cx, cy = sx + size, sy
                a1, a2 = 0.5 * math.pi + angle1, 0.5 * math.pi + angle2
            
            x1 = cx + size * math.cos(a1)
            y1 = cy + size * math.sin(a1)
            x2 = cx + size * math.cos(a2)
            y2 = cy + size * math.sin(a2)
            
            draw.line([(x1, y1), (x2, y2)], fill=color, width=line_width)


def rule_of_thirds(draw, width, height, color, line_width):
    """Draw rule of thirds grid."""
    # Vertical lines
    draw.line([(width / 3, 0), (width / 3, height)], fill=color, width=line_width)
    draw.line([(2 * width / 3, 0), (2 * width / 3, height)], fill=color, width=line_width)
    
    # Horizontal lines
    draw.line([(0, height / 3), (width, height / 3)], fill=color, width=line_width)
    draw.line([(0, 2 * height / 3), (width, 2 * height / 3)], fill=color, width=line_width)


def diagonal_grid(draw, width, height, color, line_width):
    """Draw diagonal composition lines (baroque diagonal)."""
    # Main diagonals
    draw.line([(0, 0), (width, height)], fill=color, width=line_width)
    draw.line([(width, 0), (0, height)], fill=color, width=line_width)
    
    # Reciprocal diagonals (perpendicular to main diagonals from corners)
    # These create the "sinister" and "baroque" diagonals
    draw.line([(0, 0), (width / 2, height)], fill=color, width=line_width)
    draw.line([(width / 2, 0), (width, height)], fill=color, width=line_width)
    draw.line([(0, height / 2), (width, 0)], fill=color, width=line_width)
    draw.line([(0, height), (width, height / 2)], fill=color, width=line_width)


def root_rectangles(draw, width, height, color, line_width):
    """Draw root rectangle constructions (√2, √3, √4, √5)."""
    center_x = width / 2
    center_y = height / 2
    
    # Use the smaller dimension as base
    base = min(width, height) * 0.9
    
    roots = [1, math.sqrt(2), math.sqrt(3), 2, math.sqrt(5)]
    
    for root in roots:
        rect_width = base * root / 2
        rect_height = base / 2
        
        if rect_width <= width / 2 and rect_height <= height / 2:
            # Draw rectangle centered
            x1 = center_x - rect_width
            y1 = center_y - rect_height
            x2 = center_x + rect_width
            y2 = center_y + rect_height
            
            draw.rectangle([x1, y1, x2, y2], outline=color, width=line_width)


def golden_triangles(draw, width, height, color, line_width):
    """Draw golden triangle / sublime triangle construction."""
    # Main triangle from bottom corners to top center
    draw.line([(0, height), (width / 2, 0)], fill=color, width=line_width)
    draw.line([(width, height), (width / 2, 0)], fill=color, width=line_width)
    draw.line([(0, height), (width, height)], fill=color, width=line_width)
    
    # Inner golden divisions
    phi = (1 + math.sqrt(5)) / 2
    
    # Points along the sides at golden ratio
    left_point = (width / 2 / phi, height / phi)
    right_point = (width - width / 2 / phi, height / phi)
    
    draw.line([left_point, right_point], fill=color, width=line_width)
    draw.line([(0, height), right_point], fill=color, width=line_width)
    draw.line([(width, height), left_point], fill=color, width=line_width)


def harmonic_armature(draw, width, height, color, line_width):
    """Draw the harmonic armature - a classical composition framework."""
    # Border rectangle
    draw.rectangle([0, 0, width - 1, height - 1], outline=color, width=line_width)
    
    # Diagonals
    draw.line([(0, 0), (width, height)], fill=color, width=line_width)
    draw.line([(width, 0), (0, height)], fill=color, width=line_width)
    
    # Midpoint lines
    draw.line([(width / 2, 0), (width / 2, height)], fill=color, width=line_width)
    draw.line([(0, height / 2), (width, height / 2)], fill=color, width=line_width)
    
    # Reciprocals from midpoints to corners
    draw.line([(0, height / 2), (width, 0)], fill=color, width=line_width)
    draw.line([(0, height / 2), (width, height)], fill=color, width=line_width)
    draw.line([(width, height / 2), (0, 0)], fill=color, width=line_width)
    draw.line([(width, height / 2), (0, height)], fill=color, width=line_width)
    
    draw.line([(width / 2, 0), (0, height)], fill=color, width=line_width)
    draw.line([(width / 2, 0), (width, height)], fill=color, width=line_width)
    draw.line([(width / 2, height), (0, 0)], fill=color, width=line_width)
    draw.line([(width / 2, height), (width, 0)], fill=color, width=line_width)


def phi_grid(draw, width, height, color, line_width):
    """Draw phi grid (golden ratio grid, tighter than rule of thirds)."""
    phi = (1 + math.sqrt(5)) / 2
    
    # Vertical lines at golden ratio positions
    draw.line([(width / phi, 0), (width / phi, height)], fill=color, width=line_width)
    draw.line([(width - width / phi, 0), (width - width / phi, height)], fill=color, width=line_width)
    
    # Horizontal lines at golden ratio positions
    draw.line([(0, height / phi), (width, height / phi)], fill=color, width=line_width)
    draw.line([(0, height - height / phi), (width, height - height / phi)], fill=color, width=line_width)


def dynamic_symmetry(draw, width, height, color, line_width):
    """Draw dynamic symmetry grid (Jay Hambidge's system)."""
    # Main diagonals
    draw.line([(0, 0), (width, height)], fill=color, width=line_width)
    draw.line([(width, 0), (0, height)], fill=color, width=line_width)
    
    # Reciprocal diagonals
    # From corners perpendicular to main diagonal
    # These hit the opposite side at specific points
    
    # Calculate where perpendicular from (0,0) to main diagonal hits the edges
    # The perpendicular from origin to line y = (h/w)x
    ratio = height / width
    
    # Perpendicular lines
    draw.line([(0, 0), (width, height * ratio * width / (width + height * ratio))], fill=color, width=line_width)
    draw.line([(width, 0), (0, height - height * ratio * width / (width + height * ratio))], fill=color, width=line_width)
    draw.line([(0, height), (width, height - height * ratio * width / (width + height * ratio))], fill=color, width=line_width)
    draw.line([(width, height), (0, height * ratio * width / (width + height * ratio))], fill=color, width=line_width)


def rabatment(draw, width, height, color, line_width):
    """Draw rabatment of the rectangle - squares from short sides."""
    short_side = min(width, height)
    
    # Left square
    draw.line([(short_side, 0), (short_side, height)], fill=color, width=line_width)
    # Diagonal of left square
    draw.line([(0, 0), (short_side, height)], fill=color, width=line_width)
    draw.line([(0, height), (short_side, 0)], fill=color, width=line_width)
    
    # Right square
    draw.line([(width - short_side, 0), (width - short_side, height)], fill=color, width=line_width)
    # Diagonal of right square
    draw.line([(width - short_side, 0), (width, height)], fill=color, width=line_width)
    draw.line([(width - short_side, height), (width, 0)], fill=color, width=line_width)


def concentric_circles(draw, width, height, color, line_width):
    """Draw concentric circles based on golden ratio."""
    center_x = width / 2
    center_y = height / 2
    
    phi = (1 + math.sqrt(5)) / 2
    max_radius = min(width, height) / 2
    
    radius = max_radius
    for i in range(6):
        bbox = [
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius
        ]
        draw.ellipse(bbox, outline=color, width=line_width)
        radius = radius / phi


# Pattern registry
PATTERNS = {
    'spiral': ('Golden Ratio Spiral', golden_ratio_spiral),
    'thirds': ('Rule of Thirds', rule_of_thirds),
    'diagonal': ('Diagonal Grid', diagonal_grid),
    'root': ('Root Rectangles', root_rectangles),
    'triangle': ('Golden Triangles', golden_triangles),
    'armature': ('Harmonic Armature', harmonic_armature),
    'phi': ('Phi Grid', phi_grid),
    'dynamic': ('Dynamic Symmetry', dynamic_symmetry),
    'rabatment': ('Rabatment', rabatment),
    'circles': ('Concentric Circles', concentric_circles),
}


def apply_overlay(image_path, patterns, output_path=None, color=(255, 255, 255, 180), line_width=1):
    """
    Apply geometric overlay patterns to an image.
    
    Args:
        image_path: Path to input image
        patterns: List of pattern names to apply (or 'all')
        output_path: Output path (default: input_name_overlay.png)
        color: RGBA color tuple for lines
        line_width: Width of lines in pixels
    """
    # Load image
    img = Image.open(image_path).convert('RGBA')
    width, height = img.size
    
    # Create transparent overlay
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Apply selected patterns
    if patterns == ['all']:
        patterns = list(PATTERNS.keys())
    
    for pattern_name in patterns:
        if pattern_name in PATTERNS:
            name, func = PATTERNS[pattern_name]
            print(f"Applying: {name}")
            func(draw, width, height, color, line_width)
        else:
            print(f"Unknown pattern: {pattern_name}")
    
    # Composite overlay onto image
    result = Image.alpha_composite(img, overlay)
    
    # Generate output path if not specified
    if output_path is None:
        input_path = Path(image_path)
        output_path = input_path.parent / f"{input_path.stem}_overlay.png"
    
    # Save result
    result.save(output_path, 'PNG')
    print(f"Saved: {output_path}")
    
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description='Apply geometric construction overlays to images',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available patterns:
  spiral    - Golden ratio spiral with construction rectangles
  thirds    - Rule of thirds grid
  diagonal  - Diagonal composition lines (baroque diagonal)
  root      - Root rectangle constructions (√2, √3, √4, √5)
  triangle  - Golden triangle construction
  armature  - Harmonic armature (classical composition framework)
  phi       - Phi grid (golden ratio grid)
  dynamic   - Dynamic symmetry grid (Hambidge's system)
  rabatment - Rabatment of the rectangle
  circles   - Concentric circles based on golden ratio

Examples:
  %(prog)s painting.jpg -p spiral phi
  %(prog)s painting.jpg -p all -w 2
  %(prog)s painting.jpg -p armature -c 255 255 255 100 -o output.png
        """
    )
    
    parser.add_argument('image', help='Input image path')
    parser.add_argument('-p', '--patterns', nargs='+', default=['spiral'],
                        help='Patterns to apply (space-separated, or "all")')
    parser.add_argument('-o', '--output', help='Output path')
    parser.add_argument('-c', '--color', nargs=4, type=int, default=[255, 255, 255, 180],
                        metavar=('R', 'G', 'B', 'A'),
                        help='Line color as RGBA values (0-255)')
    parser.add_argument('-w', '--width', type=int, default=1,
                        help='Line width in pixels')
    parser.add_argument('-l', '--list', action='store_true',
                        help='List available patterns and exit')
    
    args = parser.parse_args()
    
    if args.list:
        print("Available patterns:")
        for key, (name, _) in PATTERNS.items():
            print(f"  {key:12} - {name}")
        return
    
    apply_overlay(
        args.image,
        args.patterns,
        args.output,
        tuple(args.color),
        args.width
    )


if __name__ == '__main__':
    main()