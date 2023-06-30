from datetime import datetime
from lofty_career import db

class Admin(db.Model):
    admin_id= db.Column(db.Integer, autoincrement=True,primary_key=True)
    admin_fname = db.Column(db.String(45),nullable=False)
    admin_lname = db.Column(db.String(45),nullable=False)
    admin_phoneno = db.Column(db.Integer,nullable=True)
    admin_email= db.Column(db.String(155)) 
    admin_pwd=db.Column(db.String(155),nullable=False)

class State(db.Model):
    state_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    state_name = db.Column(db.String(45),nullable=False) 
    #Foreign keys
    slga = db.relationship('Lga',back_populates='state_deets')

class Lga(db.Model):
    lga_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    lga_stateid = db.Column(db.Integer, db.ForeignKey('state.state_id'),nullable=False) 
    lga_name = db.Column(db.String(45),nullable=False)
    #Foreign keys
    state_deets = db.relationship('State',back_populates='slga')
    lgauserid = db.relationship('User',back_populates='userlga')
    lgajob = db.relationship('Job',back_populates='joblga')
    lga_jobapp= db.relationship('JobApplication',back_populates='job_lga')

class Dislike(db.Model):
    dislike_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    dislike_job_id = db.Column(db.Integer, db.ForeignKey('job.job_id'),nullable=False)
    dislike_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False) 
    #Foreign keys
    dislikeby = db.relationship('User',back_populates='mydislike')
    disliketo = db.relationship('Job',back_populates='jobdislike')

class User(db.Model):
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True) 
    user_fname = db.Column(db.String(45),nullable=False) 
    user_lname = db.Column(db.String(45),nullable=False) 
    user_username = db.Column(db.String(45),nullable=False)
    user_email = db.Column(db.String(150),nullable=False) 
    user_pwd=db.Column(db.String(120),nullable=False)  
    user_education = db.Column(db.String(100),nullable=True) 
    user_experience = db.Column(db.String(255),nullable=True) 
    user_pastwork = db.Column(db.String(255),nullable=True) 
    user_photo = db.Column(db.String(255),nullable=True) 
    user_resume = db.Column(db.String(255),nullable=True) 
    user_phoneno = db.Column(db.String(20),nullable=False) 
    user_address = db.Column(db.String(255),nullable=False) 
    user_gender = db.Column(db.String(45),nullable=False)  
    user_sec_que = db.Column(db.String(45),nullable=False)  
    user_sec_ans = db.Column(db.String(45),nullable=False)  
    user_lga_id = db.Column(db.Integer, db.ForeignKey('lga.lga_id'),nullable=False) 
    #Foreign keys
    userlga = db.relationship('Lga',back_populates='lgauserid')
    mydislike = db.relationship('Dislike',back_populates='dislikeby')
    user_jobapp = db.relationship('JobApplication',back_populates='jobapp_user')
    viewuser = db.relationship('JobView',back_populates='userview')
    viewlike = db.relationship('Like',back_populates='userlike')
    skillacq = db.relationship('Skill',back_populates='userskill')
    monitored = db.relationship('Watchlist',back_populates='userwatchlist')

class Employer(db.Model):
    employer_id = db.Column(db.Integer, autoincrement=True, primary_key=True) 
    employer_fname = db.Column(db.String(45),nullable=False) 
    employer_lname = db.Column(db.String(45),nullable=False) 
    employer_username = db.Column(db.String(45),nullable=False)
    employer_email = db.Column(db.String(150),nullable=False)
    employer_pwd = db.Column(db.String(155),nullable=False)  
    e_company_name = db.Column(db.String(150),nullable=False) 
    e_comp_address = db.Column(db.String(150),nullable=False) 
    e_comp_phoneno = db.Column(db.String(20),nullable=False) 
    e_comp_website = db.Column(db.Text(),nullable=True) 
    e_comp_photo = db.Column(db.String(255),nullable=True) 
    e_comp_logo = db.Column(db.String(255),nullable=True)  
    e_sec_que = db.Column(db.String(45),nullable=False)  
    e_sec_ans = db.Column(db.String(45),nullable=False) 
    #Foreign Keys
    jobemployer = db.relationship('Job',back_populates='employerjob')
    jappemp = db.relationship('JobApplication',back_populates='empjapp')

class Job(db.Model):
    job_id = db.Column(db.Integer, autoincrement=True, primary_key=True) 
    job_employer_id = db.Column(db.Integer, db.ForeignKey('employer.employer_id'),nullable=False)
    job_job_subcategory_id = db.Column(db.Integer, db.ForeignKey('job_subcategory.job_subcategory_id'),nullable=False)
    job_title = db.Column(db.String(155),nullable=False) 
    job_exp_required = db.Column(db.String(255),nullable=False)
    job_min_education = db.Column(db.String(150),nullable=False)  
    job_description = db.Column(db.String(255),nullable=False) 
    job_role = db.Column(db.String(150),nullable=False) 
    job_responsibilities = db.Column(db.String(255),nullable=False) 
    job_lga_id = db.Column(db.Integer, db.ForeignKey('lga.lga_id'),nullable=False) 
    job_workhours = db.Column(db.String(45),nullable=False) 
    job_salary = db.Column(db.String(45),nullable=False) 
    job_vacancy = db.Column(db.String(45),nullable=False) 
    job_type = db.Column(db.String(45),nullable=False) 
    job_postdate = db.Column(db.DateTime(), default=datetime.utcnow) 
    job_status = db.Column(db.String(45),nullable=False)
    #Foreign Keys
    employerjob = db.relationship('Employer',back_populates='jobemployer')
    jobsub = db.relationship('JobSubcategory',back_populates='subcat')
    jobdislike = db.relationship('Dislike',back_populates='disliketo')
    jobapplied = db.relationship('JobApplication',back_populates='appliedjob')
    joblike = db.relationship('Like',back_populates='likedjob')
    linkedjob = db.relationship('Watchlist',back_populates='jobwatched')
    joblga = db.relationship('Lga',back_populates='lgajob')
    
class JobApplication(db.Model):
    job_application_id = db.Column(db.Integer, autoincrement=True, primary_key=True) 
    j_app_status = db.Column(db.String(45),nullable=False)
    j_app_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False) 
    j_app_employer_id = db.Column(db.Integer, db.ForeignKey('employer.employer_id'),nullable=False)
    j_app_lga_id = db.Column(db.Integer, db.ForeignKey('lga.lga_id'),nullable=False) 
    j_app_job_id = db.Column(db.Integer, db.ForeignKey('job.job_id'),nullable=False) 
    j_app_feedback = db.Column(db.String(255),nullable=True) 
    j_app_date_applied = db.Column(db.DateTime(), default=datetime.utcnow)
    #Foreign Keys
    jobapp_user = db.relationship('User',back_populates='user_jobapp')
    job_lga = db.relationship('Lga',back_populates='lga_jobapp')
    appliedjob = db.relationship('Job',back_populates='jobapplied')
    empjapp = db.relationship('Employer',back_populates='jappemp')
class JobCategory(db.Model):
    job_category_id = db.Column(db.Integer, autoincrement=True, primary_key=True) 
    job_category = db.Column(db.String(45),nullable=False) 
    #Foreign Keys
    jobcategory = db.relationship('JobSubcategory',back_populates='jobsubcategory')

class JobSubcategory(db.Model):
    job_subcategory_id = db.Column(db.Integer, autoincrement=True, primary_key=True) 
    job_subcategory = db.Column(db.String(45),nullable=False)
    job_subcategory_job_category_id = db.Column(db.Integer, db.ForeignKey('job_category.job_category_id'),nullable=False)
    #Foreign Keys
    jobsubcategory = db.relationship('JobCategory',back_populates='jobcategory')
    subcat = db.relationship('Job',back_populates='jobsub')

class JobView(db.Model):
    job_view_id = db.Column(db.Integer, autoincrement=True, primary_key=True) 
    Job_view_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False)  
    #Foreign Keys
    userview = db.relationship('User',back_populates='viewuser')

class Like(db.Model):
    like_id = db.Column(db.Integer, autoincrement=True, primary_key=True) 
    like_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False) 
    like_job_id = db.Column(db.Integer, db.ForeignKey('job.job_id'),nullable=False) 
    #Foreign Keys
    userlike = db.relationship('User',back_populates='viewlike')
    likedjob = db.relationship('Job',back_populates='joblike')

class Skill(db.Model):
    skill_id = db.Column(db.Integer, autoincrement=True, primary_key=True) 
    skill_name = db.Column(db.String(155),nullable=True)
    skill_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False) 
    #Foreign Keys
    userskill = db.relationship('User',back_populates='skillacq')

class Watchlist(db.Model):
    watchlist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    wl_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False)
    wl_job_id = db.Column(db.Integer, db.ForeignKey('job.job_id'),nullable=False) 
    #Foreign Keys
    userwatchlist = db.relationship('User',back_populates='monitored')
    jobwatched = db.relationship('Job',back_populates='linkedjob')