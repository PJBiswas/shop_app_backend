from io import BytesIO
from fastapi.responses import StreamingResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
import matplotlib.pyplot as plt
import tempfile
import pandas as pd


def generate_pdf_report(purchases):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # --- Title and Summary ---
    elements.append(Paragraph("Installment Report", styles['Title']))
    elements.append(Spacer(1, 0.3 * inch))

    total = len(purchases)
    completed = sum(p.is_completed for p in purchases)
    pending = total - completed

    elements.append(Paragraph(f"Total Purchases: {total}", styles["Normal"]))
    elements.append(Paragraph(f"Completed Purchases: {completed}", styles["Normal"]))
    elements.append(Paragraph(f"Pending Purchases: {pending}", styles["Normal"]))
    elements.append(Spacer(1, 0.2 * inch))

    # --- Pie Chart ---
    fig, ax = plt.subplots()
    ax.pie([completed, pending], labels=["Completed", "Pending"], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
        chart_path = tmpfile.name
        plt.savefig(chart_path)
        plt.close()
        elements.append(Image(chart_path, width=4 * inch, height=3 * inch))
        elements.append(Spacer(1, 0.3 * inch))

    # --- Purchase History Table ---
    elements.append(Paragraph("Purchase History", styles['Heading2']))
    purchase_data = [["ID", "Customer", "Product", "Amount", "Date", "Completed"]]
    purchase_data += [
        [
            str(p.id),
            f"{p.user.first_name} {p.user.last_name}",
            p.product.name,
            f"{p.total_amount:.2f}",
            p.created_at.strftime("%Y-%m-%d"),
            "✅" if p.is_completed else "❌"
        ] for p in purchases
    ]
    purchase_table = Table(purchase_data, repeatRows=1)
    purchase_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    elements.append(purchase_table)
    elements.append(Spacer(1, 0.4 * inch))

    # --- Installment History Table ---
    elements.append(Paragraph("Installment History", styles['Heading2']))
    installment_data = [["ID", "Customer", "Due Date", "Amount Due", "Paid"]]
    installment_data += [
        [
            str(i.id),
            f"{p.user.first_name} {p.user.last_name}",
            i.due_date.strftime("%Y-%m-%d"),
            f"{i.amount_due:.2f}",
            "✅" if i.is_paid else "❌"
        ]
        for p in purchases for i in p.installments_schedule
    ]
    installment_table = Table(installment_data, repeatRows=1)
    installment_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    elements.append(installment_table)

    doc.build(elements)
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=installment_report.pdf"}
    )


def generate_excel_report(purchases):
    purchase_data = [{
        "Purchase ID": p.id,
        "Customer Name": f"{p.user.first_name} {p.user.last_name}",
        "Product Name": p.product.name,
        "Total Amount": float(p.total_amount),
        "Created At": p.created_at.strftime("%Y-%m-%d"),
        "Is Completed": p.is_completed
    } for p in purchases]

    installment_data = [{
        "Schedule ID": i.id,
        "Customer Name": f"{p.user.first_name} {p.user.last_name}",
        "Due Date": i.due_date.strftime("%Y-%m-%d"),
        "Amount Due": float(i.amount_due),
        "Is Paid": i.is_paid
    } for p in purchases for i in p.installments_schedule]

    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        pd.DataFrame(purchase_data).to_excel(writer, index=False, sheet_name="Purchases")
        pd.DataFrame(installment_data).to_excel(writer, index=False, sheet_name="Installments")

    buffer.seek(0)
    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=installment_report.xlsx"}
    )
