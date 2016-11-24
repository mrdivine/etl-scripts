import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders

def process(tr, parameters, tableBuilder):
  """
	Service to notify qbic and send project tsv if a user chose
	not to register a project but to inquire about costs in the
	wizard.
  """

  server = "smtpserv.uni-tuebingen.de"
  fromA = "notification_service@qbis.qbic.uni-tuebingen.de"

  project = parameters.get("project")
  space = parameters.get("space")
  user = parameters.get("user")

  roles = tr.getAuthorizationService().listRoleAssignments(). This returns you a collection of IRoleAssignmentImmutable. With this you can get the user id (IUserImmutable getUser()). When you use the email address as userID you have what you want. 


  subject = user+" would like to register the new project "+project
  toA = ''
  for mail in ["andreas.friedrich@uni-tuebingen.de"]:#test
    toA += '%s,' % mail

  text = "Hi,\n\n%s would like to register the Project %s in Space %s.\nI've attached the project TSV for you.\n\nHave a nice day,\nYour friendly mail service plugin." % (user,project,space)
  #msg = MIMEText(text)
  msg = MIMEMultipart()
  msg['From'] = fromA
  msg['To'] = toA
  msg['Subject'] = subject
  #msg['reply-to'] = "info@qbic.uni-tuebingen.de"

  part = MIMEBase('application', "octet-stream")
  part.set_payload("multiline text\n to be found in the attached file\nkthxbye")
  Encoders.encode_base64(part)

  part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(project+"_plan.tsv")
  msg.attach(part)

  smtpServer = smtplib.SMTP(server)
  smtpServer.sendmail(fromA, toA, msg.as_string())
  smtpServer.close()