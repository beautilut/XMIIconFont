# coding: utf-8
import os
from . import apiIndex_views
from flask import request , redirect , url_for , render_template , flash ,json
import leancloud

from views.Models import XMI_Theme , XMI_Theme_Identifier



def dict_generator(indict, pre=None):
    pre = pre[:] if pre else []
    if isinstance(indict, dict):
        for key, value in indict.items():
            if isinstance(value, dict):
                if len(value) == 0:
                    yield pre+[key, '{}']
                else:
                    for d in dict_generator(value, pre + [key]):
                        yield d
            elif isinstance(value, list):
                if len(value) == 0:
                    yield pre+[key, '[]']
                else:
                    for index , v in enumerate(value):
                        for d in dict_generator(v, pre + [str(index)]  + [key]):
                            yield d
            elif isinstance(value, tuple):
                if len(value) == 0:
                    yield pre+[key, '()']
                else:
                    for v in value:
                        for d in dict_generator(v, pre + [key]):
                            yield d
            else:
                yield pre + [key, value]
    else:
        yield pre+[indict]


@apiIndex_views.route('/upload' , methods = ['GET' , 'POST'])
def uploadThemeFile():
    if request.method == 'POST':
        orignalFile = request.files.get('file')
        file = str(orignalFile.read(),encoding='UTF-8');

        theme = XMI_Theme()
        if 'dark' in orignalFile.filename:
            theme = XMI_Theme.create_without_data('5cbd6688c8959c00751e248c')
        elif 'white' in orignalFile.filename:
            theme = XMI_Theme.create_without_data('5cbd6693a673f50068fed4fe')
        theme.fetch()


        sValue = json.loads(file)
        for i in dict_generator(sValue):
            key = '.'.join(i[0:-1])
            value = i[-1]

            try:
                obj = leancloud.Object.extend('XMI_Theme_Identifier').query.contains('key' , key).first()
                item = XMI_Theme_Identifier.create_without_data(obj.id)
                item.set(theme.get('theme'), value)
                item.save()
            except:
                pass
                identifier = XMI_Theme_Identifier()
                identifier.set('key' , key)
                identifier.set(theme.get('theme') , value)
                identifier.save()


    return "hello"

@apiIndex_views.route('/themeIdentifer/searchWithKey' , methods = ['GET'])
def getThemeIdentifierList():
    data = request.args.to_dict()

    if any(data) is False :
        data = {}
        data['key'] = ''
    try:
        dic = json.loads(data['key'])

        query = leancloud.Object.extend('XMI_Theme_Identifier').query

        for key in dic.keys():
            query = query.matched(key , dic[key] , ignore_case=True)

        list = query.find()

        newlist = []
        for item in list:
            dic = {}
            for key , value in item._attributes.items():
                dic[key] = value

            newlist.append(dic)

        t = {}
        t['data'] = newlist
        return json.dumps(t, ensure_ascii=False)

    except:
        return 'error'

@apiIndex_views.route('/getIconfontCSS' , methods = ['GET'])
def getIconfontCssPath():
    return os.environ.get('outLinkPath')