from fileinput import filename
from py_compile import main
import sys
from wsgiref import headers
from PyQt6.QtWidgets import QFileDialog
import os
import shutil
import requests
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QMessageBox, QDateEdit, QComboBox
)
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QFont, QPalette, QColor



# ===== KONFIG API =====
API_URL = "https://fxxcgtdvvxhoxyqcwsub.supabase.co"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ4eGNndGR2dnhob3h5cWN3c3ViIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njc5Mzc0MzksImV4cCI6MjA4MzUxMzQzOX0.xsMfeKDydAW9fr-sPK3ZFCdv51HNqOqUxl5m5d4PMYY"

HEADERS = {
    "apikey": API_KEY,
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

TABLE_URL = f"{API_URL}/rest/v1/surat"


class LibrarySurat(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Library Surat")
        self.setGeometry(200, 100, 1000, 600)

        self.set_app_style()
        self.initUI()
        self.load_data()

    # ===== STYLE VIA PYTHON =====
    def set_app_style(self):
        app = QApplication.instance()

        # FONT
        font = QFont("Segoe UI", 10)
        app.setFont(font)
        # DARK PALETTE
        palette = QPalette()

        palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(220, 220, 220))
        palette.setColor(QPalette.ColorRole.Base, QColor(45, 45, 45))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(60, 60, 60))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Text, QColor(220, 220, 220))
        palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(220, 220, 220))
        palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
        app.setPalette(palette)

    # ===== UI =====
    def initUI(self):
        central = QWidget()
        self.setCentralWidget(central)

        main = QVBoxLayout(central)
        main.setSpacing(12)
        main.setContentsMargins(16, 16, 16, 16)
        self.file_pdf_path = ""

        # ===== JUDUL =====
        title = QLabel("📂 Library Surat")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main.addWidget(title)
        # ===== FORM INPUT SURAT =====
        form = QHBoxLayout()
        form.setSpacing(8)

        self.tanggal = QDateEdit()
        self.tanggal.setDate(QDate.currentDate())
        self.tanggal.setCalendarPopup(True)
        self.kode = QLineEdit()
        self.kode.setPlaceholderText("Kode")

        self.nama = QLineEdit()
        self.nama.setPlaceholderText("Nama Surat")
        self.asal = QLineEdit()
        self.asal.setPlaceholderText("Dari")

        self.tujuan = QLineEdit()
        self.tujuan.setPlaceholderText("Ke")
        self.jenis = QComboBox()
        self.jenis.addItems(["Masuk", "Keluar"])

        btn_tambah = QPushButton("➕ Tambah Surat")
        btn_tambah.clicked.connect(self.tambah_surat)
        form.addWidget(self.tanggal)
        form.addWidget(self.kode)
        form.addWidget(self.nama)
        form.addWidget(self.asal)
        form.addWidget(self.tujuan)
        form.addWidget(self.jenis)
        form.addWidget(btn_tambah)

        main.addLayout(form)

        # ===== FITUR PDF (DI BAWAH FORM) =====
        pdf_layout = QHBoxLayout()
        pdf_layout.setSpacing(10)

        btn_pdf = QPushButton("📄 Pilih PDF")
        btn_pdf.clicked.connect(self.pilih_pdf)
        btn_buka_pdf = QPushButton("👁️ Buka PDF")
        btn_buka_pdf.clicked.connect(self.buka_pdf)

        pdf_layout.addStretch()
        pdf_layout.addWidget(btn_pdf)
        pdf_layout.addWidget(btn_buka_pdf)
        main.addLayout(pdf_layout)

        # ===== SEARCH =====
        search_layout = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Cari kode / nama / asal / tujuan")
        self.search.textChanged.connect(self.cari_surat)

        search_layout.addWidget(QLabel("Cari:"))
        search_layout.addWidget(self.search)
        main.addLayout(search_layout)

        # ===== TABLE =====
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ["Tanggal", "Kode", "Nama", "Asal", "Tujuan", "Jenis", "PDF"]
        )
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setMinimumHeight(320)
        main.addWidget(self.table)

    # ===== DELETE =====
        btn_hapus = QPushButton("🗑️ Hapus Data Terpilih")
        btn_hapus.clicked.connect(self.hapus_surat)
        main.addWidget(btn_hapus, alignment=Qt.AlignmentFlag.AlignRight)

    # ===== LOAD DATA =====
    def load_data(self):
        self.table.setRowCount(0)

        res = requests.get(
            TABLE_URL,
            headers=HEADERS,
            params={"select": "*", "order": "tanggal_surat.desc"}
        )

        for row, d in enumerate(res.json()):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(d.get("tanggal_surat", "")))
            self.table.setItem(row, 1, QTableWidgetItem(d.get("kode_surat", "")))
            self.table.setItem(row, 2, QTableWidgetItem(d.get("nama_surat", "")))
            self.table.setItem(row, 3, QTableWidgetItem(d.get("asal_surat", "")))
            self.table.setItem(row, 4, QTableWidgetItem(d.get("tujuan_surat", "")))
            self.table.setItem(row, 5, QTableWidgetItem(d.get("jenis_surat", "")))
            self.table.setItem(row, 6, QTableWidgetItem(d.get("file_pdf", "")))
        

    # ===== TAMBAH =====
    def tambah_surat(self):
        payload = {
            "tanggal_surat": self.tanggal.date().toString("yyyy-MM-dd"),
            "kode_surat": self.kode.text(),
            "nama_surat": self.nama.text(),
            "asal_surat": self.asal.text(),
            "tujuan_surat": self.tujuan.text(),
            "jenis_surat": self.jenis.currentText()
        }

        if not payload["kode_surat"] or not payload["nama_surat"]:
            QMessageBox.warning(self, "Peringatan", "Kode dan Nama wajib diisi")
            return

        res = requests.post(TABLE_URL, headers=HEADERS, json=payload)

        if res.status_code == 201:
            self.load_data()
            self.kode.clear()
            self.nama.clear()
            self.asal.clear()
            self.tujuan.clear()
        else:
            QMessageBox.critical(self, "Error", res.text)

    # ===== DELETE =====
    def hapus_surat(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, "Info", "Pilih data dulu")
            return

        kode = self.table.item(row, 1).text()

        res = requests.delete(
            TABLE_URL,
            headers=HEADERS,
            params={"kode_surat": f"eq.{kode}"}
        )

        if res.status_code == 204:
            self.load_data()
        else:
            QMessageBox.critical(self, "Error", res.text)

    # ===== Pilih PDF =====
    def pilih_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Pilih File PDF",
            "",
            "PDF Files (*.pdf)"
        )

        if file_path:
            self.file_pdf_path = file_path
            QMessageBox.information(self, "PDF Dipilih", os.path.basename(file_path))

    # ===== TAMBAH SURAT =====
    def tambah_surat(self):
        if not self.file_pdf_path:
            QMessageBox.warning(self, "Error", "PDF surat wajib dipilih")
            return

        os.makedirs("pdf_surat", exist_ok=True)

        filename = os.path.basename(self.file_pdf_path)
        target_path = os.path.join("pdf_surat", filename)

        shutil.copy(self.file_pdf_path, target_path)

        payload = {
            "tanggal_surat": self.tanggal.date().toString("yyyy-MM-dd"),
            "kode_surat": self.kode.text(),
            "nama_surat": self.nama.text(),
            "asal_surat": self.asal.text(),
            "tujuan_surat": self.tujuan.text(),
            "jenis_surat": self.jenis.currentText(),
            "file_pdf": target_path
        }

        res = requests.post(TABLE_URL, headers=HEADERS, json=payload)

        if res.status_code == 201:
            self.load_data()
            self.file_pdf_path = ""
            QMessageBox.information(self, "Sukses", "Surat berhasil ditambahkan")
        else:
            QMessageBox.critical(self, "Error", res.text)

    # ===== Buka PDF =====
    def buka_pdf(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Info", "Pilih surat dulu")
            return

        file_path = self.table.item(row, 6).text()

        if not os.path.exists(file_path):
            QMessageBox.critical(self, "Error", "File PDF tidak ditemukan")
            return
        os.startfile(file_path)

    # ===== SEARCH =====
    def cari_surat(self):
        keyword = self.search.text().strip()

        if not keyword:
            self.load_data()
            return

        params = {
            "select": "*",
            "or": (
                f"(kode_surat.ilike.%{keyword}%,"
                f"nama_surat.ilike.%{keyword}%,"
                f"asal_surat.ilike.%{keyword}%,"
                f"tujuan_surat.ilike.%{keyword}%)"
            )
        }

        res = requests.get(TABLE_URL, headers=HEADERS, params=params)

        if res.status_code != 200:
            QMessageBox.critical(self, "Error API", res.text)
            return

        data = res.json()
    # 🔒 VALIDASI PENTING
        if not isinstance(data, list):
            QMessageBox.critical(self, "Error", "Data pencarian tidak valid")
            return

        self.table.setRowCount(0)
        for row, d in enumerate(data):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(d.get("tanggal_surat", ""))))
            self.table.setItem(row, 1, QTableWidgetItem(str(d.get("kode_surat", ""))))
            self.table.setItem(row, 2, QTableWidgetItem(str(d.get("nama_surat", ""))))
            self.table.setItem(row, 3, QTableWidgetItem(str(d.get("asal_surat", ""))))
            self.table.setItem(row, 4, QTableWidgetItem(str(d.get("tujuan_surat", ""))))
            self.table.setItem(row, 5, QTableWidgetItem(str(d.get("jenis_surat", ""))))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LibrarySurat()
    win.show()
    sys.exit(app.exec())
