# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import pymysql
import pymongo
import os
import urllib.request

from BDSeePjt.items import BdseepjtItem
from BDSeePjt.items import BdseepjtItemDetail
from scrapy.conf import settings

from qiniu import Auth, put_file, etag
import qiniu.config

class BdseepjtPipeline(object):
    def __init__(self):
        self.file1 = codecs.open("item_list.json", 'wb', encoding="utf-8")
        self.file2 = codecs.open("item_detail.json", 'wb', encoding="utf-8")

        self.conn = pymysql.connect(host="127.0.0.1",user="root", passwd="sunny741", db = "BDSeeDB")

        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbName = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[dbName]
        self.post = tdb[settings['MONGODB_DOCNAME']]
        self.post_detail = tdb[settings['MONGODB_DOCNAME_MOVIE_DETAIL']]

        #qiniu 需要填写你的 Access Key 和 Secret Key
        access_key = 'CYvrg9XiH9soiLGQ9xjJkAb51ZLBkn4QG9i1KrDX'
        secret_key = 'L7V4fEsEoRMrwAOUKWM0l7zyQT4ZR11HedjVqzxI'
        #构建鉴权对象
        self.q = Auth(access_key, secret_key)
        #要上传的空间
        self.bucket_name = 'movieimgs'
        self.bucket_url = "pkaclys25.bkt.clouddn.com"
        
        #Picture download dir
        self.download_dir = "/home/sunny/Work/Blog/source/_posts/"
        self.img_download_dir = "/home/sunny/Work/tmp/"

    def upload_img(self, bucket_name, file_name, file_path):
        # generate token
        token = self.q.upload_token(bucket_name, file_name, 3600)
        ret, info = put_file(token, file_name, file_path)
        print(info)
        assert ret['key'] == file_name
        assert ret['hash'] == etag(file_path)

    def get_img_url(self,bucket_url, file_name):
        img_url = 'http://%s/%s' % (bucket_url, file_name)
        # generate md_url
        imageName = file_name.split('.')
        md_url = "![](%s)\n" % ( img_url)
        return md_url

    def process_item(self, item, spider):
        if isinstance(item, BdseepjtItem):
            print(">>>>>>>>>>>>>>>>>>>>>Start to witer JSON(Movie List)<<<<<<<<<<<<<<<<<<<<<<")
            for j in range(0, len(item["title"])):
                movie = {
                "title":item["title"][j],
                "description":item["description"][j],
                "link":item["link"][j],
                "comments_num":item["comments_num"][j],
                "published_date":item["published_date"][j],
                "category":item["category"][j],
                "category_tag":item["category_tag"][j],
                "image_url":item["image_url"][j],
                "score":item["score"][j],
                }

                # =========================write json========================
                #line = json.dumps(dict(movie), ensure_ascii=False)+'\n'
                #self.file1.write(line)

                #==========================write mysql=======================
                '''
                cur =self.conn.cursor()
                try:
                    sql = "insert into tb_movielist(\
                    title,description,link,comments_num,published_date,category,category_tag,image_url,score) VALUES(\
                    \""+movie['title']+"\",\
                    \""+movie['description']+"\",\
                    \""+movie['link']+"\",\
                    \""+movie['comments_num']+"\",\
                    \""+movie['published_date']+"\",\
                    \""+movie['category']+"\",\
                    \""+movie['category_tag']+"\",\
                    \""+movie['image_url']+"\",\
                    \""+movie['score']+"\"\
                    )"
                    cur.execute(sql)
                    self.conn.commit()
                except Exception as err:
                    self.conn.rollback()
                    '''
                #write mongodb
                #self.post.insert(dict(movie))
                #self.post.update({'link': movie['link']}, {'$set': dict(movie)}, True)

        elif isinstance(item, BdseepjtItemDetail):
            print(">>>>>>>>>>>>>>>>>>>>>Start to witer JSON(Movie Detail)<<<<<<<<<<<<<<<<<<<<<<")
            movie = {
            "title":item["title"],
            "link":item["link"],
            "published_date":item["published_date"],
            "category":item["category"],
            "category_tag":item["category_tag"],
            
            "image_url":item["image_url"],
            "descriptions":item['descriptions'],

            "contents":item["contents"],
            "content_imgs":item["content_imgs"],
            "download_links":item["download_links"],
            }

            # =========================write json=========================
            #line = json.dumps(dict(movie), ensure_ascii=False)+'\n'
            #self.file2.write(line)

            #==========================write mysql========================
            '''
            cur =self.conn.cursor()
            try:
                sql = "insert into tb_moviedetail(\
                title,link,published_date,category,category_tag,image_url,descriptions,contents,content_imgs,download_links) VALUES(\
                \""+movie['title']+"\",\
                \""+movie['link']+"\",\
                \""+movie['published_date']+"\",\
                \""+movie['category']+"\",\
                \""+movie['category_tag']+"\",\
                \""+str(movie['image_url'])+"\",\
                \""+str(movie['descriptions'])+"\",\
                \""+str(movie['contents'])+"\",\
                \""+str(movie['content_imgs'])+"\",\
                \""+str(movie['download_links'])+"\"\
                )"
                cur.execute(sql)
                self.conn.commit()
            except Exception as err:
                self.conn.rollback()
                '''
            #============================write mongodb=========================
            movie_save_db = {
            "title":item["title"],
            "link":item["link"],
            "published_date":item["published_date"],
            "category":item["category"],
            "category_tag":item["category_tag"]
            }

            #self.post.insert(dict(movie))
            result = self.post_detail.update({'title': movie['title']}, {'$set': dict(movie_save_db)}, True)
            print(result)
            '''
            if result['updatedExisting'] is True:
                #alreay exist  return 
                return item
            '''

            print("==========find a new movie, create markdown page============")
            #create markdown page            
            try:
                with open(self.download_dir+movie['title']+".md",'w') as f:
                    f.write("---"+"\n")
                    f.write("title: "+ movie["title"]+"\n")
                    f.write("date: "+movie["published_date"]+"\n")
                    f.write("categories: "+movie["category"]+"\n")
                    f.write("tags: "+"\n")
                    f.write("  - "+movie["category_tag"]+"\n")
                    f.write("---"+"\n")
                    
                    #download picture
                    #image_dir = self.download_dir+movie['title']+"/"
                    image_dir = self.img_download_dir
                    if not os.path.exists(image_dir):
                        os.makedirs(image_dir)

                    #download image
                    img_file_name = movie["image_url"].split('/')[-1]
                    img_local_path= image_dir+img_file_name
                    try:
                        urllib.request.urlretrieve(movie["image_url"], filename=img_local_path)
                    except Exception as e:
                        print ('str(Exception):\t', str(Exception))
                        print ('str(e):\t\t', str(e))
                        print ('repr(e):\t', repr(e))
                        print ('e.message:\t', e.message)
                    
                    #upload to qiniu
                    self.upload_img(self.bucket_name, img_file_name, img_local_path)
                    img_md_url = self.get_img_url(self.bucket_url, img_file_name)
                    f.write(img_md_url+"\n")
                    #delete image file
                    os.remove(img_local_path)

                    #f.write("{% asset_img "+img_file_name.split("/")[-1]+" ["+movie["title"]+"] %}"+"\n")


                    for description in movie["descriptions"]:
                        f.write(description+"\n")

                    f.write("<!--more-->"+"\n")

                    f.write("***"+"\n")

                    for content in movie["contents"]:
                        f.write(content+"\n")
                    f.write("***"+"\n")

                    for content_img_url in movie["content_imgs"]:
                        #download image
                        img_file_name = content_img_url.split('/')[-1]
                        img_local_path = image_dir + img_file_name
                        try:
                            urllib.request.urlretrieve(content_img_url, filename=img_local_path)
                        except Exception as e:
                            print ('str(Exception):\t', str(Exception))
                            print ('str(e):\t\t', str(e))
                            print ('repr(e):\t', repr(e))
                            print ('e.message:\t', e.message)

                        #upload to qiniu
                        self.upload_img(self.bucket_name, img_file_name, img_local_path)
                        img_md_url = self.get_img_url(self.bucket_url, img_file_name)
                        f.write(img_md_url+"\n")
                        #delete image file
                        os.remove(img_local_path)

                    for download_link in movie["download_links"]:
                        link_name = download_link["link_name"]
                        f.write("**"+link_name+"** ")
                        link_details = download_link["link_details"]
                        for link_detail in link_details:
                            link_type = link_detail["link_type"]
                            link_href = link_detail["link_href"]
                            f.write("["+link_type+"]"+"("+link_href+" "+" \""+link_type+"\""+") ")
                        f.write("\n")

            except Exception as e:
                print ('str(Exception):\t', str(Exception))
                print ('str(e):\t\t', str(e))
                print ('repr(e):\t', repr(e))

        return item

    def close_spider(self, spider):
        self.file1.close()
        self.file2.close()
        self.conn.close()
