# coding: utf-8

from flask import request  , Blueprint , redirect , url_for , render_template , flash , json
from leancloud import Object , Query , LeanCloudError
import leancloud
from . import apiIndex_views
from views.Models import IconFont , XMI_Theme

@apiIndex_views.route('/indexs/getIconFontList', methods=['GET'])
def iconFontList():
    try:
        iconFonts = Query(IconFont).add_descending('createdAt').find()
    except LeanCloudError as e:
        flash(e.error)

    list = []
    for icon in iconFonts:
        dic = icon.get('themeValue')
        dic['name'] = icon.get('key')
        dic['objectId'] = icon.get('objectId')
        dic['description'] = icon.get('description')
        dic['size'] = icon.get('size')
        dic['icon'] = icon.get('icon')
        list.append(dic)

    t = {}
    t['data'] = list
    return json.dumps(t , ensure_ascii = False)

#拉取主题列表
@apiIndex_views.route('/indexs/getThemes' , methods=['GET'])
def xmi_themeList():
    try:
        themes = Query(XMI_Theme).add_descending('createdAt').find()
    except LeanCloudError as e:
        flash(e.error)

    list = []
    for theme in themes:
        list.append(theme.get('theme'))

    t = {}
    t['data'] = list
    return json.dumps(t , ensure_ascii = False)

#MARK:TODO 新增方法未确定
@apiIndex_views.route('/indexs/addNewTheme' , methods = ['POST' , 'GET'])
def xmi_createTheme():
    # theme = XMI_Theme()
    # theme.set('theme' , 'dark')
    # theme.save()
    return "OK"

@apiIndex_views.route('/indexs/addNewIconFont' , methods = ['POST' , 'GET'])
def xmi_newIconFont():
    # icon = IconFont()
    # icon.set('key','test2')
    # icon.set('themeValue' , {'dark' : '#000001' , 'white' : '#FFFFF1'})
    # icon.save()
    t = {}
    t['data'] = "ok"
    return json.dumps(t, ensure_ascii=False)

@apiIndex_views.route('/indexs/editIconFont' , methods = ['POST' , 'GET'])
def xmi_editIconFont():
    data = request.args.to_dict()

    print(data)

    key = 'objectId'
    try:
        objId = data[key]
        data.pop(key)
        icon = IconFont.create_without_data(objId)
    except:
        icon = IconFont()

    name = data['name']
    icon.set('key' , name)
    data.pop('name')

    description = data['description']
    icon.set('description' , description)
    data.pop('description')

    size = data['size']
    icon.set('size' , size)
    data.pop('size')

    iconName = data['icon']
    icon.set('icon' , iconName)
    data.pop('icon')

    icon.set('themeValue' , data)
    icon.save()

    t = {}
    t['data'] = "ok"
    return json.dumps(t, ensure_ascii=False)

@apiIndex_views.route('/indexs/removeIconFont' , methods = ['POST' , 'GET'])
def xmi_removeIconFont():
    data = request.args.to_dict()

    try:
        objId = data['objectId']
        icon = IconFont.create_without_data(objId)
        icon.destroy()
    except:
        print("remove error")

    t = {}
    t['data'] = "ok"
    return json.dumps(t, ensure_ascii=False)

@apiIndex_views.route('/indexs/searchIconFont' , methods = ['POST' , 'GET'])
def xmi_searchIconFont():
    data = request.args.to_dict()
    print(data['key'])
    try:
        query = leancloud.Object.extend('IconFont').query
        iconFonts = query.contains('key' , data['key']).add_descending('createdAt').find()

    except LeanCloudError as e:
        flash(e.error)

    list = []
    for icon in iconFonts:
        dic = icon.get('themeValue')
        dic['name'] = icon.get('key')
        dic['objectId'] = icon.get('objectId')
        dic['description'] = icon.get('description')
        dic['size'] = icon.get('size')
        dic['icon'] = icon.get('icon')
        list.append(dic)

    t = {}
    t['data'] = list
    return json.dumps(t , ensure_ascii = False)

@apiIndex_views.route('/indexs/getAllIconFonts' , methods = ['POST' , 'GET'])
def xmi_getAllIconFonts():
    data = request.args.to_dict()
    try:
        iconFonts = Query(IconFont).add_descending('createdAt').find()
    except LeanCloudError as e:
        flash(e.error)

    dic = {}
    for icon in iconFonts:
        # dic = icon.get('themeValue')

        aDic = icon.get('themeValue')
        try:
            dic[icon.get('key')] = aDic[data['theme']]
            list.append(dic)
        except:
            print("error")


    t = {}
    t['IconFont'] = dic
    return json.dumps(t, ensure_ascii=False)