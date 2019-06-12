from flask import Flask, render_template, request, url_for, redirect, session
from support import getCompanys, getDirectors, getVocals, getTags, getAll, dbConnect, dbDisconnect, getAnimeAllInfo
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
import os
import settings

app = Flask(__name__)
app.config.from_object(settings.DevelopmentConfig)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 动画条目中收藏按钮不显示是否收藏，如果收藏了还点会弹出提示，但暂时不根据是否收藏改变按钮样式，是一个轻松一点的折中方案
@app.route('/')
def index():
    user = ""
    if 'username' in session:
        user = session['username']
    else:
        user = None
    db = dbConnect()
    cursor = db.cursor()
    anime_select_top_ten_query = """SELECT * FROM anime                
ORDER BY RAND()
LIMIT 5"""
    cursor.execute(anime_select_top_ten_query)
    data = cursor.fetchall()
    vocals = []
    directors = []
    companys = []
    tags = []
    for anime in data:
        tags.append(getTags(anime[0], db))
        companys.append(getCompanys(anime[0], db))
        directors.append(getDirectors(anime[0], db))
        vocals.append(getVocals(anime[0], db))

    dbDisconnect(db)
    return render_template('index.html', data=data, tags=tags, vocals=vocals, directors=directors, companys=companys,
                           user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # 登陆过就直接进去吧 不要再登陆了
    if request.method == "GET":
        if 'username' not in session:
            return render_template('login.html')
        else:
            return redirect('/')
    else:
        db = dbConnect()
        cursor = db.cursor()
        user_name = request.form.get('user')
        pwd = request.form.get('pwd')
        check_has_user_query = """SELECT * FROM `user`
WHERE `usr_name`='{}'"""
        statement = check_has_user_query.format(user_name)
        cursor.execute(statement)
        data = cursor.fetchall()
        if len(data) != 0:
            user = data[0]
            pwd_hash = user[1]
            if check_password_hash(pwd_hash, pwd):
                session['username'] = user_name
                dbDisconnect(db)
                return redirect('/')
            else:
                dbDisconnect(db)
                return render_template('login.html', error="密码错误")  # error不能用中文
        else:
            dbDisconnect(db)
            return render_template('login.html', error="没有该用户，请去注册")


@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    if request.method == "GET":
        return render_template('signUp.html')
    else:
        db = dbConnect()
        cursor = db.cursor()
        user = request.form.get('user')
        pwd = request.form.get('pwd')
        email = request.form.get('email')
        check_user_unique_query = """SELECT `usr_name` FROM `user`
WHERE `usr_name`='{}'"""
        statement = check_user_unique_query.format(user)
        cursor.execute(statement)
        data = cursor.fetchall()
        if len(data) >= 1:
            return render_template('signUp.html', error="有同名用户，请换个名字吧")
        else:
            pwd = generate_password_hash(pwd)
            user_insert_query = """INSERT INTO `USER`(usr_name,`pwd`,email)
VALUES('{}','{}','{}')"""
            statement = user_insert_query.format(user, pwd, email)
            cursor.execute(statement)
            db.commit()
        dbDisconnect(db)
        return redirect('/login')


# 这个逻辑应该是没问题的 session是存储在本地的，跟随http下层的tcp连接传输的，因此不需要用户名参数
@app.route('/logout')
def LogOut():
    session.clear()
    return redirect('/')


@app.route('/anime/<anime_name>')
def anime(anime_name):
    user = ""
    if 'username' in session:
        user = session['username']
    else:
        user = None

    anime_select_query = """SELECT * FROM anime                
WHERE `name`='{}'"""
    statement = anime_select_query.format(anime_name)
    db = dbConnect()
    cursor = db.cursor()
    cursor.execute(statement)
    data = cursor.fetchall()
    vocals = []
    directors = []
    companys = []
    tags = []
    for anime in data:
        tags.append(getTags(anime[0], db))
        companys.append(getCompanys(anime[0], db))
        directors.append(getDirectors(anime[0], db))
        vocals.append(getVocals(anime[0], db))
    dbDisconnect(db)
    return render_template('anime.html', data=data, tags=tags, vocals=vocals, directors=directors, companys=companys,
                           user=user)


@app.route('/user/<user_name>')
def user(user_name):
    db = dbConnect()
    cursor = db.cursor()
    print("select usr_name from user where usr_name='%s'" % user_name)
    cursor.execute("select usr_name from user where usr_name='%s'" % user_name)
    data = cursor.fetchall()
    dbDisconnect(db)
    if data.__len__() == 0:
        return "no such user"
    else:
        return "hello " + user_name + " !"


# 在编写SQL时，在第一步去掉了关系表与anime表的连接操作，即不要求anime有外码约束，查找到的anime可能没有任何信息
@app.route('/type/result', methods=['POST'])
def type_result():
    user = ""
    if 'username' in session:
        user = session['username']
    else:
        user = None

    db = dbConnect()
    with_sub_query = """WITH temp(name) AS (SELECT * FROM
    {})"""
    subset_query = """(SELECT DISTINCT anime_name
    FROM {}
    WHERE `{}` LIKE '{}')"""

    query_type = []
    query_vocal = []
    query_company = []
    query_director = []

    m_form = request.form
    # 似乎字典的键不能有空格 在这之前还是A-1 PICTURE，到这里变成了A-1，因此后面将使用like匹配
    for key in m_form.keys():
        # print(key)
        if m_form[key] == 'type':
            query_type.append(key)
        elif m_form[key] == 'vocal':
            query_vocal.append(key)
        elif m_form[key] == 'company':
            query_company.append(key)
        elif m_form[key] == 'director':
            query_director.append(key)
        else:
            pass
    # print(query_director)
    # print(query_type)
    # print(query_vocal)
    # print(query_company)

    statement = ""
    final_query = """SELECT `name` FROM temp"""
    m_subset_query = ""
    total_query_num = len(query_vocal) + len(query_type) + len(query_director) + len(query_company)
    alias_temp = 0
    cursor = db.cursor()

    if total_query_num == 0:
        # 获取全部动画
        animes = getAll(db)
    else:
        # 添加vocal查询语句
        for i in range(query_vocal.__len__()):
            if alias_temp < total_query_num - 1:
                m_subset_query = m_subset_query + subset_query.format("act", "vocal_name",
                                                                      query_vocal[i]) + " AS temp" + str(
                    alias_temp) + " NATURAL JOIN\n"
            else:
                m_subset_query = m_subset_query + subset_query.format("act", "vocal_name",
                                                                      query_vocal[i]) + " AS temp" + str(alias_temp)
            alias_temp = alias_temp + 1
        # 添加type查询语句
        for i in range(query_type.__len__()):
            if alias_temp < total_query_num - 1:
                m_subset_query = m_subset_query + subset_query.format("anime_type", "type",
                                                                      query_type[i]) + " AS temp" + str(
                    alias_temp) + " NATURAL JOIN\n"
            else:
                m_subset_query = m_subset_query + subset_query.format("anime_type", "type",
                                                                      query_type[i]) + " AS temp" + str(alias_temp)
            alias_temp = alias_temp + 1
        # 添加company查询语句
        for i in range(query_company.__len__()):
            if alias_temp < total_query_num - 1:
                m_subset_query = m_subset_query + subset_query.format("produce", "comp_name",
                                                                      query_company[i] + "%") + " AS temp" + str(
                    alias_temp) + " NATURAL JOIN\n"
            else:
                m_subset_query = m_subset_query + subset_query.format("produce", "comp_name",
                                                                      query_company[i] + "%") + " AS temp" + str(
                    alias_temp)
            alias_temp = alias_temp + 1
        # 添加director查询语句
        for i in range(query_director.__len__()):
            if alias_temp < total_query_num - 1:
                m_subset_query = m_subset_query + subset_query.format("direct", "dir_name",
                                                                      query_director[i]) + " AS temp" + str(
                    alias_temp) + " NATURAL JOIN\n"
            else:
                m_subset_query = m_subset_query + subset_query.format("direct", "dir_name",
                                                                      query_director[i]) + " AS temp" + str(alias_temp)
            alias_temp = alias_temp + 1

        statement = with_sub_query.format(m_subset_query) + "\n" + final_query
        print(statement)
        cursor.execute(statement)
        # 所有满足要求的anime_name
        animes = cursor.fetchall()
        # print(animes)

    # 获取anime相关所需信息
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
    return render_template('result.html', data=data, tags=tags, vocals=vocals, directors=directors, companys=companys,
                           user=user)


@app.route('/tag/result', methods=['POST'])
def tag_result():
    user = ""
    if 'username' in session:
        user = session['username']
    else:
        user = None

    db = dbConnect()
    with_sub_query = """WITH temp(name) AS (SELECT * FROM
        {})"""
    subset_query = """(SELECT DISTINCT anime_name
        FROM usr_tag_anime
        WHERE tag='{}')"""

    query_tag = []
    m_form = request.form
    for key in m_form.keys():
        if m_form[key] == 'tag':
            query_tag.append(key)

    final_query = """SELECT `name` FROM temp"""
    m_subset_query = ""
    alias_temp = 0
    cursor = db.cursor()

    if len(query_tag) == 0:
        # 获取全部动画
        animes = getAll(db)
    else:
        for i in range(query_tag.__len__()):
            if alias_temp < query_tag.__len__() - 1:
                m_subset_query = m_subset_query + subset_query.format(query_tag[i]) + " AS temp" + str(
                    alias_temp) + " NATURAL JOIN\n"
            else:
                m_subset_query = m_subset_query + subset_query.format(query_tag[i]) + " AS temp" + str(alias_temp)
            alias_temp = alias_temp + 1
        statement = with_sub_query.format(m_subset_query) + "\n" + final_query
        # print(statement)
        cursor.execute(statement)
        # 所有满足要求的anime_name
        animes = cursor.fetchall()
    dbDisconnect(db)
    # 获取anime相关所需信息
    data, tags, vocals, directors, companys = getAnimeAllInfo(animes)
    return render_template('result.html', data=data, tags=tags, vocals=vocals, directors=directors, companys=companys,
                           user=user)


# 查询动画相关信息的函数如果可以模块化的话就很好，现在冗余有点高
# 这里这个参数应该不用传的，可以从session里获得
@app.route('/watchlist/<username>')
def WatchList(username):
    db = dbConnect()
    cursor = db.cursor()
    watch_select_query = """SELECT anime_name FROM `watch`
WHERE usr_name='{}'"""
    statement = watch_select_query.format(username)
    cursor.execute(statement)
    animes = cursor.fetchall()
    # 获取anime相关所需信息
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

    # 获取每个动画的评价
    # 此处评价为所有人添加在该动画上的TAG。将来可能改成用户自己添加的TAG
    tags = []
    tag_query = """SELECT tag,agree_num FROM usr_tag_anime
    WHERE anime_name='{}'"""
    for anime in data:
        statement = tag_query.format(anime[0])
        # print(statement)
        cursor.execute(statement)
        tags.append(cursor.fetchall())
    dbDisconnect(db)
    return render_template('watchlist.html', data=data, tags=tags, vocals=vocals, directors=directors,
                           companys=companys, user=username)


@app.route('/addAnime', methods=['GET', 'POST'])
def addAnime():
    if 'username' not in session:
        return redirect('/login')
    user = ""
    if 'username' in session:
        user = session['username']
    else:
        user = None
    db = dbConnect()
    if (request.method == 'GET'):
        cursor = db.cursor()
        type_select_query = """SELECT `type` FROM classification"""
        cursor.execute(type_select_query)
        data = cursor.fetchall()
        dbDisconnect(db)
        return render_template('addAnime.html', data=data, user=user)
    else:
        m_form = request.form
        file_name = ""
        temp_filename = ""
        upload_files = request.files.getlist("file")
        # 确保有名字！只能传一张！
        if len(upload_files) > 0:
            for file in upload_files:
                if allowed_file(file.filename):
                    file_name = m_form['name'] + '.' + file.filename.rsplit('.', 1)[1]
                    temp_filename = file_name
                    file_name = os.path.join('static', file_name)
                    print(file_name)
                    file.save(file_name)

        # 向anime中插入元组
        anime_value = """VALUES('{}','{}',{},'{}',{},'{}','{}','{}')"""
        anime_insert_query = """INSERT INTO anime(`name`,`describe`,weight,`year`,episode_num,score,image,link)
        """
        statement = anime_insert_query + anime_value.format(m_form['name'], m_form['describe'], 1, m_form['year'],
                                                            m_form['episode_num'], m_form['score'], temp_filename,
                                                            'NULL')
        # 图片为文件名，需要添加路径，直接存路径会有反斜杠被转义的问题

        # print(statement)
        cursor = db.cursor()
        cursor.execute(statement)

        # 向anime_type中插入元祖
        type_value = []
        anime_name = m_form['name']
        for key in m_form.keys():
            if (m_form[key] == 'type'):
                type_value.append(key)
        anime_type_insert_query = """INSERT INTO anime_type(`type`,anime_name)
VALUES"""
        for i in range(type_value.__len__()):
            if i != type_value.__len__() - 1:
                anime_type_insert_query = anime_type_insert_query + "('{}','{}'),".format(type_value[i], anime_name)
            else:
                anime_type_insert_query = anime_type_insert_query + "('{}','{}')".format(type_value[i], anime_name)
        cursor.execute(anime_type_insert_query)

        # 向usr_tag_anime中插入元组

        tags = m_form['tag'].split(' ')
        usr_tag_anime_insert_query = """INSERT INTO usr_tag_anime(usr_name,tag,anime_name,agree_num)
VALUES"""
        for i in range(len(tags)):
            if i != len(tags) - 1:
                usr_tag_anime_insert_query = usr_tag_anime_insert_query + "('{}','{}','{}',1),".format('admin', tags[i],
                                                                                                       anime_name)
            else:
                usr_tag_anime_insert_query = usr_tag_anime_insert_query + "('{}','{}','{}',1)".format('admin', tags[i],
                                                                                                      anime_name)
        cursor.execute(usr_tag_anime_insert_query)

        # 向act中插入元组
        vocals = m_form['vocal'].split(' ')
        act_insert_query = """INSERT INTO act(anime_name,vocal_name)
VALUES"""
        for i in range(len(vocals)):
            if i != len(vocals) - 1:
                act_insert_query = act_insert_query + "('{}','{}'),".format(anime_name, vocals[i])
            else:
                act_insert_query = act_insert_query + "('{}','{}')".format(anime_name, vocals[i])
        cursor.execute(act_insert_query)

        # 向produce中插入元组
        companys = m_form['company'].split(' ')
        comp_insert_query = """INSERT INTO produce(anime_name,comp_name)
VALUES"""
        for i in range(len(companys)):
            if i != len(companys) - 1:
                comp_insert_query = comp_insert_query + "('{}','{}'),".format(anime_name, companys[i])
            else:
                comp_insert_query = comp_insert_query + "('{}','{}')".format(anime_name, companys[i])
        cursor.execute(comp_insert_query)

        # 向direct中插入元组
        directors = m_form['director'].split(' ')
        direct_insert_query = """INSERT INTO direct(anime_name,dir_name)
        VALUES"""
        for i in range(len(directors)):
            if i != len(directors) - 1:
                direct_insert_query = direct_insert_query + "('{}','{}'),".format(anime_name, directors[i])
            else:
                direct_insert_query = direct_insert_query + "('{}','{}')".format(anime_name, directors[i])
        cursor.execute(direct_insert_query)

        db.commit()
        dbDisconnect(db)
        return redirect('/anime/' + anime_name)


# 这个函数和addAnime冗余较高，如果修改需要多注意！
@app.route('/modifyAnime/<anime_name>', methods=['POST', 'GET'])
def ModifyAnime(anime_name):
    if 'username' not in session:
        return redirect('/login')
    db = dbConnect()
    cursor = db.cursor()
    if request.method == "GET":
        tags = getTags(anime_name, db)
        companys = getCompanys(anime_name, db)
        directors = getDirectors(anime_name, db)
        vocals = getVocals(anime_name, db)
        temp = []
        for tag in tags:
            temp.append(tag[0])
        tag = " ".join(temp)
        temp = []
        for company in companys:
            temp.append(company[0])
        company = " ".join(temp)
        temp = []
        for director in directors:
            temp.append(director[0])
        director = " ".join(temp)
        temp = []
        for vocal in vocals:
            temp.append(vocal[0])
        vocal = " ".join(temp)

        anime_select_query = """SELECT * FROM anime                
        WHERE `name`= '{}'"""
        print(anime_name)
        cursor.execute(anime_select_query.format(anime_name))
        data = cursor.fetchall()
        # print(data)
        return render_template("modifyAnime.html", data=data[0], vocal=vocal, company=company, director=director,
                               tag=tag, user=user)
    else:
        m_form = request.form
        # 向anime中更新元组

        anime_update_query = """UPDATE anime
SET {}
WHERE `name`='{}'"""
        anime_update_value = """`describe`='{}',`year`='{}',`score`='{}',`episode_num`='{}'"""
        statement = anime_update_query.format(
            anime_update_value.format(m_form['describe'], m_form['year'], m_form['score'], m_form['episode_num']),
            m_form['name'])
        # print(statement)
        cursor = db.cursor()
        cursor.execute(statement)
        db.commit()

        # 向usr_tag_anime中更新元组
        # 先删除全部相关元组，再重新添加
        # 现在没有考虑用户不同的情况 当添加用户时 可以在GET返回页面时只返回该用户添加的tag 这里删除的逻辑不受影响
        anime_name = m_form['name']
        usr_tag_anime_delete_query = """DELETE FROM usr_tag_anime
WHERE anime_name='{}'"""
        statement = usr_tag_anime_delete_query.format(anime_name)
        cursor.execute(statement)
        db.commit()

        tags = m_form['tag'].split(' ')
        usr_tag_anime_insert_query = """INSERT INTO usr_tag_anime(usr_name,tag,anime_name,agree_num)
        VALUES"""
        for i in range(len(tags)):
            if i != len(tags) - 1:
                usr_tag_anime_insert_query = usr_tag_anime_insert_query + "('{}','{}','{}',1),".format('admin', tags[i],
                                                                                                       anime_name)
            else:
                usr_tag_anime_insert_query = usr_tag_anime_insert_query + "('{}','{}','{}',1)".format('admin', tags[i],
                                                                                                      anime_name)
        cursor.execute(usr_tag_anime_insert_query)

        # 向act中更新元组
        # 逻辑与上面相同
        act_delete_query = """DELETE FROM `act`
        WHERE anime_name='{}'"""
        statement = act_delete_query.format(anime_name)
        cursor.execute(statement)
        db.commit()

        vocals = m_form['vocal'].split(' ')
        act_insert_query = """INSERT INTO act(anime_name,vocal_name)
        VALUES"""
        for i in range(len(vocals)):
            if i != len(vocals) - 1:
                act_insert_query = act_insert_query + "('{}','{}'),".format(anime_name, vocals[i])
            else:
                act_insert_query = act_insert_query + "('{}','{}')".format(anime_name, vocals[i])
        cursor.execute(act_insert_query)

        # 向produce中插入元组
        produce_delete_query = """DELETE FROM `produce`
                WHERE anime_name='{}'"""
        statement = produce_delete_query.format(anime_name)
        cursor.execute(statement)
        db.commit()

        companys = m_form['company'].split(' ')
        comp_insert_query = """INSERT INTO produce(anime_name,comp_name)
        VALUES"""
        for i in range(len(companys)):
            if i != len(companys) - 1:
                comp_insert_query = comp_insert_query + "('{}','{}'),".format(anime_name, companys[i])
            else:
                comp_insert_query = comp_insert_query + "('{}','{}')".format(anime_name, companys[i])
        cursor.execute(comp_insert_query)

        # 向direct中插入元组
        direct_delete_query = """DELETE FROM `direct`
                WHERE anime_name='{}'"""
        statement = direct_delete_query.format(anime_name)
        cursor.execute(statement)
        db.commit()

        directors = m_form['director'].split(' ')
        direct_insert_query = """INSERT INTO direct(anime_name,dir_name)
                VALUES"""
        for i in range(len(directors)):
            if i != len(directors) - 1:
                direct_insert_query = direct_insert_query + "('{}','{}'),".format(anime_name, directors[i])
            else:
                direct_insert_query = direct_insert_query + "('{}','{}')".format(anime_name, directors[i])
        cursor.execute(direct_insert_query)

        db.commit()
        dbDisconnect(db)
        return redirect('/anime/' + anime_name)


@app.route('/type')
def type():
    user = ""
    if 'username' in session:
        user = session['username']
    else:
        user = None

    db = dbConnect()
    # 当时脑抽表名写成了classification注意不要写错了 还有type要加反引号转义
    select_query = """SELECT `type` FROM classification"""
    cursor = db.cursor()
    cursor.execute(select_query)
    types = cursor.fetchall()
    # print(types)
    # types = convert_type_to_chi(types)
    # print(types)

    select_query = """SELECT vocal_name FROM vocal"""
    cursor.execute(select_query)
    vocals = cursor.fetchall()

    select_query = """SELECT company_name FROM company"""
    cursor.execute(select_query)
    companys = cursor.fetchall()

    select_query = """SELECT `name` FROM director"""
    cursor.execute(select_query)
    directors = cursor.fetchall()
    # print(directors)
    dbDisconnect(db)
    return render_template('type.html', types=types, vocals=vocals, companys=companys, directors=directors, user=user)


@app.route('/tag')
def tag():
    user = ""
    if 'username' in session:
        user = session['username']
    else:
        user = None

    db = pymysql.connect("localhost", "temp", "123456", "anime")
    cursor = db.cursor()
    tag_query = """SELECT tag,COUNT(anime_name) FROM usr_tag_anime
GROUP BY tag"""
    cursor.execute(tag_query)
    tags = cursor.fetchall()
    db.close()
    return render_template('tag.html', tags=tags, user=user)


# 根本没有错误处理 太惨了
# 要解决并发访问的问题 刷新页面的时候就会遇到 packet sequence number wwrong - got 1 expected 2
# 作为唯三一个调用接口，需要注意动画名字中可能包含&，与url中的字符相冲突，这里进行了一次字符转换
# 其他涉及了动画名字在url传参的情况，都使用flask另一种接受参数的方式，不需要转换处理
@app.route('/addTag')
def addTag():
    db = dbConnect()
    anime_name = request.args.get('name')
    anime_name = anime_name.replace('^', '&')
    a_tag = request.args.get('tag')
    tags = a_tag.split(' ')

    cursor = db.cursor()
    tag_insert_query = """INSERT INTO usr_tag_anime(usr_name,anime_name,tag,agree_num)
VALUES"""
    tag_value = """('{}','{}','{}',{})"""
    for i in range(len(tags)):
        if i != len(tags) - 1:
            tag_insert_query = tag_insert_query + tag_value.format("admin", anime_name, tags[i], 1) + ',\n'
        else:
            tag_insert_query = tag_insert_query + tag_value.format("admin", anime_name, tags[i], 1)

    print(tag_insert_query)
    cursor.execute(tag_insert_query)
    db.commit()
    dbDisconnect(db)
    return "success"


@app.route('/searchAnime', methods=['POST'])
def SearchAnime():
    db = dbConnect()
    cursor = db.cursor()
    search_anime = request.form.get('SA')
    anime_search_query = """SELECT `name` FROM anime
WHERE `name` LIKE '%{}%'"""
    statement = anime_search_query.format(search_anime)
    print(statement)
    cursor.execute(statement)
    animes = cursor.fetchall()
    dbDisconnect(db)

    data, tags, vocals, directors, companys = getAnimeAllInfo(animes)
    if 'username' in session:
        user = session['username']
    else:
        user = None
    return render_template('result.html', data=data, tags=tags, vocals=vocals, directors=directors, companys=companys,
                           user=user)


# 需要检查是否收藏过
@app.route('/addAnimeToWatch/<anime_name>')
def AddAnimeToWatch(anime_name):
    if 'username' not in session:
        return "not login yet"
    db = dbConnect()
    cursor = db.cursor()
    user_name = session['username']
    check_watched_query = """SELECT COUNT(*) FROM `watch`
WHERE usr_name='{}' AND anime_name='{}'"""
    statement = check_watched_query.format(user_name, anime_name)
    cursor.execute(statement)
    data = cursor.fetchone()
    print(data[0])
    if data[0] != 0:
        dbDisconnect(db)
        return "duplicated"
    else:
        insert_watch_query = """INSERT INTO `watch`(anime_name,usr_name)
VALUES('{}','{}')"""
        statement = insert_watch_query.format(anime_name, user_name)
        cursor.execute(statement)
        db.commit()
        dbDisconnect(db)
        return "success"


# 这个接口现在只在watchlist中出现，因此不进行存在性检查
@app.route('/removeAnimeFromWatch/<anime_name>')
def RemoveAnimeFromWatch(anime_name):
    db = dbConnect()
    cursor = db.cursor()
    user_name = session['username']
    delete_watch_query = """DELETE FROM `watch`
WHERE usr_name='{}' AND anime_name='{}'"""
    statement = delete_watch_query.format(user_name, anime_name)
    cursor.execute(statement)
    db.commit()
    dbDisconnect(db)
    return "success"


if __name__ == '__main__':
    app.run()
