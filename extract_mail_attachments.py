import os
from email.parser import Parser


def extract_pdf_attachments(inbox_dir):
    """
  Extracts all PDF attachments from emails in a directory with INBOX structure.

  Args:
    inbox_dir: Path to the directory containing the INBOX structure.

  Returns:
    None. Saves extracted PDFs in a dedicated folder.
  """
    pdf_folder = "/var/www/cngapp/pdfs"
    os.makedirs(pdf_folder, exist_ok=True)
    for root, dirs, files in os.walk(inbox_dir):
        for filename in files:
            print(filename)
            filepath = os.path.join(root, filename)
            with open(filepath, "rt") as f:
                print(type(f))
                try:
                    msg = Parser().parse(f)
                except UnicodeDecodeError:
                    f.close()
                    with open(filepath, "rt", encoding='iso-8859-1') as g:
                        msg = Parser().parse(g)
            if msg:
                print('Yes')
            for part in msg.walk():
                print(part.get_content_maintype())
                if part.get_content_maintype() == "multipart":
                    continue
                filename = part.get_filename()
                if filename and filename.lower().endswith(".pdf") and "kasticket" in filename:
                    content = part.get_payload(decode=True)
                    pdf_path = os.path.join(pdf_folder, filename)
                    with open(pdf_path, "wb") as pdf_file:
                        pdf_file.write(content)
                        print(f"Extracted PDF: {pdf_path}")


inbox_dir = "/var/www/cngapp/mail/"
extract_pdf_attachments(inbox_dir)
print(inbox_dir)
