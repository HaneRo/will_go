import requests
import time
import random
token = "tokentokentokentokentokentokentokentokentoken"
company_id = 12345


def step():
    # 获取当前时间戳
    time_str = int(time.time())

    # 获取 180-240 秒前的时间戳
    # start_time = end_time - random.randint(180, 240)

    # 目标 URL
    url = "https://capi.wewillpro.com/sport/addSportRecord"

    # 数据
    data = {
        "time_str": time_str,
        "step_count": random.randint(6000, 6420),
        "token": token
    }

    # 发送 POST 请求
    response = requests.post(url, data=data)

    # 打印响应内容
    print(response.text)


def gymnastics(now_times, counts):
    # 获取当前时间戳
    end_time = int(time.time())
    # use_time = random.randint(180, 240)
    use_time = 220
    # 获取 180-240 秒前的时间戳
    start_time = end_time - use_time

    perfect_counts = random.randint(int(counts/8), int(counts/4))
    nice_counts = random.randint(int(counts/8), int(counts/4))
    good_counts = random.randint(int(counts/8), int(counts/4))
    miss_counts = counts-perfect_counts-nice_counts-good_counts
    score = perfect_counts*5+nice_counts*3+good_counts
    calorie = int(score/10)
    print(score)
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

    # print(extra)

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

    # 打印响应内容
    print(response.text)


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
        print(times, counts)
        return times, counts
# gymnastics(get_gyminfo())
# step()
# get_gyminfo()


def random_get_new_id():
    url = "https://capi.wewillpro.com/new_activity/get_list?token=" + \
        token + "&activity_id=15883&page=1&limit=32"

    response = requests.get(url)
    print(response.json())
    if response.json()["code"] == 200:
        return random.choice(response.json()['data']['data'])['new_id']


def share_new(news_id):
    url = "https://capi.wewillpro.com/qz_activity/share_news"

    # 数据
    data = {
        "token": token,
        "activity_id": 15883,
        "company_id": company_id,
        "news_id":news_id
    }

    # 发送 POST 请求
    response = requests.post(url, data=data)

    # 打印响应内容
    print(response.text)



def get_task_list():
    to_do_list = []
    url = "https://esapi.wewillpro.com/ai_map_seven/get_task_list?token=" + \
        token+"&activity_id=15883&company_id="+company_id

    response = requests.get(url)
    if response.json()["code"] == 200:
        # print(response.text)
        for info in response.json()["result"]:
            if info["is_reach"] != 1:
                to_do_list.append(info["title"])
        return to_do_list

to_do_list=get_task_list()
if to_do_list:
    print('、'.join(to_do_list)+"未完成")
else:
    print("已全部完成")
    exit(0)

if "首页步数" in to_do_list:
    print("开始执行首页步数任务")
    step()
    time.sleep(5)
if "工间操" in to_do_list:
    print("开始执行工间操任务")
    gymnastics(get_gyminfo())
    time.sleep(5)
if "知识问答" in to_do_list:
    # print("开始执行知识问答任务")
    # step()
    # time.sleep(5)
    print("暂无知识问答功能")
if "学习阅读" in to_do_list:
    print("开始执行学习阅读任务")
    share_new(random_get_new_id())
    time.sleep(5)

time.sleep(5)
not_do_list=get_task_list()
if not_do_list:
    print('、'.join(not_do_list)+"未完成")
else:
    print("已全部完成")