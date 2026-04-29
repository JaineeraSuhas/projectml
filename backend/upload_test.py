import requests

url = 'http://127.0.0.1:8000/upload'
files = {'file': ('test_sample.csv', open('test_sample.csv', 'rb'), 'text/csv')}
try:
    r = requests.post(url, files=files, timeout=30)
    print('status_code:', r.status_code)
    print('response:', r.text[:2000])
except Exception as e:
    print('error', e)
