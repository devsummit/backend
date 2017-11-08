import os, codecs
from app.services.helper import Helper


class EmailHackaton():
	"""docstring for EmailPurchase"""

	def __init__(self):
		currpath = os.path.abspath(os.curdir)
		file_path = "%s/%s" % ("app/models/email_templates", "devsummit-hackathon.html")
		path = os.path.join(currpath, file_path)
		f = codecs.open(path, 'r', 'utf-8')
		template_list = f.read()
		f.close()
		self.template = str(template_list)

	def build(self, name):
		return self.template.replace('[ name ]', name)
