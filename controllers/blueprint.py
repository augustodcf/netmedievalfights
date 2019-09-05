
#from flask import flask, Blueprint, render_template, redirect, url_for, flash
#from flask_login import current_user, login_required


#control_blueprint = Blueprint('control', __name__)

#userControlPages = [ '/managepages' ]

#configure Login manager
#    @login_manager.user_loader
#    def load_user(id):
#        try:
#            return (User.get(id))
#        except:
#          return

#    login_manager.anonymous_user = Anonymous

#    @login_manager.unauthorized_handler
#    def unauthorized():
#        return redirect(url_for('frontend.unauthorized'))#, 401

