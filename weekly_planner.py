import json
import os
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle,
    Flowable,
    Macro,
    Image,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# --- CORE CONFIGURATION SETTINGS ---
PLANNER_YEAR = 2027
START_DATE = datetime(PLANNER_YEAR, 1, 1)

# Dynamically resolve absolute project folder context directories
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_FILE_PATH = os.path.join(PROJECT_DIR, "GloriaHallelujah-Regular.ttf")

# --- CUSTOM FONT INITIALIZATION CONFIGURATION ---
try:
    pdfmetrics.registerFont(TTFont("GloriaHallelujah", FONT_FILE_PATH))
    FONT_HANDWRITTEN = "GloriaHallelujah"
    print("✨ Successfully registered 'Gloria Hallelujah' handwritten font layer!")
except Exception as e:
    print(f"⚠️ Custom font missing, falling back to system Helvetica-Bold: {e}")
    FONT_HANDWRITTEN = "Helvetica-Bold"


class DrawingCanvasBlock(Flowable):
    """A custom flowable layout element that paints its own box framework, dot matrix, or guide lines."""

    def __init__(self, width, height, has_dots=True, is_lettering_track=False):
        super().__init__()
        self.width = width
        self.height = height
        self.has_dots = has_dots
        self.is_lettering_track = is_lettering_track

    def wrap(self, availWidth, availHeight):
        return self.width, self.height

    def draw(self):
        self.canv.saveState()
        border_color = HexColor("#D1D1D1")
        dot_color = HexColor("#C7C7C7")
        line_color = HexColor("#E5E5E5")

        self.canv.setStrokeColor(border_color)
        self.canv.setLineWidth(1)
        self.canv.rect(0, 0, self.width, self.height, stroke=1, fill=0)

        if self.is_lettering_track:
            self.canv.setStrokeColor(line_color)
            row_height = 18
            margin_y = 12
            current_y = self.height - margin_y
            while current_y - row_height >= margin_y:
                top_y = current_y
                mid_y = current_y - (row_height / 2)
                base_y = current_y - row_height

                self.canv.setLineWidth(0.5)
                self.canv.setDash([])
                self.canv.line(0, top_y, self.width, top_y)

                self.canv.setLineWidth(0.5)
                self.canv.setDash()
                self.canv.line(0, mid_y, self.width, mid_y)

                self.canv.setLineWidth(0.75)
                self.canv.setDash([])
                self.canv.line(0, base_y, self.width, base_y)

                current_y -= row_height + 16

        elif self.has_dots:
            dot_spacing, dot_radius = 14, 0.70
            self.canv.setFillColor(dot_color)
            self.canv.setStrokeColor(dot_color)
            for x in range(dot_spacing, int(self.width), dot_spacing):
                for y in range(dot_spacing, int(self.height), dot_spacing):
                    self.canv.circle(x, y, dot_radius, stroke=0, fill=1)

        self.canv.restoreState()


class MoodTrackerWidget(Flowable):
    """Draws a custom, centered reflection title and three widely spaced vector mood face circles."""

    def __init__(self, width=224, height=35):
        super().__init__()
        self.width = width
        self.height = height

    def wrap(self, availWidth, availHeight):
        return self.width, self.height

    def draw(self):
        self.canv.saveState()
        stroke_color = HexColor("#D1D1D1")
        text_color = HexColor("#415A77")

        self.canv.setFont(FONT_HANDWRITTEN, 8)
        self.canv.setFillColor(text_color)
        title_text = "How do you feel now that you've finished this day?"
        self.canv.drawCentredString(self.width / 2, self.height - 10, title_text)

        self.canv.setStrokeColor(stroke_color)
        self.canv.setLineWidth(1)

        cy = 10
        spacing = self.width / 4

        for i in range(1, 4):
            cx = spacing * i
            self.canv.circle(cx, cy, 8, stroke=1, fill=0)

            if i == 1:
                self.canv.line(cx - 3, cy + 2, cx - 1, cy + 2)
                self.canv.line(cx + 1, cy + 2, cx + 3, cy + 2)
                mouth = self.canv.beginPath()
                mouth.moveTo(cx - 3, cy - 3)
                mouth.curveTo(cx - 1, cy - 1, cx + 1, cy - 1, cx + 3, cy - 3)
                self.canv.drawPath(mouth, stroke=1, fill=0)

            elif i == 2:
                self.canv.circle(cx - 2, cy + 2, 0.75, stroke=0, fill=1)
                self.canv.circle(cx + 2, cy + 2, 0.75, stroke=0, fill=1)
                self.canv.line(cx - 3, cy - 2, cx + 3, cy - 2)

            elif i == 3:
                self.canv.circle(cx - 2, cy + 2, 0.75, stroke=0, fill=1)
                self.canv.circle(cx + 2, cy + 2, 0.75, stroke=0, fill=1)
                mouth = self.canv.beginPath()
                mouth.moveTo(cx - 3, cy - 1)
                mouth.curveTo(cx - 1, cy - 4, cx + 1, cy - 4, cx + 3, cy - 1)
                self.canv.drawPath(mouth, stroke=1, fill=0)

        self.canv.restoreState()


class NotebookPageStackCanvas(canvas.Canvas):
    """Background painter class generating 3D paper stack styles and clickable binder tab hotspots."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active_month = "2027"

    def update_month(self, month_str):
        self.active_month = month_str

    def showPage(self):
        self.saveState()

        border_color = HexColor("#D1D1D1")
        page_edge_color = HexColor("#EAEAEA")
        spine_color = HexColor("#B5B5B5")
        default_tab_bg = HexColor("#F8F9FA")
        brand_coral_color = HexColor("#E07A5F")

        self.setLineWidth(1)
        self.setStrokeColor(border_color)
        self.setFillColor(HexColor("#FFFFFF"))
        self.rect(45, 60, 488, 692, stroke=1, fill=0)

        right_wall_x = 533
        self.setLineWidth(0.75)
        self.setStrokeColor(page_edge_color)
        for offset in range(1, 4):
            gap = offset * 1.5
            self.line(right_wall_x + gap, 60 - gap, right_wall_x + gap, 752)
            self.line(45, 60 - gap, right_wall_x + gap, 60 - gap)

        self.setStrokeColor(spine_color)
        self.setLineWidth(2)
        self.line(47, 60, 47, 752)
        self.setLineWidth(0.5)
        self.setStrokeColor(page_edge_color)
        self.line(50, 60, 50, 752)

        tabs_list = [
            "2027",
            "JAN",
            "FEB",
            "MAR",
            "APR",
            "MAY",
            "JUN",
            "JUL",
            "AUG",
            "SEP",
            "OCT",
            "NOV",
            "DEC",
        ]
        tab_x, tab_w, tab_h, start_y = 533, 42, 38, 706

        for i, tab_name in enumerate(tabs_list):
            current_y = start_y - (i * (tab_h + 5))

            is_active = tab_name == self.active_month
            current_tab_bg = brand_coral_color if is_active else default_tab_bg
            current_text_color = HexColor("#FFFFFF") if is_active else brand_coral_color
            current_border_color = brand_coral_color if is_active else border_color

            tab_path = self.beginPath()
            tab_path.moveTo(tab_x, current_y + tab_h)
            tab_path.lineTo(tab_x + tab_w - 4, current_y + tab_h)
            tab_path.curveTo(
                tab_x + tab_w,
                current_y + tab_h,
                tab_x + tab_w,
                current_y + tab_h - 4,
                tab_x + tab_w,
                current_y + tab_h - 4,
            )
            tab_path.lineTo(tab_x + tab_w, current_y + 4)
            tab_path.curveTo(
                tab_x + tab_w,
                current_y,
                tab_x + tab_w - 4,
                current_y,
                tab_x + tab_w - 4,
                current_y,
            )
            tab_path.lineTo(tab_x, current_y)

            self.setFillColor(current_tab_bg)
            self.setStrokeColor(current_border_color)
            self.setLineWidth(1)
            self.drawPath(tab_path, stroke=1, fill=1)

            if tab_name == "2027":
                self.setFont(FONT_HANDWRITTEN, 7)
            else:
                self.setFont(FONT_HANDWRITTEN, 8)

            self.setFillColor(current_text_color)
            text_x = tab_x + (tab_w / 2)
            text_y = current_y + (tab_h / 2) - 3
            self.drawCentredString(text_x, text_y, tab_name)

            # --- SECURED UNIFORM NAVIGATION MATRIX ANCHOR MAPPING ---
            destination_name = (
                "page_index" if tab_name == "2027" else f"page_{tab_name}"
            )
            x1, y1 = tab_x, current_y
            x2, y2 = tab_x + tab_w, current_y + tab_h

            self.linkAbsolute(
                contents=f"Go to {tab_name}",
                destinationname=destination_name,
                Rect=(x1, y1, x2, y2),
                Border="[0 0 0]",
            )

        self.restoreState()
        super().showPage()


def load_json_data(json_path):
    full_path = os.path.join(PROJECT_DIR, json_path)
    if os.path.exists(full_path):
        with open(full_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def generate_yearly_planner(year=2027, filename="My_Cozy_Notebook_Journal.pdf"):
    user_home = os.path.expanduser("~")
    local_output_path = os.path.join(user_home, filename)

    doc = SimpleDocTemplate(
        local_output_path,
        pagesize=letter,
        leftMargin=50,
        rightMargin=84,
        topMargin=44,
        bottomMargin=54,
    )

    styles = getSampleStyleSheet()

    TEXT_MAIN_COLOR = HexColor("#1D2D44")
    PROMPT_COLOR = HexColor("#E07A5F")
    TEXT_QUOTE_COLOR = HexColor("#415A77")

    title_style = ParagraphStyle(
        "DayTitle",
        parent=styles["Heading1"],
        fontName=FONT_HANDWRITTEN,
        fontSize=15,
        leading=18,
        textColor=TEXT_MAIN_COLOR,
        spaceAfter=0,
        rightIndent=0,
        leftIndent=0,
        firstLineIndent=0,
    )
    prompt_style = ParagraphStyle(
        "StudioPrompt",
        parent=styles["Normal"],
        fontName=FONT_HANDWRITTEN,
        fontSize=10,
        leading=14,
        textColor=PROMPT_COLOR,
        spaceAfter=0,
        rightIndent=35,
        leftIndent=0,
        firstLineIndent=0,
        alignment=0,
    )
    box_header_style = ParagraphStyle(
        "BoxHeader",
        parent=styles["Normal"],
        fontName=FONT_HANDWRITTEN,
        fontSize=9,
        leading=12,
        textColor=TEXT_QUOTE_COLOR,
        spaceAfter=4,
    )
    quote_style = ParagraphStyle(
        "CozyQuote",
        parent=styles["Normal"],
        fontName=FONT_HANDWRITTEN,
        fontSize=10,
        leading=14,
        textColor=TEXT_QUOTE_COLOR,
        alignment=1,
        rightIndent=40,
        leftIndent=40,
    )
    nav_link_style = ParagraphStyle(
        "NavLink",
        parent=styles["Normal"],
        fontName=FONT_HANDWRITTEN,
        fontSize=8.5,
        leading=11,
        textColor=HexColor("#415A77"),
        alignment=2,
    )
    index_title_style = ParagraphStyle(
        "IndexTitle",
        parent=styles["Heading1"],
        fontName=FONT_HANDWRITTEN,
        fontSize=15,
        leading=18,
        textColor=TEXT_MAIN_COLOR,
        alignment=1,
        spaceAfter=8,
    )
    index_month_style = ParagraphStyle(
        "IndexMonth",
        parent=styles["Normal"],
        fontName=FONT_HANDWRITTEN,
        fontSize=9,
        leading=11,
        textColor=PROMPT_COLOR,
        alignment=1,
    )
    index_day_link_style = ParagraphStyle(
        "IndexDayLink",
        parent=styles["Normal"],
        fontName=FONT_HANDWRITTEN,
        fontSize=7.5,
        leading=9,
        alignment=1,
    )
    divider_title_style = ParagraphStyle(
        "DivTitle",
        parent=styles["Heading1"],
        fontName=FONT_HANDWRITTEN,
        fontSize=32,
        leading=38,
        textColor=TEXT_MAIN_COLOR,
        alignment=1,
    )
    story = []

    prompts_pool = load_json_data("prompts.json")
    quotes_pool = load_json_data("quotes.json")

    # --- UNIFIED LAYOUT MATRICES AND MEASUREMENTS ---
    TOTAL_CONTENT_WIDTH = 458
    WIDTHS_TWIN_BOXES = [224, 10, 224]
    WIDTHS_HEADER_ROW = [278, 180]

    # =========================================================================
    # --- PHASE 0: COZY ABSTRACT COVER PAGE ---
    # =========================================================================
    print("Designing cozy abstract cover sheet...")
    story.append(Macro("canvas.update_month('2027')"))
    story.append(Paragraph('<a name="page_cover"/>', styles["Normal"]))

    cover_title_style = ParagraphStyle(
        "CoverTitle",
        parent=styles["Heading1"],
        fontName=FONT_HANDWRITTEN,
        fontSize=28,
        leading=34,
        textColor=TEXT_MAIN_COLOR,
        alignment=1,
        spaceAfter=15,
    )
    story.append(Spacer(1, 40))
    story.append(Paragraph("My Art Journal 2027", cover_title_style))
    story.append(Spacer(1, 20))

    cover_image_path = os.path.join(PROJECT_DIR, "cover_art.png")
    if os.path.exists(cover_image_path):
        art_element = Image(cover_image_path, width=330, height=330)
    else:
        print("cover_art.png not found, building temporary grid placeholder block")
        art_element = DrawingCanvasBlock(330, 330, has_dots=True)

    art_center_table = Table([[art_element]], colWidths=[TOTAL_CONTENT_WIDTH])
    art_center_table.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    story.append(art_center_table)
    story.append(Spacer(1, 40))

    cover_owner_style = ParagraphStyle(
        "CoverOwner",
        parent=styles["Normal"],
        fontName=FONT_HANDWRITTEN,
        fontSize=12,
        leading=16,
        textColor=TEXT_QUOTE_COLOR,
        alignment=1,
    )
    story.append(Paragraph("This notebook belongs to:", cover_owner_style))
    story.append(Spacer(1, 10))

    name_line_table = Table([[""]], colWidths=[200], rowHeights=[20])
    name_line_table.setStyle(
        TableStyle(
            [
                ("LINEBELOW", (0, 0), (-1, -1), 1, HexColor("#D1D1D1")),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )

    centered_name_container = Table(
        [[name_line_table]], colWidths=[TOTAL_CONTENT_WIDTH]
    )
    centered_name_container.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    story.append(centered_name_container)
    story.append(PageBreak())

    # =========================================================================
    # --- PHASE 1: GENERATE INTERACTIVE YEARLY INDEX DASHBOARD ---
    # =========================================================================
    print("Designing unified 12-month quick-jump master index grid...")
    story.append(Paragraph('<a name="page_index"/>', styles["Normal"]))

    index_nav_html = (
        '<a href="#page_JAN"><font color="#E07A5F">Next (Jan Divider) →</font></a>'
    )
    index_title_with_cover = f'<a href="#page_cover"><font color="#E07A5F">← Cover</font></a>    Yearly Index — {PLANNER_YEAR}'

    index_header_table = Table(
        [
            [
                Paragraph(index_title_with_cover, index_title_style),
                Paragraph(index_nav_html, nav_link_style),
            ]
        ],
        colWidths=WIDTHS_HEADER_ROW,
    )
    index_header_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    story.append(index_header_table)
    story.append(Spacer(1, 14))

    months_list = [
        ("JANUARY", 1),
        ("FEBRUARY", 2),
        ("MARCH", 3),
        ("APRIL", 4),
        ("MAY", 5),
        ("JUNE", 6),
        ("JULY", 7),
        ("AUGUST", 8),
        ("SEPTEMBER", 9),
        ("OCTOBER", 10),
        ("NOVEMBER", 11),
        ("DECEMBER", 12),
    ]

    master_index_widths = [114.5, 114.5, 114.5, 114.5]
    grid_rows = []
    current_row_cells = []

    for idx, (m_name, m_num) in enumerate(months_list):
        month_flowables = [
            Paragraph(f"<b>{m_name}</b>", index_month_style),
            Spacer(1, 2),
        ]
        cal_matrix = [["S", "M", "T", "W", "T", "F", "S"]]
        day_row = [""] * 7

        first_day_date = datetime(PLANNER_YEAR, m_num, 1)
        start_weekday = (first_day_date.weekday() + 1) % 7

        for fill_idx in range(start_weekday):
            day_row[fill_idx] = ""

        curr_date = first_day_date
        while curr_date.month == m_num:
            w_idx = (curr_date.weekday() + 1) % 7
            tag_id = curr_date.strftime("day_%m_%d")
            day_num_str = str(curr_date.day)

            day_row[w_idx] = (
                f'<a href="#{tag_id}"><font color="#1D2D44">{day_num_str}</font></a>'
            )
            if w_idx == 6 or (curr_date + timedelta(days=1)).month != m_num:
                cal_matrix.append(day_row)
                day_row = [""] * 7
            curr_date += timedelta(days=1)

        cal_table_data = []
        for row in cal_matrix:
            cal_table_data.append(
                [
                    Paragraph(cell, index_day_link_style) if cell else Spacer(1, 1)
                    for cell in row
                ]
            )

        minical_table = Table(cal_table_data, colWidths=[14.5] * 7)
        minical_table.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                    ("TOPPADDING", (0, 0), (-1, -1), 1),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
                ]
            )
        )

        month_flowables.append(minical_table)
        month_flowables.append(Spacer(1, 8))
        current_row_cells.append(month_flowables)

        if (idx + 1) % 4 == 0:
            grid_rows.append(current_row_cells)
            current_row_cells = []

    index_master_table = Table(grid_rows, colWidths=master_index_widths)
    index_master_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 1),
                ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    story.append(index_master_table)
    story.append(Spacer(1, 14))

    story.append(Paragraph("Index Notes & Planning Goals", box_header_style))
    story.append(Spacer(1, 4))
    story.append(
        DrawingCanvasBlock(
            TOTAL_CONTENT_WIDTH, 200, has_dots=True, is_lettering_track=False
        )
    )
    story.append(PageBreak())

    # =========================================================================
    # --- PHASE 2: GENERATE THE CORE 365 JOURNAL SHEETS + MONTHLY DIVIDERS ---
    # =========================================================================
    print(
        "Compiling 365 perfectly scaled sheets with interactive monthly divider calendars..."
    )

    MONTH_NAMES_FULL = {
        "JAN": "January",
        "FEB": "February",
        "MAR": "March",
        "APR": "April",
        "MAY": "May",
        "JUN": "June",
        "JUL": "July",
        "AUG": "August",
        "SEP": "September",
        "OCT": "October",
        "NOV": "November",
        "DEC": "December",
    }

    stored_month_first_prompt = ""

    for day_offset in range(365):
        current_date = START_DATE + timedelta(days=day_offset)
        day_title = current_date.strftime("%A, %B %d, %Y")
        m_key = current_date.strftime("%b").upper()

        is_first_day = current_date.day == 1
        tomorrow_date = current_date + timedelta(days=1)
        is_last_day = tomorrow_date.month != current_date.month

        # ---------------------------------------------------------------------
        # --- MONTHLY INTERACTIVE DIVIDER CALENDAR GENERATOR ---
        # ---------------------------------------------------------------------
        if is_first_day:
            story.append(Macro(f"canvas.update_month('{m_key}')"))
            story.append(Paragraph(f'<a name="page_{m_key}"/>', styles["Normal"]))

            full_month_name = MONTH_NAMES_FULL[m_key]
            div_title = f"{full_month_name} — {PLANNER_YEAR}"

            div_links_html = ""
            # --- CONTINUATION OF MONTHLY INTERACTIVE DIVIDER CALENDAR ---
            if day_offset > 0:
                prev_date = current_date - timedelta(days=1)
                p_tag = prev_date.strftime("day_%m_%d")
                div_links_html += (
                    f'<a href="#{p_tag}"><font color="#E07A5F">← Prev</font></a>'
                )
            else:
                div_links_html += (
                    '<a href="#page_index"><font color="#E07A5F">← Index</font></a>'
                )

            div_links_html += "  |  "
            curr_day_tag = current_date.strftime("day_%m_%d")
            div_links_html += (
                f'<a href="#{curr_day_tag}"><font color="#E07A5F">Next →</font></a>'
            )

            div_header_table = Table(
                [
                    [
                        Paragraph(div_title, divider_title_style),
                        Paragraph(div_links_html, nav_link_style),
                    ]
                ],
                colWidths=WIDTHS_HEADER_ROW,
            )
            div_header_table.setStyle(
                TableStyle(
                    [
                        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 0),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                        ("TOPPADDING", (0, 0), (-1, -1), 0),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                    ]
                )
            )
            story.append(div_header_table)
            story.append(Spacer(1, 15))

            div_cal_matrix = [["S", "M", "T", "W", "T", "F", "S"]]
            div_day_row = [""] * 7

            first_of_month = datetime(PLANNER_YEAR, current_date.month, 1)
            div_start_weekday = (first_of_month.weekday() + 1) % 7
            for fill_idx in range(div_start_weekday):
                div_day_row[fill_idx] = ""

            loop_date = first_of_month
            while loop_date.month == current_date.month:
                w_idx = (loop_date.weekday() + 1) % 7
                day_tag = loop_date.strftime("day_%m_%d")

                div_day_row[w_idx] = (
                    f'<a href="#{day_tag}"><font color="#1D2D44">{loop_date.day}</font></a>'
                )

                if (
                    w_idx == 6
                    or (loop_date + timedelta(days=1)).month != current_date.month
                ):
                    div_cal_matrix.append(div_day_row)
                    div_day_row = [""] * 7
                loop_date += timedelta(days=1)

            div_table_data = []
            for row in div_cal_matrix:
                div_table_data.append(
                    [
                        Paragraph(cell, index_day_link_style) if cell else Spacer(1, 1)
                        for cell in row
                    ]
                )

            month_divider_table = Table(div_table_data, colWidths=[65.4] * 7)
            month_divider_table.setStyle(
                TableStyle(
                    [
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 0),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                        ("TOPPADDING", (0, 0), (-1, -1), 8),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                        ("LINEBELOW", (0, 0), (-1, 0), 1, HexColor("#E5E5E5")),
                    ]
                )
            )

            centered_div_container = Table(
                [[month_divider_table]], colWidths=[TOTAL_CONTENT_WIDTH]
            )
            centered_div_container.setStyle(
                TableStyle(
                    [
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 0),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                    ]
                )
            )
            story.append(centered_div_container)
            story.append(Spacer(1, 10))

            story.append(
                Paragraph(
                    f"{full_month_name} Notes, Projects & Manifestations",
                    box_header_style,
                )
            )
            story.append(Spacer(1, 4))

            div_canvas = DrawingCanvasBlock(
                TOTAL_CONTENT_WIDTH, 290, has_dots=True, is_lettering_track=False
            )
            div_center_table = Table([[div_canvas]], colWidths=[TOTAL_CONTENT_WIDTH])
            div_center_table.setStyle(
                TableStyle(
                    [
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 0),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                        ("TOPPADDING", (0, 0), (-1, -1), 0),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                    ]
                )
            )
            story.append(div_center_table)
            story.append(PageBreak())
        # ---------------------------------------------------------------------

        # --- CORE DAILY PAGE TRACK WRITER ---
        story.append(Macro(f"canvas.update_month('{m_key}')"))

        tag_id = current_date.strftime("day_%m_%d")
        story.append(Paragraph(f'<a name="{tag_id}"/>', styles["Normal"]))

        nav_links_html = ""
        if day_offset > 0:
            yesterday_date = current_date - timedelta(days=1)
            y_tag = yesterday_date.strftime("day_%m_%d")
            if yesterday_date.month != current_date.month:
                prev_m_key = yesterday_date.strftime("%b").upper()
                nav_links_html += f'<a href="#page_{prev_m_key}"><font color="#E07A5F">← Divider</font></a>'
            else:
                nav_links_html += (
                    f'<a href="#{y_tag}"><font color="#E07A5F">← Prev</font></a>'
                )
        else:
            nav_links_html += (
                '<a href="#page_index"><font color="#E07A5F">← Index</font></a>'
            )

        nav_links_html += "  |  "

        if day_offset < 364:
            tomorrow_date = current_date + timedelta(days=1)
            t_tag = tomorrow_date.strftime("day_%m_%d")
            if tomorrow_date.month != current_date.month:
                next_m_key = tomorrow_date.strftime("%b").upper()
                nav_links_html += f'<a href="#page_{next_m_key}"><font color="#E07A5F">Divider →</font></a>'
            else:
                nav_links_html += (
                    f'<a href="#{t_tag}"><font color="#E07A5F">Next →</font></a>'
                )
        else:
            nav_links_html += (
                '<a href="#page_index"><font color="#E07A5F">Index →</font></a>'
            )

        if prompts_pool:
            if is_first_day:
                cleaned_json_prompt = str(
                    prompts_pool[day_offset % len(prompts_pool)]
                ).strip()
                stored_month_first_prompt = cleaned_json_prompt
                raw_prompt = f"Prompt: {cleaned_json_prompt}"
            elif is_last_day:
                raw_prompt = f"Prompt (Month-End Review): {stored_month_first_prompt}"
            else:
                cleaned_json_prompt = str(
                    prompts_pool[day_offset % len(prompts_pool)]
                ).strip()
                raw_prompt = f"Prompt: {cleaned_json_prompt}"
        else:
            if is_last_day:
                raw_prompt = "Prompt (Month-End Review): Re-draw your first creation of the month and track your growth."
            else:
                raw_prompt = "Prompt: Open your canvas, pick a vibrant color, and let lines flow."

        if quotes_pool:
            quote_item = quotes_pool[day_offset % len(quotes_pool)]
            q_text = str(quote_item.get("text", "")).strip()
            q_author = str(quote_item.get("from", "")).strip()
            raw_quote = f"“{q_text}” — {q_author}"
        else:
            raw_quote = "“Creativity is intelligence having fun.” — Albert Einstein"

        header_table_data = [
            [
                Paragraph(day_title, title_style),
                Paragraph(nav_links_html, nav_link_style),
            ]
        ]
        header_row_table = Table(header_table_data, colWidths=WIDTHS_HEADER_ROW)
        header_row_table.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                    ("TOPPADDING", (0, 0), (-1, -1), 0),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                ]
            )
        )

        story.append(header_row_table)
        story.append(Spacer(1, 14))
        story.append(Paragraph(raw_prompt, prompt_style))
        story.append(Spacer(1, 24))

        table_data = [
            [
                Paragraph("Brain Dump to clear your mind.", box_header_style),
                Spacer(1, 1),
                Paragraph("☕ 5-Minute Doodle", box_header_style),
            ],
            [
                DrawingCanvasBlock(224, 250, has_dots=False),
                Spacer(1, 1),
                DrawingCanvasBlock(224, 250, has_dots=True),
            ],
            [Spacer(1, 24), Spacer(1, 1), Spacer(1, 1)],
            [
                Paragraph("Daily Lettering Practice", box_header_style),
                Spacer(1, 1),
                Spacer(1, 1),
            ],
            [
                DrawingCanvasBlock(458, 190, has_dots=False, is_lettering_track=True),
                Spacer(1, 1),
                Spacer(1, 1),
            ],
            [Spacer(1, 16), Spacer(1, 1), Spacer(1, 1)],
            [
                Paragraph(raw_quote, quote_style),
                Spacer(1, 1),
                MoodTrackerWidget(width=224, height=35),
            ],
        ]

        master_page_table = Table(table_data, colWidths=WIDTHS_TWIN_BOXES)
        master_page_table.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                    ("TOPPADDING", (0, 0), (-1, -1), 0),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                    ("SPAN", (0, 3), (2, 3)),
                    ("SPAN", (0, 4), (2, 4)),
                    ("SPAN", (0, 5), (2, 5)),
                    ("SPAN", (0, 6), (1, 6)),
                ]
            )
        )
        story.append(master_page_table)

        if day_offset < 364:
            story.append(PageBreak())

    print("Launching layout renderer engine...")
    doc.build(story, canvasmaker=NotebookPageStackCanvas)
    print("\nSUCCESS! Your interactive 3D stacked notebook has compiled flawlessly.")


if __name__ == "__main__":
    generate_yearly_planner()
