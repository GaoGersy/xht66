# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib

import scrapy
from gevent import os
from scrapy.utils.project import get_project_settings
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes


class Xht66Pipeline(ImagesPipeline):
    IMAGES_STORE = get_project_settings().get("IMAGES_STORE")

    def get_media_requests(self, item, info):
        image_url = item["link"]
        print(image_url)
        yield scrapy.Request(image_url)

    def item_completed(self, result, item, info):
        image_path = [x["path"] for ok, x in result if ok]
        dirName = item['name']
        arr = list(str(item['link']).split("/"))
        imageName = arr[len(arr) - 1]
        path = self.IMAGES_STORE + "/" + dirName
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
        os.rename(self.IMAGES_STORE + "/" + image_path[0], path + "/" + imageName)

        item["imagePath"] = self.IMAGES_STORE + "/" + item["name"]

        return item
