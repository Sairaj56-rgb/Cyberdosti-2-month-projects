import dns.resolver
from email import policy
from email.parser import BytesParser
import re


# Helper function to extract the domain from an email address
def extract_domain(email_address):
    match = re.search(r'@([\w.-]+)', email_address)
    if match:
        return match.group(1)
    return None


# Function to perform DNS lookup for SPF records
def check_spf(domain):
    try:
        answers = dns.resolver.resolve(domain, 'TXT')
        for rdata in answers:
            if str(rdata).startswith('"v=spf1'):
                return str(rdata)
    except Exception as e:
        print(f"DNS lookup failed for {domain}: {e}")
    return None


# Function to check if the email is spoofed
def is_email_spoofed(email_path):
    with open(email_path, 'rb') as f:
        email = BytesParser(policy=policy.default).parse(f)

    from_header = email['From']
    if from_header is None:
        print("No From header found")
        return True

    from_address = re.search(r'<(.+?)>', from_header)
    if not from_address:
        print("Invalid From header format")
        return True

    from_address = from_address.group(1)
    from_domain = extract_domain(from_address)
    if from_domain is None:
        print("Could not extract domain from From address")
        return True

    spf_record = check_spf(from_domain)
    if spf_record is None:
        print(f"No SPF record found for {from_domain}")
        return True

    received_headers = email.get_all('Received', [])
    if not received_headers:
        print("No Received headers found")
        return True

    for received_header in received_headers:
        match = re.search(r'from\s+([\w.-]+)', received_header)
        if match:
            received_domain = match.group(1)
            if from_domain == received_domain:
                print("Email appears to be valid")
                return False

    print("Email is likely spoofed")
    return True
