from flask import *
import os
from datetime import *

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def basic():
    if request.method == 'POST':
        f = open('creden.txt', 'r+')
        global uname = request.form['username']
        password = request.form['password']
        users = f.readlines()
        for user in users:
            user = user.split(',')
            if user[0] == uname:
                if user[1] == password:
                    global code = user[2]
                    res = flask.make_response()
                    res.set_cookie("virtualstreamUser", value=uname)
                    if code == 0:
                        return render_template("admin/admin.html")
                    elif code == 1:
                        return render_template(uname+"/admin.html")
                    elif code == 2:
                        return render_template(user[4]+"/rep/"+uname+"/admin.html")
                else:
                    flash("Check your credentials", "info")
                    return render_template("index.html")
        flash("Check your credentials", "info")
        return render_template("index.html")
    else:
        return render_template("index.html")

#UPLOAD_FOLDER = path to be uploaded later.

@app.route('/handel_user', methods = ['GET', 'POST'])
def hanuser():
    if request.method == 'POST':
        if code == 0:
            user = request.form['user']
            password = request.form['pass']
            acc = request.form['code']
            date = datetime.datetime.now()
            channel = request.form['channel']
            f = open('creden.txt', 'a+')
            f.write(user+","+password+","+acc+","+date+","+channel+"\n")
            f.close()
            if acc == 1:
                os.system("mkdir cd ../"+user)
                os.system("cp -r ../_blank/* ../"+user)
                #os.system("cd ../"+user+" && screen -d -m python yours.py")
                #os.system("cd ../"+user+" && screen -S "+user+" -d -m python stream.py")
            if acc == 2:
                os.system("mkdir cd ../"+channel+"/rep/"+user)
                os.system("cp -r ../_blank2/* ../"+channel+"/rep/"+user)
                # A line to be added
        if code == 1:
            user = request.form['user']
            password = request.form['pass']
            acc = 2
            date = datetime.datetime.now()
            channel = request.form['channel']
            f = open('creden.txt', 'a+')
            f.write(user+","+password+","+acc+","+date+","+channel+"\n")
            f.close()
            os.system("mkdir cd ../"+channel+"/rep/"+user)
            os.system("cp -r ../_blank2/* ../"+channel+"/rep/"+user)
            # A line to be added
    f = open("creden.txt", "r+")
    users = f.readlines()
    f.close()
    return render_template("handel_users.html", u = users)

@app.route('/deluser', methods=['GET', 'POST'])
def deluser():
    if request.method == 'POST':
        user = form.request['del']
        f = open("creden.txt", "r+")
        users = f.readlines()
        new = []
        f.close()
        for u in users:
            n = u.split(',')
            if n[0] == user:
                cd = n[2]
                ch = n[4]
                pass
            else:
                new.append(u)
        f = open("creden.txt", "w+")
        for n in new:
            f.write(n+"\n")
        if code == 0:
            if cd == 1:
                os.system("rm -R ../"+user)
            if cd == 2:
                os.system("rm -R ../"+ch+"/rep/"+user)
        elif code == 1:
            if cd == 2:
                os.system("rm -R rep/"+user)
    f = open("creden.txt", "r+")
    users = f.readlines()
    f.close()
    return render_template("handel_users.html", u = users)
    

@app.route('/changekey', methods=['GET', 'POST'])
def key():
    if request.method == 'POST':
        nkey = request.form['key']
        f = open("key.txt", "w+")
        f.write(nkey)
        f.close()
    f = open("key.txt", "r+")
    k = f.readlines()
    f.close()
    return render_template("change_key.html", key = k[0])

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        vid = request.files['fileToUpload']
        link = request.form['link']
        if vid:
            vid.save("#location"+vid.filename)
        if link:
            lin = link.split('/')
            fileID = 'x'
            linkType = '_'
            if "youtu" in link and ".be" in link:
                os.system("youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' -o \"#location/%(title)s.%(ext)s\" \'"+link+"\'")
            elif "/d/" in link:
                no = 0
                for l in lin:
                    no = no +1
                    if l == 'd':
                        break
                os.system("wget  --no-check-certificate -r 'https://docs.google.com/uc?export=download&id="+lin[no+2]+"' -O '"+lin[no+2]+".mp4'")
            else:
                #error
                pass

@app.route('/editing', methods=['GET', 'POST'])
def editing():
    return render_template("videoeditor.html")