# -*- coding: utf-8 -*-
__author__ = 'daotuanvu'
create_date = '2/6/2015'

import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import os
import logging.config
import logging
import yaml
from flask import Flask
import flask_restful
from flask_restful.representations.json import output_json

output_json.func_globals['settings'] = {'ensure_ascii': False, 'encoding': 'utf8'}
app = Flask(__name__)
api = flask_restful.Api(app)

# remove handler
from handler.user_item_realtime import UserItemsRealtime
from handler.shop_report import ShopReportHandler
from handler.enb.item_report_week import EnbacWeekReportHandler
from handler.recommendation_hander import RecommendationHander
from handler.item_report import ItemReportHandler
from handler.muare.user_category import UserCategoryHandle
from handler.muare.user_item import UserItemHandle
from handler.muare.user_shop import UserShopHandle
from handler.muare.user_top_item import UserTopItemHandle
from handler.muare.user_top_shop import UserTopShopHandle
from handler.muare.item_top_user import ItemTopUserHandle
from handler.muare.shop_top_user import ShopTopUserHandler
from handler.muare.update_score_mr import UpdateScoreMuareHandler
from handler.muare.user_top_category import UserTopCategoryHandler
from handler.muare.admicro_info import AdmicroInformationHandler
from handler.enb.user_item_list_realtime import EnbacRealtimeReportHandler
from handler.enb.update_time_realtime import UpdateRealtimeReportHandler
from handler.statistics_report import StatisticsReportHandle
from handler.muare.shop_top_user_daily import ShopTopUserDailyReportHandle
from handler.muare.shop_score_daily import ShopScoreReportHandler
from handler.enb.user_shop_interested_item import EnbacUserShopListInterestedItemHandler
from handler.search.search_keyword import SearchKeyWord
from handler.muare.shop_user_statistic import ShopUserVisitStatisticHandler
from handler.muare.shop_user_detail import ShopUserDetailHandler
from handler.muare.item_source_view import ItemSourceViewHandler
from handler.chat.chat_report import ChatReportHandler
from handler.chat.user import User
from handler.chat.user_visit_statistic import UserVisitStatistic
from handler.muare.shop_action import ShopActionHandler
from handler.enb.user_item_interested import UserItemHandler
from handler.max_social import MaxSocialHandler
from handler.rongbay.keyword_statistic import KeywordStatisticHandler
from wit.quickstart import Chatbot
from wit.bot import ChatBotHandler
from handler.plaza_seeding import PlazaSeedingHandler
from wit.postback import PostbackHandler
from wit.bds_handler import BDSChatbotHandler
from wit.plaza_handler import PlazaChatbotHandler
# from wit.muachung_handler import MuachungChatbotHandler
from wit.bot_handler import ChatbotHandlerVer2
from wit.sohagame_handler import SohagameHandler

from handler.muachung.plaza.PlazaHotDeal import PlazaHotDealHandler
from handler.chat_log import ChatLogHandler

api.add_resource(ItemReportHandler, r"/report/<string:project>/item")
api.add_resource(ShopReportHandler, r"/report/<string:project>/shop")
api.add_resource(StatisticsReportHandle, r"/report/<string:project>/statistic")
api.add_resource(EnbacUserShopListInterestedItemHandler, r"/report/enb/user_interested_item")

api.add_resource(EnbacWeekReportHandler, r"/report/enb/week")

# remove UserItemsRealtime
# api.add_resource(UserItemRealtime, r"/report/<string:project>/user_view_item")
api.add_resource(UserItemsRealtime, r"/report/<string:project>/user/item")

api.add_resource(RecommendationHander, r"/mc_recommendation")

api.add_resource(UserCategoryHandle, r"/report/muare/user_category")
api.add_resource(UserShopHandle, r"/report/muare/user_shop")
api.add_resource(UserItemHandle, r"/report/muare/user_item")
api.add_resource(UserTopItemHandle, r"/report/muare/user_top_item")

api.add_resource(UserTopShopHandle, r"/report/muare/user_top_shop")
api.add_resource(ItemTopUserHandle, r"/report/muare/item_top_user")
api.add_resource(ShopTopUserHandler, r"/report/muare/shop_top_user")
api.add_resource(ShopTopUserDailyReportHandle, r"/report/muare/shop_top_user_daily")

api.add_resource(ShopScoreReportHandler, r"/report/muare/shop_score_daily")
api.add_resource(UpdateScoreMuareHandler, r"/report/muare/update_score")
api.add_resource(UserTopCategoryHandler, r"/report/muare/user_top_category")
api.add_resource(AdmicroInformationHandler, r"/report/muare/admicro_info")

api.add_resource(ShopUserVisitStatisticHandler, r"/report/muare/shop_user_statistic")
api.add_resource(ShopUserDetailHandler, r"/report/muare/shop_user_detail")
api.add_resource(ItemSourceViewHandler, r"/report/muare/item_source_view")
api.add_resource(ShopActionHandler, r"/report/muare/shop_action")

api.add_resource(ChatReportHandler, r"/report/chat/chat_report")
api.add_resource(User, r"/report/chat/user")
api.add_resource(UserVisitStatistic, r"/report/chat/user_visit_statistic")

api.add_resource(EnbacRealtimeReportHandler, r"/report/enb/user_list_realtime")
api.add_resource(UpdateRealtimeReportHandler, r"/report/enb/update_time_realtime")
api.add_resource(UserItemHandler, r"/report/enb/user_visit_interested")

api.add_resource(MaxSocialHandler, r"/max_social")

api.add_resource(SearchKeyWord, r'/search/<string:project>/keyword')

from handler.action.actions import URLAction, PageNameAction

api.add_resource(URLAction, r"/report/<string:project>/actions/url")
api.add_resource(PageNameAction, r"/report/<string:project>/actions/page_name")

from handler.action.actions import URLAction, PageNameAction

# support old url
api.add_resource(URLAction, r"/report/<string:project>/nemo/actions/url", endpoint="old_version_url_action")
api.add_resource(PageNameAction, r"/report/<string:project>/nemo/actions/page_name",
                 endpoint="old_version_page_name_actions")

from handler.muachung.order_analytics import OrderAnalytics

api.add_resource(OrderAnalytics, r"/report/muachung_plaza/order")

from handler.muachung.plaza.UserVisitHandler import PlazaUserHistory

api.add_resource(PlazaUserHistory, r"/report/muachung_plaza/user_history")

# 2016-04-04 api thong ke search keyword rongbay
api.add_resource(KeywordStatisticHandler, r"/report/rongbay/keyword_statistic")

from handler.warehouse.muachung.MuachungAdvertisement import MuachungAdvertisement

api.add_resource(MuachungAdvertisement, r"/warehouse/muachung/advertisement")

from handler.tag_generation.tag_generation_muare import MuareTagGeneration

api.add_resource(MuareTagGeneration, r"/tag_generation/muare")

# 2016-04-20 add api test chatbot
# api.add_resource(Chatbot, r"/chatbot")

# 2016-04-22 add api plaza_seeding
api.add_resource(PlazaSeedingHandler, r"/plaza_seeding")

# 2016-05-05 add api test chatbot
api.add_resource(PostbackHandler, r"/postback")

# 2016-05-20 postback
api.add_resource(ChatBotHandler, r"/test")

# 2016-05-26 bds_chatbot
api.add_resource(BDSChatbotHandler, r"/bds_chatbot")

# 2016-06-02 plaza_chatbot
api.add_resource(PlazaChatbotHandler, r"/plaza_chatbot")

# 2016-09-05-05
api.add_resource(SohagameHandler, r"/chatbot/sohagame")

# 2016-07-04 muachung_chatbot
# api.add_resource(MuachungChatbotHandler, r"/muachung_chatbot")

# 2016-07-04 all chatbot
api.add_resource(ChatbotHandlerVer2, r"/chatbot")

from handler.muachung.plaza.NewProductLogHandler import NewProductLogHandler

api.add_resource(NewProductLogHandler, r"/plaza/new_product_log")

# 2016-09-06
api.add_resource(PlazaHotDealHandler, r"/plaza/hot_deal")

# 2016-09-27
api.add_resource(ChatLogHandler, r"/chat/log")

from handler.bds_rongbay.BdsRongbayProjectHandler import BdsRongbayProjectHandler

api.add_resource(BdsRongbayProjectHandler, r"/bds_rongbay/projects")

from handler.bds_rongbay.BdsRongbayUserProfile import BdsRongbayUserProfile

api.add_resource(BdsRongbayUserProfile, r"/bds_rongbay/user_profile")


# Setup logging configuration
def setup_logging(default_path='logging.yaml', default_level=logging.INFO, env_key='LOG_CFG'):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
