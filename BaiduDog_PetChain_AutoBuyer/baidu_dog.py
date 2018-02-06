#-*- coding:utf-8 -*-

import requests
import threading
import time
import json
import base64
from PIL import Image
#import ocr
requests.packages.urllib3.disable_warnings()
from daili import get_proxys,chose_proxy,del_proxy

class PetChain():
    isAuto = 0
    seed = ''
    captcha = ''
    UA = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3067.6 Safari/537.36'
    Cookie = 'BAIDUID=474CD567FB5D5B93568E7C5E50409876:FG=1; BIDUPSID=474CD567FB5D5B93568E7C5E50409876; PSTM=1492571295; __cfduid=dfdafacd1ecde2bc1627d181240f176221510724973; MCITY=-218%3A; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; FP_UID=3199f3167951c96089d2912e75cd9574; BDUSS=WNFUG1PS2t3aHBIcjQ5bUJSbkVYfkRLb1lZRmxYVjR6Z2RwcU5wb29sU0p6S0JhQVFBQUFBJCQAAAAAAAAAAAEAAAA-j-YUdGVuZ3ppuOe45wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIk~eVqJP3laZ; PSINO=3; H_PS_PSSID=1430_21106_17001_22158'  # 换成你自己的Cookie
    headers = {
        'Cookie': Cookie,
        'Referer': 'https://pet-chain.baidu.com',
        'User-Agent': UA,
        'Origin': 'https://pet-chain.baidu.com',
        'accept': 'application/json',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'content-type': 'application/json'
    }

    def find_pets(self,proxy_dict):
        # post请求找狗
        url='https://pet-chain.baidu.com/data/market/queryPetsOnSale'
        param=json.loads('{"pageNo":1,"pageSize":10,"querySortType":"AMOUNT_ASC","petIds":[],"lastAmount":null,"lastRareDegree":null,"requestId":1517896655264,"appId":1,"tpl":""}')
        param['requestId']  = int(time.time() * 1000)
        r=requests.post(url,data=json.dumps(param),headers=self.headers,verify=False,proxies=proxy_dict)        
        pets = r.json()['data']['petsOnSale']
        print('status_code:',r.status_code,' find dog :',len(pets))      
        for pet in pets:         
            # 筛选目标狗 # amount/价格 rareDegree/稀有程度:4神话 3史诗           
            if float(pet['amount']) <= 2000 : # and int(pet['petId']) <= 30000 :
                #print(pet)
                #self.buy_pet(pet)   
                t = threading.Thread(target=self.buy_pet, args=(pet,))
                t.start() 

    def genCaptcha(self):
        data = {
            "appId": 1,
            "requestId": int(round(time.time() * 1000)),
            "tpl": "",
        }
        page = requests.post("https://pet-chain.baidu.com/data/captcha/gen", headers=self.headers, data=json.dumps(data), timeout=2)
        jPage = page.json()
        if jPage.get(u"errorMsg") == "success":
            self.seed = jPage.get(u"data").get(u"seed")
            img = jPage.get(u"data").get(u"img")
            with open('captcha.jpg', 'wb') as f:
                f.write(base64.b64decode(img))
            return True
        else:
            print('获取验证码失败！')
            return False

    def buy_pet(self,pet):
        # 生成验证码
        self.genCaptcha()
        #img = Image.open("./captcha.jpg")
        captcha = input('请输入验证码：')
        pet_validcode = pet.get(u"validCode")
        data = {"petId": pet['petId'],
            "amount": pet['amount'],
            "seed": self.seed,
            "captcha": captcha,
            "validCode": pet_validcode,
            "requestId": int(round(time.time() * 1000)),
            "appId": 1,
            "tpl": ""
        }
        url = 'https://pet-chain.baidu.com/data/txn/create'
        try:
            r = requests.post(url, data=json.dumps(data),headers=self.headers, verify=False)
            msg = r.json()['errorMsg']
            print('Buy Dog {0} ,msg: {1}'.format(pet["petId"], msg))
        except Exception as err:
            print('buy_pet ',err)


if __name__ == '__main__':
    # 获取IP代理
    proxys_list = get_proxys(1)
    # 选择一个ip
    now_proxy = chose_proxy(proxys_list)
    print("使用代理:", now_proxy)
    
    P = PetChain()
    while True:          
        try:
            P.find_pets(now_proxy)
            time.sleep(1)
        except Exception as err:
            print('main ', err)
            #break
            # 发生异常则更换代理
            del_proxy(proxys_list,now_proxy)
            now_proxy = chose_proxy(proxys_list)
            print("使用代理:", now_proxy)
            
