import requests,json

def log(session,account):
	s=session.post("https://mbasic.facebook.com/login",
		data=
			{
				"email":account.split("|")[-0],
				"pass":account.split("|")[-1]
			}
	).url
	if "save-device" in s or "m_sess" in s:
		return True
	else:
		return False

def baselogin(session):
	j=json.loads(open("config/config.json").read())
	s=session.post("https://mbasic.facebook.com/login",
		data={"email":j["email"],"pass":j["pass"]}).url
	if "save-device" in s or "m_sess" in s:
		return True
	else:return False