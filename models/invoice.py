from datetime import datetime

class Invoice:
    def __init__(self, invoice_id, patient_id, amount, emission_date, payment_date=None, status="Pending", payment_method=None):
        self.invoice_id = invoice_id
        self.patient_id = patient_id
        self.amount = amount
        self.emission_date = emission_date
        self.payment_date = payment_date
        self.status = status  # Pending, Paid, Cancelled
        self.payment_method = payment_method

    def generate(self):
        # Logic to generate the invoice
        pass

    def mark_as_paid(self, payment_method):
        self.status = "Paid"
        self.payment_date = datetime.now()
        self.payment_method = payment_method

    def __str__(self):
        return f"Invoice ID: {self.invoice_id}, Amount: {self.amount}, Status: {self.status}" 