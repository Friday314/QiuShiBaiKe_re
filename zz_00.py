import requests
import re
import time

_headers = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) "
                 "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
}


info_lists = []


# 获取用户性别
def judgment_sex(class_name):

    if class_name == "womenIcon":
        return "女"
    else:
        return "男"


# 获取详细信息
def get_info(url):

    # 调用头文件
    res = requests.get(url, headers=_headers)

    ids = re.findall("<h2>(.*?)</h2>", res.text, re.S)
    # print(ids)

    levels = re.findall('<div class="articleGender \D+Icon">(.*?)</div>', res.text, re.S)
    # print(levels)

    sexs = re.findall('<div class="articleGender (.*?)">', res.text, re.S)
    # print(sexs)

    contents = re.findall('<div class="content">.*?<span>(.*?)</span>', res.text, re.S)
    # print(contents)

    laughs = re.findall('<span class="stats-vote"><i class="number">(\d+)</i> 好笑</span>', res.text, re.S)
    # print(laughs)

    comments = re.findall('<i class="number">(\d+)</i>', res.text, re.S)
    # print(comments)

    for _id, level, sex, content, laugh, comment in zip(ids, levels, sexs, contents, laughs, comments):

        # 获取的数据，存入字典中
        info = {
            'id': _id.strip(),
            'level': level.strip(),
            'sex': judgment_sex(sex),
            'content': content.strip(),
            'laugh': laugh.strip(),
            'comment': comment.strip()
        }

        info_lists.append(info)


# 程序入口
if __name__ == "__main__":

    # 网址列表
    urls = ["https://www.qiushibaike.com/text/page/{}/".format(str(i))
            for i in range(1, 2)]

    # 遍历网址，调用get_info()方法
    for url in urls:

        get_info(url)

        # 睡眠一秒
        time.sleep(1)

    for info_list in info_lists:

        # 创建文件，使用追加模式
        f = open("Qoushi.txt", "a+")

        try:
            f.write(info_list['id'] + "\t")
            f.write(info_list['level'] + "\t")
            f.write(info_list['sex'] + "\n")
            f.write(info_list['content'] + "\n")
            f.write(info_list['laugh'] + "\t")
            f.write(info_list['comment'] + "\n\n")
            f.close()

        # 过滤错误信息
        except UnicodeDecodeError:
            pass
