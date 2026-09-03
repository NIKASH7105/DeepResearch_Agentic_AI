"""
Script to generate DeepResearch Agent Project Documentation PDF using ReportLab
"""
import os
import sys
from pathlib import Path
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and render 'Page X of Y' and header/footer styling.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        
        # Suppress headers/footers on cover page (Page 1)
        if self._pageNumber > 1:
            # Header line and text
            self.setStrokeColor(colors.HexColor('#CBD5E1'))
            self.setLineWidth(0.75)
            self.line(54, letter[1] - 40, letter[0] - 54, letter[1] - 40)
            
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor('#1E3A8A'))
            self.drawString(54, letter[1] - 34, "DEEPRESEARCH AGENT")
            
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor('#64748B'))
            self.drawRightString(letter[0] - 54, letter[1] - 34, "Project Documentation & Architecture")

            # Footer line and text
            self.line(54, 45, letter[0] - 54, 45)
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor('#64748B'))
            self.drawString(54, 32, "Confidential • DeepResearch Agent Documentation")
            
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(letter[0] - 54, 32, page_text)
            
        self.restoreState()


def create_documentation_pdf(output_path: str):
    """Generate the styled documentation PDF."""
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Palette
    COLOR_PRIMARY = colors.HexColor('#1E3A8A')     # Navy Blue
    COLOR_SECONDARY = colors.HexColor('#2563EB')   # Bright Blue
    COLOR_DARK = colors.HexColor('#1F2937')        # Charcoal Body Text
    COLOR_LIGHT_BG = colors.HexColor('#F8FAFC')    # Light Gray Surface
    COLOR_BORDER = colors.HexColor('#E2E8F0')      # Subtle Border
    COLOR_ACCENT = colors.HexColor('#0D9488')      # Teal Accent

    # Custom Typography Styles
    styles.add(ParagraphStyle(
        name='DocCoverTitle',
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=COLOR_PRIMARY,
        alignment=TA_LEFT,
        spaceAfter=10
    ))

    styles.add(ParagraphStyle(
        name='DocCoverSubtitle',
        fontName='Helvetica',
        fontSize=14,
        leading=20,
        textColor=COLOR_SECONDARY,
        alignment=TA_LEFT,
        spaceAfter=25
    ))

    styles.add(ParagraphStyle(
        name='DocH1',
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=COLOR_PRIMARY,
        spaceBefore=18,
        spaceAfter=10,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        name='DocH2',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=COLOR_SECONDARY,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        name='DocBody',
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=COLOR_DARK,
        spaceAfter=8,
        alignment=TA_LEFT
    ))

    styles.add(ParagraphStyle(
        name='DocBullet',
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=COLOR_DARK,
        leftIndent=15,
        spaceAfter=4
    ))

    styles.add(ParagraphStyle(
        name='DocCode',
        fontName='Courier',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#0F172A'),
        backColor=colors.HexColor('#F1F5F9'),
        borderColor=COLOR_BORDER,
        borderWidth=0.5,
        borderPadding=6,
        spaceAfter=8,
        spaceBefore=4
    ))

    styles.add(ParagraphStyle(
        name='TableHeader',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.white,
        alignment=TA_LEFT
    ))

    styles.add(ParagraphStyle(
        name='TableCell',
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=COLOR_DARK,
        alignment=TA_LEFT
    ))

    story = []

    # ---------------------------------------------------------
    # COVER SECTION
    # ---------------------------------------------------------
    story.append(Spacer(1, 20))
    story.append(Paragraph("DeepResearch Agent", styles['DocCoverTitle']))
    story.append(Paragraph("System Architecture, Process Workflow & Technical Documentation", styles['DocCoverSubtitle']))
    
    story.append(HRFlowable(width="100%", thickness=3, color=COLOR_PRIMARY, spaceBefore=0, spaceAfter=15))

    # Meta Table
    meta_data = [
        [Paragraph("<b>Project Name:</b>", styles['TableCell']), Paragraph("DeepResearch Agent", styles['TableCell'])],
        [Paragraph("<b>System Type:</b>", styles['TableCell']), Paragraph("Autonomous Multi-Agent AI Research Engine", styles['TableCell'])],
        [Paragraph("<b>Execution Cycle:</b>", styles['TableCell']), Paragraph("Plan → Act → Observe → Evaluate → Synthesize", styles['TableCell'])],
        [Paragraph("<b>Target Deliverable:</b>", styles['TableCell']), Paragraph("Cited Research Reports & Formatted PDF Exports", styles['TableCell'])],
        [Paragraph("<b>Generated On:</b>", styles['TableCell']), Paragraph(datetime.now().strftime('%B %d, %Y'), styles['TableCell'])],
    ]
    meta_table = Table(meta_data, colWidths=[1.8*inch, 4.8*inch])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 15))

    # ---------------------------------------------------------
    # SECTION 1: WHAT IS WANTED
    # ---------------------------------------------------------
    story.append(Paragraph("1. Executive Summary & Core Objectives (What is Wanted)", styles['DocH1']))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_SECONDARY, spaceBefore=0, spaceAfter=8))
    
    story.append(Paragraph("<b>Problem Statement:</b> Standard conversational AI interfaces fail at multi-layered academic or enterprise research due to single-turn prompt limitations, lack of live source attribution, and output restricted to unstructured raw text.", styles['DocBody']))
    
    story.append(Paragraph("<b>Core Solution:</b> DeepResearch Agent provides an end-to-end autonomous research workflow that deconstructs user topics, queries live web indexes, extracts verified facts, evaluates knowledge sufficiency, and compiles publication-grade PDF reports complete with numerical citations.", styles['DocBody']))

    story.append(Paragraph("<b>Key Agent Capabilities:</b>", styles['DocH2']))
    story.append(Paragraph("• <b>Autonomous Planning:</b> Automatically splits complex prompts into targeted sub-questions.", styles['DocBullet']))
    story.append(Paragraph("• <b>Multi-Source Gathering:</b> Performs web and image searches with rate-limit handling.", styles['DocBullet']))
    story.append(Paragraph("• <b>Granular Fact Extraction:</b> Distills key facts from web pages before synthesis.", styles['DocBullet']))
    story.append(Paragraph("• <b>Iterative Quality Check:</b> Evaluates answer sufficiency and fills information gaps.", styles['DocBullet']))
    story.append(Paragraph("• <b>Cited Synthesis & PDF Export:</b> Produces structured reports with [1], [2] citations and PDF exports.", styles['DocBullet']))

    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # SECTION 2: WHAT IS USED WHERE
    # ---------------------------------------------------------
    story.append(Paragraph("2. System Architecture & Tech Stack (What is Used Where)", styles['DocH1']))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_SECONDARY, spaceBefore=0, spaceAfter=8))

    story.append(Paragraph("The system is divided into a modern React frontend, a FastAPI asynchronous backend, and a LangGraph agentic decision graph.", styles['DocBody']))

    # Tech Stack Table
    stack_data = [
        [Paragraph("Layer", styles['TableHeader']), Paragraph("Technology", styles['TableHeader']), Paragraph("Purpose & Module", styles['TableHeader'])],
        [Paragraph("Frontend UI", styles['TableCell']), Paragraph("React 18 + Vite", styles['TableCell']), Paragraph("User interface, state coordination (<code>src/App.jsx</code>)", styles['TableCell'])],
        [Paragraph("Data Polling", styles['TableCell']), Paragraph("TanStack Query", styles['TableCell']), Paragraph("Polls <code>/api/research/{id}/status</code> every 2s", styles['TableCell'])],
        [Paragraph("HTTP Client", styles['TableCell']), Paragraph("Axios", styles['TableCell']), Paragraph("API request dispatching (<code>src/services/api.js</code>)", styles['TableCell'])],
        [Paragraph("Backend Framework", styles['TableCell']), Paragraph("FastAPI", styles['TableCell']), Paragraph("Async API routes & background tasks (<code>app/main.py</code>)", styles['TableCell'])],
        [Paragraph("Agent State Graph", styles['TableCell']), Paragraph("LangGraph", styles['TableCell']), Paragraph("Cyclic execution workflow (<code>app/agents/agent_graph.py</code>)", styles['TableCell'])],
        [Paragraph("LLM Integration", styles['TableCell']), Paragraph("Ollama / OpenAI", styles['TableCell']), Paragraph("Planning, evaluation & synthesis prompting", styles['TableCell'])],
        [Paragraph("Web Search Tool", styles['TableCell']), Paragraph("DuckDuckGo (ddgs)", styles['TableCell']), Paragraph("Live web search tool (<code>app/tools/web_search.py</code>)", styles['TableCell'])],
        [Paragraph("Image Acquisition", styles['TableCell']), Paragraph("DDG Images + httpx", styles['TableCell']), Paragraph("Image downloading (<code>app/tools/image_search.py</code>)", styles['TableCell'])],
        [Paragraph("PDF Generator", styles['TableCell']), Paragraph("ReportLab + Pillow", styles['TableCell']), Paragraph("PDF compilation (<code>app/services/pdf_generator.py</code>)", styles['TableCell'])],
    ]
    
    stack_table = Table(stack_data, colWidths=[1.3*inch, 1.7*inch, 3.6*inch])
    stack_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('BOX', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_LIGHT_BG]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(stack_table)
    story.append(Spacer(1, 15))

    # ---------------------------------------------------------
    # SECTION 3: THE PROCESS
    # ---------------------------------------------------------
    story.append(Paragraph("3. End-to-End Execution Process (The Workflow)", styles['DocH1']))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_SECONDARY, spaceBefore=0, spaceAfter=8))

    proc_code = (
        "[ User Request ] -> POST /api/research/start\n"
        "      │\n"
        "      ▼\n"
        "1. Plan Node (planner.py) -----------> Generates 3-5 Sub-Questions\n"
        "      │\n"
        "      ▼\n"
        "2. Research Node (web_search.py) ----> Executes DDG Search & Fact Extraction\n"
        "      │\n"
        "      ▼\n"
        "3. Evaluate Node (agent_graph.py) ---> Sufficient Sources? (≥ 6 or Max Iter)\n"
        "      ├───── NO  ─────────> Research More Node (Identify Gaps) ───────┐\n"
        "      └───── YES ──────────────────────────────────────────────────┐  │\n"
        "                                                                   │  │\n"
        "4. Synthesize Node (evidence_extractor.py) <───────────────────────┘  │\n"
        "   (Generates cited markdown [1], [2])                                │\n"
        "      │                                                               │\n"
        "      ▼                                                               │\n"
        "5. PDF Generator (pdf_generator.py) <─────────────────────────────────┘\n"
        "   (Downloads media, builds ReportLab PDF document)\n"
        "      │\n"
        "      ▼\n"
        "[ Downloadable PDF Report Delivered to User UI ]"
    )
    story.append(Paragraph(proc_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), styles['DocCode']))

    story.append(Paragraph("<b>Detailed Process Steps:</b>", styles['DocH2']))
    story.append(Paragraph("1. <b>Initiation:</b> User submits topic on frontend (`ResearchForm.jsx`). POST `/api/research/start` creates session and triggers background task `run_research`.", styles['DocBody']))
    story.append(Paragraph("2. <b>Planning (`plan_research`):</b> LLM creates 3-5 targeted research questions to cover multiple angles of the user topic.", styles['DocBody']))
    story.append(Paragraph("3. <b>Tool Search & Fact Extraction (`conduct_research`):</b> System searches DuckDuckGo for each sub-question, extracts 2-3 key evidence facts per source snippet using LLM, and logs reasoning.", styles['DocBody']))
    story.append(Paragraph("4. <b>Quality Evaluation & Gap Analysis (`evaluate_research`):</b> Evaluates collected sources. If insufficient, generates gap queries via `research_more` and loops back to research.", styles['DocBody']))
    story.append(Paragraph("5. <b>Synthesis (`synthesize_answer`):</b> Synthesizes evidence into a cited markdown response with inline source brackets (`[1]`, `[2]`).", styles['DocBody']))
    story.append(Paragraph("6. <b>PDF Compilation (`PDFReportGenerator`):</b> On download, system fetches images via `ImageSearchTool`, constructs ReportLab layout (Cover, Metadata, Plan, Cited Findings, Image Gallery, References), and outputs PDF.", styles['DocBody']))

    story.append(Spacer(1, 15))

    # ---------------------------------------------------------
    # SECTION 4: EXAMPLE DRY RUN
    # ---------------------------------------------------------
    story.append(Paragraph("4. Concrete Example Dry Run Trace", styles['DocH1']))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_SECONDARY, spaceBefore=0, spaceAfter=8))

    story.append(Paragraph("<b>Topic:</b> <i>Impact of Quantum Computing on Financial Cybersecurity</i>", styles['DocBody']))
    
    dryrun_data = [
        [Paragraph("Step", styles['TableHeader']), Paragraph("Execution Details", styles['TableHeader'])],
        [
            Paragraph("1. Plan Generation", styles['TableCell']),
            Paragraph("LLM outputs 3 sub-questions:<br/>"
                      "1. <i>How do quantum algorithms (Shor's) threaten RSA encryption in finance?</i><br/>"
                      "2. <i>What Post-Quantum Cryptography (PQC) standards are banks adopting?</i><br/>"
                      "3. <i>What is the estimated timeline for quantum cybersecurity readiness?</i>", styles['TableCell'])
        ],
        [
            Paragraph("2. Web Search & Fact Extraction", styles['TableCell']),
            Paragraph("• <b>Source [1]:</b> <i>'Quantum Threats to Financial Systems'</i><br/>"
                      "  Fact: Shor's algorithm efficiently factors large integers, invalidating RSA-2048.<br/>"
                      "• <b>Source [2]:</b> <i>'NIST PQC Standards'</i><br/>"
                      "  Fact: NIST finalized CRYSTALS-Kyber for post-quantum key encapsulation.", styles['TableCell'])
        ],
        [
            Paragraph("3. Evaluation", styles['TableCell']),
            Paragraph("Evaluator checks total sources (6 found across 3 sub-questions). Determines quality is <b>SUFFICIENT</b>. Proceeds to synthesis.", styles['TableCell'])
        ],
        [
            Paragraph("4. Citation Synthesis", styles['TableCell']),
            Paragraph("<i>'Quantum computing threatens financial systems by breaking RSA encryption via Shor's algorithm [1]. Central banks are migrating to NIST-approved algorithms such as CRYSTALS-Kyber [2].'</i>", styles['TableCell'])
        ],
        [
            Paragraph("5. PDF Output", styles['TableCell']),
            Paragraph("Downloads 2 related graphics via `ImageSearchTool`, builds ReportLab document layout, and delivers <code>research_report_eb719a42.pdf</code>.", styles['TableCell'])
        ]
    ]

    dryrun_table = Table(dryrun_data, colWidths=[1.5*inch, 5.1*inch])
    dryrun_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('BOX', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_LIGHT_BG]),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(dryrun_table)

    story.append(Spacer(1, 20))
    story.append(Paragraph("Documentation compiled successfully. File ready for distribution.", styles['DocBody']))

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] PDF generated successfully: {output_path}")


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    pdf_path_root = project_root / "DeepResearch_Agent_Project_Documentation.pdf"
    pdf_path_docs = project_root / "Docs" / "DeepResearch_Agent_Project_Documentation.pdf"
    
    create_documentation_pdf(str(pdf_path_root))
    create_documentation_pdf(str(pdf_path_docs))
