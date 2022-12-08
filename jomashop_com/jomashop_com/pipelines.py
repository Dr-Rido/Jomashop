# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import pymongo
from copy import deepcopy


class JomashopComPipeline:
    def __init__(self, settings, ifname="eth0"):
        self.count = 0
        self.update_count = 0
        '''线上测试数据库环境'''
        # try:
        #     import fcntl
        #     soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #     IPaddress = socket.inet_ntoa(
        #         fcntl.ioctl(soc.fileno(), 0x8915, struct.pack('256s', bytes(ifname[:15], 'utf-8')))[20:24])
        #     print("====", IPaddress)
        #     if IPaddress == "172.16.16.24":
        #         self.mongo_cli = pymongo.MongoClient(host='127.0.0.1', port=21077)
        #     else:
        #         self.mongo_cli = pymongo.MongoClient(host='xxx.xxx.xxx.xxx', port=27017, username='xxxxxx',
        #                                              password='xxxxxx')
        # except:

        self.mongo_cli = pymongo.MongoClient(host='127.0.0.1', port=27017)  # 本地数据库测试环境
        # self.mongo_cli = pymongo.MongoClient(host='192.168.131.163', port=27017, username='xxxxxx',
        #                                      password='xxxxxx')
        self.mongo_db = self.mongo_cli[settings['MONGODB_DB']]
        self.collection = self.mongo_db[settings['MONGODB_COLLECTION']]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def close_spider(self, spider):
        self.mongo_cli.close()
        logging.log(msg=f'=====insert count{self.count}=====', level=logging.INFO)
        logging.log(msg=f'=====update count{self.update_count}=====', level=logging.INFO)

    def process_item(self, item, spider):
        itemd = dict(item)
        cond1 = {'uuid': itemd['uuid'], 'source_id': itemd['source_id']}

        c1 = self.collection.find_one(filter=cond1)
        if c1:
            # 已存在的产品更新价格
            data = deepcopy(itemd)
            try:
                del data['_id']
            except KeyError:
                pass
            del data['add_time']
            if c1['uploaded'] == 1:
                del data['uploaded']
                del data['product_small_image']
                del data['product_big_images']
                del data['product_thumb_images']
                del data['image_urls']
            if c1['out_url_status'] == 1:
                del data['out_url_status']
                del data['out_url']
                del data['retailler_domain']
            try:
                ret = self.collection.update_one(filter=cond1, update={'$set': data}, upsert=True)
                self.update_count += 1
            except Exception as e:
                logging.log(msg="fAILED UPDATE MONGO %s" % e, level=logging.INFO)
            else:
                logging.log(msg=f"UPDATE MONGO {itemd['uuid']} COUNT {self.update_count}", level=logging.INFO)
                # self.push_item(itemd)
            # else:
            #    logging.log(msg=f'{item["uuid"]} 数据无需更新...', level=logging.INFO)
            #    raise DropItem('item existing!')
        else:
            try:
                self.collection.insert_one(dict(item))
                self.count += 1
            except Exception as e:
                logging.log(msg="FAILED TO INSERT INTO MONGO %s" % e, level=logging.INFO)

            else:
                logging.log(msg=f"INSERT INTO MONGO {itemd['uuid']} COUNT {self.count}", level=logging.INFO)
                # self.push_item(itemd)

        return item



