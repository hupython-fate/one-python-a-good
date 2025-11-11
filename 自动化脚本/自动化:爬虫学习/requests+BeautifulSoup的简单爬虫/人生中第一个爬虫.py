import requests

def ren_shen_di_yi_ci():
    head={'User-Agent':'Mozilla/5.0(Windows NT 10.0; Win64; x64)'}
    response=requests.get('https://www.gushicimingju.com/shiren/libai/')
    print(response)
    print(response.status_code)#即http状态码，如果状态码等于200，说明请求成功。
#如果状态码是404，得检查一下传入的url是否正确。
    if response.ok:
        print('ok')
        print(response.text)
ren_shen_di_yi_ci()