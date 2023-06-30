from flask import render_template,redirect,flash,session,request,url_for
from werkzeug.security import generate_password_hash,check_password_hash
from lofty_career import app,db
from lofty_career.models import Admin,Job,Employer,User,JobApplication


@app.route('/admin/home')
def admin_home():
    if session.get('admin') != None:
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('admin_form'))


@app.route('/admin/form')
def admin_form():
    return render_template('admin/adminform.html')




@app.route('/admin/login/',methods=['POST','GET'])
def admin_login():
    if request.method =='GET':
        return redirect(url_for('admin_form'))
    else:
        email=request.form.get('email')
        pwd=request.form.get('pwd')
        deets=db.session.query(Admin).filter(Admin.admin_email==email).first()
        if deets != None:
            pwd_indb= deets.admin_pwd
            chk=check_password_hash(pwd_indb,pwd)
            if chk == True:
                id= deets.admin_id
                session['admin']=id
                return redirect (url_for('admin_dashboard'))
            else:
                flash("Email or Password is not correct")
                return redirect(url_for('admin_login'))
        else:
            flash("Invalid Credentials")
            return redirect(url_for('admin_login'))


@app.route('/admin/dashboard/')
def admin_dashboard():
    if session.get('admin') != None:
        job =Job.query.all()
        emp =Employer.query.all()
        user = User.query.all()
        id=session.get('admin')
        admin_deet = Admin.query.get(id)
        return render_template('admin/index.html',job=job,admin_deet=admin_deet,emp=emp,user=user)
    else:
        return redirect(url_for('admin_form'))


@app.route('/admin/profile')
def admin_profile():
    if session.get('admin') != None:
        id=session.get('admin')
        admin_deets = Admin.query.get(id)
        return render_template('admin/adminprofile.html',admin_deets=admin_deets)
    else:
        return redirect(url_for('admin_form'))


@app.route('/admin/job/delete/<id>')
def delete_job(id):
    if session.get('admin') == None:
        return redirect(url_for('admin_login'))
    else:
        jobobj = Job.query.get_or_404(id)
        db.session.delete(jobobj)
        db.session.commit()
        flash("Successfully Deleted!")
        return redirect(url_for('admin_dashboard'))




@app.route('/admin/job/description/<id>')
def admin_jobdesc(id):
    if session.get('admin') != None:
        job =Job.query.get_or_404(id)
        return render_template('admin/admin_jobdesc.html',job=job)
    else:
        return redirect(url_for('admin_form'))




@app.route('/admin/applicant/details/<id>')
def admin_applicant_info(id):
    if session.get('admin') != None:
        user = db.session.query(User).filter(User.user_id==id).all()
        return render_template("admin/admin_applicant_info.html",user=user)
    else:
        return redirect(url_for('admin_form'))
        





@app.route('/admin/company/info/<id>')
def admin_company_info(id):
    if session.get('admin') != None:
        job = db.session.query(Job).filter(Job.job_employer_id==id).first()
        jobs = db.session.query(Job).filter(Job.job_employer_id==id).all()
        return render_template('admin/admin_company_info.html',job=job,jobs=jobs) 
    else:
        return redirect(url_for('admin_form'))





@app.errorhandler(404)
def page404(error):
    return render_template('admin/error404.html',error=error), 404


@app.errorhandler(500)
def internalerror(error):
    return render_template('admin/error404.html',error=error), 500



@app.route('/admin/logout/')
def admin_logout():
    if session.get('admin') != None:
        session.pop('admin',None)
    return redirect(url_for('admin_form'))
