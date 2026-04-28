"""
Dialog UI — Form tambah/edit transaksi.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QComboBox, QDoubleSpinBox,
    QDateEdit, QPushButton, QRadioButton,
    QButtonGroup, QGroupBox, QMessageBox, QFrame,
)
from PySide6.QtCore import Qt, QDate
from models.transaction import Transaction

class TransactionDialog(QDialog):
    # Daftar kategori untuk masing-masing jenis
    KATEGORI_PEMASUKAN = ["Gaji", "Freelance", "Investasi", "Bonus", "Hadiah", "Lainnya"]
    KATEGORI_PENGELUARAN = ["Makanan & Minuman", "Transportasi", "Belanja", "Tagihan", "Kesehatan", "Pendidikan", "Hiburan", "Lainnya"]
    METODE_PEMBAYARAN = ["Cash", "Transfer Bank", "E-Wallet", "Kartu Kredit", "Kartu Debit"]

    def __init__(self, parent=None, transaction=None):
        super().__init__(parent)
        self.transaction = transaction
        self.is_edit_mode = transaction is not None

        if self.is_edit_mode:
            self.setWindowTitle("Edit Transaksi")
        else:
            self.setWindowTitle("Tambah Transaksi")

        self.setMinimumWidth(450)
        self._setup_ui()
        self._connect_signals()

        if self.is_edit_mode:
            self._populate_data()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(20, 20, 20, 20)

        if self.is_edit_mode:
            header = QLabel("Edit Transaksi")
        else:
            header = QLabel("Tambah Transaksi Baru")
        header.setObjectName("dialogHeader")
        layout.addWidget(header)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #dddddd;")
        layout.addWidget(sep)

        form = QFormLayout()
        form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setDisplayFormat("dd MMMM yyyy")
        self.date_edit.setMaximumDate(QDate.currentDate())
        form.addRow("Tanggal:", self.date_edit)

        jenis_group = QGroupBox()
        jenis_group.setObjectName("jenisGroup")
        jenis_layout = QHBoxLayout(jenis_group)
        jenis_layout.setContentsMargins(8, 4, 8, 4)

        self.radio_pemasukan = QRadioButton("Pemasukan")
        self.radio_pengeluaran = QRadioButton("Pengeluaran")
        self.radio_pengeluaran.setChecked(True) #Default pilihan

        self.jenis_button_group = QButtonGroup(self)
        self.jenis_button_group.addButton(self.radio_pemasukan, 0)
        self.jenis_button_group.addButton(self.radio_pengeluaran, 1)

        jenis_layout.addWidget(self.radio_pemasukan)
        jenis_layout.addWidget(self.radio_pengeluaran)
        form.addRow("Jenis:", jenis_group)

        self.combo_kategori = QComboBox()
        self.combo_kategori.addItems(self.KATEGORI_PENGELUARAN)
        form.addRow("Kategori:", self.combo_kategori)

        self.spin_jumlah = QDoubleSpinBox()
        self.spin_jumlah.setPrefix("Rp ")
        self.spin_jumlah.setRange(0, 999_999_999_999)
        self.spin_jumlah.setDecimals(0)
        self.spin_jumlah.setSingleStep(10000)
        self.spin_jumlah.setGroupSeparatorShown(True)
        form.addRow("Jumlah:", self.spin_jumlah)

        self.combo_metode = QComboBox()
        self.combo_metode.addItems(self.METODE_PEMBAYARAN)
        form.addRow("Metode Bayar:", self.combo_metode)

        self.line_deskripsi = QLineEdit()
        self.line_deskripsi.setPlaceholderText("Contoh: Beli makan siang")
        self.line_deskripsi.setMaxLength(200)
        form.addRow("Deskripsi:", self.line_deskripsi)

        layout.addLayout(form)
        #Tombol batal dan simpan/update
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.btn_cancel = QPushButton("Batal")
        self.btn_cancel.setObjectName("btnCancel")

        if self.is_edit_mode:
            self.btn_save = QPushButton("Update")
        else:
            self.btn_save = QPushButton("Simpan")
        self.btn_save.setObjectName("btnSave")
        self.btn_save.setDefault(True)

        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_save)
        layout.addLayout(btn_layout)

    def _connect_signals(self):
        self.jenis_button_group.idClicked.connect(self._on_jenis_changed)
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_save.clicked.connect(self._on_save)

    def _on_jenis_changed(self, id):
        #Ganti daftar kategori sesuai jenis yang dipilih
        self.combo_kategori.clear()
        if id == 0:
            self.combo_kategori.addItems(self.KATEGORI_PEMASUKAN)
        else:
            self.combo_kategori.addItems(self.KATEGORI_PENGELUARAN)

    def _on_save(self):
        if self.spin_jumlah.value() <= 0:
            QMessageBox.warning(
                self, "Validasi Gagal",
                "Jumlah transaksi harus lebih dari Rp 0.",
            )
            self.spin_jumlah.setFocus()
            return
        self.accept()

    def get_transaction_data(self):
        if self.radio_pemasukan.isChecked():
            jenis = "Pemasukan"
        else:
            jenis = "Pengeluaran"

        return Transaction(
            id=self.transaction.id if self.is_edit_mode else 0,
            tanggal=self.date_edit.date().toString("yyyy-MM-dd"),
            jenis=jenis,
            kategori=self.combo_kategori.currentText(),
            jumlah=self.spin_jumlah.value(),
            metode_pembayaran=self.combo_metode.currentText(),
            deskripsi=self.line_deskripsi.text().strip(),
        )

    def _populate_data(self):
        #Menampilkan data saat dalam mode edit
        trx = self.transaction

        parts = trx.tanggal.split("-")
        if len(parts) == 3:
            self.date_edit.setDate(QDate(int(parts[0]), int(parts[1]), int(parts[2])))

        if trx.jenis == "Pemasukan":
            self.radio_pemasukan.setChecked(True)
            self._on_jenis_changed(0)
        else:
            self.radio_pengeluaran.setChecked(True)
            self._on_jenis_changed(1)

        idx = self.combo_kategori.findText(trx.kategori)
        if idx >= 0:
            self.combo_kategori.setCurrentIndex(idx)

        self.spin_jumlah.setValue(trx.jumlah)

        idx = self.combo_metode.findText(trx.metode_pembayaran)
        if idx >= 0:
            self.combo_metode.setCurrentIndex(idx)

        self.line_deskripsi.setText(trx.deskripsi)