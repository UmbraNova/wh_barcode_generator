import os
import openpyxl
from barcode import Code128
from barcode.writer import ImageWriter
from jinja2 import Template

def generate_barcodes_from_excel(file_path, column="A", output_dir="barcodes"):
    """
    Citeste fisier Excel, genereaza barcodes dintr-o coloana, creaza HTML file pentru printing.
    
    Args:
        file_path (str): Excel file path.
        column (str): Column letter containing barcode data.
        output_dir (str): Directory to store generated barcode pngs.
    """

    try:
        wb = openpyxl.load_workbook(file_path)
        sheet = wb.active
    except FileNotFoundError:
        print(f"File {file_path} not found!")
        return
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return


    if not os.path.exists(output_dir):  # Create output directory if it doesn't exist
        os.makedirs(output_dir)

    # Read the specified column and generate barcodes
    barcodes = []
    for row in sheet.iter_rows(
        min_col=ord(column.upper()) - 64, 
        max_col=ord(column.upper()) - 64, 
        min_row=2, 
        values_only=True
    ):
        value = row[0]
        print(f"Processing value: {value}")  # Debug log
        if value and isinstance(value, (str, int)):  # Ensure value is valid
            barcode_path = os.path.join(output_dir, f"{value}")
            try:
                Code128(str(value), writer=ImageWriter()).save(barcode_path)
                barcodes.append(barcode_path)
            except Exception as e:
                print(f"Failed to generate barcode for value {value}: {e}")
        else:
            print(f"Skipping invalid or empty value: {value}")


    # Generate HTML for printing
    if barcodes:
        create_barcode_html(barcodes, output_dir)
        print(f"Barcodes generated and saved to '{output_dir}'. Open 'barcodes.html' to preview or print.")
    else:
        print("No valid barcodes generated.")

def create_barcode_html(barcodes, output_dir):
    """
    Genereaza HTML file pt barcode printing
    
    Args:
        barcodes (list): Lista barcode image paths.
        output_dir (str): Directory to save the HTML file
    """
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Barcodes</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
            }
            .barcode {
                margin: 10px;
                text-align: center;
            }
            .barcode img {
                width: 200px;
                height: auto;
            }
            .barcode p {
                margin-top: 5px;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        {% for barcode in barcodes %}
        <div class="barcode">
            <img src="{{ barcode }}" alt="Barcode">
            <p>{{ barcode.split('/')[-1].split('.')[0] }}</p>
        </div>
        {% endfor %}
    </body>
    </html>
    """

    # Render the HTML with the barcodes
    template = Template(html_template)
    html_content = template.render(barcodes=[os.path.relpath(b, output_dir) for b in barcodes])
    
    html_path = os.path.join(output_dir, "barcodes.html")  # Save the HTML file
    with open(html_path, "w", encoding="utf-8") as html_file:
        html_file.write(html_content)

if __name__ == "__main__":
    excel_file = "X:/AUR/11.2024/20.11.2024/Warehouse Zones and Bins Template 07.11.24.xlsx"  # Replace with your Excel file path
    generate_barcodes_from_excel(excel_file, column="B")
