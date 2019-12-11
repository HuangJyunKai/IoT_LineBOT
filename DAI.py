import time, random, requests
import DAN


def weather():
    import requests
    from io import open
    from bs4 import BeautifulSoup
    
    
    #region = 'BaoShan'
    region = 'Tainan'
    #url = 'https://www.cwb.gov.tw/V7/observe/24real/Data/C0D58.htm'
    url = 'https://www.cwb.gov.tw/V7/observe/24real/Data/46741.htm'
    
    
    def f(url, fn):
    	headers = {
         'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    	}
    	res = requests.get(url, headers=headers)
    	res.encoding = 'utf-8'
    
    	open(fn,'wb').write(res.text.encode('utf-8'))
    
    fn = region+ '.html'.format(0,0)
    f(url, fn)
    
    def get_element(soup, tag, class_name):
        data = []
        table = soup.find(tag, attrs={'class':class_name})
        rows = table.find_all('tr')
        del rows[0]
        
        for row in rows:
            first_col = row.find_all('th')
            cols = row.find_all('td')
            cols.insert(0, first_col[0])
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele]) 
        return data
    
    region ='Tainan'
       
    file_name = region+".html"
    
    f = open (file_name,'r', encoding='utf-8')
    s = f.readlines()
    s = ''.join(s)
    
    soup = BeautifulSoup(s, "lxml")
    
    df_tmp = get_element(soup, 'table','BoxTable')
    
    #print(df_tmp)
    #print(df_tmp[0])
    Temperature = df_tmp[0][1]
    WindDirection = df_tmp[0][4]
    WindPower = df_tmp[0][5]
    Gust = df_tmp[0][6]
    Humidity = df_tmp[0][8]
    Rainfall = df_tmp[0][9]
    
    lst=[]
    lst.append(Temperature)
    lst.append(WindDirection)
    lst.append(WindPower)
    lst.append(Gust)
    lst.append(Humidity)
    lst.append(Rainfall)
    #print(Temperature,WindDirection,WindPower,Gust,Humidity,Rainfall)
    return lst
def RunDevice():
    ServerURL = 'https://6.iottalk.tw' #with SSL connection
    Reg_addr = 'qwgigfiwffuyhihihrjdn' #if None, Reg_addr = MAC address

    DAN.profile['dm_name']='W0858605_1'
    DAN.profile['df_list']=['AtPressure','Humidity','Windspeed','presentwind','rain','winddirection', 'Temperature-O',
           'WindDirection-O','WindSpeed-O','presentwind-O','Humidity-O','RainFall-O']
#DAN.profile['d_name']= 'Assign a Device Name' 

    DAN.device_registration_with_retry(ServerURL, Reg_addr)
#weather=weather()
#print(weather)
#DAN.deregister()  #if you want to deregister this device, uncomment this line
#exit()            #if you want to deregister this device, uncomment this line
    only=0
    while True:
        try:
            ww=weather()
            print(ww)
        #IDF_data = random.uniform(1, 10)
        #IDF_data = weather
            DAN.push ('AtPressure', ww[0]) #Push data to an input device feature "Dummy_Sensor" #Temperature
            DAN.push ('Humidity', ww[4]) #humidity
            DAN.push ('Windspeed', ww[2][:3]) #風力
            DAN.push ('presentwind', ww[3][:3]) #陣風
            DAN.push ('rain', ww[5])
            DAN.push ('winddirection', ww[1])
            #DAN.push ('MSG-I',ww[0])

        #==================================

        #ODF_data = DAN.pull('Dummy_control')#Pull data from an output device feature "Dummy_Control"
            '''
            Temperature=DAN.pull('Temperature-O')
            WindDirection=DAN.pull('WindDirection-O')
            WindPower=DAN.pull('WindSpeed-O')
            Gust=DAN.pull('presentwind-O')
            Humidity=DAN.pull('Humidity-O')
            Rainfall=DAN.pull('RainFall-O')
            Line_Temp=DAN.pull('MSG-O')
            '''
            #print(Line_Temp)
            #print(Temperature,WindDirection,WindPower,Gust,Humidity,Rainfall)
        #time.sleep(5)
    
        #if ODF_data != None and only!=  ODF_data[0]:
        #    print (ODF_data[0]) ##一維度
        #    only = ODF_data[0]
        except Exception as e:
            print(e)
            if str(e).find('mac_addr not found:') != -1:
                print('Reg_addr is not found. Try to re-register...')
                DAN.device_registration_with_retry(ServerURL, Reg_addr)
            else:
                print('Connection failed due to unknow reasons.')
                time.sleep(1)    
        time.sleep(5)

#ServerURL = 'http://IP:9999'      #with non-secure connection

if __name__ == "__main__":
    RunDevice()