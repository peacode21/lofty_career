import os,random,string

from flask import render_template,request,session,flash,redirect,url_for

import json

from sqlalchemy.sql import text

from sqlalchemy import or_

from werkzeug.security import generate_password_hash,check_password_hash

from lofty_career import app,db

from lofty_career.models import Employer,Job,Lga,JobCategory,JobSubcategory,State,JobApplication,User




@app.route('/home/employer')
def comp_home():
    if session.get('employer') != None:
        return render_template("company/index.html")
    else:
        return redirect(url_for('comp_form'))
    


@app.route("/home/comp_register/", methods=['GET','POST'])
def comp_register():
    if request.method =='GET':
        return redirect(url_for('comp_form'))
    else:
        fname=request.form.get('fname')
        lname=request.form.get('lname')
        email=request.form.get('email')
        compname=request.form.get('compname')
        compadd=request.form.get('compadd')
        comp_phoneno=request.form.get('comp_phoneno')
        pwd=request.form.get('pwd')
        esecque = request.form.get('secque')
        esecans = request.form.get('secans')
        eusername = request.form.get('username')
        hashed_pwd=generate_password_hash(pwd)
        if fname !='' and lname !='' and email !='' and pwd !='' and compname !='' and compadd !='' and comp_phoneno !='' and esecque !='' and esecans !='' and eusername !='':
            emp=db.session.query(Employer).filter(Employer.employer_username==eusername).first()
            if emp != None:
                flash("Username Already Exists")
                return redirect(url_for('comp_form'))
            else:
                e=Employer(employer_fname=fname,employer_lname=lname,employer_email=email,employer_pwd=hashed_pwd,e_company_name=compname,e_comp_address=compadd,e_comp_phoneno=comp_phoneno,e_sec_que=esecque,e_sec_ans=esecans,employer_username=eusername)
                db.session.add(e)
                db.session.commit()
                employerid=e.employer_id
                session['employer']=employerid
                return redirect(url_for('comp_home'))
        else:
            flash("You must complete all the fields to signup")
            return redirect(url_for('comp_form'))


@app.route('/form/employer', methods=['GET','POST'])
def comp_form():
    return render_template("company/form.html")


@app.route('/home/login/employer',methods=['GET','POST'])
def comp_login():
    if request.method =='GET':
        return redirect(url_for('comp_form'))
    else:
        email=request.form.get('email')
        pwd=request.form.get('pwd')
        log=db.session.query(Employer).filter(Employer.employer_email==email).first()
        if email !='' and pwd !='':
            if log != None:
                pwd_indb= log.employer_pwd
                chk=check_password_hash(pwd_indb,pwd)
                if chk == True:
                    id= log.employer_id
                    session['employer']=id
                    return redirect(url_for('comp_home'))
                else:
                    flash("Invalid Credential")
                    return redirect(url_for('comp_form'))
            else:
                flash("Invalid Credentials")
                return redirect(url_for('comp_form'))
        else:
            flash("One or more fields are empty, Please complete the form")
            return redirect(url_for('comp_form'))

        
@app.route('/home/dashboard/employer')
def comp_jobpost():
    if session.get('employer') != None:
        job = db.session.query(Job).filter(Job.job_employer_id==session.get('employer')).all()
        return render_template("company/jobpost.html",job=job)
    else:
        return redirect(url_for('comp_form'))





@app.route('/home/dashboard/applicants')
def comp_jobapplicants():
    if session.get('employer') != None:
        jobapp = db.session.query(JobApplication).filter(JobApplication.j_app_employer_id==session.get('employer')).all()
        return render_template("company/applicants.html",jobapp=jobapp)
    else:
        return redirect(url_for('comp_form'))






@app.route('/home/applicant/details/<id>')
def applicant_info(id):
    if session.get('employer') != None:
        jobapp = JobApplication.query.get(id)
        return render_template("company/applicant_info.html",jobapp=jobapp)
    else:
        return redirect(url_for('comp_form'))




@app.route('/employer/job/description/<id>')
def comp_jobdesc(id):
    if session.get('employer') != None:
        job = Job.query.get_or_404(id)
        return render_template("company/comp_jobdesc.html",job=job)
    else:
        return redirect(url_for('comp_form'))






@app.route('/employer/job/delete/<id>')
def comp_deletejob(id):
    if session.get('employer') == None:
        return redirect(url_for('comp_form'))
    else:
        jobobj = Job.query.get_or_404(id)
        db.session.delete(jobobj)
        db.session.commit()
        flash("Successfully Deleted!")
        return redirect(url_for('comp_jobpost'))




@app.route('/employer/profile')
def comp_profile():
    if session.get('employer') != None:
        id=session.get('employer')
        emp_deets = Employer.query.get(id)
        return render_template("company/comp_profile.html",emp_deets=emp_deets)
    else:
        return redirect(url_for('comp_form'))



@app.route('/employer/profile/update/account')
def comp_update():
    if session.get('employer') == None:
        return redirect(url_for('comp_form'))
    else:
        return render_template('company/comp_update.html')




@app.route('/employer/profile/update',methods=['GET','POST'])
def comp_profile_update():
    if request.method != "GET":
        if session.get('employer') == None:
            return redirect(url_for('comp_form'))
        else:
            compname=request.form.get('compname')
            compadd=request.form.get('compadd')
            comp_phoneno=request.form.get('comp_phoneno')
            compweb=request.form.get('compweb')
            if compname !='' and compadd !='' and comp_phoneno !='' and compweb !='':
                id=session.get('employer')
                e = Employer.query.get(id)
                e.e_company_name = compname
                e.e_comp_address = compadd
                e.e_comp_phoneno = comp_phoneno
                e.e_comp_website = compweb
                db.session.commit()
                flash("Updated Successfully")
                return redirect(url_for('comp_profile'))
            else:
                flash('One or more fields are empty, Please complete the form to proceed')
                return redirect(url_for('comp_profile_update'))
    else:
        return redirect(url_for('comp_form'))




@app.route('/employer/profile/updatepassword')
def comp_pwd_update():
    if session.get('employer') == None:
        return redirect(url_for('comp_form'))
    else:
        return render_template('company/comp_update_pwd.html')



@app.route('/employer/updateprofile',methods=['GET','POST'])
def comp_update_pwd():
    if request.method != "GET":
        if session.get('employer') == None:
            return redirect(url_for('comp_form'))
        else:
            secque = request.form.get('secque')
            secans = request.form.get('secans')
            newpwd = request.form.get('pwd')
            if secans != ''and secque != '' and newpwd != '':
                emp = db.session.query(Employer).filter(Employer.e_sec_ans==secans).filter(Employer.e_sec_que==secque).first()
                if emp!= None:
                    id=session.get('employer')
                    e = Employer.query.get(id)
                    e.employer_pwd=newpwd
                    db.session.commit()
                    flash('Password successfully updated!')
                    return redirect(url_for('comp_profile'))
                else:
                    flash('Incorrect Credentials')
                    return redirect(url_for('comp_update_pwd'))
            else:
                flash('One or more fields are empty, Please complete the form')
                return redirect(url_for('comp_update_pwd'))
    else:
        return redirect(url_for('comp_form'))


@app.route('/employer/create',methods=['GET','POST'])
def job_details():
    if session.get('employer') !=None:
        if request.method == 'GET':
            return redirect (url_for('comp_form'))
        else:
            title = request.form.get('title')
            subcat = request.form.get('sub')
            exp = request.form.get('exp')
            edu = request.form.get('edu')
            desc = request.form.get('desc')
            role = request.form.get('role')
            respon = request.form.get('responsibilities')
            lg = request.form.get('lgvt')
            duration = request.form.get('duration')
            salary = request.form.get('salary')
            vacancy = request.form.get('vacancy')
            types = request.form.get('type')
            status = request.form.get('status')
            if title !='' and subcat !='' and exp !='' and desc !='' and role !='' and respon !='' and lg !='' and duration !='' and salary !='' and vacancy !='' and types !='' and status !='':
                subs=db.session.query(JobSubcategory).filter(JobSubcategory.job_subcategory==subcat).first()
                local=db.session.query(Lga).filter(Lga.lga_name==lg).first()
                j=Job(job_title=title,job_job_subcategory_id=subs.job_subcategory_id,job_exp_required=exp,job_min_education=edu,job_description=desc,job_role=role,job_responsibilities=respon,job_lga_id=local.lga_id,job_workhours=duration,job_salary=salary,job_vacancy=vacancy,job_type=types,job_status=status,job_employer_id=session.get('employer'))
                db.session.add(j)
                db.session.commit()
                flash("Post Submitted Successfully")
                return redirect(url_for('comp_jobpost'))
            else:
                flash("You cannot submit an empty field,")
                return redirect(url_for('job_details'))
    else:
        return redirect (url_for('comp_form'))





@app.route('/categories/<category>')
def category(category):
    cats = db.session.query(JobSubcategory).filter(JobSubcategory.job_subcategory_job_category_id==category).all()
    categories = '<select name="sub" class="form-control border-dark">'
    for c in cats:
        categories =categories+"<option>"+c.job_subcategory +"</option>"
    categories = categories+ "</select>"
    
    return categories





@app.route('/lga/<stateid>')
def loadlga(stateid):
    #using gets method
    #state_id = request.args.get('state_id')
    lgas = db.session.query(Lga).filter(Lga.lga_stateid==stateid).all()
    data2send = '<select name="lgvt" class="form-select form-select-md mb-1">'
    for s in lgas:
        data2send =data2send+"<option>"+s.lga_name +"</option>"
    data2send = data2send+ "</select>"
    
    return data2send





@app.route('/employer/jobs')
def comp_post():
    if session.get('employer') == None:
        return redirect(url_for('comp_form'))
    else:
        jobdeets = Job.query.all()
        jobcat = JobCategory.query.all()
        jobsubcat = JobSubcategory.query.all()
        state = State.query.all()
        lgas = Lga.query.all()
        return render_template('company/postjob.html',jobdeets=jobdeets,jobcat=jobcat,jobsubcat=jobsubcat,state=state,lgas=lgas)
 




@app.route('/employer/status/<id>')
def change_stats(id):
    if session.get('employer') == None:
        return redirect(url_for('comp_form'))
    else:
        job = Job.query.get(id)
        return render_template('company/change_status.html',job=job)




@app.route('/employer/change/status/<id>',methods=['GET','POST'])
def change_status(id):
    if request.method != "GET":
        if session.get('employer') == None:
            return redirect(url_for('comp_form'))
        else:
            status = request.form.get('status')
            if status != '':
                j = Job.query.get(id)
                j.job_status = status
                db.session.commit()
                return redirect(url_for('comp_jobpost'))
            else:
                flash('An option must be selected before you can proceed')
                return redirect(url_for('/employer/change/status'))
        
    else:
        return redirect(url_for('comp_jobpost'))




@app.errorhandler(404)
def page404(error):
    return render_template("company/404.html",error=error), 404

@app.errorhandler(500)
def internalerror(error):
    return render_template("company/404.html",error=error), 500



@app.route('/employer/profile/uploads/',methods=["POST","GET"])
def comp_pix():
    if session.get('employer') == None:
        return redirect(url_for('comp_form'))
    else:
        return render_template('company/comp_picture.html')



@app.route('/employer/profile/updated/',methods=["POST","GET"])
def comp_picture():
    if session.get('employer') == None:
        return redirect(url_for('comp_form'))
    else:
        if request.method == 'GET':
            return redirect(url_for('comp_pix'))
        else:
            file=request.files['pix']
            files=request.files['pic']
            filename= file.filename
            filenames= files.filename
            allowed = ['.png','.jpg','.jpeg','.JPG','.PNG','.JPEG']
            if filename !='' and filenames !='':
                name,names = os.path.splitext(filenames)
                named,ext = os.path.splitext(filename)
                if ext in allowed and names in allowed:
                    newname= generate_name()+ext
                    newnames= generate_name()+names
                    file.save('lofty_career/static/uploads/'+newname)
                    files.save('lofty_career/static/uploads/'+newnames)
                    empic=db.session.query(Employer).get(session['employer'])
                    empic.e_comp_logo = newnames
                    empic.e_comp_photo = newname
                    db.session.commit()
                    flash("<div class='alert alert-success'>File Uploaded Successfully</div>")
                    return redirect(url_for('comp_profile'))
                else:
                    flash('<div class="alert alert-danger">File type not allowed</div>')
                    return redirect(url_for('comp_picture'))
            else:
                flash("<div class='alert alert-danger'>Please choose a file</div>")
                return redirect(url_for('comp_picture'))





def generate_name():
    filename = random.sample(string.ascii_lowercase,10)
    return ''.join(filename)






@app.route('/employer/logout/')
def comp_logout():
    if session.get('employer')!=None:
        session.pop('employer',None)
    return redirect('/')
