from pymongo import MongoClient
from Article import *


class SearchController:



    def __init__(self):
        self.__article_list = []
        self.__query = None


    def set_query(self, query):
        self.__query = query


    def get_query(self):
        return self.__query
        
   
        



    def search(self, search):
    
        self.set_query(search.split())
       
    
        #Connect to database
        client = MongoClient("mongodb+srv://Allan123:School123@cluster0.gqdysfd.mongodb.net/Articles?retryWrites=true&w=majority")
        database = client["Articles"]
        first_collection = database["Computer Science"]
        second_collection = database["Math"]
        

        #///////////////////////////////#
        #                               #
        #   Search First Collection     #
        #                               #
        #///////////////////////////////#


        results = first_collection.find()
        for result in results:
        
            article = Article()
            article.set_id(result.get("_id"))
            article.set_title(result.get("title"))
            article.set_isPartOf(result.get("isPartOf"))
            article.set_publicationYear(result.get("publicationYear"))
            article.set_url(result.get("url"))
            article.set_creator(result.get("creator"))
            article.set_publisher(result.get("publisher"))
            article.set_keyphrase(result.get("keyphrase"))

             
            keyphrase_intersection = intersection(self.get_query(), article.get_keyphrase())
            title_intersection = intersection(self.get_query(), article.get_split_title())
            pd_intersection = intersection(keyphrase_intersection, title_intersection)
            
            total_match = (len(keyphrase_intersection) + len(title_intersection) - len(pd_intersection))
            if (total_match > 0):
            
                article.set_queryMatch(total_match)
                self.__article_list.append(article)
    
            self.__article_list.sort(key = lambda article: article.get_queryMatch(), reverse = True)
            
        for article in range(len(self.__article_list)):
            print(self.__article_list[article].get_title())
            print(self.__article_list[article].get_url()) 
            print(self.__article_list[article].get_keyphrase()) 
            print(self.__article_list[article].get_queryMatch()) 
  
    
   
def intersection(lst1, lst2):
    return [value for value in lst1 if value in lst2]
