from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

FAQ_CONTENT = [
    ("CartNest Customer Support Knowledge Base", None, "title"),

    ("1. Orders & Tracking", None, "section"),
    ("Q: How do I place an order on CartNest?",
     "Browse the catalog, add items to your cart, and proceed to checkout. Enter your delivery address and complete payment. A confirmation email and SMS will be sent within 3 minutes of a successful order.", "qa"),
    ("Q: How can I track my order?",
     "Once dispatched, a tracking ID is shared via email and SMS. Go to 'My Orders' > 'Track Order' on the CartNest app or website. Courier tracking is also available directly on the partner site. Updates reflect within 12 hours of dispatch.", "qa"),
    ("Q: Can I cancel or modify my order?",
     "Orders can be cancelled or modified within 45 minutes of placement. After this window, the order moves to our fulfillment center and cannot be changed. Go to 'My Orders' > select order > 'Request Cancellation'. Refunds are processed within 5-7 business days.", "qa"),
    ("Q: My order shows delivered but I have not received it.",
     "Check with building security or neighbors first. If still missing, report it within 48 hours via 'My Orders' > 'Report Issue' > 'Not Received'. Our logistics team investigates and resolves within 3 business days.", "qa"),
    ("Q: What happens if my order is delayed?",
     "If delivery exceeds the estimated date by more than 2 days, you will receive an automatic notification. Contact support for priority resolution. For significant delays, CartNest provides a discount voucher as compensation.", "qa"),

    ("2. Payments & Billing", None, "section"),
    ("Q: What payment methods does CartNest accept?",
     "CartNest accepts Visa, Mastercard, RuPay cards, UPI (GPay, PhonePe, Paytm), net banking, CartNest Credits, EMI on select cards, and Cash on Delivery for eligible orders under Rs.4000.", "qa"),
    ("Q: I was charged twice for the same order.",
     "Check your bank statement to confirm both charges. Duplicate blocks from failed transactions are usually auto-reversed within 5-7 business days. If both are confirmed debits, contact CartNest Support with your Order ID and bank statement screenshot.", "qa"),
    ("Q: How does EMI work on CartNest?",
     "EMI is available on orders above Rs.2500 using select credit cards. At checkout, choose 'Pay via EMI', select your bank, and pick a 3, 6, or 12 month tenure. No-cost EMI is available on select products. Processing fees, if any, are shown before confirmation.", "qa"),
    ("Q: Why was my payment declined?",
     "Common causes include insufficient funds, incorrect card details, exceeded UPI daily limit, or a bank security block. Try an alternate method or contact your bank. If money was deducted but the order failed, a refund is auto-initiated within 5-7 business days.", "qa"),
    ("Q: How do I download my invoice?",
     "GST invoices are generated for all orders. Go to 'My Orders' > select order > 'Download Invoice'. Business users can add their GSTIN in Account Settings for B2B invoices.", "qa"),

    ("3. Returns & Refunds", None, "section"),
    ("Q: What is CartNest's return policy?",
     "CartNest offers a 7-day return window from delivery date for most categories. Items must be unused, in original packaging, with all tags and accessories. Electronics have a 5-day replacement-only policy. Perishables, innerwear, and customised items are non-returnable.", "qa"),
    ("Q: How do I initiate a return?",
     "Go to 'My Orders', select the item, tap 'Return or Replace', choose the reason, and schedule a free pickup. Our courier collects within 2-4 business days. Pack the item securely. Refund is initiated after warehouse quality check.", "qa"),
    ("Q: When will I receive my refund?",
     "After quality check clears (1-2 business days): Original payment method: 5-7 business days. CartNest Credits: instant. UPI: 1-3 business days. COD refunds go via NEFT to your registered bank account within 7 business days.", "qa"),
    ("Q: My return was rejected. Why?",
     "Returns can be rejected for signs of use, damage, missing accessories or packaging, or an expired return window. A rejection email with details is sent. Appeal within 48 hours by contacting support with photo evidence.", "qa"),
    ("Q: Can I exchange instead of returning?",
     "Exchanges are available for a different size or colour of the same product, subject to stock availability. Go to 'My Orders' > 'Return or Replace' > 'Exchange'. If the variant is unavailable, a full refund is issued automatically.", "qa"),

    ("4. Account & Security", None, "section"),
    ("Q: How do I reset my password?",
     "On the login screen, tap 'Forgot Password', enter your registered mobile or email, and complete OTP verification. The reset link is valid for 10 minutes. If you do not receive it, check spam or retry after 2 minutes.", "qa"),
    ("Q: My account has been hacked or compromised.",
     "Reset your password immediately via 'Forgot Password' to lock out the intruder. Go to Settings > Security > Sign Out of All Devices. Check recent orders for unauthorized activity. Contact security@cartnest.in right away. Never share your OTP or password with anyone.", "qa"),
    ("Q: How do I update my mobile number or email?",
     "Go to Account Settings > Personal Details > Edit. OTP verification is required on the new contact. Both email and phone cannot be changed simultaneously. Changes take effect immediately after verification.", "qa"),
    ("Q: How do I delete my CartNest account?",
     "Account deletion is permanent and irreversible. Cancel active orders and withdraw any CartNest Credits first. Then go to Settings > Account > Delete Account and confirm. All data including order history will be erased.", "qa"),

    ("5. Products & Sellers", None, "section"),
    ("Q: How do I verify a product is genuine?",
     "All CartNest sellers go through a verification process. Look for the 'CartNest Verified' badge on listings. Electronics include serial number verification post-delivery. Report suspected counterfeits via 'My Orders' > 'Report Counterfeit'.", "qa"),
    ("Q: I received a wrong product.",
     "Report within 48 hours via 'My Orders' > 'Report Issue' > 'Wrong Item Received'. Attach clear photos. We will arrange a reverse pickup and either send the correct product or issue a full refund.", "qa"),
    ("Q: How do I write a product review?",
     "After delivery, go to 'My Orders' > select product > 'Write a Review'. Add a star rating, written review, and optional photos or video. Reviews go through a 24-hour moderation process before publishing.", "qa"),
    ("Q: Can I contact the seller directly?",
     "Message sellers from the product page via 'Ask the Seller' or from your order page via 'Contact Seller'. Response time is typically 24-48 hours. For delivery or quality issues, always contact CartNest Support directly for faster resolution.", "qa"),

    ("6. Shipping & Delivery", None, "section"),
    ("Q: What are CartNest's delivery charges?",
     "Delivery is free on orders above Rs.599. Orders below Rs.599 have a flat Rs.49 delivery fee. Express next-day delivery is available in select metro cities for an additional Rs.79. CartNest Prime members get free delivery on all orders.", "qa"),
    ("Q: Does CartNest deliver outside India?",
     "CartNest currently delivers within India across 25,000+ pin codes. Remote areas may take 7-10 business days. International delivery is planned for 2025.", "qa"),
    ("Q: Can I change my delivery address after ordering?",
     "Address can be changed within 45 minutes of placing the order. After that, the order is locked for fulfillment. For critical cases, contact support immediately and we will attempt to intercept the shipment, though this is not guaranteed.", "qa"),
    ("Q: What is CartNest Prime?",
     "CartNest Prime is available at Rs.249 per year or Rs.39 per month. Benefits include free delivery on all orders, early sale access, exclusive member discounts, priority support, and free returns on eligible products.", "qa"),

    ("7. Escalation & Complaints", None, "section"),
    ("Q: How do I escalate an unresolved issue?",
     "If your complaint is not resolved on time, escalate via Live Chat > 'Escalate to Specialist', email escalation@cartnest.in, or call our Senior Support Line at 1800-XXX-XXXX (Mon-Sat, 9AM-7PM). Escalated cases are resolved within 24 hours.", "qa"),
    ("Q: How do I file a formal complaint?",
     "Write to grievance@cartnest.in with your Order ID, issue description, and supporting documents. Our Grievance Officer will respond within 48 hours as required by consumer protection regulations.", "qa"),
    ("Q: What if I encounter fraud or a scam?",
     "Report phishing, impersonation, or fraud immediately to fraud@cartnest.in or our fraud helpline. Never make payments outside the CartNest platform. CartNest will never ask for your OTP, CVV, or net banking credentials.", "qa"),
]


def generate_pdf(output_path="data/cartnest_support_kb.pdf"):
    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    doc = SimpleDocTemplate(output_path, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()

    title_style    = ParagraphStyle('title', parent=styles['Heading1'], fontSize=18, spaceAfter=16)
    section_style  = ParagraphStyle('section', parent=styles['Heading2'], fontSize=13, spaceAfter=8, spaceBefore=18)
    question_style = ParagraphStyle('question', parent=styles['Normal'], fontSize=11, spaceAfter=4, spaceBefore=10, fontName='Helvetica-Bold')
    answer_style   = ParagraphStyle('answer', parent=styles['Normal'], fontSize=10, spaceAfter=8, leading=14, leftIndent=10)

    story = []
    for item in FAQ_CONTENT:
        if item[2] == "title":
            story.append(Paragraph(item[0], title_style))
            story.append(Paragraph("Version 1.0 | Customer Support Knowledge Base", styles['Normal']))
            story.append(Spacer(1, 0.4*cm))
        elif item[2] == "section":
            story.append(Paragraph(item[0], section_style))
        elif item[2] == "qa":
            story.append(Paragraph(item[0], question_style))
            story.append(Paragraph(item[1], answer_style))

    doc.build(story)
    print(f"PDF generated: {output_path}")


if __name__ == "__main__":
    generate_pdf()
