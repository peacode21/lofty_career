import os,random,string

from flask import render_template,request,session,flash,redirect,url_for

from sqlalchemy.sql import text

from sqlalchemy import or_

from werkzeug.security import generate_password_hash,check_password_hash

from lofty_career import app,db

from lofty_career.models import User,Lga,Job,JobApplication,Skill,State



@app.route('/')
def home():
    return render_template("user/index2.html")
        
    

@app.route('/home')
def homes():
    return render_template("user/index.html")
        
    


@app.route("/home/register/", methods=['GET','POST'])
def register():
    if request.method =='GET':
        return redirect(url_for('form'))
    else:
        lgas=request.form.get('lgaid')
        fname=request.form.get('fname')
        lname=request.form.get('lname')
        email=request.form.get('email')
        pwd=request.form.get('pwd')
        address=request.form.get('address')
        number = request.form.get('number')
        username = request.form.get('username')
        secque = request.form.get('user_sec_que')
        secans = request.form.get('user_sec_ans')
        gender = request.form.get('gender')
        hashed_pwd=generate_password_hash(pwd)
        if fname !='' and lname !='' and email !='' and pwd !='' and lgas !='' and address !=''  and username !=''  and secque !=''  and secans !='' and number !='':
            user=db.session.query(User).filter(User.user_username==username).first()
            local=db.session.query(Lga).filter(Lga.lga_name==lgas).first()
            if user != None:
                flash("Username Already Exists")
                return redirect(url_for('form'))
            else:
                u=User(user_fname=fname,user_lname=lname,user_email=email,user_pwd=hashed_pwd,user_lga_id=local.lga_id,user_sec_que=secque,user_sec_ans=secans,user_username=username,user_phoneno=number,user_address=address,user_gender=gender)
                db.session.add(u)
                db.session.commit()
                userid=u.user_id
                session['user']=userid
                return redirect(url_for('homes'))
        else:
            flash("You must complete all the fields to signup")
            return redirect(url_for('form'))




@app.route('/form/', methods=['GET','POST'])
def form():
    state = State.query.all()
    lgas = Lga.query.all()
    return render_template("user/form.html",lgas=lgas,state=state)





@app.route('/home/login/',methods=['GET','POST'])
def user_login():
    if request.method =='GET':
        return redirect(url_for('form'))
    else:
        email=request.form.get('email')
        pwd=request.form.get('pwd')
        logs=db.session.query(User).filter(User.user_email==email).first()
        if email !='' and pwd !='':
            if logs != None:
                pwd_indb= logs.user_pwd
                chk=check_password_hash(pwd_indb,pwd)
                if chk == True:
                    id= logs.user_id
                    session['user']=id
                    return redirect(url_for('homes'))
                else:
                    flash("Invalid Credentials")
                    return redirect(url_for('form'))
            else:
                flash("Invalid Credentials")
                return redirect(url_for('form'))
        else:
            flash("One or more fields are empty, Please complete the form")
            return redirect(url_for('form'))





        
@app.route('/home/dashboard/')
def dashboard():
    if session.get('user') != None:
        job = Job.query.all()
        return render_template("user/jobview.html",job=job)
    else:
        return redirect(url_for('form'))






@app.route('/job/description/<id>')
def description(id):
    if session.get('user') != None:
        job = Job.query.get_or_404(id)
        jobs = Job.query.all()
        return render_template("user/jobdesc.html",job=job,jobs=jobs)
    else:
        return redirect(url_for('form'))





@app.route('/job/apply/<id>',methods=['GET','POST'])
def apply(id):
    if session.get('user') != None:
        fb = request.form.get('feedback')
        job = Job.query.get_or_404(id)
        if fb != '':
            japp=JobApplication(j_app_status=job.job_status,j_app_user_id=session['user'],j_app_lga_id=job.job_lga_id,j_app_job_id=job.job_id,j_app_feedback=fb,j_app_employer_id=job.job_employer_id)
            db.session.add(japp)
            db.session.commit()
            flash('Applied Successfully')
            return redirect(url_for('applied',id=job.job_id))
        else:
            flash('You cannot submit an empty field')
            return redirect(url_for('apply'),id=japp.job_application_id)
    else:
        return redirect(url_for('form'))






@app.route('/home/search/jobs',methods=['GET','POST'])
def search():
    if session.get('user') != None:
        if request.method =='GET':
            return redirect(url_for('form'))
        else:
            jobs = request.form.get('searched')
            if jobs != '':
                job = Job.query.filter(Job.job_title.ilike("%"+ jobs + "%")).all()
                if job != []:
                    return render_template('user/search_jobs.html',job=job)
                else:
                    flash('One or more fields are empty, Please complete the form to proceed')
                return redirect(url_for('homes'))
            else:
                flash('One or more fields are empty, Please complete the form to proceed')
                return redirect(url_for('homes'))
    else:
        return redirect(url_for('form'))





@app.route('/load_lga/<stateid>')
def load_lga(stateid):
    lgas = db.session.query(Lga).filter(Lga.lga_stateid==stateid).all()
    data2send = '<select name="lgaid" class="form-select form-select-md mb-1">'
    for s in lgas:
        data2send =data2send+"<option>"+s.lga_name +"</option>"
    data2send = data2send+ "</select>"
    
    return data2send





@app.route('/profile/picture/change',methods=["POST","GET"])
def pix():
    if session.get('user') == None:
        return redirect(url_for('form'))
    else:
        return render_template('user/picture.html')



@app.route('/profile/picture/',methods=["POST","GET"])
def picture():
    if session.get('user') == None:
        return redirect(url_for('form'))
    else:
        if request.method == 'GET':
            return redirect(url_for('pix'))
        else:
            file=request.files['pix']
            files=request.files['resume']
            filename= file.filename
            filenames= files.filename
            allowed = ['.png','.jpg','.jpeg','.JPG','.PNG','.JPEG']
            allows = ['.png','.jpg','.jpeg','.JPG','.PNG','.JPEG','.PDF','.pdf','.csv','.CSV']
            if filename !='' and filenames !='':
                name,ext = os.path.splitext(filename)
                names,exts = os.path.splitext(filenames)
                if ext in allowed and exts in allows:
                    newname= generate_name()+ext
                    newnames= generate_name()+exts
                    file.save('lofty_career/static/uploads/'+newname)
                    files.save('lofty_career/static/resume/'+newnames)
                    userpic=db.session.query(User).get(session['user'])
                    userpic.user_photo = newname
                    userpic.user_resume = newnames
                    db.session.commit()
                    flash("File Uploaded Successfully")
                    return redirect(url_for('user_profile'))
                else:
                    flash('File type not allowed')
                    return redirect(url_for('picture'))
            else:
                flash("Please choose a file")
                return redirect(url_for('picture'))



def generate_name():
    filename = random.sample(string.ascii_lowercase,10)
    return ''.join(filename)






@app.route('/job/applied')
def applied():
    if session.get('user') != None:
        id=session.get('user')
        japp = db.session.query(JobApplication).filter(JobApplication.j_app_user_id==id).all()
        return render_template('user/apply.html',japp=japp) 
    else:
        return redirect(url_for('form'))
    






@app.route('/job/company/info/<id>')
def company_info(id):
    if session.get('user') != None:
        job = db.session.query(Job).filter(Job.job_employer_id==id).first()
        jobs = db.session.query(Job).filter(Job.job_employer_id==id).all()
        return render_template('user/company_info.html',job=job,jobs=jobs) 
    else:
        return redirect(url_for('form'))
    




@app.route('/profile/update/account')
def update():
    if session.get('user') == None:
        return redirect(url_for('form'))
    else:
        return render_template('user/update.html')




@app.route('/profile/update',methods=['GET','POST'])
def profile_update():
    if request.method != "GET":
        if session.get('user') == None:
            return redirect(url_for('form'))
        else:
            edu=request.form.get('edu')
            exp=request.form.get('exp')
            skill=request.form.get('skill')
            add=request.form.get('add')
            phoneno=request.form.get('phoneno')
            pastwork=request.form.get('pastwork')
            if add !='' and phoneno !='' and pastwork !='' and skill !='' and edu !='' and exp !='':
                id=session.get('user')
                sk = db.session.query(Skill).filter(Skill.skill_user_id==id).first()
                if sk != None:
                    sk.skill_name = skill
                    sk.skill_user_id = id
                    sk.skill_id = id
                    u = User.query.get(id)
                    u.user_address = add
                    u.user_phoneno = phoneno
                    u.user_pastwork = pastwork
                    u.user_experience = exp
                    u.user_education = edu
                    db.session.commit()
                    flash("Updated Successfully")
                    return redirect(url_for('user_profile'))
                else:
                    u = User.query.get(id)
                    u.user_address = add
                    u.user_phoneno = phoneno
                    u.user_pastwork = pastwork
                    u.user_experience = exp
                    u.user_education = edu
                    skill_add = Skill(skill_id=id,skill_name=skill,skill_user_id=id)
                    db.session.add(skill_add)
                    db.session.commit()
                    flash("Updated Successfully")
                    return redirect(url_for('user_profile'))
            else:
                flash('One or more fields are empty, Please complete the form to proceed')
                return redirect(url_for('profile_update'))
    else:
        return redirect(url_for('form'))





@app.route('/profile/updatepassword')
def pwd_update():
    if session.get('user') == None:
        return redirect(url_for('form'))
    else:
        return render_template('user/update_pwd.html')



@app.route('/profile/update',methods=['GET','POST'])
def update_pwd():
    if request.method != "GET":
        if session.get('user') == None:
            return redirect(url_for('form'))
        else:
            secque = request.form.get('secque')
            secans = request.form.get('secans')
            newpwd = request.form.get('pwd')
            if secans != ''and secque != '' and newpwd != '':
                user = db.session.query(User).filter(User.user_sec_ans==secans).filter(User.user_sec_que==secque).first()
                if user!= None:
                    id=session.get('user')
                    u = User.query.get(id)
                    u.user_pwd=newpwd
                    db.session.commit()
                    flash('Password successfully updated!')
                    return redirect(url_for('profile'))
                    
                else:
                    flash('Incorrect Credentials')
                    return redirect(url_for('update_pwd'))
            else:
                flash('One or more fields are empty, Please complete the form')
                return redirect(url_for('update_pwd'))
    else:
        return redirect(url_for('form'))




@app.route('/user/logout/')
def user_logout():
    if session.get('user')!=None:
        session.pop('user',None)
    return redirect(url_for("home"))


@app.route('/user/profile')
def user_profile():
    if session.get('user') != None:
        id=session.get('user')
        job = Job.query.all()
        data_deets = User.query.get(id)
        return render_template("user/profile.html",data_deets=data_deets,job=job)
    else:
        return redirect(url_for('form'))



@app.errorhandler(404)
def page404(error):
    return render_template("user/404.html",error=error), 404



@app.errorhandler(500)
def internalerror(error):
    return render_template("user/404.html",error=error), 500

