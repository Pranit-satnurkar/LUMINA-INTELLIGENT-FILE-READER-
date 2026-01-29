from reportlab.pdfgen import canvas
import os

def create_dummy_pdf():
    if not os.path.exists("./docs"):
        os.makedirs("./docs")
    
    c = canvas.Canvas("./docs/climate_report.pdf")
    c.drawString(100, 800, "Global Climate Change Report 2024")
    c.drawString(100, 780, "CONFIDENTIAL - FOR LIBRARY ARCHIVES ONLY")
    
    text = """
    Climate change is driving significant shifts in global weather patterns. 
    The average global temperature has risen by 1.2 degrees Celsius since the pre-industrial era.
    Key drivers include carbon dioxide emissions from burning fossil fuels and deforestation.
    Sea levels are rising at a rate of 3.3 millimeters per year.
    Renewable energy sources such as solar and wind are critical for mitigation.
    
    The 'Green Protocol' of 2023 mandates a 50% reduction in industrial carbon output by 2030.
    Scientists warn that crossing the 1.5 degree threshold will lead to irreversible ecosystem damage.
    """
    
    y = 750
    for line in text.split('\n'):
        c.drawString(100, y, line.strip())
        y -= 20
        
    c.save()
    print("Created dummy PDF: ./docs/climate_report.pdf")

if __name__ == "__main__":
    create_dummy_pdf()
