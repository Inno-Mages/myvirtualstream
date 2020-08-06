from flask import *
import os
from datetime import *
import noisereduce as nr

app = Flask(__name__)

def trim_v(videoPath, stime, etime):
    vpath = videoPath.split('.')
    videoOutput = vpath[0]+"_trim."+vpath[1]
    os.system("ffmpeg -i "+videoPath+" -ss "+stime+" -t "+etime+" -async 1 "+videoOutput")
    f = open(chan+"/"+uname+"/videos.txt", "r+")
    lines = f.readlines()
    f.close()
    l = []
    for line in lines:
        arr = line.split(',')
        if videoPath == arr[0]:
            l.append(videoOutput+","+arr[1]+","+arr[2])
        else:
            l.append(line)

def splitVideo(videoPath, audioOutput=None, videoOutput=None):
    if videoOutput is not None:
        os.system("ffmpeg -i "+videoPath+" -an "+videoOutput)
    if audioOutput is not None:
        os.system("ffmpeg -i "+videoPath+" -vn "+audioOutput)

def mergeAudio(base, input, startingPos, output):
    inp = ['-i '+vid for vid in input]
    inp = ' '.join(inp)
    pos = ['['+str(p+1)+']adelay='+str(startingPos[p]*1000)+'|'+str(startingPos[p]*1000)+'[s'+str(p+1)+'];' for p in range(len(startingPos))]
    pos2 = ['[s'+str(p+1)+']' for p in range(len(startingPos))]
    count = str(len(startingPos)+1)
    mixer = '-filter_complex \"'+''.join(pos)+'[a:0]'+''.join(pos2)+'amix='+count+'[mixout]\" -map '+count+':v -map [mixout]'
    os.system("ffmpeg -i "+base+" -i "+inp+" "+mixer+" "+output)

def noiseRemove():
    rate, data = wavfile.read("mywav.wav")
    noisy_part = data[10000:15000]
    reduced_noise = nr.reduce_noise(audio_clip=data, noise_clip=noisy_part, verbose=True)

def mergeAudioVideo(audio, video, output):
    os.system("ffmpeg -i "+audio+" -i "+video+" "+output)

@app.route('/', methods=['GET', 'POST'])
def basic():
    if request.method == 'POST':
        global uname = request.form['username']
        password = request.form['password']
        f = open('creden.txt', 'r+')
        users = f.readlines()
        f.close()
        for user in users:
            user = user.split(',')
            if user[0] == uname:
                if user[1] == password:
                    global code = user[2]
                    res = flask.make_response()
                    res.set_cookie("virtualstreamUser", value=uname)
                    if code == 0:
                        return render_template("admin.html")
                    elif code == 1:
                        global chan = user[4]
                        return render_template("channel.html")
                    elif code == 2:
                        global chan = user[4]
                        return render_template("reporter.html")
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
            if channel == "":
                channel = user
            f = open('creden.txt', "r+")
            lines = f.readlines()
            f.close
            a = False
            for line in lines:
                line = line.split(',')
                if line[0] == channel:
                    a = True
                    break
                else:
                    pass
            if acc != 0:
                f = open('creden.txt', 'a+')
                f.write(user+","+password+","+acc+","+date+","+channel+"\n")
                f.close()
            if acc == 1:
                os.system("mkdir cd "+user)
                os.system("cp -r _blank/* "+user)
                #os.system("cd ../"+user+" && screen -d -m python yours.py")
                #os.system("cd ../"+user+" && screen -S "+user+" -d -m python stream.py")
            if acc == 2:
                if a:
                    os.system("mkdir cd "+channel+"/rep/"+user)
                    os.system("cp -r _blank2/* "+channel+"/rep/"+user)
                    # A line to be added
                else:
                    #Create Channel First
        if code == 1:
            user = request.form['user']
            password = request.form['pass']
            acc = 2
            date = datetime.datetime.now()
            channel = uname
            f = open('creden.txt', 'a+')
            f.write(user+","+password+","+acc+","+date+","+channel+"\n")
            f.close()
            os.system("mkdir cd "+channel+"/rep/"+user)
            os.system("cp -r _blank2/* "+channel+"/rep/"+user)
            # A line to be added
    if code == 0:
        f = open("creden.txt", "r+")
        users = f.readlines()
        f.close()
    elif code == 1:
        f = open("creden.txt", "r+")
        u = f.readlines()
        f.close()
        users = []
        for user in u:
            use = split.user(',')
            if use[2] == 2 and use[4] == uname:
                users.append(user)
    return render_template("handel_users.html", u = users)

@app.route('/deluser', methods=['GET', 'POST'])
def deluser():
    if request.method == 'POST':
        user = form.request['del']
        f = open("creden.txt", "r+")
        users = f.readlines()
        f.close()
        new = []
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
                os.system("rm -R "+user)
            if cd == 2:
                os.system("rm -R "+ch+"/rep/"+user)
            else:
                #No Access
        elif code == 1:
            if cd == 2:
                os.system("rm -R "+ch+"/rep/"+user)
            else:
                #No Access
    if code == 0:
        f = open("creden.txt", "r+")
        users = f.readlines()
        f.close()
    elif code == 1:
        f = open("creden.txt", "r+")
        u = f.readlines()
        f.close()
        users = []
        for user in u:
            use = split.user(',')
            if use[2] == 2 and use[4] == uname:
                users.append(user)
    return render_template("handel_users.html", u = users)
    

@app.route('/changekey', methods=['GET', 'POST'])
def key():
    if request.method == 'POST':
        nkey = request.form['key']
        f = open(uname+"/key.txt", "w+")
        f.write(nkey)
        f.close()
    f = open(uname+"/key.txt", "r+")
    k = f.readlines()
    f.close()
    return render_template("change_key.html", key = k[0])

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        vid = request.files['fileToUpload']
        link = request.form['link']
        if vid:
            vid.save(chan+"/"+user+"/"+vid.filename)
        if link:
            lin = link.split('/')
            fileID = 'x'
            linkType = '_'
            if "youtu" in link and ".be" in link:
                os.system("youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' -o \""chan+"/"+user+"/"%(title)s.%(ext)s\" \'"+link+"\'")
            elif "/d/" in link:
                no = 0
                for l in lin:
                    no = no +1
                    if l == 'd':
                        break
                os.system("wget  --no-check-certificate -r 'https://docs.google.com/uc?export=download&id="+lin[no+2]+"' -O '"chan+"/"+user+"/""+lin[no+2]+".mp4'")
            else:
                #error
    return render_template("reporterdash.html")    

@app.route('reTrim')
def rTrim():
    directory = os.listdir(chan+"/"+uname)
    f = open(chan+"/"+uname+"/videos.txt", "w+")
    i = 0
    for video in directory:
        i = i+1
        f.write(chan+"/"+uname+"/"+video+","+i+",0")
    f.close()
    f = open(chan+"/"+uname+"/videos.txt", "r+")
    lines = f.readlines()
    f.close
    n = len(lines)
    data = []
    for line in lines:
        line = line.split(',')
        data.append(line)
    return render_template("trim.html", num = n, d = data)


@app.route('/trim', methods=['GET', 'POST'])
def trim():
    def example(vname):
        f = open(chan+"/"+uname+"/videos.txt", "r+")
        lines = f.readlines()
        f.close()
        new = []
        for line in lines:
            l = line.split(',')
            if vname == l[0]:
                if l[2] == 1:
                    l[2] = 0
                elif l[2] == 0:
                    l[2] = 1
                new.append(l[0]+","+l[1]+","+l[2])
            else:
                new.append(line)
        f = open(chan+"/"+uname+"/videos.txt", "w+")
        for line in new:
            f.write(line+"\n")
        f.close()
    if request.method == 'POST'
        smin = request.form['s_minute']
        ssec = request.form['s_seconds']
        emin = request.form['e_minute']
        esec = request.form['e_seconds']
        vname = request.form['formname']
        stime = "00:"+smin+":"+ssec
        etime = "00:"+emin+":"+esec
        trim_v(chan+"/"+uname+"/"+vname, stime, etime)
    f = open(chan+"/"+uname+"/videos.txt", "r+")
    lines = f.readlines()
    f.close
    n = len(lines)
    data = []
    for line in lines:
        line = line.split(',')
        data.append(line)
    return render_template("trim.html", num = n, d = data)

@app.route('/seq', methods=['GET', 'POST'])
def seq():
    def example(vname):
        f = open(chan+"/"+uname+"/videos.txt", "r+")
        lines = f.readlines()
        f.close()
        new = []
        for line in lines:
            l = line.split(',')
            if vname == l[0]:
                if l[2] == 1:
                    l[2] = 0
                elif l[2] == 0:
                    l[2] = 1
                new.append(l[0]+","+l[1]+","+l[2])
            else:
                new.append(line)
        f = open(chan+"/"+uname+"/videos.txt", "w+")
        for line in new:
            f.write(line+"\n")
        f.close()
    if request.method == 'POST':
        no = request.form['sequencebox']
        video = request.form['formname']
        f = open(chan+"/"+uname+"videos.txt", "r+")
        lines = f.readlines()
        f.close()
        new = []
        for line in lines:
            l = line.split(',')
            if l[0] == video:
                temp = l[1]
                l[1] = no
                new.append(l[0]+","+l[1]+","+l[2])
                for line in lines:
                    l = line.split(',')
                    if l[0] != video and l[1] == no:
                        l[1] == temp
                        new.append(l[0]+","+l[1]+","+l[2])
        for line in lines:
            l = line.split(',')
            if l[0] == video or l[1] == no:
                pass
            else:
                new.append(line)
        f = open(chan+"/"+uname+"/videos.txt", "w+")
        for line in new:
            f.write(line+"\n")
        f.close()
    f = open(chan+"/"+uname+"/videos.txt", "r+")
    lines = f.readlines()
    f.close
    n = len(lines)
    data = []
    for line in lines:
        line = line.split(',')
        data.append(line)
    return render_template("trim.html", num = n, d = data)

@app.route('/up', methods=['GET', 'POST'])
def up():
    def example(vname):
        f = open(chan+"/"+uname+"/videos.txt", "r+")
        lines = f.readlines()
        f.close()
        new = []
        for line in lines:
            l = line.split(',')
            if vname == l[0]:
                if l[2] == 1:
                    l[2] = 0
                elif l[2] == 0:
                    l[2] = 1
                new.append(l[0]+","+l[1]+","+l[2])
            else:
                new.append(line)
        f = open(chan+"/"+uname+"/videos.txt", "w+")
        for line in new:
            f.write(line+"\n")
        f.close()
    if request.method == 'POST':
        video = request.form['formname']
        f = open(chan+"/"+uname+"videos.txt", "r+")
        lines = f.readlines()
        f.close()
        new = []
        for line in lines:
            l = line.split(',')
            if l[0] == video:
                global temp = l[1]
                l[1] = l[1] - 1
                new.append(l[0]+","+l[1]+","+l[2])
                for line in lines:
                    l = line.split(',')
                    if l[0] != video and l[1] == temp - 1:
                        l[1] == temp
                        new.append(l[0]+","+l[1]+","+l[2])
        for line in lines:
            l = line.split(',')
            if l[0] == video or l[1] == temp - 1:
                pass
            else:
                new.append(line)
        f = open(chan+"/"+uname+"/videos.txt", "w+")
        for line in new:
            f.write(line+"\n")
        f.close()
    f = open(chan+"/"+uname+"/videos.txt", "r+")
    lines = f.readlines()
    f.close
    n = len(lines)
    data = []
    for line in lines:
        line = line.split(',')
        data.append(line)
    return render_template("trim.html", num = n, d = data)

@app.route('/down', methods=['GET', 'POST'])
def down():
    def example(vname):
        f = open(chan+"/"+uname+"/videos.txt", "r+")
        lines = f.readlines()
        f.close()
        new = []
        for line in lines:
            l = line.split(',')
            if vname == l[0]:
                if l[2] == 1:
                    l[2] = 0
                elif l[2] == 0:
                    l[2] = 1
                new.append(l[0]+","+l[1]+","+l[2])
            else:
                new.append(line)
        f = open(chan+"/"+uname+"/videos.txt", "w+")
        for line in new:
            f.write(line+"\n")
        f.close()
    if request.method == 'POST':
        video = request.form['formname']
        f = open(chan+"/"+uname+"videos.txt", "r+")
        lines = f.readlines()
        f.close()
        new = []
        for line in lines:
            l = line.split(',')
            if l[0] == video:
                global temp = l[1]
                l[1] = l[1] + 1
                new.append(l[0]+","+l[1]+","+l[2])
                for line in lines:
                    l = line.split(',')
                    if l[0] != video and l[1] == temp + 1:
                        l[1] == temp
                        new.append(l[0]+","+l[1]+","+l[2])
        for line in lines:
            l = line.split(',')
            if l[0] == video or l[1] == temp + 1:
                pass
            else:
                new.append(line)
        f = open(chan+"/"+uname+"/videos.txt", "w+")
        for line in new:
            f.write(line+"\n")
        f.close()
    f = open(chan+"/"+uname+"/videos.txt", "r+")
    lines = f.readlines()
    f.close
    n = len(lines)
    data = []
    for line in lines:
        line = line.split(',')
        data.append(line)
    return render_template("trim.html", num = n, d = data)

@app.route('/delsel', methods=['GET', 'POST']):
    f = open(chan+"/"+uname+"/videos.txt", "r+")
    lines = f.readlines()
    f.close()
    new = []
    for line in lines:
        l = line.split(',')
        if l[2] == 1:
            os.system("rm -R "+l[0])
        else:
            new.append(line)
    f = open(chan+"/"+uname+"/videos.txt", "w+")
    for line in new:
        f.write(line+"\n")
    f.close()
    f = open(chan+"/"+uname+"/videos.txt", "r+")
    lines = f.readlines()
    f.close
    n = len(lines)
    data = []
    for line in lines:
        line = line.split(',')
        data.append(line)
    return render_template("trim.html", num = n, d = data)

@app.route('/preset', methods=['GET', 'POST'])
def preset():
    