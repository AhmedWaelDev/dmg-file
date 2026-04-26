import os
import datetime as dt
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw, ImageFont

EURO = "\u20ac"


class QuoteApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Quote PDF + Photo Generator")
        self.items = []

        self._build_ui()

    def _build_ui(self):
        main = ttk.Frame(self.root, padding=10)
        main.pack(fill="both", expand=True)

        form = ttk.LabelFrame(main, text="Quote Details", padding=10)
        form.pack(fill="x")

        self.vars = {
            "company_name": tk.StringVar(value="LINEA CHIARA INFISSI"),
            "company_address": tk.StringVar(value="Tromello via Garlasco 5"),
            "company_email": tk.StringVar(value="mohamedonly112@gmail.com"),
            "company_vat": tk.StringVar(value="P.IVA 02937780183"),
            "company_phone": tk.StringVar(value="320 1581689"),
            "client_name": tk.StringVar(value="ABDELADOUD MOHAMED"),
            "client_address": tk.StringVar(value="Via Sora n\u00b0 11 - 27020 Tromello PV"),
            "quote_date": tk.StringVar(value=dt.date.today().strftime("%d/%m/%Y")),
            "subject": tk.StringVar(value="Offerta materiali e posa in opera"),
            "footer_heading": tk.StringVar(value="CONDIZIONI GENERALI DI VENDITA:"),
            "footer_payment": tk.StringVar(value="CONDIZIONI DI PAGAMENTO : 50% acconto saldo a fine lavori"),
        }

        left_fields = [
            ("Company Name", "company_name"),
            ("Company Address", "company_address"),
            ("Company Email", "company_email"),
            ("Company VAT", "company_vat"),
            ("Company Phone", "company_phone"),
        ]
        right_fields = [
            ("Client Name", "client_name"),
            ("Client Address", "client_address"),
            ("Quote Date (dd/mm/yyyy)", "quote_date"),
            ("Subject", "subject"),
        ]

        for i, (label, key) in enumerate(left_fields):
            ttk.Label(form, text=label).grid(row=i, column=0, sticky="w", padx=(0, 8), pady=2)
            ttk.Entry(form, textvariable=self.vars[key], width=44).grid(row=i, column=1, sticky="we", pady=2)

        for i, (label, key) in enumerate(right_fields):
            ttk.Label(form, text=label).grid(row=i, column=2, sticky="w", padx=(24, 8), pady=2)
            ttk.Entry(form, textvariable=self.vars[key], width=42).grid(row=i, column=3, sticky="we", pady=2)

        form.columnconfigure(1, weight=1)
        form.columnconfigure(3, weight=1)

        notes_frame = ttk.LabelFrame(main, text="Description / Notes", padding=10)
        notes_frame.pack(fill="x", pady=(10, 0))
        self.notes = tk.Text(notes_frame, height=4, wrap="word")
        self.notes.pack(fill="x")
        self.notes.insert("1.0", "Grato di avermi interpellato, vi sottopongo la mia migliore offerta dei seguenti materiali: vendita serramenti pvc e legno, riparazione zanzariere, restauro persiane, infissi in legno, porte blindate, porte interne, tapparelle normali ed elettriche, tende da sole. Specializzazioni: POSA SERRAMENTI, INFERRIATE IN FERRO.")

        footer_ui_frame = ttk.LabelFrame(main, text="Conditions & Payment", padding=10)
        footer_ui_frame.pack(fill="x", pady=(10, 0))

        ttk.Label(footer_ui_frame, text="Heading").grid(row=0, column=0, sticky="w", padx=(0, 5))
        ttk.Entry(footer_ui_frame, textvariable=self.vars["footer_heading"], width=60).grid(row=0, column=1, sticky="we", pady=2)

        ttk.Label(footer_ui_frame, text="Delivery / Validity").grid(row=1, column=0, sticky="nw", padx=(0, 5))
        self.footer_delivery = tk.Text(footer_ui_frame, height=2, width=50, wrap="word")
        self.footer_delivery.grid(row=1, column=1, sticky="we", pady=2)
        self.footer_delivery.insert("1.0", "La presente offerta ha validita di 30 giorni dalla data di emissione\nTermini di consegna : 6/7 settimane circa dall' ordine")

        ttk.Label(footer_ui_frame, text="Payment").grid(row=2, column=0, sticky="w", padx=(0, 5))
        ttk.Entry(footer_ui_frame, textvariable=self.vars["footer_payment"], width=60).grid(row=2, column=1, sticky="we", pady=2)

        ttk.Label(footer_ui_frame, text="Closing / Saluti").grid(row=3, column=0, sticky="nw", padx=(0, 5))
        self.footer_closing = tk.Text(footer_ui_frame, height=2, width=50, wrap="word")
        self.footer_closing.grid(row=3, column=1, sticky="we", pady=2)
        self.footer_closing.insert("1.0", "Fiducioso in un benevole accoglimento della presente offerta, resto a sua completa disposizione per ulteriori chiarimenti porgo\nDistinti saluti")

        footer_ui_frame.columnconfigure(1, weight=1)

        entry_frame = ttk.LabelFrame(main, text="Add Row", padding=10)
        entry_frame.pack(fill="x", pady=(10, 0))

        self.qty_var = tk.StringVar(value="1")
        self.size_var = tk.StringVar()
        self.desc_var = tk.StringVar()
        self.unit_var = tk.StringVar(value="0")

        ttk.Label(entry_frame, text="Qty").grid(row=0, column=0, sticky="w")
        ttk.Entry(entry_frame, textvariable=self.qty_var, width=8).grid(row=0, column=1, padx=(4, 16))

        ttk.Label(entry_frame, text="Size").grid(row=0, column=2, sticky="w")
        ttk.Entry(entry_frame, textvariable=self.size_var, width=16).grid(row=0, column=3, padx=(4, 16))

        ttk.Label(entry_frame, text="Description").grid(row=0, column=4, sticky="w")
        ttk.Entry(entry_frame, textvariable=self.desc_var, width=42).grid(row=0, column=5, padx=(4, 16), sticky="we")

        ttk.Label(entry_frame, text="Unit Price").grid(row=0, column=6, sticky="w")
        ttk.Entry(entry_frame, textvariable=self.unit_var, width=12).grid(row=0, column=7, padx=(4, 10))

        ttk.Button(entry_frame, text="Add Material", command=lambda: self.add_item("Material")).grid(row=0, column=8, padx=4)
        ttk.Button(entry_frame, text="Add Working Cost", command=lambda: self.add_item("Work")).grid(row=0, column=9, padx=4)
        ttk.Button(entry_frame, text="Remove Selected", command=self.remove_selected).grid(row=0, column=10, padx=4)

        entry_frame.columnconfigure(5, weight=1)

        table_frame = ttk.LabelFrame(main, text="Rows", padding=10)
        table_frame.pack(fill="both", expand=True, pady=(10, 0))

        cols = ("type", "qty", "size", "description", "unit", "total")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=11)
        self.tree.heading("type", text="Type")
        self.tree.heading("qty", text="Qty")
        self.tree.heading("size", text="Size")
        self.tree.heading("description", text="Description")
        self.tree.heading("unit", text="Unit Price")
        self.tree.heading("total", text="Total")

        self.tree.column("type", width=80, anchor="center")
        self.tree.column("qty", width=50, anchor="center")
        self.tree.column("size", width=120, anchor="center")
        self.tree.column("description", width=380, anchor="w")
        self.tree.column("unit", width=110, anchor="e")
        self.tree.column("total", width=110, anchor="e")

        ysb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=ysb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        ysb.pack(side="right", fill="y")

        bottom = ttk.Frame(main)
        bottom.pack(fill="x", pady=(10, 0))

        self.total_lbl = ttk.Label(bottom, text="Total (VAT Excluded): EUR 0.00", font=("Segoe UI", 11, "bold"))
        self.total_lbl.pack(side="left")

        ttk.Button(bottom, text="Export PDF + Photo", command=self.export_files).pack(side="right")

    def add_item(self, item_type: str):
        try:
            qty = float(self.qty_var.get().strip())
            unit = float(self.unit_var.get().strip().replace(",", "."))
        except ValueError:
            messagebox.showerror("Invalid number", "Qty and Unit Price must be numeric.")
            return

        desc = self.desc_var.get().strip()
        if not desc:
            messagebox.showerror("Missing description", "Please enter description.")
            return

        size = self.size_var.get().strip()
        total = qty * unit
        item = {
            "type": item_type,
            "qty": qty,
            "size": size,
            "description": desc,
            "unit": unit,
            "total": total,
        }
        self.items.append(item)
        self.tree.insert(
            "",
            "end",
            values=(
                item["type"],
                self._fmt_qty(qty),
                size,
                desc,
                self._money(unit),
                self._money(total),
            ),
        )

        self.desc_var.set("")
        self.size_var.set("")
        self.qty_var.set("1")
        self.unit_var.set("0")
        self._refresh_total()

    def remove_selected(self):
        selected = self.tree.selection()
        if not selected:
            return

        idxs = sorted((self.tree.index(i) for i in selected), reverse=True)
        for idx in idxs:
            del self.items[idx]
        for i in selected:
            self.tree.delete(i)
        self._refresh_total()

    def _refresh_total(self):
        total = sum(i["total"] for i in self.items)
        self.total_lbl.config(text=f"Total (VAT Excluded): {self._money(total)}")

    def export_files(self):
        if not self.items:
            messagebox.showerror("No rows", "Add at least one material or working cost row.")
            return

        out_dir = filedialog.askdirectory(title="Select output folder")
        if not out_dir:
            return

        data = self._collect_data()
        stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_path = os.path.join(out_dir, f"quote_{stamp}.pdf")
        png_path = os.path.join(out_dir, f"quote_{stamp}.png")

        try:
            generate_pdf(data, pdf_path)
            generate_image(data, png_path)
        except Exception as ex:
            messagebox.showerror("Export failed", str(ex))
            return

        messagebox.showinfo("Success", f"Files created:\n{pdf_path}\n{png_path}")

    def _collect_data(self):
        return {
            "company_name": self.vars["company_name"].get().strip(),
            "company_address": self.vars["company_address"].get().strip(),
            "company_email": self.vars["company_email"].get().strip(),
            "company_vat": self.vars["company_vat"].get().strip(),
            "company_phone": self.vars["company_phone"].get().strip(),
            "client_name": self.vars["client_name"].get().strip(),
            "client_address": self.vars["client_address"].get().strip(),
            "quote_date": self.vars["quote_date"].get().strip(),
            "subject": self.vars["subject"].get().strip(),
            "notes": self.notes.get("1.0", "end").strip(),
            "footer_heading": self.vars["footer_heading"].get().strip(),
            "footer_delivery": self.footer_delivery.get("1.0", "end").strip(),
            "footer_payment": self.vars["footer_payment"].get().strip(),
            "footer_closing": self.footer_closing.get("1.0", "end").strip(),
            "items": self.items,
            "total": sum(i["total"] for i in self.items),
        }

    @staticmethod
    def _fmt_qty(q):
        return str(int(q)) if float(q).is_integer() else f"{q:.2f}"

    @staticmethod
    def _money(v):
        return f"{EURO} {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def draw_wrapped(draw_obj, text, x, y, max_width, font, line_height):
    words = text.split()
    line = ""
    for w in words:
        test = (line + " " + w).strip()
        if draw_obj.textlength(test, font=font) <= max_width:
            line = test
        else:
            draw_obj.text((x, y), line, fill="black", font=font)
            y += line_height
            line = w
    if line:
        draw_obj.text((x, y), line, fill="black", font=font)
        y += line_height
    return y


def generate_image(data, out_path):
    scale = 3
    w, h = int(595 * scale), int(842 * scale)
    img = Image.new("RGB", (w, h), "white")
    d = ImageDraw.Draw(img)

    def sx(v):
        return int(v * scale)

    font_big = ImageFont.load_default()
    font = ImageFont.load_default()

    y = sx(42)
    d.text((sx(40), y), data["company_name"], fill="black", font=font_big)
    y += sx(16)
    d.text((sx(40), y), data["company_address"], fill="black", font=font)
    y += sx(15)
    d.text((sx(40), y), f"e-mail: {data['company_email']}", fill="black", font=font)
    y += sx(14)
    d.text((sx(40), y), f"{data['company_vat']}    cell. {data['company_phone']}", fill="black", font=font)

    d.text((sx(350), sx(92)), "GENT.MO", fill="black", font=font)
    d.text((sx(350), sx(108)), data["client_name"], fill="black", font=font)
    d.text((sx(350), sx(124)), data["client_address"], fill="black", font=font)

    sep_y = sx(160)
    d.line((sx(40), sep_y, sx(560), sep_y), fill="black", width=1)

    y = sx(176)
    d.text((sx(40), y), f"OGGETTO PREVENTIVO DEL {data['quote_date']}", fill="black", font=font)
    y += sx(18)
    y = draw_wrapped(d, data["notes"], sx(40), y, sx(520), font, sx(14))

    y += sx(8)
    d.line((sx(40), y, sx(560), y), fill="black", width=1)
    y += sx(18)

    d.text((sx(40), y), "MISURA", fill="black", font=font)
    d.text((sx(95), y), "ESTERNO TELAIO", fill="black", font=font)
    d.text((sx(420), y), "PR UNIT", fill="black", font=font)
    d.text((sx(510), y), "PR TOT", fill="black", font=font)
    y += sx(16)

    for row in data["items"]:
        desc = row["description"]
        if row["type"] == "Work":
            desc = f"[WORK] {desc}"
        d.text((sx(40), y), f"N\u00b0 {int(row['qty']) if row['qty'].is_integer() else row['qty']}", fill="black", font=font)
        d.text((sx(95), y), row["size"], fill="black", font=font)
        d.text((sx(200), y), desc, fill="black", font=font)
        d.text((sx(405), y), money(row["unit"]), fill="black", font=font)
        d.text((sx(500), y), money(row["total"]), fill="black", font=font)
        y += sx(14)

    y += sx(10)
    d.line((sx(40), y, sx(560), y), fill="black", width=1)
    y += sx(22)

    d.text((sx(40), y), f"TOTALE IVA ESCLUSA   {money(data['total'])}", fill="black", font=font)
    y += sx(35)

    d.text((sx(40), y), data["footer_heading"], fill="black", font=font)
    y += sx(14)
    y = draw_wrapped(d, data["footer_delivery"], sx(40), y, sx(520), font, sx(14))
    y += sx(8)
    d.text((sx(40), y), data["footer_payment"], fill="black", font=font)
    y += sx(16)
    y = draw_wrapped(d, data["footer_closing"], sx(40), y, sx(520), font, sx(14))
    y += sx(16)
    d.text((sx(40), y), "Per Accettazione                         Firma Il Cliente", fill="black", font=font)

    img.save(out_path, "PNG")


def money(v):
    return f"{EURO} {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def generate_pdf(data, out_path):
    c = canvas.Canvas(out_path, pagesize=A4)
    width, height = A4

    y = height - 60
    c.setFont("Helvetica-Bold", 18)
    c.drawString(40, y, data["company_name"])

    c.setFont("Helvetica", 12)
    y -= 24
    c.drawString(40, y, data["company_address"])
    y -= 18
    c.drawString(40, y, f"e-mail: {data['company_email']}")
    y -= 18
    c.drawString(40, y, f"{data['company_vat']}    cell. {data['company_phone']}")

    c.setFont("Helvetica-Bold", 13)
    c.drawString(360, height - 110, "GENT.MO")
    c.drawString(360, height - 132, data["client_name"])
    c.drawString(360, height - 154, data["client_address"])

    c.line(40, height - 180, width - 40, height - 180)

    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, height - 210, f"OGGETTO PREVENTIVO DEL {data['quote_date']}")

    c.setFont("Helvetica", 12)
    text = c.beginText(40, height - 232)
    text.setLeading(16)
    for ln in wrap_text_for_pdf(data["notes"], 85):
        text.textLine(ln)
    c.drawText(text)

    current_y = text.getY() - 8
    c.line(40, current_y, width - 40, current_y)
    current_y -= 24

    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, current_y, "MISURA")
    c.drawString(95, current_y, "ESTERNO TELAIO")
    c.drawString(430, current_y, "PR UNIT")
    c.drawString(510, current_y, "PR TOT")

    current_y -= 20
    c.setFont("Helvetica", 12)
    for row in data["items"]:
        desc = row["description"]
        if row["type"] == "Work":
            desc = f"[WORK] {desc}"
        qty_text = f"N\u00b0 {int(row['qty']) if row['qty'].is_integer() else row['qty']}"

        c.drawString(40, current_y, qty_text)
        c.drawString(95, current_y, row["size"])
        c.drawString(200, current_y, desc[:37])
        c.drawRightString(500, current_y, money(row["unit"]))
        c.drawRightString(560, current_y, money(row["total"]))
        current_y -= 18

    current_y -= 10
    c.line(40, current_y, width - 40, current_y)
    current_y -= 30

    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, current_y, f"TOTALE IVA ESCLUSA   {money(data['total'])}")

    current_y -= 40
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, current_y, data["footer_heading"])
    current_y -= 16

    c.setFont("Helvetica", 11)
    text_footer = c.beginText(40, current_y)
    text_footer.setLeading(14)
    for ln in wrap_text_for_pdf(data["footer_delivery"], 90):
        text_footer.textLine(ln)
    c.drawText(text_footer)
    
    current_y = text_footer.getY() - 10
    c.drawString(40, current_y, data["footer_payment"])
    current_y -= 20

    text_closing = c.beginText(40, current_y)
    text_closing.setLeading(14)
    for ln in wrap_text_for_pdf(data["footer_closing"], 90):
        text_closing.textLine(ln)
    c.drawText(text_closing)

    current_y = text_closing.getY() - 30
    c.drawString(40, current_y, "Per Accettazione")
    c.drawRightString(width - 40, current_y, "Firma Il Cliente")

    c.showPage()
    c.save()


def wrap_text_for_pdf(text, max_chars):
    words = text.split()
    lines = []
    line = ""
    for w in words:
        candidate = (line + " " + w).strip()
        if len(candidate) <= max_chars:
            line = candidate
        else:
            lines.append(line)
            line = w
    if line:
        lines.append(line)
    return lines


def main():
    root = tk.Tk()
    root.geometry("1240x760")
    app = QuoteApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
