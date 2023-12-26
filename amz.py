# from bs4 import BeautifulSoup
# import requests

# url="https://www.amazon.in/Ainclu-Womens-Classic-Layered-Lace-Up/dp/B00K69XHGY/ref=b2b_gw_d_csf_b2b_sccl_1/258-8837396-8497212?pd_rd_w=SvU1u&content-id=amzn1.sym.80118820-a13a-4810-a5d3-0816775952fa&pf_rd_p=80118820-a13a-4810-a5d3-0816775952fa&pf_rd_r=80CBD46BM18R81225Y26&pd_rd_wg=0hL82&pd_rd_r=c516329a-4a79-48da-8432-a3ec36ed9d0f&pd_rd_i=B083QDVK83&psc=1"
# result=requests.get(url)
# doc=BeautifulSoup(result.text,"html.parser")
# prices=doc.find_all(text="₹")
# parent=prices[0].parent
# print(parent)

# #tags=doc.find_all(["p","div",";li"])

# #tags=doc.find_all(text=re.compile("\$"),limit=1)
# #for tag in tags:
#    #print(tag.strip())
from requests_html import HTMLSession
import json
import time
#Python is an “object-oriented programming language.” This means that almost all the code is 
#implemented using a special construct called classes. Programmers use classes to keep related 
#things together. This is done using the keyword “class,” which is a grouping of object-oriented 
#constructs.
#A class is a code template for creating objects. 
#Objects have member variables and have behaviour associated with them.
#An object is created using the constructor of the class. 
#This object will then be called the instance of the class. In Python we create instances in the following manner
#Instance = class(arguments)
class Reviews:
    def __init__(self, asin) -> None:
        self.asin=asin
        self.session=HTMLSession() #this is our object tht we ll use whenever class instance is called
        self.headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        self.url= f'https://www.amazon.in/OnePlus-Nord-Pastel-128GB-Storage/product-reviews/{self.asin}/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber='

    def pagination(self,page):
        r=self.session.get(self.url+str(page))
        if not r.html.find('div[data-hook=review]'):
            return False
        else:
            return r.html.find('div[data-hook=review]')

   
    def parse(self,reviews):
        total=[]  
        rating_count=0   
        ratings=0  
        avg_rating=0 
        for review in reviews:
            title=review.find('a[data-hook=review-title]',first=True).text
            rating=review.find('i[data-hook=review-star-rating] span',first=True).text
            body=review.find('span[data-hook=review-body] span',first=True).text.replace('\n','').strip()
            rating_count=rating_count+1
            ratings=ratings+(int(rating[0]))
            


            data={
                'rating_count':rating_count,
                'title':title,
                'rating':rating,
                'body':body[:100]
                
                
            }
            total.append(data)
        avg_rating=ratings/rating_count
        return total,avg_rating
    
    
    
    def save(self,results):
        with open(self.asin+'-reviews.json','w') as f:
            json.dump(results,f)


if __name__=='__main__':
    amz=Reviews('B0BY8JZ22K')
    results=[]
    average_rating=0
    for i in range(1,5):
        
        time.sleep(0.3)
        reviews=amz.pagination(i)
        if reviews is not False:
            results.append(amz.parse(reviews))
            temp,average_rating=amz.parse(reviews)
            print(f"The average rating is: {average_rating}")
        else :
            print("No more pages")
            break
    
    amz.save(results) 
            

