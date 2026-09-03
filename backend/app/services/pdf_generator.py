"""
PDF report generator with images
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from datetime import datetime
from typing import List, Dict
from pathlib import Path
from PIL import Image as PILImage
import io
import os


class PDFReportGenerator:
    """Generate professional PDF reports with images"""
    
    def __init__(self, output_dir: str = "./reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e40af'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Heading style
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#4f46e5'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Body style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=11,
            leading=16,
            alignment=TA_JUSTIFY,
            spaceAfter=12
        ))
        
        # Citation style
        self.styles.add(ParagraphStyle(
            name='Citation',
            parent=self.styles['BodyText'],
            fontSize=9,
            textColor=colors.HexColor('#6b7280'),
            leftIndent=20,
            spaceAfter=6
        ))
    
    def _resize_image(self, image_path: str, max_width: float = 5*inch, max_height: float = 3*inch):
        """
        Resize image to fit within constraints
        
        Args:
            image_path: Path to image
            max_width: Maximum width (already in reportlab units)
            max_height: Maximum height (already in reportlab units)
            
        Returns:
            Tuple of (width, height) in reportlab units or None if error
        """
        try:
            print(f"📐 Resizing image: {image_path}")
            
            # Check if file exists
            if not os.path.exists(image_path):
                print(f"❌ Image file not found: {image_path}")
                return None
            
            with PILImage.open(image_path) as img:
                # Get original dimensions in pixels
                orig_width, orig_height = img.size
                print(f"   Original size: {orig_width}x{orig_height} pixels")
                
                # Calculate aspect ratio
                aspect = orig_width / orig_height
                
                # Start with max dimensions (already in reportlab units)
                width = max_width
                height = width / aspect
                
                # If height exceeds max, scale down
                if height > max_height:
                    height = max_height
                    width = height * aspect
                
                print(f"   PDF size: {width/inch:.2f}\" x {height/inch:.2f}\"")
                return (width, height)
                
        except Exception as e:
            print(f"❌ Image resize error: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def generate_report(
        self, 
        session_id: str,
        query: str,
        answer: str,
        sources: List[Dict],
        research_plan: List[str] = None,
        image_paths: List[str] = None
    ) -> str:
        """
        Generate PDF report
        
        Args:
            session_id: Research session ID
            query: Research query
            answer: Research answer with citations
            sources: List of source dictionaries
            research_plan: Research plan steps
            image_paths: Paths to images to include
            
        Returns:
            Path to generated PDF
        """
        print(f"\n📄 Generating PDF report for session: {session_id}")
        print(f"   Query: {query}")
        print(f"   Sources: {len(sources)}")
        print(f"   Images: {len(image_paths) if image_paths else 0}")
        
        # Create filename
        filename = f"research_report_{session_id}.pdf"
        filepath = self.output_dir / filename
        
        # Create document
        doc = SimpleDocTemplate(
            str(filepath),
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
        )
        
        # Container for PDF elements
        story = []
        
        # Title Page
        story.append(Spacer(1, 2*inch))
        story.append(Paragraph("Research Report", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.3*inch))
        story.append(Paragraph(query, self.styles['CustomHeading']))
        story.append(Spacer(1, 0.5*inch))
        
        # Add hero image if available
        if image_paths and len(image_paths) > 0:
            print(f"🖼️  Adding hero image: {image_paths[0]}")
            try:
                img_size = self._resize_image(image_paths[0], max_width=4*inch, max_height=3*inch)
                if img_size:
                    img = Image(image_paths[0], width=img_size[0], height=img_size[1])
                    story.append(img)
                    story.append(Spacer(1, 0.2*inch))
                    print(f"✓ Hero image added")
                else:
                    print(f"⚠️  Could not resize hero image")
            except Exception as e:
                print(f"❌ Error adding hero image: {e}")
        else:
            print("⚠️  No images available for hero image")
        
        # Date
        date_text = f"Generated: {datetime.now().strftime('%B %d, %Y')}"
        story.append(Paragraph(date_text, self.styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Summary info
        summary_data = [
            ['Research Query:', query],
            ['Sources Found:', str(len(sources))],
            ['Report Date:', datetime.now().strftime('%Y-%m-%d')]
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 4*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        
        story.append(summary_table)
        story.append(PageBreak())
        
        # Research Plan (if available)
        if research_plan and len(research_plan) > 0:
            story.append(Paragraph("Research Plan", self.styles['CustomHeading']))
            story.append(Spacer(1, 0.1*inch))
            
            for i, question in enumerate(research_plan, 1):
                story.append(Paragraph(f"{i}. {question}", self.styles['CustomBody']))
            
            story.append(Spacer(1, 0.3*inch))
        
        # Findings Section
        story.append(Paragraph("Research Findings", self.styles['CustomHeading']))
        story.append(Spacer(1, 0.2*inch))
        
        # Split answer into paragraphs and add
        paragraphs = answer.split('\n\n')
        for para in paragraphs:
            if para.strip():
                story.append(Paragraph(para.strip(), self.styles['CustomBody']))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Add additional images in findings
        if image_paths and len(image_paths) > 1:
            story.append(Paragraph("Related Images", self.styles['CustomHeading']))
            story.append(Spacer(1, 0.1*inch))
            
            images_added = 0
            for img_path in image_paths[1:3]:  # Add up to 2 more images
                print(f"🖼️  Adding related image: {img_path}")
                try:
                    img_size = self._resize_image(img_path, max_width=3*inch, max_height=2*inch)
                    if img_size:
                        img = Image(img_path, width=img_size[0], height=img_size[1])
                        story.append(img)
                        story.append(Spacer(1, 0.2*inch))
                        images_added += 1
                        print(f"✓ Related image added")
                except Exception as e:
                    print(f"❌ Error adding related image: {e}")
            
            print(f"✓ Added {images_added} related images")
        
        story.append(PageBreak())
        
        # References Section
        story.append(Paragraph("References", self.styles['CustomHeading']))
        story.append(Spacer(1, 0.2*inch))
        
        for i, source in enumerate(sources, 1):
            citation = f"[{i}] <b>{source.get('title', 'Unknown')}</b><br/>"
            citation += f"&nbsp;&nbsp;&nbsp;&nbsp;URL: {source.get('url', 'N/A')}<br/>"
            
            if source.get('evidence'):
                citation += f"&nbsp;&nbsp;&nbsp;&nbsp;Key Facts: {len(source['evidence'])} extracted<br/>"
            
            story.append(Paragraph(citation, self.styles['Citation']))
            story.append(Spacer(1, 0.1*inch))
        
        # Build PDF
        doc.build(story)
        
        print(f"✅ PDF generated: {filepath}\n")
        return str(filepath)


# Global instance
pdf_generator = PDFReportGenerator()
