# -*- coding: utf-8 -*-
# 趣动WillGo 河北省职工 线上健步走和工间操活动 脚本
'''
new Env('趣动WillGo');
33 20 * * * WillGo.py
'''
import requests
import time
import random
from datetime import datetime
import os

# 可以在这里填写token，也可以在环境变量中设置WillGo_Token
token = ""
if os.getenv("WillGo_Token"):
    token = os.getenv("WillGo_Token")
if not token:
    print("未填写token")
    exit(0)

def addSportRecord():
    # 获取当前时间戳
    time_str = int(time.time())
    step = random.randint(6000, 6200)
    # 目标 URL
    url = "https://capi.wewillpro.com/sport/addSportRecord"

    # 数据
    data = {
        "time_str": time_str,
        "request_time": time_str,
        "step_count": step,
        "mServerStep": step,
        "token": token,
        "app_type": 1,
        "data_source": 1,
        "app_version": "3.1.7",
        "mHuaWeiStep": 0,
        "time_zone": "GMT+08:00",
        "mPhoneStep": 0,
        "mTotalStep": 0,
        "mWechatStep": step,
        "sport_type": 0,
        "mPhoneServerStepIncreased": 0
    }

    # 发送 POST 请求
    response = requests.post(url, data=data)

    # 打印响应内容
    if response.json()["code"] == 200:
        print("步数上传成功,当前步数", step)


def gymnastics(now_times, counts):
    # 获取当前时间戳
    end_time = int(time.time())
    # use_time = random.randint(180, 240)
    use_time = 228
    # 获取 180-240 秒前的时间戳
    start_time = end_time - use_time

    perfect_counts = random.randint(int(counts/8), int(counts/4))
    nice_counts = random.randint(int(counts/8), int(counts/4))
    good_counts = random.randint(int(counts/8), int(counts/4))
    miss_counts = counts-perfect_counts-nice_counts-good_counts
    score = perfect_counts*5+nice_counts*3+good_counts
    calorie = int(score/10)
    # 定义变量
    a, b, c, d = perfect_counts, nice_counts, good_counts, miss_counts
    items = [a, b, c, d]
    scores = [5, 3, 1, 0]
    total_periods = 22
    period_scores = []
    now_scores = 0
    for i in range(total_periods):
        if i >= counts % total_periods:
            j = counts // total_periods
        else:
            j = counts // total_periods + 1

        for _ in range(j):
            k = random.randint(1, 4)
            while 0 < k < 5:
                if items[k-1] > 0:
                    items[k-1] -= 1
                    now_scores += scores[k-1]
                    break
                else:
                    k -= 1
                if k == 0:
                    k = 4

                # 当没有任何项可以分配时
                if sum(items) == 0:
                    k = -1

            if k == -1:
                break

        period_scores.append(now_scores)

    extra = [{"score": score, "time": (index + 1) * 10}
             for index, score in enumerate(period_scores)]

    # 目标 URL
    url = "https://capi.wewillpro.com/gymnastics/saveMsg"

    # 数据
    data = {
        "end_time": end_time,
        "start_time": start_time,
        "time_str": end_time,
        "token": token,
        "perfect": perfect_counts,
        "nice": nice_counts,
        "good": good_counts,
        "miss": miss_counts,
        "score": score,
        "calorie": calorie,
        "extra": extra,
        "is_end": 1,
        "use_time": use_time,
        "now_times": now_times,
        "gid": 1,
        "app_type": 1
    }
    # 发送 POST 请求
    response = requests.post(url, data=data)

    if response.json()["code"] == 200:
        print("工间操数据上传成功,得分", score)


def get_gyminfo():
    url = "https://capi.wewillpro.com/gymnastics/gymInfo"
    data = {
        "token": token,
        "gid": 1,
        "app_type": 1
    }
    response = requests.post(url, data=data)
    if response.json()["code"] == 200:
        times = response.json()["data"]["times"]
        counts = len(response.json()["data"]["top_score_list"])
        return times, counts


def get_last_new_id():
    url = "https://capi.wewillpro.com/new_activity/get_list?token=" + \
        token + "&activity_id=15883&page=1&limit=32"

    response = requests.get(url)
    if response.json()["code"] == 200:
        return response.json()['data']['data'][-1]['new_id']


def share_new(news_id):
    url = "https://capi.wewillpro.com/qz_activity/share_news"

    # 数据
    data = {
        "token": token,
        "activityid": 15883,
        "companyid": company_id,
        "news_id": news_id
    }

    # 发送 POST 请求
    response = requests.post(url, data=data)

    if response.json()["code"] == 200:
        print("学习阅读任务完成")


def get_daily_knowledge(i):
    times = datetime.now().strftime('%Y%m%d')
    url = "https://capi.wewillpro.com/qz_activity/get_daily_knowledge?token=" + \
        token + "&companyid="+company_id+"&activityid=15883&times="+times
    response = requests.get(url)
    if response.json()["code"] == 200:
        k = 0
        use_time = random.randint(15, 20)
        for ask_info in response.json()['data']:
            if k == i:
                print("当前回答", ask_info["ask_id"], "选择", [option['option_id']
                      for option in ask_info['options'] if option['answer'] == 1], "随机等待", use_time)
                time.sleep(use_time)
                user_ask(ask_info["ask_id"], [option['option_id']
                         for option in ask_info['options'] if option['answer'] == 1], use_time)
            k += 1


def user_ask(ask_id, option_id_list, use_time):
    url = "https://capi.wewillpro.com/qz_activity/user_ask"
    option_id = ','.join(map(str, option_id_list))
    data = {
        "token": token,
        "companyid": company_id,
        "activityid": 15883,
        "ask_id": ask_id,
        "option_id": option_id,
        "use_time": use_time
    }
    response = requests.post(url, data=data)
    if response.json()["code"] == 200:
        print(ask_id, "回答完成")


def ask():
    for i in range(5):
        get_daily_knowledge(i)


def get_company_id():
    url = "https://capi.wewillpro.com/user/get_current_company?token=" + token

    response = requests.get(url)
    if response.json()["code"] == 200:
        return response.json()["data"]["company_id"]


def get_task_list():
    to_do_list = []
    url = "https://esapi.wewillpro.com/ai_map_seven/get_task_list?token=" + \
        token+"&activity_id=15883&company_id="+company_id

    response = requests.get(url)
    if response.json()["code"] == 200:
        for info in response.json()["result"]:
            if info["is_reach"] != 1:
                to_do_list.append(info["title"])
        return to_do_list


company_id = get_company_id()

to_do_list = get_task_list()
if to_do_list:
    print('、'.join(to_do_list)+"未完成")
else:
    print("已全部完成")
    exit(0)

if "首页步数" in to_do_list:
    print("开始执行首页步数任务")
    addSportRecord()
    time.sleep(5)
if "工间操" in to_do_list:
    print("开始执行工间操任务")
    now_times, counts = get_gyminfo()
    gymnastics(now_times, counts)
    time.sleep(5)
if "知识问答" in to_do_list:
    print("开始执行知识问答任务")
    ask()
    time.sleep(5)
if "学习阅读" in to_do_list:
    print("开始执行学习阅读任务")
    share_new(get_last_new_id())  # 不知道如何获取newsid，总之先最后一个
    time.sleep(5)

time.sleep(5)
not_do_list = get_task_list()
if not_do_list:
    print('、'.join(not_do_list)+"未完成")
else:
    print("已全部完成")
