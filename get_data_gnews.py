import gnews
from gnews import GNews
import pandas as pd
from sqlalchemy import create_engine



iss = pd.read_excel('index_saham_syariah_mei2021.xlsx')



#con = create_engine('sqlite:///malifin.db')

con2 = create_engine('mysql+pymysql://zaenal:T0raja$am@192.168.100.149:3306/google_news')

google_news = GNews()

google_news = GNews(language='id', country='ID', period='7d', max_results=1000)

old_key = ["Bank Syariah Indonesia"]

keywords = [*old_key ,*iss['Kode Saham'].values.tolist(), *iss['Nama Penerbit Efek'].values.tolist()]


for j in keywords :
  json_resp = google_news.get_news(j)

  all_art = []
  for i in range(len(json_resp)) :
    try : 
      article = google_news.get_full_article(json_resp[i]['url'])
      information = [j,json_resp[i]['published date'],
                      article.title,
                      json_resp[i]['description'],
                      article.text,
                      article.url,
                      json_resp[i]['publisher']]
      all_art.append(information)
    except :
      print(i)
      pass
    
  df = pd.DataFrame(all_art, columns = ["keyword", "published_date", "title", 
                            "description", "text", "url", "publisher"])
  
  df['published_date'] = pd.to_datetime(df['published_date'], 
              format = "%a, %d %b %Y %H:%M:%S %Z")
  
  df.to_sql("news", con2, index = False, if_exists = "append")
