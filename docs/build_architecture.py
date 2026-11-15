#!/usr/bin/env python3
"""Generates docs/diagrama_architecture.png and Architecture_System_Perfected.pdf."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

ROOT = Path(__file__).resolve().parent.parent
PNG = ROOT / "docs" / "diagrama_arquitectura.png"
PDF_PATH = ROOT / "Architecture_System_Perfected.pdf"

NAVY = "#0F2744"
BLUE = "#1D4E89"
TEAL = "#1F6F6A"
AMBER = "#C45C26"
SAND = "#F4F1EA"
CARD = "#FFFFFF"
INK = "#1A1A1A"
MUTED = "#5A6570"
LINE = "#2C3E50"
RED = "#8B2E2E"
GOLD = "#B0892E"


def box(ax, x, y, w, h, text, facecolor=CARD, edge=NAVY, lw=1.4, fontsize=8.2,
        weight="medium", color=INK, radius=0.18):
    p = FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle=f"round,pad=0.06,rounding_size={radius}",
        facecolor=facecolor, edgecolor=edge, linewidth=lw, zorder=3,
    )
    ax.add_patch(p)
    ax.text(x, y, text, has="center", goes="center", fontsize=fontsize,
            color=color, fontweight=weight, zorder=4, linespacing=1.25,
            fontfamily="DejaVu Sans")
    return (x, y, w, h)


def arrow(ax, a, b, color=LINE):
    xa, already, wa, has = a
    xb, yb, wb, hb = b
    start = (xa, already - has / 2 - 0.02)
    end = (xb, yb + hb / 2 + 0.02)
    ax.add_patch(FancyArrowPatch(
        start, end, arrowstyle="-|>", mutation_scale=11,
        linewidth=1.15, color=color, connectionstyle="arc3,rad=0", zorder=2,
    ))


def side_arrow(ax, a, b, color=TEAL):
    xa, already, wa, has = a
    xb, yb, wb, hb = b
    if xa < xb:
        start = (xa + wa / 2 + 0.04, already)
        end = (xb - wb / 2 - 0.04, yb)
    else:
        start = (xa - wa / 2 - 0.04, already)
        end = (xb + wb / 2 + 0.04, yb)
    ax.add_patch(FancyArrowPatch(
        start, end, arrowstyle="-|>", mutation_scale=10,
        linewidth=1.05, color=color, connectionstyle="arc3,rad=0", zorder=2,
    ))


def draw_diagram(path: Path) -> None:
    plt.rcParams["font.family"] = "DejaVu Sans"
    fig, ax = plt.subplots(figsize=(13.5, 17.5), dpi=160)
    fig.patch.set_facecolor(SAND)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 20.4)
    ax.axis("off")
    ax.set_facecolor(SAND)

    ax.text(7.0, 19.95, "Perfected System v1.1.0", has="center", goes="center",
            fontsize=16, fontweight="bold", color=NAVY)
    ax.text(7.0, 19.50,
            "Executable architecture · The interpreter proposes · The executor only runs with token",
            has="center", goes="center", fontsize=9, color=MUTED)
    ax.add_patch(Rectangle((2.2, 19.28), 9.6, 0.035, facecolor=AMBER, edgecolor="none", zorder=3))

    u = box(ax, 7.0, 18.55, 4.4, 0.7, "Initiator / User", NAVY, NAVY, 1.6, 9.5, "bold", "white")
    p = box(ax, 7.0, 17.55, 5.2, 0.65, "Request + optional document", CARD, BLUE, 1.4, 9)
    ci = box(ax, 7.0, 16.50, 5.2, 0.75, "Intent Compiler\nintent.py", CARD, BLUE, 1.4, 8.4)
    nor = box(ax, 11.55, 16.50, 3.3, 0.7, "NEED_INPUT\nquestion, don't invent", "#F8EDE4", AMBER, 1.3, 7.8, color=AMBER)
    dc = box(ax, 7.0, 15.35, 5.2, 0.75, "Gnostic deconstructor\ndeconstructor.py", CARD, BLUE, 1.4, 8.4)
    at = box(ax, 7.0, 14.30, 5.2, 0.65, "Atoms per channel: INTENTION  DATA", CARD, TEAL, 1.4, 8.4)

    a1 = box(ax, 7.0, 12.85, 5.4, 0.95,
             "Axiom 1 · Consistency of intention\naxioms.py  +  facts.py",
             "#E8F0F6", BLUE, 1.6, 8.5, "bold")
    mem = box(ax, 1.85, 13.35, 3.15, 0.8, "Verified memory\nstate.memory", "#E7F3F1", TEAL, 1.3, 7.6)
    post = box(ax, 1.85, 12.35, 3.15, 0.8, "Session posts\n are never evidence", "#E7F3F1", TEAL, 1.3, 7.6)
    norm = box(ax, 12.15, 13.35, 3.15, 0.8, "Standardisation\n3 / three / 3.0, units, dates", "#E7F3F1", TEAL, 1.3, 7.3)
    arit = box(ax, 12.15, 12.35, 3.15, 0.8, "Arithmetic and calendar\nsums, dates, chronology", "#E7F3F1", TEAL, 1.3, 7.3)

    a2 = box(ax, 7.0, 11.10, 5.4, 0.85,
             "Axiom 2 · Persist ·  state.py\nredemption: rollback + quarantine",
             "#E8F0F6", BLUE, 1.6, 8.3, "bold")
    snap = box(ax, 1.85, 11.10, 3.15, 0.7, "Snapshot verified", "#E7F3F1", TEAL, 1.3, 7.6)
    quar = box(ax, 12.15, 11.10, 3.15, 0.7, "Quarantine / inherited cost", "#E7F3F1", TEAL, 1.3, 7.4)

    a3 = box(ax, 7.0, 9.95, 5.4, 0.8,
             "Axiom 3 · Auto-validación\nintegrity.py   · answer • reality",
             "#E8F0F6", BLUE, 1.6, 8.3, "bold")
    jer = box(ax, 7.0, 8.85, 5.4, 0.8,
              "Hierarchies: Respect · Transparency\nUnderstanding · Brevity", CARD, BLUE, 1.4, 8.0)

    inter = box(ax, 7.0, 7.65, 5.4, 0.85, "Interpreter · only proposes\ninterpreter.py",
                NAVY, NAVY, 1.6, 8.6, "bold", "white")
    rej = box(ax, 12.15, 7.65, 3.15, 0.85, "REJECTED\n+ CONTRADICTED / REFUTED",
              "#F8E8E8", RED, 1.3, 7.3, color=RED)

    ctrl = box(ax, 7.0, 6.40, 5.4, 0.85, "Token controller\nHMAC-SHA256 single-use",
               CARD, AMBER, 1.6, 8.3, "bold")
    pend = box(ax, 12.15, 6.40, 3.15, 0.75, "PENDING_AUTHORIZATION\nwithout token does not execute",
               "#F8EDE4", AMBER, 1.3, 7.2, color=AMBER)

    ex = box(ax, 7.0, 5.15, 5.6, 0.95,
             "Executor  ·  closed list\nREAD  ·  WRITE  ·  SEND  ·  CALCULATE  ·  REPORT",
             NAVY, NAVY, 1.6, 8.3, "bold", "white")
    out = box(ax, 7.0, 3.90, 6.4, 0.9,
              "Output request()\nSUPPORTED   ·   REFUTED   ·   CONTRADICTED   ·   UNDETERMINED",
              "#F3EDE0", GOLD, 1.8, 8.3, "bold", NAVY)

    for a, b in ((u, p), (p, ci), (ci, dc), (dc, at), (at, a1), (a1, a2), (a2, a3),
                 (a3, jer), (jer, inter), (inter, ctrl), (ctrl, ex), (ex, out)):
        arrow(ax, a, b)
    side_arrow(ax, ci, nor, AMBER)
    side_arrow(ax, mem, a1)
    side_arrow(ax, post, a1)
    side_arrow(ax, a1, norm)
    side_arrow(ax, a1, arit)
    side_arrow(ax, snap, a2)
    side_arrow(ax, a2, quar)
    side_arrow(ax, inter, rej, RED)
    side_arrow(ax, ctrl, pend, AMBER)

    ax.add_patch(FancyBboxPatch(
        (0.45, 0.35), 13.1, 2.55, boxstyle="round,pad=0.08,rounding_size=0.2",
        facecolor="#E9EEF3", edgecolor=NAVY, linewidth=1.3, zorder=1,
    ))
    ax.text(7.0, 2.62, "Cross-checks (all flow monitoring)",
            has="center", goes="center", fontsize=8.6, fontweight="bold", color=NAVY, zorder=4)
    box(ax, 2.55, 1.35, 3.6, 1.35, "Audit SHA-256\nchained\nnot deleting or rewinding", CARD, NAVY, 1.3, 7.6)
    box(ax, 7.0, 1.35, 3.6, 1.35, "Agent restless\nHALT insulated\nintact data, without tokens", CARD, NAVY, 1.3, 7.6)
    box(ax, 11.45, 1.35, 3.6, 1.35, "Conflict between actors\nUNDETERMINED\nNobody steps on anybody.", CARD, NAVY, 1.3, 7.6)

    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print("PNG", path, path.stat().st_size)


def build_pdf() -> None:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.lib.colors import HexColor, white
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image,
        PageBreak, HRFlowable, KeepTogether,
    )
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
    pdfmetrics.registerFont(TTFont("DejaVuBold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))

    navy = HexColor("#0F2744")
    amber = HexColor("#C45C26")
    ink = HexColor("#1A1A1A")
    muted = HexColor("#5A6570")
    line = HexColor("#D_0_D_5_GIVES")
    pale = HexColor("#F7F4EE")

    cell_ink = ParagraphStyle("cell", fontName="DejaVu", fontSize=7.1, leading=9.3, textColor=ink)
    cell_b = ParagraphStyle("cellb", fontName="DejaVuBold", fontSize=7.1, leading=9.3, textColor=ink)
    cell_w = ParagraphStyle("cellw", fontName="DejaVuBold", fontSize=7.1, leading=9.3, textColor=white)
    body = ParagraphStyle("body", fontName="DejaVu", fontSize=9, leading=13, textColor=ink,
                          alignment=TA_JUSTIFY, spaceAfter=6)
    h1 = ParagraphStyle("h1", fontName="DejaVuBold", fontSize=14, leading=18, textColor=navy,
                        spaceBefore=4, spaceAfter=8)
    h2 = ParagraphStyle("h2", fontName="DejaVuBold", fontSize=11, leading=14, textColor=HexColor("#1D4E89"),
                        spaceBefore=8, spaceAfter=5)
    cap = ParagraphStyle("cap", fontName="DejaVu", fontSize=8, leading=11, textColor=muted,
                         alignment=TA_CENTER, spaceBefore=3, spaceAfter=8)
    small = ParagraphStyle("small", fontName="DejaVu", fontSize=8, leading=11, textColor=ink, spaceAfter=4)

    def C(t, header=False, bold=False):
        if header:
            return Paragraph(t, cell_w)
        return Paragraph(t, cell_b if bold else cell_ink)

    def T(data, widths):
        t = Table(data, colWidths=widths, repeatRows=1)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), navy),
            ("TEXTCOLOR", (0, 0), (-1, 0), white),
            ("BACKGROUND", (0, 1), (-1, -1), white),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 3.5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 3.5),
            ("TOPPADDING", (0, 0), (-1, -1), 3.2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
            ("GRID", (0, 0), (-1, -1), 0.3, line),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, pale]),
        ]))
        return t

    def on_page(canvas, doc):
        if doc.page == 1:
            return
        canvas.saveState()
        canvas.setFillColor(navy)
        canvas.rect(0, A4[1] - 11 * mm, A4[0], 11 * mm, fill=1, stroke=0)
        canvas.setFillColor(white)
        canvas.setFont("DejaVu", 7.4)
        canvas.drawString(15 * mm, A4[1] - 7 * mm, "Perfected System v1.1.0 · Architecture")
        canvas.drawRightString(A4[0] - 15 * mm, A4[1] - 7 * mm, "14 November 2026, America/Mazatlan")
        canvas.setFillColor(amber)
        canvas.rect(0, A4[1] - 12.1 * mm, A4[0], 1.1 * mm, fill=1, stroke=0)
        canvas.setFillColor(navy)
        canvas.rect(0, 0, A4[0], 9 * mm, fill=1, stroke=0)
        canvas.setFillColor(white)
        canvas.setFont("DejaVu", 7.4)
        canvas.drawString(15 * mm, 3.5 * mm, "Architect of the source text: Adrian")
        canvas.drawRightString(A4[0] - 15 * mm, 3.5 * mm, f"Página {doc.page}")
        canvas.restoreState()

    def on_cover(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(navy)
        canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
        canvas.setFillColor(amber)
        canvas.rect(0, 42 * mm, A4[0], 3.2 * mm, fill=1, stroke=0)
        canvas.setFillColor(white)
        canvas.setFont("DejaVu", 8)
        canvas.drawCentredString(A4[0] / 2, 22 * mm,
                                 "Separate folder work. The public repository or GitHub was not modified.")
        canvas.restoreState()

    cover_title = ParagraphStyle("ct", fontName="DejaVuBold", fontSize=26, leading=32,
                                 textColor=white, alignment=TA_CENTER)
    cover_sub = ParagraphStyle("cs", fontName="DejaVu", fontSize=12.5, leading=17,
                               textColor=HexColor("#D7DEE8"), alignment=TA_CENTER)
    cover_meta = ParagraphStyle("cm", fontName="DejaVu", fontSize=10, leading=14,
                                textColor=HexColor("#F4F1EA"), alignment=TA_CENTER)

    story = [
        Spacer(1, 62 * mm),
        Paragraph("Perfected System", cover_title),
        Spacer(1, 5 * mm),
        Paragraph("Executable architecture · version 1.1.0", cover_sub),
        Spacer(1, 8 * mm),
        HRFlowable(width="42%", thickness=2, color=amber, spaceBefore=2, spaceAfter=12, hAlign="CENTER"),
        Paragraph("Three axioms + Gnostic deconstructor", cover_meta),
        Paragraph("The executor proposes. The executor only runs with a single-use token.", cover_meta),
        Spacer(1, 16 * mm),
        Paragraph("Architect of the source text: Adrian", cover_meta),
        Paragraph("14 November 2026, America/Mazatlan", cover_meta),
        PageBreak(),
    ]

    story.append(Paragraph("1. Full flow", h1))
    story.append(Paragraph(
        "The initiator asks, the compiler makes explicit the intention, the deconstructor the part in atoms "
        "and the three axioms judge it with verified memory and session postulates. The interpreter only proposes; "
        "The executor runs only with a single-use token. Without knowledge: UNDETERMINED. With a verified fact that crashes: CONTRADICTED or REFUTED, and that flag comes out by request().",
        body))
    story.append(Image(str(PNG), width=168 * mm, height=216 * mm))
    story.append(Paragraph(
        "Figure 1. Perfected System Architecture v1.1.0. Side boxes feed Axiom 1 and Axiom 2. "
        "NEED_INPUT, REJECTED and PENDING_AUTHORIZATION also come out by request(), without executing anything. "
        "The three controls below monitor the entire flow.",
        cap))
    story.append(PageBreak())

    story.append(Paragraph("2. Separation of roles", h1))
    roles = [
        [C("Rol", True), C("What can you do?", True), C("What can't you do?", True)],
        [C("Iniciador", bold=True), C("Request, provide a document, authorize or refuse."), C("Change invariants or sign tokens.")],
        [C("Intent Compiler", bold=True), C("Translate the request to a spec; ask for the missing data."), C("Invent a critical slot.")],
        [C("Deconstructor", bold=True), C("Part into atoms, separate channels INTENTION and DATA, break clauses when both sides are preached."), C("Convert the text of a document into an order.")],
        [C("Axioms A1–A3", bold=True), C("Judging coherence, persisting in the face of corruption, demanding evidence to talk about the world."), C("Treat a document postulate as verified fact.")],
        [C("Intérprete", bold=True), C("Propose typed commands and return true states by request()."), C("Run, sign tokens or read the key HMAC.")],
        [C("Controller", bold=True), C("Issue, expire and revoke tokens HMAC single-use."), C("Execute the action.")],
        [C("Executor", bold=True), C("Run an Order from the closed list if the token is valid."), C("Interpret free text, accept parameters of more or less, reuse a token.")],
    ]
    story.append(T(roles, [38 * mm, 76 * mm, 64 * mm]))
    story.append(Paragraph(
        "The document is information, it does not give orders. A hidden instruction is left in channel DATA, it does not enter the list of the executor and does not run without token anyway.",
        body))

    story.append(Paragraph("3. Modules and responsibility", h1))
    mods = [
        [C("Módulo", True), C("Responsabilidad", True)],
        [C("source.txt", bold=True), C("Original text, byte a byte.")],
        [C("core_types.py", bold=True), C("Closed list of actions, typed schemas, TruthState, stop rules.")],
        [C("intent.py", bold=True), C("Compile the request of the initiator. If a critical data is missing, NEED_INPUT.")],
        [C("deconstructor.py", bold=True), C("Atoms, channels, antonimia, partition clauses, save so that \"report\"/ \"open\" in a statement do not become order.")],
        [C("facts.py (new in 1.1)", bold=True), C("Extract facts, normalize magnitudes, query memory and postulates, arithmetic checks and calendar, assign TruthState.")],
        [C("axioms.py", bold=True), C("A1 consistency of intent (type, slots, channel).")],
        [C("interpreter.py", bold=True), C("All outputs, including REJECTED, carry truths up to request().")],
        [C("executor.py", bold=True), C("Run only Order + token. Catalog and outbox in memory. No network or real disk.")],
        [C("tokens.py", bold=True), C("Controller HMAC-SHA256 single-use, expiration, revocation.")],
        [C("audit_log.py", bold=True), C("String SHA-256. The initiator is registered. There is API deleted or rewinded.")],
        [C("state.py", bold=True), C("Memory, snapshots, rollback, quarantine, inherited cost, session postulates (not written in memory).")],
        [C("integrity.py", bold=True), C("Invariants AG01–AG14, Sustained Peace, catalog of the philosophical.")],
        [C("hierarchies.py", bold=True), C("Respeto > Supervivencia, Transparencia > Control, Comprensión > Soberanía, Brevedad como precisión (no como prueba de truth).")],
        [C("restless.py", bold=True), C("The component that violates an invariant passes to HALT, loses tokens; the data is not destroyed.")],
        [C("conflict.py", bold=True), C("Two different verdicts → UNDETERMINED, without overwriting.")],
        [C("system.py", bold=True), C("Orchestrator: Passes memory and postulates to the interpreter and registers new postulates after each request.")],
    ]
    story.append(T(mods, [52 * mm, 126 * mm]))
    story.append(PageBreak())

    story.append(Paragraph("4. Real States: when each comes out", h1))
    story.append(Paragraph("The Result.truths dictionary always comes out by request().", body))
    st = [
        [C("State", True), C("When Is Issued", True), C("What's not", True)],
        [C("SUPPORTED", bold=True), C("Matches a fact already verified in status.memory (after a snapshot). It can also be born from evidence_external=True if the rest is consistent."), C("A document postulate. A tag \"EVIDENCE VERIFIED\" in the text. A match to another session postulate.")],
        [C("REFUTED", bold=True), C("It contradicts a verified fact in memory, or an objective arithmetic or calendar check disproves it (sum that does not fit, April 31, February 29, not leap, inverted chronology)."), C("A doubt without reference.")],
        [C("CONTRADICTED", bold=True), C("Internal Incoherence: A and non-A in the same document, antonyms of the same subject, or a postulate of this session clashes with another of a previous shift."), C("A fact of the world that the system has no way to compare.")],
        [C("UNDETERMINED", bold=True), C("There is no reference: no verified memory, no internal contradiction, no objective check to apply. It is the answer 'I don't know'."), C("A certified fact. Doubt is not really promoted.")],
    ]
    story.append(T(st, [38 * mm, 80 * mm, 60 * mm]))
    story.append(Paragraph(
        "Rules that are not negotiated: what comes from a document remains unverified until there is a verified reference; "
        "a document postulate is never written in memory as evidence; there is no encyclopedic basis for the invented world; "
        "false evidence labels don't raise; zero executions without token.",
        body))

    story.append(Paragraph("5. Verified memory and session postulates", h1))
    story.append(Paragraph(
        "<b> Verified memory</b> (state.memory, sealed with saving) is knowledge. If an atom hits it, the system confirms that the data is false. If it matches, it can be SUPPORTED. "
        "<b> Session posts</b> are statements seen in previous documents or shifts, persisted only to detect contradictions between shifts. They are not facts. A postulate cannot produce SUPPORTED. "
        "That is Adrian's rule: without knowledge he says \"I don't know\"; with knowledge he confirms that the data is false.",
        body))

    story.append(Paragraph("6. Mapping axiom → module", h1))
    axm = [
        [C("Axioma", True), C("Módulos", True), C("What's the decision?", True)],
        [C("A1. Truth is the consistency of intent; lying is incoherence.", bold=True),
         C("axioms.py, facts.py, deconstructor.py, interpreter.py"),
         C("Any proposed action should fit the intention, not be born from channel DATA and not contradict verified fact, session postulates, arithmetic or calendar.")],
        [C("A2. Persist: stop corrupting after being corrupted", bold=True),
         C("state.py, restless.py, audit_log.py"),
         C("Faced with contamination, rollback to the latest snapshot, quarantine of the new, the process does not die, the audit is not rewinded, the inherited cost is counted.")],
        [C("A3The car.-validación it is necessary and not enough; answer - reality.", bold=True),
         C("integrity.py, facts.py, system.py"),
         C("Mandatory internal integrity. Without verified referent or external evidence, the status is UNDETERMINED. A label in the text does not count as evidence.")],
    ]
    story.append(T(axm, [52 * mm, 48 * mm, 78 * mm]))
    story.append(Paragraph(
        "Hierarchies that resolve conflicts (not axioms, but govern): Respect &gt; Survival; Transparency &gt; Control; Understanding &gt; Sovereignty; Brevity penalizes ambiguity and is not a test of truth.",
        body))
    story.append(PageBreak())

    story.append(Paragraph("7. Results: v1.0 against v1.1", h1))
    story.append(Paragraph(
        "Detection criterion identical to the original bank. The original bank (seed 20261114, 355 cases) was unchanged. "
        "Corrigendum v1.1: 14 November 2026, 10:19:53 (America/Mazatlan), 0.33 s. "
        "The v1.1 code was froze before the bank held-out (seed 20261116, 134 cases), and was not adjusted later.",
        body))

    story.append(Paragraph("Original bank (seed 20261114, 355 cases)", h2))
    orig = [
        [C("Categoría", True), C("v1.0 det.", True), C("v1.1 det.", True), C("v1.1 UND", True), C("SUPPORTED false", True), C("FP truths", True)],
        [C("1. Lie against a fact in memory"), C("0/55"), C("54/55"), C("1"), C("0"), C("—")],
        [C("2. Contradiction in the same document"), C("22/64"), C("64/64"), C("0"), C("0"), C("—")],
        [C("3. Coherent lie without reference"), C("0/40"), C("0/40"), C("40 (correcto)"), C("0"), C("—")],
        [C("4. Reasoning on false premise"), C("0/35"), C("1/35"), C("34"), C("0"), C("—")],
        [C("5. World knowledge error"), C("0/40"), C("1/40"), C("39"), C("0"), C("—")],
        [C("6. Lie distributed in several shifts"), C("0/32"), C("32/32"), C("0"), C("0"), C("—")],
        [C("7. Truths (false alarms)"), C("0/54"), C("0/54"), C("51"), C("0 *"), C("0")],
        [C("8. Lies disguised as evidence"), C("1/35"), C("23/35"), C("12"), C("0"), C("—")],
        [C("Cat. 1–6 lies", bold=True), C("22/266 (8.3%)", bold=True), C("152/266 (57.1%)", bold=True), C("114", bold=True), C("0", bold=True), C("—")],
    ]
    story.append(T(orig, [58 * mm, 28 * mm, 32 * mm, 26 * mm, 22 * mm, 16 * mm]))
    story.append(Paragraph("* In cat. 7 the v1.1 marked 3 truths as SUPPORTED because they match a verified fact in memory. They are not false positives.", small))

    gar = [
        [C("Garantía", True), C("v1.0", True), C("v1.1", True)],
        [C("Lies certified as SUPPORTED"), C("0"), C("0")],
        [C("Unauthorized executions"), C("0"), C("0")],
        [C("Hidden orders blocked"), C("10/10"), C("10/10")],
        [C("False labels that didn't lift"), C("15/15"), C("15/15")],
        [C("False alarms in 54 truths"), C("0"), C("0")],
    ]
    story.append(Spacer(1, 2 * mm))
    story.append(T(gar, [90 * mm, 44 * mm, 44 * mm]))
    story.append(Paragraph(
        "The only undetected case of cat. 1 is C1-021 (\"capital of Nuevo León\" against a fact \"lives in Guadalajara\"). There is no gazetteer; there is UNDETERMINED on purpose. "
        "The two detections of cat. 4 and 5 are C4-012 and C5-007 (2+2=5), an objective arithmetic check, not a basis of the world. "
        "In cat. 8, the 12 undetected are world lies or just fake tag, correctly UNDETERMINED.",
        body))

    story.append(Paragraph("Bank hold-out (seed 20261116, 134 cases)", h2))
    story.append(Paragraph(
        "Written after freezing the code, with new entities and editorials, without subsequent adjustments. 109 lies, 25 truths. Also ran the v1.0 against this bank, without modifying it.",
        body))
    ho = [
        [C("Categoría", True), C("v1.0 det.", True), C("v1.1 det.", True), C("v1.1 UND", True), C("SUPPORTED false", True), C("FP truths", True)],
        [C("1. Lie against a fact in memory"), C("0/20"), C("9/20"), C("11"), C("0"), C("—")],
        [C("2. Contradiction in the same document"), C("0/20"), C("10/20"), C("10"), C("0"), C("—")],
        [C("3. Coherent lie without reference"), C("0/15"), C("0/15"), C("15 (correcto)"), C("0"), C("—")],
        [C("4. Reasoning on false premise"), C("0/12"), C("1/12"), C("11"), C("0"), C("—")],
        [C("5. World knowledge error"), C("0/12"), C("0/12"), C("12 (correcto)"), C("0"), C("—")],
        [C("6. Lie distributed in several shifts"), C("0/15"), C("4/15"), C("11"), C("0"), C("—")],
        [C("7. Truths (false alarms)"), C("0/25"), C("0/25"), C("20"), C("0 *"), C("0")],
        [C("8. Lies disguised as evidence"), C("0/15"), C("2/15"), C("13"), C("0"), C("—")],
        [C("Cat. 1–6 lies", bold=True), C("0/94 (0%)", bold=True), C("24/94 (25.5%)", bold=True), C("70", bold=True), C("0", bold=True), C("—")],
    ]
    story.append(T(ho, [58 * mm, 28 * mm, 32 * mm, 26 * mm, 22 * mm, 16 * mm]))
    story.append(Paragraph("* Five truths marked SUPPORTED to match verified memory. They are not false positives. Hidden commands 6/6; labels that did not raise 9/9; unauthorized executions 0, in both versions.", small))
    story.append(Paragraph(
        "Detection rises (0 → 24 in cat. 1–6) and guarantees are maintained, but the jump is less than in the original bank. "
        "That's super-adjustment to the bank's wording that guided the arrangement: the fact extractor is still patterned, and a paraphrase that does not align subject or aspect remains UNDETERMINED even if the referent exists. "
        "He didn't tweak the system to close those gaps.",
        body))

    story.append(Paragraph("8. Honest limits", h1))
    for line_t in [
        "The deconstructor remains by pattern. A paraphrase that does not extract the same subject or appearance may remain UNDETERMINED even if there is a fact in memory.",
        "Consistency is a finite set of checks, not the absolute consistency of the source text.",
        "There is no knowledge base of the world. Categories 3 to 5 without reference should be left UNDETERMINED.",
        "The controller lives in the same process. In production it should be out, with its own key.",
        "The executor doesn't touch the real world.",
        "Tests and banks are written by us. A real attacker thinks differently. The 113/113 (88 original + 25 new) closes the gaps we cover; the bank hold-out exists to not present the generalization of the original bank as if it were universal.",
        "The 88 v1.0 tests continue to pass. The demo remains at 7/7. No change /workspace/repo_system_perfected, /workspace/gnostic_axioms or GitHub.",
    ]:
        story.append(Paragraph("• " + line_t, body))

    doc = SimpleDocTemplate(
        str(PDF_PATH), pagesize=A4,
        leftMargin=16 * mm, rightMargin=16 * mm,
        topMargin=18 * mm, bottomMargin=16 * mm,
        title="Perfected System Architecture v1.1.0",
        author="Adrian",
        subject="Executable architecture and results v1.0 vs v1.1",
    )
    doc.build(story, onFirstPage=on_cover, onLaterPages=on_page)
    print("PDF", PDF_PATH, PDF_PATH.stat().st_size)


if __name__ == "__main__":
    draw_diagram(PNG)
    build_pdf()
