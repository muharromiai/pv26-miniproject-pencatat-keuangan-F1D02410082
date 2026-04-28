from database.db_manager import DatabaseManager
from models.transaction import Transaction

class TransactionController:
    def __init__(self, db_manager):
        self.db = db_manager

    def add_transaction(self, trx):
        #Menambahkan transaksi
        error = self._validate(trx)
        if error:
            return error
        self.db.insert_transaction(trx)
        return None

    def update_transaction(self, trx):
        #Update transaksi berdasarkan id
        error = self._validate(trx)
        if error:
            return error
        self.db.update_transaction(trx)
        return None

    def delete_transaction(self, trx_id):
        self.db.delete_transaction(trx_id)

    def get_all_transactions(self):
        return self.db.get_all_transactions()

    def get_transaction_by_id(self, trx_id):
        return self.db.get_transaction_by_id(trx_id)

    def get_summary(self):
        return self.db.get_summary()

    def _validate(self, trx):
        #Validasi data transaksi
        if not trx.tanggal:
            return "Tanggal tidak boleh kosong."
        if trx.jenis not in ("Pemasukan", "Pengeluaran"):
            return "Jenis transaksi harus Pemasukan atau Pengeluaran."
        if not trx.kategori:
            return "Kategori tidak boleh kosong."
        if trx.jumlah <= 0:
            return "Jumlah harus lebih dari 0."
        if not trx.metode_pembayaran:
            return "Metode pembayaran harus dipilih."
        return None