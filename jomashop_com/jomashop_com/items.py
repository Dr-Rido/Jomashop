# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JomashopComItem(scrapy.Item):
    id = scrapy.Field()                 # id
    add_time = scrapy.Field()           # 添加时间
    update_time = scrapy.Field()        # 更新时间
    delete_time = scrapy.Field()        # 删除时间
    lang_country = scrapy.Field()       # 语言-市场
    currency = scrapy.Field()           # 货币展示
    category = scrapy.Field()           # 一级category
    sub_category = scrapy.Field()       # 二级category
    third_category = scrapy.Field()     # 三级category
    subdivision_cat = scrapy.Field()    # 第四个category
    # 产品列表页字段
    product_small_image = scrapy.Field()  # 单图
    title = scrapy.Field()              # 产品标题
    url = scrapy.Field()                # 商品详情页
    brand_name = scrapy.Field()         # 产品品牌
    price_now = scrapy.Field()          # 当前价格
    price_original = scrapy.Field()     # 原始价格
    discount = scrapy.Field()           # 折扣【float】,不包含%
    condition = scrapy.Field()          # 使用度（全新/轻微使用）
    # 详情页字段
    out_url = scrapy.Field()            # 产品出站地址-去除联盟参数
    out_url_status = scrapy.Field()     # 出站状态标记， 默认0，没有跳出去。1是跳出去了
    retailler_domain = scrapy.Field()   # out_url解析后domain
    uuid = scrapy.Field()               # 产品唯一标识符
    source_id = scrapy.Field()          # 定义抓取的所属同行
    product_big_images = scrapy.Field()  # 大图列表
    product_thumb_images = scrapy.Field()  # 缩略图
    description = scrapy.Field()        # 产品描述
    material = scrapy.Field()  # 材质

    product_details = scrapy.Field()    # 去除的非标签名以外的信息，保留基本样式
    image_urls = scrapy.Field()         # 待下载图片列表
    images = scrapy.Field()             # 图片下载后地址
    # 新增字段
    uploaded = scrapy.Field()           # 默认0
    color = scrapy.Field()              # 产品颜色
