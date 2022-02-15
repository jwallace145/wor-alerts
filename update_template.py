from src.aws_gateways.ses_gateway import SesGateway

ses_gateway = SesGateway()

response = ses_gateway.update_template(
    template_file_path="./src/email_templates/alert_email.html", subject="69420"
)

print(response)
