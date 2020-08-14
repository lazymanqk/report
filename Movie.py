import numpy as np
import pandas as pd
from os import walk
from os.path import join
import matplotlib.pyplot as plt
import re

font = {"family" : "Microsoft JhengHei","weight" : "bold","size"  : "16"}
plt.rc("font", **font) 
plt.rc("axes",unicode_minus=False) 


def getCSV():   #建立自定義函式，下載目標所有CSV檔
    import requests
    from bs4 import BeautifulSoup
    import re
    html = requests.get("https://data.gov.tw/dataset/94224")    #取得網頁文本
    bsobj = BeautifulSoup(html.content, "lxml")     #建立樹狀元素物件

    #定位下載頁面的div，用回圈下載每一個CSV並命名
    for single_div in bsobj\
            .find("div", {"class": "field field-name-field-dataset-resource field-type-dgresource-resouce field-label-inline clearfix"})\
            .find("div", {"class", "field-items"})\
            .findAll("a", string="CSV"):

        href = single_div.get("href")   #取得下載連結
        currency_name = single_div.parent.find("span", {"class", "ff-desc"}).text   #取得標籤名稱做為要下載的檔名
        currency_name = re.sub("[全國電影票房.]", "", currency_name)

        file_name = r"C:\Users\ASUS\Desktop\27\downcav\m" + currency_name + ".csv"
        r = requests.get(href)
        with open(file_name, "wb") as code:
            code.write(r.content)

# getCSV()


def csvSolve(df):   #建立自定義函式，處理欄位名稱與value的轉數值
    #捨棄不要的欄位
    dropColumns = ["序號", "申請人", "發行","累計銷售金額", "累計銷售票數", "上映日數", "累計票數", "累計金額"]
    dropMask = df.columns.isin(dropColumns)
    df = df.drop(df.columns[dropMask], axis=1)

    #把欄位名稱「周票數變動率」、「週票數變動率」統一為變動率，並對原數據無該欄位的df做新增欄位
    reColMask = [col for col in df.columns if "變動" in col]
    try:
        reCol = reColMask[0]
        df = df.rename(columns={reCol: "變動率"})
    except:
        df["變動率"] = "0"

    #將value轉態，字串轉數值
    df.loc[:,"銷售票數"] = df.loc[:,"銷售票數"].apply(lambda x: "".join([i for i in x if i.isdigit()])).astype(int)
    df.loc[:,"變動率"] = df.loc[:, "變動率"].str.replace("%","").str.replace(",","").astype(float).apply(lambda x: x/100)
    df.loc[:,"銷售金額"] = df.loc[:,"銷售金額"].apply(lambda x: "".join([i for i in x if i.isdigit()])).astype(int)

    #重新排序欄位
    df = df[["國別地區","中文片名","上映日期","出品","變動率","上映院數","銷售票數","銷售金額"]]
    return df

dfChange = pd.DataFrame(columns=["國別地區","中文片名"])# 每週變動率
dfAcnt = pd.DataFrame(columns=["國別地區","中文片名"])# 每週上映院數
dfTicket = pd.DataFrame(columns=["國別地區","中文片名"])# 每週銷售票數
dfMoney = pd.DataFrame(columns=["國別地區","中文片名"])# 每週銷售金額


mypath = r"C:\Users\ASUS\Desktop\27\downcav"  # 絕對路徑
for root, dirs, files in walk(mypath):  # 從目標路徑的資料夾中找出每一個根目錄root、資料夾dirs、檔案files
    for f in files:  # 用迴圈讀取每一個檔案
        
        fullpath = join(root, f)
        # fullpath= 資料夾根目錄root+檔案名稱f
             # 將f檔案名稱，去除部分字元，並將日期各位數部分補0。
        name = re.sub("[至m.csv]","",f)
        name = re.split(r"[年月日]",name)[0:3]
        dfName = ""  
        for i in name:
            if len(i) < 2:
                i = "0"+i
            dfName += i


        globals()["df"+dfName ] = pd.read_csv(fullpath)
        globals()["df"+dfName ] = csvSolve(globals()["df"+ dfName])
        
        dfChange = pd.merge(dfChange,globals()["df"+dfName].iloc[:,[0,1,4]],on=["國別地區","中文片名"],how = "outer")
        dfAcnt = pd.merge(dfAcnt,globals()["df"+dfName].iloc[:,[0,1,5]],on=["國別地區","中文片名"],how = "outer")
        dfTicket = pd.merge(dfTicket,globals()["df"+dfName].iloc[:,[0,1,6]],on=["國別地區","中文片名"],how = "outer")
        dfMoney = pd.merge(dfMoney,globals()["df"+dfName].iloc[:,[0,1,7]],on=["國別地區","中文片名"],how = "outer")
        


# 每週變動率
dfChange.columns= ["國別地區","中文片名",
                  "12月30日","1月06日","1月13日","1月20日","1月27日",
                  "2月03日","2月10日","2月17日","2月24日",
                  "3月02日","3月09日","3月16日","3月23日","3月30日",
                  "4月06日","4月13日","4月20日","4月27日",
                  "5月04日","5月11日","5月18日","5月25日",
                  "6月01日","6月08日","6月15日","6月22日","6月29日",
                  "7月06日","7月13日"]
# 每週上映院數
dfAcnt.columns= ["國別地區","中文片名",
                  "12月30日","1月06日","1月13日","1月20日","1月27日",
                  "2月03日","2月10日","2月17日","2月24日",
                  "3月02日","3月09日","3月16日","3月23日","3月30日",
                  "4月06日","4月13日","4月20日","4月27日",
                  "5月04日","5月11日","5月18日","5月25日",
                  "6月01日","6月08日","6月15日","6月22日","6月29日",
                  "7月06日","7月13日"]
# 每週銷售票數
dfTicket.columns= ["國別地區","中文片名",
                  "12月30日","1月06日","1月13日","1月20日","1月27日",
                  "2月03日","2月10日","2月17日","2月24日",
                  "3月02日","3月09日","3月16日","3月23日","3月30日",
                  "4月06日","4月13日","4月20日","4月27日",
                  "5月04日","5月11日","5月18日","5月25日",
                  "6月01日","6月08日","6月15日","6月22日","6月29日",
                  "7月06日","7月13日"]

# 每週銷售金額
dfMoney.columns= ["國別地區","中文片名",
                  "12月30日","1月06日","1月13日","1月20日","1月27日",
                  "2月03日","2月10日","2月17日","2月24日",
                  "3月02日","3月09日","3月16日","3月23日","3月30日",
                  "4月06日","4月13日","4月20日","4月27日",
                  "5月04日","5月11日","5月18日","5月25日",
                  "6月01日","6月08日","6月15日","6月22日","6月29日",
                  "7月06日","7月13日"]





MovieCsvs = [
             df20191230,
             df20200106,
             df20200113,
             df20200120,
             df20200127,
             
             df20200203,
             df20200210,
             df20200217,
             df20200224,
             
             df20200302,
             df20200309,
             df20200316,
             df20200323,
             df20200330,
             
             df20200406,
             df20200413,
             df20200420,
             df20200427,
             
             df20200504,
             df20200511,
             df20200518,
             df20200525,
             
             df20200601,
             df20200608,
             df20200615,
             df20200622,
             df20200629,
             
             df20200706,
             df20200713]






#=================================================================

# 2020各國銷售金額 圓餅圖

MovieCsvsMerge = pd.concat(MovieCsvs)
#csv合併
GgroupNation = MovieCsvsMerge.groupby(["國別地區"])
NationErea = GgroupNation.sum().sort_values("銷售金額",ascending=False).reset_index()
# reset_index() ;groupby("國別地區")，國別地區變成索引值，把國別地區從索引值釋放
# 把國別地區groupby，銷售金額做總合後，排序最高在第一位
NationErea.loc["40"] = NationErea.iloc[5:,1:].sum()
# 最底下新增一列從各國Top5以下國家的的總合為「40」列
NationErea.iloc[40,0]="其它"
NationEreaTop5 = NationErea.iloc[[0,1,2,3,4,40],:]


# 2020各國銷售金額累計比例 圓餅圖
plt.figure(dpi=150)
plt.pie(
        NationEreaTop5.iloc[:,4],
        labels=NationEreaTop5["國別地區"], 
        autopct="%1.1f%%",
        explode=(0.05,0,0,0,0,0),
        labeldistance=1.05,
        pctdistance=0.7,
        textprops={"fontsize":15},  #設定字體大小
        startangle=45,              #x軸字體傾斜45度
        shadow=True,)               #圓餅圖增加陰影效果
plt.xlabel("各國銷售金額累計比例",fontsize="20",
          fontweight="bold", color="r")
plt.axis("equal") 
plt.show()
plt.close()


# 2020各國銷售票數累計比例 圓餅圖
plt.figure(dpi=150)
plt.pie(
        NationEreaTop5.iloc[:,3],
        labels=NationEreaTop5["國別地區"], 
        autopct="%1.1f%%",
        explode=(0.05,0,0,0,0,0),
        labeldistance=1.05,
        pctdistance=0.7,
        textprops={"fontsize":15},
        startangle=45,
        shadow=True,)
plt.xlabel("各國銷售票數累計比例",fontsize="20",
          fontweight="bold", color="r")
plt.axis("equal") 
plt.show()
plt.close()



# 2020各國上映院數累計比例 圓餅圖
plt.figure(dpi=150)
plt.pie(
        NationEreaTop5.iloc[:,2],
        labels=NationEreaTop5["國別地區"], 
        autopct="%1.1f%%",
        explode=(0.05,0,0,0,0,0),
        labeldistance=1.05,
        pctdistance=0.7,
        textprops={"fontsize":15},
        startangle=45,
        shadow=True,)
plt.xlabel("各國上映院數累計比例",fontsize="20",
          fontweight="bold", color="r")
plt.axis("equal") 
plt.show()
plt.close()


# 2020各國片數總計 圓餅圖

NationMovieCount = MovieCsvsMerge.groupby(["國別地區"],as_index=False)['國別地區'].agg({'Cnt':'count'})
NationMovieCount = NationMovieCount.sort_values("Cnt",ascending=False)
NationMovieCount.loc["40"] = NationMovieCount.iloc[8:,1:].sum()
NationMovieCount.iloc[40,0]="其它"
plt.figure(dpi=150)
NationMovieCount = NationMovieCount.iloc[[0,1,2,3,4,5,6,7,40],:]
plt.pie(
        NationMovieCount.iloc[:,1],
        labels = NationMovieCount["國別地區"], 
        autopct=lambda p:f'{p:.0f}% ({p*sum(NationMovieCount.iloc[:,1])/100 :.0f})', 
        explode=(0.05,0,0,0,0,0,0,0,0),
        labeldistance=1.05,
        pctdistance=0.7,
        textprops={"fontsize":8},
        startangle=45)
plt.xlabel("各國上映片數總計",fontsize="20",
          fontweight="bold", color="r")
plt.axis("equal") 
plt.show()
plt.close()





#=================================================================

# 2020各國週銷售金額折線圖
dfMoneyGroupby = dfMoney.groupby(["國別地區"]).sum().reset_index()
dfMoneyGroupby["Sum"] = dfMoneyGroupby.loc[:].sum(axis=1) 
dfMoneyGroupby = dfMoneyGroupby.sort_values("Sum",ascending=False).head(5)
dfMoneyGroupby = dfMoneyGroupby.drop("Sum",axis=1)
plt.figure(figsize=[15,6],dpi=150)
# 圖紙大小figsize=[x軸,y軸],dpi解析度
plt.plot(
    dfMoneyGroupby.columns[1:],
    dfMoneyGroupby.iloc[0,1:],
    label=dfMoneyGroupby.iloc[0,0],
    linewidth=2
    )
plt.plot(
    dfMoneyGroupby.iloc[1,1:],
    label=dfMoneyGroupby.iloc[1,0],
    linewidth=2
    )
plt.plot(
    dfMoneyGroupby.iloc[2,1:],
    label=dfMoneyGroupby.iloc[2,0],
    linewidth=2
    )
plt.plot(
    dfMoneyGroupby.iloc[3,1:],
    label=dfMoneyGroupby.iloc[3,0],
    linewidth=2
    )
plt.plot(
    dfMoneyGroupby.iloc[4,1:],
    label=dfMoneyGroupby.iloc[4,0],
    linewidth=2
    )

plt.xticks(rotation=45) 
# x軸名稱傾斜45度
plt.title("各國週銷售金額折線圖",fontsize="20",
          fontweight="bold", color="r")
plt.legend(loc = "upper right",fontsize=15)
plt.show()
plt.close()



#=================================================================


# 各國累計銷售金額前三名電影排行 橫條圖
AllNationMTop3 = dfMoney.copy()
# AllNationMTop3變數需重新宣告DF或是複製給它，不然系統無法判斷是共用還是另開啟一個變數
AllNationMTop3["Sum"] = AllNationMTop3.sum(axis=1)


UsNationMTop3 = AllNationMTop3[AllNationMTop3["國別地區"].isin(["美國"])]
UsNationMTop3 = UsNationMTop3.sort_values("Sum",ascending=False).head(3)

KrNationMTop3 = AllNationMTop3[AllNationMTop3["國別地區"].isin(["南韓"])]
KrNationMTop3 = KrNationMTop3.sort_values("Sum",ascending=False).head(3)

JpNationMTop3 = AllNationMTop3[AllNationMTop3["國別地區"].isin(["日本"])]
JpNationMTop3 = JpNationMTop3.sort_values("Sum",ascending=False).head(3)

HkNationMTop3 = AllNationMTop3[AllNationMTop3["國別地區"].isin(["香港"])]
HkNationMTop3 = HkNationMTop3.sort_values("Sum",ascending=False).head(3)

TwNationMTop3 = AllNationMTop3[AllNationMTop3["國別地區"].isin(["中華民國"])]
TwNationMTop3 = TwNationMTop3.sort_values("Sum",ascending=False).head(3)


plt.figure(figsize=[9,6],dpi=200)
ax = plt.subplot()
UsTop3 = plt.barh(UsNationMTop3["中文片名"],
                UsNationMTop3.iloc[:,31],
                label="美國")
KrTop3 = plt.barh(KrNationMTop3["中文片名"],
                KrNationMTop3.iloc[:,31],
                label="南韓")
JpTop3 = plt.barh(JpNationMTop3["中文片名"],
                JpNationMTop3.iloc[:,31],
                label="日本")
HkTop3 = plt.barh(HkNationMTop3["中文片名"],
                HkNationMTop3.iloc[:,31],
                label="香港")
TwTop3 = plt.barh(TwNationMTop3["中文片名"],
                TwNationMTop3.iloc[:,31],
                label="中華民國")




#設定顯示橫條圖各國電影的數值
for rect in UsTop3:
    w = rect.get_width()
    ax.text(w, rect.get_y()+rect.get_height()/2, "%d" %
            int(w), ha="left", va="center", fontsize = 12, color="b")
for rect in KrTop3:
    w = rect.get_width()
    ax.text(w, rect.get_y()+rect.get_height()/2, "%d" %
            int(w), ha="left", va="center", fontsize = 12, color="b")
for rect in JpTop3:
    w = rect.get_width()
    ax.text(w, rect.get_y()+rect.get_height()/2, "%d" %
            int(w), ha="left", va="center", fontsize = 12, color="b")
for rect in HkTop3:
    w = rect.get_width()
    ax.text(w, rect.get_y()+rect.get_height()/2, "%d" %
            int(w), ha="left", va="center", fontsize = 12, color="b")
for rect in TwTop3:
    w = rect.get_width()
    ax.text(w, rect.get_y()+rect.get_height()/2, "%d" %
            int(w), ha="left", va="center", fontsize = 12, color="b")


#設定圖表標題
plt.title("各國累計銷售金額前三名電影排行",fontsize="20",
          fontweight="bold", color="r")
plt.xlim(0,100_000_000) #設定x軸的金額
plt.legend(loc = "upper right",fontsize=12) 
plt.show()
plt.close()

#=================================================================

































