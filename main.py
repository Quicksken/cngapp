import os
import re
import connector
from classes import Invoice, Payment

payments = []
invoices = []


def create_payment_bulk():
    global payments
    global invoices
    pdf_dir = '/var/www/cngapp/pdfs'
    invoices_list = os.listdir(pdf_dir)
    for invoice in invoices_list:
        path = pdf_dir + invoice
        invoice_file = open(path, encoding="utf-8")
        payment_lines = []
        for line in invoice_file:
            if re.search(r'([0-9]{2}:[0-9]{2}:[0-9]{2}) ([A-Z][a-z]+) . [0-9]{2,3}\.[0-9]{2}', line) is not None:
                payment_lines.append(line)
        total_cost = 0.00
        for line in payment_lines:
            total_cost += float(re.search(r'\d+\.\d{2}', line).group())
        timestamp = re.search(r'([0-9]{2}-[0-9]{2}-[0-9]{4})+', invoice).group()
        invoices.append(Invoice(path, total_cost, "Colruyt", timestamp))
        Invoice.add_to_db(invoices[-1])
        invoice_id = str(mysql_cursor.lastrowid)
        for line in payment_lines:
            cost = re.search(r'\d+\.\d{2}', line).group()
            method = re.search(r'([A-Z][a-z]+)', line).group()
            payments.append(Payment('sven', method, invoice_id, str(cost)))
            Payment.add_to_db(payments[-1])
        invoice_file.close()


if __name__ == '__main__':
    #sshtunnel = connector.open_ssh_tunnel()
    mysql_connection, mysql_cursor = connector.mysql_connect()
    create_payment_bulk()
    mysql_connection.commit()
    mysql_connection.close()
    #sshtunnel.close()
