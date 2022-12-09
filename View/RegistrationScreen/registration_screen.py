import os
import platform
import random
import string
import secrets
import subprocess
import tempfile
import time
import datetime

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER

from View.common.app_screen import BaseAppScreen
from kivymd.app import MDApp
from kivy.metrics import dp
from kivy.properties import (
    StringProperty, NumericProperty,
    BooleanProperty, StringProperty)
from kivy.resources import resource_add_path, resource_find

class RegistrationScreenView(BaseAppScreen):

    registration_number = StringProperty()
    email = StringProperty()
    user_name = StringProperty()
    organization = StringProperty()
    qualification = StringProperty()
    position = StringProperty()
    # is_checked = BooleanProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.ids.back_button.on_release = lambda: self.app.return_callback(self, "simulator")
    
    def on_enter(self, *args) -> None:
        self.registration_number = self.genertate_registration_number()

    def check_fields(self):
        if (self.ids.email.error==True) | (
            self.ids.first_name.error==True) |(
            self.ids.second_name.error==True) | (
            self.ids.family_name.error==True) | (
            self.ids.organization.error==True) | (
            self.ids.qualification.error==True) | (
            self.ids.position.error==True):
            self.ids.save_pdf_button.disabled = True
            self.ids.print_button.disabled = True
        else:
            self.ids.save_pdf_button.disabled = False
            self.ids.print_button.disabled = False

    def set_email(self, email: str):
        self.email = email
        self.check_fields()
       
    def set_name(self, first_name: str, second_name: str, family_name: str):
        self.name = first_name
        self.name += " " + second_name if len(second_name) > 0 else ""
        self.name += " " + family_name if len(family_name) > 0 else ""
        self.check_fields()

    def set_organization(self, organization: str):
        self.organization = organization
        self.check_fields()

    def set_qualification(self, qualification: str):
        self.qualification = qualification
        self.check_fields()

    def set_position(self, position: str):
        self.position = position
        self.check_fields()

    def genertate_registration_number(self) -> str:
        alphabet = string.ascii_letters + string.digits
        while True:
            reg_number = ''.join(secrets.choice(alphabet) for i in range(32))
            if (any(c.islower() for c in reg_number)
                    and any(c.isupper() for c in reg_number)
                    and sum(c.isdigit() for c in reg_number) >= 3):
                break
        return reg_number
    
    def _get_pdf(self):
        filename = tempfile.mktemp (f"{self.registration_number}.pdf")
        pdf = SimpleDocTemplate(
            filename, pagesize=A4,
            rightMargin=72,leftMargin=72,
            topMargin=72,bottomMargin=18)

        styles=getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))

        Story = []
        logo = resource_find(f"{os.environ['PIEONE_ROOT']}/assets/images/pieone-logo.png")
        formatted_time = time.ctime()
        formatted_date = datetime.datetime.today()

        # Making header and logo
        header = Paragraph("<font size = '27'><strong>PIE ONE TESTEE SERTIFICATE</strong></font>", styles["Center"])
        Story.append(header)
        Story.append(Spacer(1, 48))
        im = Image(logo, inch, inch)
        Story.append(im)
        Story.append(Spacer(1, 12))

        # Adding Time and date
        Story.append(Paragraph(f'EXAM END TIME: {formatted_time}', styles["Normal"]))
        Story.append(Spacer(1, 12))
        
        # User Data:
        Story.append(Spacer(1, 12))
        Story.append(Paragraph( f"<font size = '14'><strong>ISSUED TO</strong></font>", styles["Center"]))
        Story.append(Spacer(1, 12))

        Story.append(Paragraph( f"<font size = '12'>TESTEE NAME: \t<strong>{self.name}</strong> </font>", styles["Normal"]))
        Story.append(Spacer(1, 12))
        Story.append(Paragraph(f"<font size = '12'>EMAIL: \t{self.email}</font>", styles["Normal"]))
        Story.append(Spacer(1, 12))
        Story.append(Paragraph(f"<font size = '12'>ORGANIZATION: \t{self.organization} </font>", styles["Normal"]))
        Story.append(Spacer(1, 12))
        Story.append(Paragraph(f"<font size = '12'>QUALIFICATION: \t{self.qualification} </font>", styles["Normal"]))
        Story.append(Spacer(1, 12))
        Story.append(Paragraph(f"<font size = '12'>POSITION: \t{self.position} </font>", styles["Normal"]))
        Story.append(Spacer(1, 12))
        Story.append(Paragraph(f"<font size = '12'>HASH ID: \t{self.registration_number} </font>", styles["Normal"]))
        Story.append(Spacer(1, 12))

        # Test Summary:
        Story.append(Spacer(1, 12))
        Story.append(Paragraph( f"<font size = '14'><strong>TEST RESULTS</strong></font>", styles["Center"]))
        Story.append(Spacer(1, 12))
        Story.append(Paragraph(f"<font size = '12'>CASES SOLVED: \t{self.app.user_data.events_solved}</font>", styles["Normal"]))
        Story.append(Spacer(1, 12))
        Story.append(Paragraph(f"<font size = '12'>USER TIME: \t{self.app.user_data.total_time}</font>", styles["Normal"]))
        Story.append(Spacer(1, 12))
        Story.append(Paragraph(f"<font size = '12'>MEAN RESPONSE TIME: \t{self.app.user_data.mean_time}</font>", styles["Normal"]))
        Story.append(Spacer(1, 12))
        Story.append(Paragraph(f"<font size = '12'>ACCURACY: \t<strong>{round(self.app.user_data.accuracy, 2)}</strong></font>", styles["Normal"]))
        Story.append(Spacer(1, 12))
        Story.append(Paragraph(f"<font size = '12'>CONFIDENCE: \t<strong>{round(self.app.user_data.confidence, 2)}</strong></font>", styles["Normal"]))
        Story.append(Spacer(1, 12))

        # Bottom Visas
        Story.append(Spacer(1, 74))
        Story.append(Paragraph(f"<font size = '12'>EXAMENER SIGNATURE:   ____________________________                VISA HERE</font>", styles["Justify"]))
        Story.append(Spacer(1, 12))
        Story.append(Paragraph(f"<font size = '12'>OBSERVER 1 SIGNATURE: ____________________________                VISA HERE</font>", styles["Justify"]))
        Story.append(Spacer(1, 12))
        Story.append(Paragraph(f"<font size = '12'>OBSERVER 2 SIGNATURE: ____________________________                VISA HERE</font>", styles["Justify"]))
        Story.append(Spacer(1, 12))
        Story.append(Paragraph(
            """<font size = '9'><bold>Attention!
            Ask your Examiner and the Observers to put their signature into the fields above.
            Visa must be provided if eligible. Unsigned sertificate is not valid!
            The Company and App Developers do not provide any certificate validation
            and not responsible for any inconvience. All exam and cerfitication-related duty and technical support 
            besides issues with Software PIE ONE lays solely on the signees above.</bold></font>
            """, styles["Justify"]))
        Story.append(Spacer(1, 12))

        pdf.build(Story)

        return filename

    def generate_pdf(self):
        pdf = self._get_pdf()

        if platform.system() == 'Darwin':       # macOS
            subprocess.call(('open', pdf))
        elif platform.system() == 'Windows':    # Windows
            os.startfile(pdf)
        else:                                   # linux variants
            subprocess.call(('xdg-open', pdf))
    
    def call_system_printer(self):
        pdf = self._get_pdf()
        if platform.system() == "Windows":
            os.startfile(pdf, "print")
        elif platform.system() == "Darwin":
            os.startfile(pdf, "print")
        elif platform.system() == "Linux":
            os.startfile(pdf, "print")
        else:
            self.app.log_callback(self, self.app.tr._(f"Printing is not supported on {platform.system()} OS yet."))

    def get_data(self) -> dict:
        return {
            'registration_number': self.registration_number,
            'email': self.email,
            'user_name': self.user_name,
            'organization': self.organization,
            'qualification': self.qualification,
            'position': self.position
            }
