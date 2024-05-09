from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle

def generate_ticket(userdata, pdf_filename):
    try:

        # Create a PDF document
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
        
        # Create content for the ticket
        elements = []
        
        # Add blue border
        border_style = ParagraphStyle(
            name='BlueBorder',
            textColor=colors.blue,
            borderColor=colors.blue,
            borderWidth=1,
            borderPadding=5,
            alignment=1
        )
        elements.append(Paragraph("<font size=12><b>INDIAN RAILWAY</b></font>", border_style))
        elements.append(Spacer(1, 0.1*inch))
        
        # Add user data
        user_data_style = getSampleStyleSheet()['BodyText']
        user_data_style.alignment = 0
        user_data_style.leading = 18

        elements.append(Paragraph(f"<b>Train Number:</b> {userdata['train_number']} | <b>Train Name:</b> {userdata['train_name']} | "
                                f"<b>Class:</b> {userdata['selected_class']} | <b>Fare:</b> {userdata['fare']} | "
                                f"<b>PNR:</b> {userdata['pnr']} | <b>Ticket Status:</b> {userdata['current_status']}", user_data_style))
        
        elements.append(Paragraph(f"<b>From Station:</b> {userdata['from_station_name'] } ({userdata['from_station_code']}) | "
                                f"<b>Departure Time:</b> {userdata['from_station_arrival_time']} | "
                                f"<b>Departure Date:</b> {userdata['from_station_arrival_date']}", user_data_style))
        
        elements.append(Paragraph(f"<b>To Station:</b> {userdata['to_station_name']} ({userdata['to_station_code']}) | "
                                f"<b>Arrival Time:</b> {userdata['to_station_arrival_time']} | "
                                f"<b>Arrival Date:</b> {userdata['to_station_arrival_date']}", user_data_style))
        
        elements.append(Paragraph(f"<b>Name:</b> {userdata['name']} | "
                                f"<b>Age:</b> {userdata['age']} | "
                                f"<b>Gender:</b> {userdata['gender']} | "
                                f"<b>Nationality:</b> {userdata['nationality']}", user_data_style))

        # Build PDF document
        doc.build(elements)
    except Exception as err:
        print(err)

