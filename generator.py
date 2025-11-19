# generator.py
import re
from typing import List, Tuple, Dict
from models import TestCase
from faker import Faker

fake = Faker()

# Templates & keywords
FEATURE_TEMPLATES = {
    'login': {
        'positive': ["Open the login page", "Enter valid email/username", "Enter valid password", "Click Login"],
        'negatives': [
            ("Invalid password", ["Open login page", "Enter valid email", "Enter invalid password", "Click Login"], "Error: incorrect credentials"),
            ("Empty fields", ["Open the login page", "Click Login without entering credentials"], "Validation: required fields")
        ],
        'priority': 'High'
    },
    'signup': {
        'positive': ["Open the signup page", "Fill required fields with valid data", "Submit the form"],
        'negatives': [
            ("Existing email", ["Open signup page", "Enter an email that already exists", "Fill other fields", "Submit"], "Error: Email already registered"),
            ("Weak password", ["Open signup page", "Enter weak password", "Submit"], "Password strength validation")
        ],
        'priority': 'High'
    },
    'reset password': {
        'positive': ["Open reset password page", "Enter registered email", "Receive OTP", "Enter OTP", "Set new password", "Submit"],
        'negatives': [
            ("Invalid OTP", ["Open reset password page", "Enter registered email", "Enter wrong OTP", "Submit"], "Error: invalid OTP"),
            ("Expired OTP", ["Request OTP", "Wait until OTP expires", "Enter OTP", "Submit"], "Error: OTP expired")
        ],
        'priority': 'High'
    },
    'upload': {
        'positive': ["Open upload area", "Choose a valid file", "Click Upload", "Verify upload success"],
        'negatives': [
            ("Too large file", ["Choose a file larger than allowed limit", "Try upload"], "Error: File size limit exceeded"),
            ("Unsupported format", ["Choose unsupported file type", "Try upload"], "Error: Unsupported file type")
        ],
        'priority': 'Medium'
    },
    'payment': {
        'positive': ["Open payment page", "Enter valid card/UPI details", "Confirm payment", "Verify transaction success"],
        'negatives': [
            ("Invalid payment details", ["Enter invalid card/UPI details", "Attempt payment"], "Payment rejected"),
            ("Insufficient funds", ["Use card with insufficient funds", "Attempt payment"], "Payment declined")
        ],
        'priority': 'High'
    },
    'cart': {
        'positive': ["Open product page", "Add item to cart", "View cart", "Verify item present and total updated"],
        'negatives': [
            ("Update to zero", ["Add item to cart", "Update quantity to 0", "Save"], "Item removed or validation"),
            ("Negative quantity", ["Attempt to set negative quantity", "Save"], "Validation error")
        ],
        'priority': 'Medium'
    },
    'search': {
        'positive': ["Open search input", "Enter valid query", "Press search", "Verify relevant results"],
        'negatives': [
            ("Empty query", ["Open search input", "Press search without query"], "Show message or no results"),
            ("Huge query", ["Enter very long query", "Search"], "Graceful handling or error")
        ],
        'priority': 'Low'
    },
    'profile': {
        'positive': ["Open profile settings", "Edit profile fields (name, email, phone)", "Save changes", "Verify profile updated"],
        'negatives': [
            ("Invalid phone", ["Enter invalid phone number formats", "Save"], "Validation error"),
            ("Oversize avatar", ["Upload avatar larger than allowed", "Save"], "Error: size limit")
        ],
        'priority': 'Medium'
    },
    'notifications': {
        'positive': ["Open notifications panel", "View unread notifications", "Mark as read", "Verify unread count updates"],
        'negatives': [
            ("Missing notifications", ["Trigger notification-producing action", "Open panel"], "Notification appears"),
            ("Mark read fail", ["Mark many notifications as read quickly", "Observe behavior"], "Graceful handling")
        ],
        'priority': 'Low'
    },
    'api': {
        'positive': ["Call the API endpoint with valid parameters", "Receive HTTP 200 and JSON body", "Validate fields in response"],
        'negatives': [
            ("Invalid params", ["Call API with invalid params", "Observe response"], "HTTP 4xx and error message"),
            ("Pagination edge", ["Request page=99999", "Observe response"], "Graceful empty results or proper error")
        ],
        'priority': 'High'
    }
}

FEATURE_KEYWORDS = {
    'login': ['login', 'sign in', 'signin'],
    'signup': ['sign up', 'signup', 'register', 'registration'],
    'reset password': ['reset password', 'forgot password', 'otp'],
    'upload': ['upload', 'profile picture', 'avatar', 'image', 'file upload'],
    'payment': ['payment', 'checkout', 'upi', 'card', 'transaction'],
    'cart': ['cart', 'add to cart', 'shopping cart'],
    'search': ['search', 'find', 'lookup'],
    'profile': ['profile', 'edit profile', 'update profile'],
    'notifications': ['notification', 'notifications', 'unread'],
    'api': ['api', 'endpoint', 'json', 'response', 'status code']
}

SIZE_REGEX = re.compile(r'(\d+)\s*(mb|kb|gb)', re.IGNORECASE)
FILE_TYPES_REGEX = re.compile(r'(jpg|jpeg|png|gif|pdf|docx|csv|xlsx)', re.IGNORECASE)
DIGITS_REGEX = re.compile(r'(\d+)\s*(digit|digits)', re.IGNORECASE)
CURRENCY_REGEX = re.compile(r'(\bINR\b|\bUSD\b|\$|₹)', re.IGNORECASE)

def detect_feature(text: str) -> str:
    t = text.lower()
    for feature, kws in FEATURE_KEYWORDS.items():
        for kw in kws:
            if kw in t:
                return feature
    # fallback: verb based
    if re.search(r'\blogin\b|\bsign in\b', t):
        return 'login'
    if re.search(r'\bsign up\b|\bregister\b', t):
        return 'signup'
    if 'reset' in t and 'password' in t:
        return 'reset password'
    return None

def extract_constraints(text: str) -> Dict:
    constraints = {}
    size = SIZE_REGEX.search(text)
    if size:
        constraints['max_size'] = f"{size.group(1)}{size.group(2)}"
    types = FILE_TYPES_REGEX.findall(text)
    if types:
        constraints['file_types'] = list({t.lower() for t in types})
    digits = DIGITS_REGEX.search(text)
    if digits:
        try:
            constraints['otp_length'] = int(digits.group(1))
        except:
            pass
    if CURRENCY_REGEX.search(text):
        constraints['money_flow'] = True
    return constraints

def make_sample_data(feature: str, constraints: Dict) -> Dict:
    data = {}
    if feature in ('login','signup','reset password','profile'):
        data['valid_email'] = fake.safe_email()
        data['invalid_email'] = "invalid-email"
        data['valid_password'] = fake.password(length=10)
        data['weak_password'] = "12345"
        if constraints.get('otp_length'):
            data['otp_valid'] = "1" * constraints['otp_length']
        else:
            data['otp_valid'] = str(fake.random_number(digits=6, fix_len=True))
    if feature == 'upload' or 'file_types' in constraints:
        allowed = constraints.get('file_types', ['png','jpg'])
        data['sample_file_valid'] = f"avatar_valid.{allowed[0]}"
        data['sample_file_large'] = f"avatar_large.{allowed[0]}"
        if constraints.get('max_size'):
            data['max_size'] = constraints['max_size']
    if feature == 'payment':
        data['dummy_upi'] = f"user@upi"
        data['dummy_card'] = "4111 1111 1111 1111"
    if feature == 'cart':
        data['sample_item_id'] = fake.uuid4()
    if feature == 'api':
        data['sample_endpoint'] = "/api/v1/resource"
        data['sample_params'] = {"page": 1, "limit": 10}
    return data

def build_cases_from_template(feature: str, requirement_text: str, num_cases: int) -> List[TestCase]:
    constraints = extract_constraints(requirement_text)
    tpl = FEATURE_TEMPLATES.get(feature)
    cases: List[TestCase] = []
    sample_data = make_sample_data(feature, constraints)

    if not tpl:
        # Generic fallback
        base_titles = [
            "Valid scenario",
            "Empty / missing inputs",
            "Malformed inputs",
            "Boundary values",
            "Security input (injection/XSS)",
            "Unauthorized access",
            "Performance / long input handling"
        ]
        idx = 1
        for title in base_titles[:num_cases]:
            steps = [
                "Open the relevant page/component",
                "Perform the normal action with valid/invalid inputs as needed",
                "Verify the outcome"
            ]
            expected = "Feature behaves correctly or shows validation/error messages"
            tags = ["generic"]
            if "Security" in title:
                tags = ["security"]
            elif "Boundary" in title:
                tags = ["edge"]
            cases.append(TestCase(id=idx, title=title, steps=steps, expected=expected, priority="Medium", tags=tags, sample_data=sample_data))
            idx += 1
        return cases

    idx = 1
    # Positive
    pos = tpl['positive']
    cases.append(TestCase(id=idx, title=f"Valid {feature} scenario", steps=pos, expected="Operation succeeds and correct UI/state shown", priority=tpl.get('priority','Medium'), tags=["positive", feature], sample_data=sample_data))
    idx += 1

    # negatives
    for neg in tpl.get('negatives', []):
        if idx > num_cases: break
        neg_title, neg_steps, neg_expected = neg
        cases.append(TestCase(id=idx, title=f"{neg_title} - {feature}", steps=neg_steps, expected=neg_expected, priority="High", tags=["negative", feature], sample_data=sample_data))
        idx += 1

    # extras
    extras = [
        ("Invalid format / validation", ["Open the relevant page", "Enter malformed inputs", "Submit"], "Validation message or sanitized input", ["validation"]),
        ("Security check (XSS/SQLi)", ["Open page", "Enter script tags or SQL-like payloads", "Submit"], "Input sanitized; no injection", ["security"]),
        ("Boundary / limits", ["Open page", "Enter values at min/max limits", "Submit"], "System handles boundary values gracefully", ["edge"]),
        ("Unauthorized / invalid state", ["Attempt action without permission or while logged out", "Observe behavior"], "Action blocked; authorization error", ["security","negative"]),
        ("Performance / long input", ["Enter extremely large inputs or perform many repeated operations", "Observe response"], "System remains responsive", ["performance"])
    ]
    for title, steps, expected, tags in extras:
        if idx > num_cases: break
        cases.append(TestCase(id=idx, title=title, steps=steps, expected=expected, priority="Medium", tags=tags, sample_data=sample_data))
        idx += 1

    while idx <= num_cases:
        cases.append(TestCase(id=idx, title=f"Additional validation {idx}", steps=["Perform related validation scenario"], expected="Appropriate validation or error", priority="Low", tags=["validation"], sample_data=sample_data))
        idx += 1

    return cases

def compute_coverage(cases: List[TestCase]) -> Tuple[int, List[str]]:
    desired = ['positive','negative','security','edge','boundary','performance','validation']
    present = set()
    for tc in cases:
        for tag in tc.tags:
            if tag in desired:
                present.add(tag)
    present_list = sorted(list(present))
    score = int((len(present_list) / len(desired)) * 100)
    missing = [d for d in desired if d not in present_list]
    return score, missing

def generate_from_requirement(requirement: str, count: int = 8) -> Tuple[List[TestCase], Dict]:
    req = requirement.strip()
    if not req:
        return [], {}
    feature = detect_feature(req)
    cases = build_cases_from_template(feature, req, count)
    for i, c in enumerate(cases, start=1):
        c.id = i
    score, missing = compute_coverage(cases)
    meta = {
        'feature_detected': feature or 'generic',
        'coverage_score': score,
        'coverage_missing': missing,
        'sample_data': cases[0].sample_data if cases else {}
    }
    return cases, meta
