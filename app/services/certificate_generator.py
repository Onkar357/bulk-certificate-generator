from pathlib import Path
from reportlab.lib.pagesizes import A4,landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
def generate_certificate(output_path:Path,certificate_id:str,recipient_name:str,certificate_title:str,event_name:str,event_date:str,issuer_name:str,issue_date:str):
    output_path.parent.mkdir(parents=True,exist_ok=True)
    w,h=landscape(A4); pdf=canvas.Canvas(str(output_path),pagesize=(w,h))
    m=15*mm
    pdf.setLineWidth(3); pdf.rect(m,m,w-2*m,h-2*m)
    pdf.setLineWidth(1); pdf.rect(m+5*mm,m+5*mm,w-2*m-10*mm,h-2*m-10*mm)
    x=w/2
    pdf.setFont("Helvetica-Bold",28); pdf.drawCentredString(x,h-45*mm,"CERTIFICATE")
    pdf.setFont("Helvetica",15); pdf.drawCentredString(x,h-55*mm,certificate_title.upper())
    pdf.setFont("Helvetica",13); pdf.drawCentredString(x,h-75*mm,"This certificate is proudly presented to")
    pdf.setFont("Helvetica-Bold",30); pdf.drawCentredString(x,h-95*mm,recipient_name)
    pdf.setFont("Helvetica",13); pdf.drawCentredString(x,h-110*mm,f"for successfully completing {event_name}")
    pdf.setFont("Helvetica",12); pdf.drawCentredString(x,h-125*mm,f"Event date: {event_date}")
    pdf.setFont("Helvetica",11); pdf.drawString(35*mm,32*mm,f"Issued by: {issuer_name}")
    pdf.drawString(35*mm,25*mm,f"Issue date: {issue_date}")
    pdf.drawRightString(w-35*mm,32*mm,f"Certificate ID: {certificate_id}")
    pdf.showPage(); pdf.save()
