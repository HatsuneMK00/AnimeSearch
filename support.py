import pymysql


def convert_type_to_chi(type_names):
    result = []
    for type_name in type_names:
        if type_name[0] == 'yinv':
            result.append(['乙女', 'yinv'])
        elif type_name[0] == 'lianai':
            result.append(['恋爱', 'lianai'])
        elif type_name[0] == 'yishijie':
            result.append(['异世界', 'yishijie'])
        elif type_name[0] == 'tiyu':
            result.append(['体育', 'tiyu'])
        elif type_name[0] == 'cuilei':
            result.append(['催泪', 'cuilei'])
        elif type_name[0] == 'junshi':
            result.append(['军事', 'junshi'])
        elif type_name[0] == 'hougong':
            result.append(['后宫', 'hougong'])
        elif type_name[0] == 'qihuan':
            result.append(['奇幻', 'qihuan'])
        elif type_name[0] == 'zigong':
            result.append(['子贡', 'zigong'])
        elif type_name[0] == 'shaonian':
            result.append(['少年', 'shaonian'])
        elif type_name[0] == 'chengren':
            result.append(['成人', 'chengren'])
        elif type_name[0] == 'zhandou':
            result.append(['战斗', 'zhandou'])
        elif type_name[0] == 'tuili':
            result.append(['推理', 'tuili'])
        elif type_name[0] == 'gaoxiao':
            result.append(['搞笑', 'gaoxiao'])
        elif type_name[0] == 'richang':
            result.append(['日常', 'richang'])
        elif type_name[0] == 'jizhan':
            result.append(['机战', 'jizhan'])
        elif type_name[0] == 'xiaoyuan':
            result.append(['校园', 'xiaoyuan'])
        elif type_name[0] == 'rexue':
            result.append(['热血', 'rexue'])
        elif type_name[0] == 'baihe':
            result.append(['百合', 'baihe'])
        elif type_name[0] == 'kehuan':
            result.append(['科幻', 'kehuan'])
        elif type_name[0] == 'qingchun':
            result.append(['青春', 'qingchun'])
        elif type_name[0] == 'yinyue':
            result.append(['音乐', 'yinyue'])
    return result


base_anime_info_select_query = """SELECT {} FROM {} WHERE anime_name='{}'"""


def getVocals(anime_name, db):
    cursor = db.cursor()

    select_query = base_anime_info_select_query.format("vocal_name", "act", anime_name)
    cursor.execute(select_query)
    result = cursor.fetchall()
    return result


def getCompanys(anime_name, db):
    cursor = db.cursor()

    select_query = base_anime_info_select_query.format("comp_name", "produce", anime_name)
    cursor.execute(select_query)
    result = cursor.fetchall()
    return result


def getDirectors(anime_name, db):
    cursor = db.cursor()

    select_query = base_anime_info_select_query.format("dir_name", "direct", anime_name)
    cursor.execute(select_query)
    result = cursor.fetchall()
    return result


def getTags(anime_name, db):
    cursor = db.cursor()

    tag_query = """SELECT tag,agree_num FROM usr_tag_anime
        WHERE anime_name='{}'"""
    statement = tag_query.format(anime_name)
    cursor.execute(statement)
    result = cursor.fetchall()
    return result


def getAll(db):
    cursor = db.cursor()

    query = """SELECT DISTINCT `name` FROM anime"""
    cursor.execute(query)
    result = cursor.fetchall()
    return result


def dbConnect():
    db = pymysql.connect("localhost", "temp", "123456", "anime")
    return db


def dbDisconnect(db):
    db.close()


def getAnimeAllInfo(animes):
    db = dbConnect()
    cursor = db.cursor()
    data = []
    vocals = []
    directors = []
    companys = []
    info_query = """SELECT {} FROM {}
            WHERE {}='{}'"""
    # 不一起执行的原因是因为一起执行返回的结果不太好处理 对应python中会成为异构list
    for anime in animes:
        cursor.execute(info_query.format("*", "anime", "`name`", anime[0]))
        data.append(cursor.fetchall()[0])
        cursor.execute(info_query.format("vocal_name", "act", "anime_name", anime[0]))
        vocals.append(cursor.fetchall())
        cursor.execute(info_query.format("dir_name", "direct", "anime_name", anime[0]))
        directors.append(cursor.fetchall())
        cursor.execute(info_query.format("comp_name", "produce", "anime_name", anime[0]))
        companys.append(cursor.fetchall())

    # print(data)
    # print(vocals)
    # print(directors)
    # print(companys)

    # 获取每个动画的评价
    tags = []
    tag_query = """SELECT tag,agree_num FROM usr_tag_anime
        WHERE anime_name='{}'"""
    for anime in data:
        statement = tag_query.format(anime[0])
        # print(statement)
        cursor.execute(statement)
        tags.append(cursor.fetchall())
    dbDisconnect(db)
    return data, tags, vocals, directors, companys
