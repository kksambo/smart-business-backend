"""
Receipt generation service for creating PDF and text receipts
"""
from io import BytesIO
from datetime import datetime
from typing import List, Dict, Optional
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


class ReceiptService:
    """Service for generating receipts in PDF and text formats"""

    @staticmethod
    def generate_text_receipt(
        sale_data: Dict,
        business_info: Dict,
        items: List[Dict],
        location_info: Optional[Dict] = None,
    ) -> str:
        """
        Generate a text-formatted receipt
        
        Args:
            sale_data: Sale information (total, date, payment method, etc.)
            business_info: Business details (name, type, etc.)
            items: List of items sold with details
            location_info: Location details if available
        
        Returns:
            Formatted text receipt
        """
        receipt_lines = []
        
        # Header
        receipt_lines.append("=" * 50)
        receipt_lines.append(business_info.get("business_name", "SMART BUSINESS RECEIPT").center(50))
        receipt_lines.append("=" * 50)
        receipt_lines.append("")
        
        # Business details
        receipt_lines.append(f"Business Type: {business_info.get('business_type', 'General')}")
        if location_info:
            receipt_lines.append(f"Location: {location_info.get('name', '')}")
            receipt_lines.append(f"Region: {location_info.get('region', '')}")
        receipt_lines.append("")
        
        # Receipt info
        receipt_date = datetime.fromisoformat(sale_data.get("created_at", datetime.now().isoformat()))
        receipt_lines.append(f"Receipt Date: {receipt_date.strftime('%Y-%m-%d %H:%M:%S')}")
        receipt_lines.append(f"Payment Method: {sale_data.get('payment_method', 'CASH').upper()}")
        if sale_data.get("customer_name"):
            receipt_lines.append(f"Customer: {sale_data.get('customer_name')}")
        receipt_lines.append("")
        
        # Items header
        receipt_lines.append("-" * 50)
        receipt_lines.append(f"{'Item':<25} {'Qty':>6} {'Price':>8} {'Total':>8}")
        receipt_lines.append("-" * 50)
        
        # Items
        total_cost = 0
        for item in items:
            name = item.get("product_name", "Item")[:24]
            qty = item.get("quantity", 0)
            price = float(item.get("unit_price", 0))
            subtotal = float(item.get("subtotal", 0))
            total_cost += subtotal
            
            receipt_lines.append(f"{name:<25} {qty:>6} {price:>8.2f} {subtotal:>8.2f}")
        
        # Totals
        receipt_lines.append("-" * 50)
        
        total_amount = float(sale_data.get("total_amount", 0))
        total_profit = total_amount - total_cost
        
        receipt_lines.append(f"{'SUBTOTAL':<33} {total_amount:>16.2f}")
        receipt_lines.append(f"{'TAX (included)':<33} {total_profit * 0.14:>16.2f}")
        receipt_lines.append("=" * 50)
        receipt_lines.append(f"{'TOTAL':<33} {total_amount:>16.2f}")
        receipt_lines.append("=" * 50)
        receipt_lines.append("")
        
        # Footer
        receipt_lines.append("Thank you for your business!".center(50))
        receipt_lines.append("".center(50))
        receipt_lines.append("Please keep your receipt for warranty".center(50))
        receipt_lines.append("and exchange purposes.".center(50))
        receipt_lines.append("".center(50))
        receipt_lines.append("=" * 50)
        
        return "\n".join(receipt_lines)

    @staticmethod
    def generate_pdf_receipt(
        sale_data: Dict,
        business_info: Dict,
        items: List[Dict],
        location_info: Optional[Dict] = None,
    ) -> bytes:
        """
        Generate a PDF receipt
        
        Args:
            sale_data: Sale information
            business_info: Business details
            items: List of items sold
            location_info: Location details if available
        
        Returns:
            PDF file as bytes
        """
        # Create PDF buffer
        buffer = BytesIO()
        
        # Create PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=0.5 * inch,
            leftMargin=0.5 * inch,
            topMargin=0.5 * inch,
            bottomMargin=0.5 * inch,
        )
        
        # Create styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#475569'),
            spaceAfter=4,
            alignment=TA_LEFT,
            fontName='Helvetica'
        )
        
        # Build content
        story = []
        
        # Title
        business_name = business_info.get("business_name", "SMART BUSINESS RECEIPT")
        story.append(Paragraph(business_name, title_style))
        story.append(Spacer(1, 0.1 * inch))
        
        # Business and receipt info
        info_data = [
            ["Business Type:", business_info.get("business_type", "General")],
            ["Receipt Date:", datetime.fromisoformat(sale_data.get("created_at", datetime.now().isoformat())).strftime('%Y-%m-%d %H:%M:%S')],
            ["Payment Method:", sale_data.get("payment_method", "CASH").upper()],
        ]
        
        if location_info:
            info_data.insert(0, ["Location:", location_info.get("name", "")])
        
        if sale_data.get("customer_name"):
            info_data.append(["Customer:", sale_data.get("customer_name")])
        
        info_table = Table(info_data, colWidths=[1.5 * inch, 3.5 * inch])
        info_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 9),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#475569')),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 0.15 * inch))
        
        # Items table
        total_cost = 0
        items_data = [["Item", "Qty", "Unit Price", "Total"]]
        
        for item in items:
            name = item.get("product_name", "Item")
            qty = item.get("quantity", 0)
            price = float(item.get("unit_price", 0))
            subtotal = float(item.get("subtotal", 0))
            total_cost += subtotal
            
            items_data.append([
                name,
                str(qty),
                f"${price:.2f}",
                f"${subtotal:.2f}"
            ])
        
        items_table = Table(
            items_data,
            colWidths=[2.5 * inch, 0.8 * inch, 1.0 * inch, 1.0 * inch]
        )
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e2e8f0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONT', (0, 1), (-1, -1), 'Helvetica', 9),
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ]))
        story.append(items_table)
        story.append(Spacer(1, 0.15 * inch))
        
        # Totals
        total_amount = float(sale_data.get("total_amount", 0))
        total_profit = total_amount - total_cost
        
        totals_data = [
            ["SUBTOTAL", f"${total_amount:.2f}"],
            ["TAX (included)", f"${total_profit * 0.14:.2f}"],
            ["TOTAL", f"${total_amount:.2f}"],
        ]
        
        totals_table = Table(totals_data, colWidths=[3.5 * inch, 1.3 * inch])
        totals_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, 1), 9),
            ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 2), (-1, 2), 11),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 2), (-1, 2), 1, colors.black),
            ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#e2e8f0')),
        ]))
        story.append(totals_table)
        story.append(Spacer(1, 0.2 * inch))
        
        # Footer
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#6b7280'),
            alignment=TA_CENTER,
        )
        story.append(Paragraph("Thank you for your business!", footer_style))
        story.append(Spacer(1, 0.05 * inch))
        story.append(Paragraph("Please keep your receipt for warranty and exchange purposes.", footer_style))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        
        return buffer.getvalue()
