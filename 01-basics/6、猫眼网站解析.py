import requests
from bs4 import BeautifulSoup

# maoyan_url="https://www.maoyan.com/cinemas"
# headers={
#     "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0",
#     'Cookie':'uuid_n_v=v1; uuid=2C701390C53011F09BD1BBABBFCD7F8E83585E82009E4A2DBE6A65788095B5DF; _csrf=fce92892b544e597421aca68473212def1ef8352383acb53562ff02e034aa500; _lxsdk_cuid=19a9b996baac8-0785afda86e1fb8-4c657b58-1bcab9-19a9b996baac8; _lxsdk=2C701390C53011F09BD1BBABBFCD7F8E83585E82009E4A2DBE6A65788095B5DF; hotMovieIds=1528577,346650,1489329,1504105,1505776,1142033,1515448,1528086,1251132,1528598,1564188,1500265,1535808,336673,1563972,1416590,1207331,1549421,1500340,1518527,1547296,1531012,1522668,1413052,1356671,1281834,1464734,1528362,257609,1499675; old-moviepage-ci=354; comingMovieIds=1443491,1528672,1504180,1565240,1281834,1413052,1547217,1528879,1373098,1504105,1528362,1535383,1607427,1142033,1399324,1589519,1528465,1380185,1489421,1522764,1462569,1428854,1502253,1551280,1518611,1462732,1470043,1480525,1427340,1374168,1490987,1531007,1251880,1535004,1501817,1435351,1543770,1254449,1536843,1298554,78463,1502849,1525198,1491440,1478868,1307114,1526722,1399234,1552202,1205713,1533022,1550284,1527959,1530820,1487265,1355532,1471073,1498191,1504573,1593791,1595576,1505633,1303013,1498217,1560007,1530742,1552828,1552835,1531087,1572309,1525896,1531752,1487870,1531501,1565162,1370922,1578248,1599810,1491711,1501767,356895,1490546,1523850,16032,4430,376806,1395127,1518012,1522873,1422798,1490085,1491824,1489992,1376912,1371742,1502895,1433394,1528908,1546367,1463806,1500853,1505654,1504556,1545361,1320415,1499664,1522761,1489955,1443420,1371005,1491283,1515510,1373968,1505531,1431804,1505554,1491759,1483055,1542636,1548780,1340084,1371106,1198213,1461184,1429503,1545360,1531115,1522280,1525000,1491455,1439044,1469785,1501854,1477992,572277,1595625,1522535,1471072,1528954,1519937,1568094,1488833,1567952,1487857,1565186,1543619,1525137,1606762; global-guide-isclose=true; __mta=175945373.1763547114436.1763547127060.1763547132578.5; _lxsdk_s=19a9b996baa-d0c-6f8-e15%7C%7C10'
# }
#
# response=requests.get(maoyan_url,headers=headers)
# response.encoding='utf-8'
# with open("maoyan.html","wb")as f:
#     f.write(response.content)

soup=BeautifulSoup(open('maoyan.html',encoding='utf-8'),features="lxml")
# print(soup.title)
# print(soup.title.string)
# print(soup.title.text)
# print(soup.div.strings)
# for i in soup.div.strings:
# #     print(i)
# for i in soup.find_all('div'):
#     print('-' * 30)
#     print(i.prettify())
# for i in soup.find_all('img'):
#     print('-' * 30)
#     # print(i.prettify())
#     if 'src' in i.attrs:
#         print(i.attrs)
#
# tags_div=soup.find(class_="tags-lines")
# for tag in tags_div.find_all(class_="tags-line tags-line-border"):
#     print(tag.find(class_="tags-title").text)
#     for line in tag.find_all("a"):
#         print(line.text,end=" ")
#     print()#相当于cout<<endl;
# print()
# movies_div=soup.find(class_="cinemas-list")
# print(movies_div.select(".cinemas-list-header" "span"))
# for movies in movies_div.find_all(class_="cinema-cell"):
#     print(movies.find("a").text)
#     print(movies.find("p").text)
#     print()

movies_div=soup.select(".cinemas-list")
print(movies_div.prettify())
# movies_div=soup.find(class_="cinemas-list")
# print(movies_div.prettify())