class Transaction:
    def __init__(self, id=0, tanggal="", jenis="", kategori="", jumlah=0.0, metode_pembayaran="", deskripsi=""):
        self.id = id
        self.tanggal = tanggal
        self.jenis = jenis
        self.kategori = kategori
        self.jumlah = jumlah
        self.metode_pembayaran = metode_pembayaran
        self.deskripsi = deskripsi

    def jumlah_formatted(self):
        return f"Rp {self.jumlah:,.0f}".replace(",", ".")

def transaction_from_tuple(row):
    return Transaction(
        id=row[0],
        tanggal=row[1],
        jenis=row[2],
        kategori=row[3],
        jumlah=row[4],
        metode_pembayaran=row[5],
        deskripsi=row[6],
    )