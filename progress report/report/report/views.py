from django.http import HttpResponse
from django.shortcuts import render
import pyrebase
from firebase import firebase
from django.contrib import auth
admin_uid = "tSSv32i3usbppGZUIxsdXczf9NM2"
name = " "
email = " "
config = {
	"apiKey": "",
	"authDomain": "",
	"databaseURL": "",
	"storageBucket": "",
	}
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

def main(request):
	return render(request,'form.html')



def mainpost(request):
	global email
	email = request.POST.get('email')
	email = str(email).rstrip(' \t\r\n\0') #new line added here --------
	password = request.POST.get('password')
	try:
		user = authe.sign_in_with_email_and_password(email, password)
	
	except :
		message = "Invalid Login Credentials"
		return render(request,'form.html', {'message':message})

	#user = authe.sign_in_with_email_and_password(email, password)
	uid = user['localId']
	request.session['fav_color'] = str(uid)
	all_users = database.child("Daily_Report").child(uid).child("details").get()
	d = all_users.val()
	print ("date here is:"+str(d))
	d = " "+str(d['name'])
	global name
	name = "<b>"+str("Hello,"+str(d))+"</b>"
	
	if email == "vishal.sharma438@gmail.com":


		return render(request,"adminhome.html")

	
	else:	
		
		status = database.child("Daily_Report").child(uid).child("details").child("status").get()
		status = status.val()
		if status == "0":
			return HttpResponse("Your Account Has Been Temporary Disabled Please Contact Admin")
		else:	
			return render(request,'home.html', {'name':name})

def signup(request):
	return render(request,'signup.html')

def home(request):
	return render(request,'home.html',{'name':name})

def signuppost(request):
	username = request.POST.get('name_field')
	password = request.POST.get('password')
	email = request.POST.get('email')	
	config = {
		"apiKey": "",
		"authDomain": "",
		"databaseURL": "",
		"storageBucket": "",
		}
	firebase = pyrebase.initialize_app(config)
	auth = firebase.auth()	
	user = auth.create_user_with_email_and_password(email, password)
	print (user)
	uid = user['localId']
	data = {"name": username,"status":"1"}
	database.child("Daily_Report").child(uid).child("details").set(data)
	#============testing code starts here==================#
	user = authe.sign_in_with_email_and_password(email, password)
	uid = user['localId']
	request.session['fav_color'] = str(uid)
	#all_users = database.child("Daily_Report").child(uid).child("details").get()
	#d = all_users.val()
	#print ("date here is:"+str(d))
	#d = " "+str(d['name'])
	global name
	name = "<b>"+str("Hello,"+str(username))+"</b>"
	message  = "Account Created Successfully"
	return render(request,'home.html', {'name':name,'message':message})

	#========== ends here
	#return render(request,'form.html')


def adminhome(request):
	return render(request,'adminhome.html')	

def createreport(request):


	return render(request,'newreport.html', {"name":name})	


def postcreatereport(request):

	import time
#	import smtplib---------------------------------------
#	from email.mime.multipart import MIMEMultipart       >---libraries for sending email ----- -->
#	from email.mime.text import MIMEText-----------------
	import pytz
	from datetime import datetime, timezone
	
	tz = pytz.timezone('Asia/Kolkata')
	utc_dt = datetime.now(timezone.utc).astimezone(tz)
	millis = int(time.mktime(utc_dt.timetuple()))
	UID = request.session['fav_color']	
	
	x = str(utc_dt)
	z,y = x.split("+")
	q,w,e = z.split(":")
	date = q +":"+ w
	global Task
	Task = request.POST.get('Text1')
	global Progress
	Progress = request.POST.get('Text2')
	data = {"date": date, "Task:": Task,"Progress:" : Progress}
	database.child("Daily_Report").child(UID).child("reports").child(millis).set(data)
	message = "Report Created Successfully"

#==============================================email sending starts here===================#
	"""all_users = database.child("Daily_Report").child(UID).child("details").get()
					d = all_users.val()
					d = d['name']
					print (email)
					fromaddr = str(email)  #==========sender mail
					toaddr = "kavin.picktick@gmail.com" #================receiver mail
					msg = MIMEMultipart()
					msg['From'] = fromaddr
					msg['To'] = toaddr
					msg['Subject'] = "Daily Progress Report Of " + str(d) 
					body = "date:"+str(date)+"\nTask:"+ str(Task) + "\nProgress:" + str(Progress)  
					msg.attach(MIMEText(body, 'plain'))
					 
					server = smtplib.SMTP('smtp.gmail.com', 587)
					server.starttls()
					server.login(fromaddr, "password-here")
					text = msg.as_string()
					server.sendmail(fromaddr, toaddr, text)
					server.quit()
					print("mail sent")
				"""	
	return render(request,'home.html',{'name':name,'message':message})

def logout(request):
	print (auth)
	auth.logout(request)

	return render(request,"form.html")	

def checkreport(request):
	import datetime
	UID = request.session['fav_color']	
	all_user_ids = database.child("Daily_Report").child(UID).shallow().child('reports').get().val()
	if all_user_ids is None:
	
		return render(request, "noreport.html", {"name":name})
	
	lis = []
	for item in all_user_ids:
		lis.append(str(item))
		lis.sort(reverse = True)
#	print (lis)
     
	dat = []
	for i in lis:
		i = float(i)
		#i = (int(i)/1000.0)
#		print ("in seconds"+str(i))
		a = datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
#		print ("in time "+ str(a))
		dat.append(str(a))
#	print (dat)	
	task = []
	for title in lis:
		b = database.child("Daily_Report").child(UID).child('reports').shallow().child(title).child('Task:').get().val()
		c = b.split(" ")
		print (len(c))
		if len(c)<10:
			task.append(b)
		else :
			ta = " ".join(c[:10])
			ta = str(ta) + "..."
			task.append(ta)

		print(task)
	lise = zip(lis, dat, task)
	return render(request, "check.html", {"lise" :lise, "name":name, "UID":UID})

def postcheck(request):
	id=request.GET.get('z')
	UID = request.session['fav_color']	
	date = database.child("Daily_Report").child(UID).child('reports').shallow().child(id).child('date').get().val()
	Progress = database.child("Daily_Report").child(UID).child('reports').shallow().child(id).child('Progress:').get().val()
	Task = database.child("Daily_Report").child(UID).child('reports').shallow().child(id).child('Task:').get().val()
	print (name)
	#a,nam = name.split(",")
	return render(request, "show.html" , {"name":name,"UID":UID,"date":date,'Progress':Progress,'Task':Task})
def lostpassword(request):

	email  = request.POST.get('email')
	text = "reset link sent to " +str(email)
	authe.send_password_reset_email(email)
	return HttpResponse(text)

def admincheck(request):
		mess = ""
		if request.method == 'GET' and 's' in request.GET:
			UID=request.GET.get('uuid')
			status=request.GET.get('s')
			if status== "1":
				data = {"status":"0"}
				global mess
				mess = "Account Disabled Successfully"
			else:
				data = {"status":"1"}			
				global mess
				mess = "Account Enabled Successfully"
			database.child("Daily_Report").child(UID).child("details").update(data)

		message = str(mess)	


		all_user_ids = database.shallow().child("Daily_Report").get().val()	
		lis=[]
		for a in all_user_ids:
			lis.append(a)
		print(lis)		
		lis.remove(admin_uid)	
		name=[]	
		for b in lis:
			i = database.child("Daily_Report").child(b).child("details").shallow().child("name").get().val()
			name.append(i)		
		print(name)		
		status=[]
		for x in lis:
			j = database.child("Daily_Report").child(x).child("details").shallow().child('status').get().val()
			status.append(j)

		lise = zip(lis, name, status)	
		return render(request,'admincheck.html',{'lise':lise,"message":message})

def postadmincheck(request):

    

	import datetime
	
	if request.method == 'GET' and 'csrfmiddlewaretoken' in request.GET:
	
		UID=request.GET.get('UUID')
		print (UID)
		search = request.GET.get('search')
		search = str(search).lower()
		print(search)
		timestamp = database.child("Daily_Report").child(UID).shallow().child('reports').get().val()
		print (timestamp)
		task = []
		for id in timestamp:
			tas = database.child("Daily_Report").child(UID).child('reports').shallow().child(id).child('Task:').get().val()
			tas = str(tas) + "$" + str(id)
			task.append(tas)
		print (task)
		matching = [str(string) for string in task if str(search) in (string.lower())]
		ftask=[]
		ftime=[]
		for d in matching:
			task,time = d.split("$")
			ftask.append(task)
			ftime.append(time)
		dat = []
		for date in ftime:
			i = float(date)
			a = datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
			dat.append(str(a))

		name = database.child("Daily_Report").child(UID).child("details").shallow().child("name").get().val()	
			
		lise = zip(ftask, ftime, dat)	
		return render(request,"search.html",{"UID":UID,"lise":lise,"name":name})
	

	else:


		import datetime
		q1=request.GET.get('q')
		ide = str(q1) 
		print (ide)
		all_user_ids = database.child("Daily_Report").child(ide).shallow().child('reports').get().val()
		print (all_user_ids)
		lis = []
		for item in all_user_ids:
			lis.append(str(item))
			lis.sort()
			lis.reverse()
		print (lis)
	     
		dat = []
		for i in lis:
			i = float(i)
			#i = (int(i)/1000.0)
			print ("in seconds"+str(i))
			a = datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
			print ("in time "+ str(a))
			dat.append(str(a))
		print (dat)	
		task = []
		for title in lis:
			b = database.child("Daily_Report").child(ide).child('reports').shallow().child(title).child('Task:').get().val()
			print ("here is the "+ b)
			c = b.split(" ")
			print (len(c))
			if len(c)<10:
				task.append(b)
			else :
				ta = " ".join(c[:10])
				ta = str(ta) + "..."
				task.append(ta)

			print(task)
		name = database.child("Daily_Report").child(ide).child("details").shallow().child("name").get().val()	
		lise = zip(lis, dat, task)
		return render(request,"adminshow.html", {'lise':lise,'name':name, 'ide':ide})

def admindetail(request):
	UID=request.GET.get('q')
	id = request.GET.get('z') 
	date = database.child("Daily_Report").child(UID).child('reports').shallow().child(id).child('date').get().val()
	Progress = database.child("Daily_Report").child(UID).child('reports').shallow().child(id).child('Progress:').get().val()
	Task = database.child("Daily_Report").child(UID).child('reports').shallow().child(id).child('Task:').get().val()
	
	return render(request, "show.html" , {"UID" : UID,"name":name,"date":date,'Progress':Progress,'Task':Task})

		

