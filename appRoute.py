#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import app
import string , json

@app.route('/getList')
def getIconFontList():
    