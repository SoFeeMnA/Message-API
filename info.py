import requests
from bs4 import BeautifulSoup
import re

def getAll():
    url = "https://th.investing.com/currencies/xau-usd"
    res = requests.get(url)

    soup = BeautifulSoup(res.text, "html.parser")
    table_body = soup.find("tbody", class_=re.compile(r"^datatable-v2_body"))

    if table_body:
        # ถ้าหาเจอแล้ว ให้หา <tr> ทั้งหมด
        find_tr = table_body.find_all("tr")
        assr = []
        count = []
        for i in find_tr:
            find_td = i.find_all("td")
            Cut = []
            for td in find_td:
                Cut.append(td.text.strip())
            
            # print(len(Cut))
            if len(Cut) == 1:
                assr.append(Cut[0])
                count.append(1)
            else:
                assr.append(Cut[3])
                count.append(0)
        # -------------หัวข้อหลัก-------------
        box1 = []
        for i in find_tr:
            num = i.find("div",class_="max-w-[240px] overflow-hidden overflow-x-clip whitespace-break-spaces sm:max-w-[410px]",)
            if num != None:
                num = i.find("div",class_="max-w-[240px] overflow-hidden overflow-x-clip whitespace-break-spaces sm:max-w-[410px]",).text
                box1.append(num)
                
        #-------------ระดับ-------------
        box2 = []
        for i in find_tr:
            num = i.find("div",class_="flex !flex-row text-secondary *:w-4")
            html_string = str(num)
            html_cut = html_string.count("opacity-60")
            if html_cut != 0 :
                box2.append(html_cut)
        
        # print("ระดับ   เนื้อหา")
        # for i in range(len(box1)):
        #     print(f"{box2[i]}   {box1[i]} ")
        final_output = ["--- ข้อมูลตัวชี้วัดเศรษฐกิจล่าสุด ---"]
        test = []
        for i in range((len(box1))):
            test.append(f"[ระดับ {box2[i]}] {box1[i]}")    
            
            
        for i in range(len(test)):
            if count[i] == 1:
                test.insert(i, f"\n{assr[i]}\n")   
        return "\n".join(test)    


    
    
    
    

        
        
        
  