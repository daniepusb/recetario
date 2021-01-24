"""
Python daily task to delete sandbox
"""
import requests
try:
    requests.get('https://danielpedroza.pythonanywhere.com/api/sandboxReset',data=None)
    #return {'message': 'Done'},200
except expression as identifier:
    pass
    #return {'message': 'Error: '+ expression},500

