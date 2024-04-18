class Invoice:
    def __init__(self, invoice_path, amount, store, timestamp):
        self.invoice_path = invoice_path
        self.amount = amount
        self.store = store
        self.timestamp = timestamp

    def __str__(self):
        return self.invoice_path + " " + self.amount + " " + self.store + " " + self.timestamp

    def add_to_db(self, cursor):
        sql = "INSERT INTO invoices (pathtotxt, cost, store, timestamp) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, [self.invoice_path, self.amount, self.store, self.timestamp])
        return


class Payment:
    def __init__(self, payer, method, invoice_id, amount):
        self.payer = payer
        self.method = method
        self.invoice_id = invoice_id
        self.amount = amount

    def __str__(self):
        return self.payer + " " + self.method + " " + self.invoice_id + " " + self.amount

    def add_to_db(self, cursor):
        sql = "INSERT INTO payments (payed_by, payment_method, invoices_id, amount) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, [self.payer, self.method, self.invoice_id, self.amount])
        return