import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Mailer:
	def __init__(self):
		self.email = 'info@digitalmediabay.com'
		self.password = 'Fiverr101$'
		self.server =  "smtp.titan.email"
		self.port = 587

	def SendMail(self, videoURL, to_email):
		message_body =  '''<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Digital Media Bay Video</title>
	<!-- Include Bootstrap CSS -->
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
	<style>
		/* Custom Styles */
		body {
			font-family: Arial, sans-serif;
			background-color: #f4f4f4;
			margin: 0;
			padding: 0;
		}
		.container {
			background-color: #ffffff;
			border-radius: 5px;
			box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
			padding: 20px;
			max-width: 600px;
			margin: 20px auto;
		}
		h1 {
			color: #333;
		}
		p {
			font-size: 16px;
			line-height: 1.6;
			color: #555;
		}
		.btn {
			display: inline-block;
			background-color: #007bff;
			color: white !important;
			padding: 10px 20px;
			margin: 10px 0;
			text-decoration: none;
			border-radius: 3px;
		}
	</style>
</head>''' + f'''
<body>
	 <div class="container">
		<p>Hello,</p>
		<p>Your Digital Media Bay video is ready for download. To download, please
		click on the "Download Video" button or use the provided link below. When
		using a mobile device, the video will be saved to the "Files" folder on
		iPhone and "My Files" or “File Manager" on Android.</p>
		<p>Please note this link will expire in 4 hours.</p>
		<p><strong>Your Video url:</strong> <a href="{videoURL}">{videoURL}</a></p>
		<a class="mb-2" href="https://digitalmediabay.vercel.app/download?url={videoURL}"
		style="
		padding: 10px 20px;
		appearance: none;
		-moz-appearance: none;
		-webkit-appearance: none;
		background: #ff2a61;
		border: none;
		border-radius: 0.5em;
		box-sizing: border-box;
		color: #fff !important;
		cursor: pointer;
		display: flex;
		height: 2.4em;
		justify-content: center;
		line-height: 1em;
		align-items:center;
		font-weight:bold;
		outline: none;
		width: -moz-fit-content;
		width: -webkit-fit-content;
		width: fit-content;
		text-decoration: none;">
		Download Video
		  </a>          
		<p>If you experience any issues with this delivery, we advise to simply create another
		video. If the issue persists, please reply to this email with a detailed description of the
		problem.</p>
		<p>Thank you,</p>
		<a href="http://www.digitalmediabay.com/">http://www.digitalmediabay.com/</a>
	</div>
</body>
</html>
		'''
		msg = MIMEMultipart("alternative")
		msg['Subject'] = "Digital Media Bay Video"
		msg['From'] = self.email
		msg['To'] = to_email
		message_body = MIMEText(message_body, "html")
		msg.attach(message_body)
		server = smtplib.SMTP(self.server, self.port)
		server.login(self.email, self.password)  # user & password
		server.send_message(msg)
		server.quit()
		print('successfully sent the mail.')


if __name__ == "__main__":
	mailer = Mailer()
	mailer.SendMail('https://res.cloudinary.com/dpynlgyfi/video/upload/v1707281410/record_data/xdtu5bfrmsquf5ysg8g9.mp4', "zain.9496@gmail.com")