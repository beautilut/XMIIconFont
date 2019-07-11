# coding: utf-8

from flask import Blueprint , request , redirect , url_for , render_template , flash , json
from leancloud import Object , Query , LeanCloudError
import leancloud

class XMI_Theme(Object):
    pass

class IconFont(Object):
    pass

index_views = Blueprint('indexs' , __name__)

# 首页
@index_views.route('')
@index_views.route('/index')
def show():
    return render_template('index.html')

#develop tools
@index_views.route("/developTools")
def developToos():
    pass