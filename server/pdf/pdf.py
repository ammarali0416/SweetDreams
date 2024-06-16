from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
from io import BytesIO
from models.database import CompletedChapter

class PDF:
    def __init__(self, title: str, chapters: list[CompletedChapter]):
        self.title = title
        self.chapters = sorted(chapters, key=lambda x: x.Number)
        self.buffer = BytesIO()
        self.styles = getSampleStyleSheet()
        self.styles.add(ParagraphStyle(name='ChapterTitle', fontSize=20, spaceAfter=10, leading=24, alignment=1))
        self.styles.add(ParagraphStyle(name='Content', fontSize=12, leading=15))

    def generate_title_page(self, elements):
        elements.append(Spacer(1, 2 * inch))
        elements.append(Paragraph(self.title, self.styles['ChapterTitle']))
        elements.append(Spacer(1, inch))
        elements.append(Paragraph("Written with the help of chat2book.io :)", self.styles['Content']))
        elements.append(PageBreak())

    def generate_chapters(self, elements):
        for chapter in self.chapters:
            elements.append(Paragraph(f"Chapter {chapter.Number}: {chapter.Title}", self.styles['ChapterTitle']))
            elements.append(Spacer(1, 0.2 * inch))
            elements.append(Paragraph(chapter.Content.replace('\n', '<br />'), self.styles['Content']))
            elements.append(PageBreak())

    def generate_pdf(self):
        doc = SimpleDocTemplate(self.buffer, pagesize=A4,
                                rightMargin=inch, leftMargin=inch,
                                topMargin=inch, bottomMargin=inch)
        elements = []
        self.generate_title_page(elements)
        self.generate_chapters(elements)
        doc.build(elements)
        self.buffer.seek(0)
        return self.buffer

    def save_pdf(self, path: str):
        with open(path, 'wb') as f:
            f.write(self.buffer.getvalue())
        self.buffer.close()
