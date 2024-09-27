


from flask import Blueprint, request, jsonify, render_template , send_file
from app.validators import validate_uploaded_document
from app.connectors import connect_document_intelligence_service

import json


#imports for exporting the mind map to pdf file
from pathlib import Path
from reportlab.lib.pagesizes import A4

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle , PageBreak
from reportlab.lib.units import inch , mm
from reportlab.lib.colors import black
import asyncio

import time
import os

from app.decorators import generate_summarizations_and_images , generate_image

export_pdf_file_bp= Blueprint("export_pdf_file", __name__)

def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 10)
    canvas.drawRightString(195 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()

def add_border(canvas, doc):
    width, height = A4
    canvas.setStrokeColor(black)
    canvas.setLineWidth(1)
    canvas.rect(0.5 * inch, 0.5 * inch, width - 1 * inch, height - 1 * inch)

@export_pdf_file_bp.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    
    
    with open("structured_output.json", "r") as file:
        data = json.load(file)

    main_title = data["mainTitle"]
    downloads_path = Path.home() / 'Downloads'
    pdf_name = f'{main_title}-mindmap.pdf'
    pdf_file = downloads_path / pdf_name
    pdf_file_str = str(pdf_file)

     
    if pdf_file.exists():
        return jsonify({"filename": pdf_name}), 200

    print('Beginning to generate PDF')
    doc = SimpleDocTemplate(str(pdf_file), pagesize=A4)

    elements = []

    styles = getSampleStyleSheet()
    title_style = styles['Title']
    title_style.fontSize = 24  
    elements.append(Paragraph(main_title, title_style))
    elements.append(Spacer(1, 0.5 * inch))  

    # Fetch pictures and summarizations for subtitles and main title
    async def prepare_content():
        paragraphs = [subtopic['paragraphs'][0] for subtopic in data['subtitles'] if subtopic.get('paragraphs')]
        subtitles = [subtopic['subtitle'] for subtopic in data['subtitles']]
        
        # Generate summarizations and images for both subtitles and the main title
        summarizations, images = await generate_summarizations_and_images(paragraphs, subtitles, main_title)
        
        for i, subtopic in enumerate(data['subtitles']):
            subtopic['summarization'] = summarizations[i]
            subtopic['picture'] = images[i]
        
        # The last image in the list is the main title's picture
        main_title_picture = images[-1]
        images.pop(-1)
        return main_title_picture

    # Run the async content preparation
    main_title_picture = asyncio.run(prepare_content())

    

    # Add picture of the main title
    if main_title_picture:
        img = Image(main_title_picture, 5 * inch, 6 * inch)
        img.hAlign = 'CENTER'
        elements.append(img)
        elements.append(Spacer(1, 0.5 * inch))  # Add some space after the image

    # Create Table of Contents
    elements.append(PageBreak())
    elements.append(Paragraph("Table of Contents", styles['Title']))
    elements.append(Spacer(1, 0.5 * inch))

    toc_data = [["Title", "Page"]]
    toc_page_map = {}  # To map subtitles to their pages
    current_page = 4 # Start from 4, after the title page
    i = 0
    for subtopic in data['subtitles']:
        toc_data.append([subtopic['subtitle'], str(current_page)])
        toc_page_map[subtopic['subtitle']] = current_page
        i+=1
        if(i==2):
            current_page += 1
            i=0

    toc_table = Table(toc_data, colWidths=[4 * inch, 2 * inch])
    toc_table.setStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 0), (-1, 0), '#f0f0f0'),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ])
    elements.append(toc_table)
    elements.append(PageBreak())

    # Create Table of Figures
    elements.append(Paragraph("Table of Figures", styles['Title']))
    elements.append(Spacer(1, 0.5 * inch))

    figures_data = [["Figure", "Page"]]
    for subtopic in data['subtitles']:
        if 'picture' in subtopic:
            figures_data.append([subtopic['subtitle'], str(toc_page_map.get(subtopic['subtitle'], ''))])

    figures_table = Table(figures_data, colWidths=[4 * inch, 2 * inch])
    figures_table.setStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 0), (-1, 0), '#f0f0f0'),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ])
    elements.append(figures_table)
    elements.append(PageBreak())

    i = 0
    # Construct the PDF content
    for subtopic in data['subtitles']:
        subtopic_title = subtopic['subtitle']
        summarization = subtopic.get('summarization', '')
        image_path = subtopic.get('picture', '')

        subtitle_style = styles['Heading2']
        subtitle_style.fontSize = 18 
        elements.append(Paragraph(subtopic_title, subtitle_style))
        elements.append(Spacer(1, 0.3 * inch))  
        

        if image_path:
            img = Image(image_path, 3 * inch, 2 * inch)
            img.hAlign = 'RIGHT'

            text_style = styles['BodyText']
            text = Paragraph(summarization, text_style)
            
            # If image is available, arrange in a table
            table_data = [[text, img]]
            table = Table(table_data, style=[
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                ('LEFTPADDING', (0, 0), (0, 0), 0),
                ('RIGHTPADDING', (1, 0), (1, 0), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ], colWidths=[4 * inch, 3 * inch])
            elements.append(table)

           
            if (i ==1 ):
                i=0
                elements.append(PageBreak())
            else:
                elements.append(Spacer(1, 2 * inch))  # Add some space after the text
                i = i + 1
    start_doc_time = time.time()
    try:
        doc.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number )
        end_doc_time = time.time()
        print(f"Document generation took {end_doc_time - start_doc_time:.2f} seconds")
        print('Document generation finished')
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return "Error generating PDF", 500

    file_str = str(main_title)  + '-mindmap.pdf'
    filename = request.form.get("filename", file_str)
    print('PDF generation complete')
    # Return the filename in JSON
    return jsonify({"filename": filename}), 200

@export_pdf_file_bp.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    downloads_path = Path.home() / 'Downloads'
    file_path = downloads_path / filename

    if file_path.exists():
        return send_file(str(file_path), as_attachment=True, download_name=filename)
    else:
        return "File not found", 404














