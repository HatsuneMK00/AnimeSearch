from flask import Flask, render_template, request, url_for,redirect
from settings import convert_type_to_chi
import pymysql
import os

app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def hello_world():
    db = pymysql.connect("localhost", "temp", "123456", "anime")
    cursor = db.cursor()
    anime_select_top_ten_query = """SELECT * FROM anime                
ORDER BY RAND()
LIMIT 5"""
    cursor.execute(anime_select_top_ten_query)
    data = cursor.fetchall()

    tags = []
    tag_query = """SELECT tag,agree_num FROM usr_tag_anime
    WHERE anime_name='{}'"""
    for anime in data:
        statement = tag_query.format(anime[0])
        cursor.execute(statement)
        tags.append(cursor.fetchall())
    db.close()
    return render_template('index.html',data=data,tags=tags)


@app.route('/anime/<anime_name>')
def anime(anime_name):
    return "there should be some anime info"


@app.route('/user/<user_name>')
def user(user_name):
    db = pymysql.connect("localhost", "temp", "123456", "anime")
    cursor = db.cursor()
    print("select usr_name from user where usr_name='%s'" % user_name)
    cursor.execute("select usr_name from user where usr_name='%s'" % user_name)
    data = cursor.fetchall()
    db.close()
    if data.__len__() == 0:
        return "no such user"
    else:
        return "hello " + user_name + " !"


@app.route('/result', methods=['POST'])
def result():
    db = pymysql.connect("localhost", "temp", "123456", "anime")
    with_sub_query = """WITH temp(name) AS (SELECT * FROM
    {})"""
    subset_query = """(SELECT DISTINCT `name`
    FROM anime JOIN anime_type ON (`name`=anime_name)
    WHERE type='{}')"""

    query_type = []
    query_tag = []
    query_year = []
    m_form = request.form
    for key in m_form.keys():
        if (m_form[key] == 'type'):
            query_type.append(key)
        elif (m_form[key] == 'tag'):
            query_tag.append(key)
        elif (m_form[key] == 'year'):
            query_year.append(key)
        else:
            pass

    statement = ""
    final_query = """SELECT * FROM anime NATURAL JOIN temp"""
    m_subset_query = ""
    alias_temp = 0

    for i in range(query_type.__len__()):
        if (i == query_type.__len__() - 1):
            m_subset_query = m_subset_query + subset_query.format(query_type[i]) + " AS temp" + str(alias_temp)
        else:
            m_subset_query = m_subset_query + subset_query.format(query_type[i]) + " AS temp" + str(
                alias_temp) + " NATURAL JOIN\n"
            alias_temp = alias_temp + 1
    statement = with_sub_query.format(m_subset_query) + "\n" + final_query

    cursor = db.cursor()
    cursor.execute(statement)
    data = cursor.fetchall()
    # print(data)

    #获取每个动画的评价
    tags = []
    tag_query = """SELECT tag,agree_num FROM usr_tag_anime
WHERE anime_name='{}'"""
    for anime in data:
        statement = tag_query.format(anime[0])
        cursor.execute(statement)
        tags.append(cursor.fetchall())
    db.close()
    return render_template('result.html', data=data,tags=tags)


@app.route('/addAnime', methods=['GET', 'POST'])
def addAnime():
    db = pymysql.connect("localhost", "temp", "123456", "anime")
    if (request.method == 'GET'):
        return render_template('addAnime.html')
    else:
        m_form = request.form
        file_name = ""
        temp_filename = ""
        upload_files = request.files.getlist("file")
#确保有名字！只能传一张！
        if len(upload_files) > 0:
            for file in upload_files:
                if allowed_file(file.filename):
                    file_name = m_form['name'] + '.' + file.filename.rsplit('.',1)[1]
                    temp_filename = file_name
                    file_name = os.path.join('static',file_name)
                    print(file_name)
                    file.save(file_name)

        # 向anime中插入元组
        anime_value = """VALUES('{}','{}',{},'{}',{},'{}','{}','{}')"""
        anime_insert_query = """INSERT INTO anime(`name`,`describe`,weight,`year`,episode_num,score,image,link)
        """
        statement = anime_insert_query + anime_value.format(m_form['name'], m_form['describe'], 1, m_form['year'],
                                                m_form['episode_num'], m_form['score'], temp_filename, 'NULL')
        #图片为文件名，需要添加路径，直接存路径会有反斜杠被转义的问题

        # print(statement)
        cursor = db.cursor()
        cursor.execute(statement)

        # 向anime_type中插入元祖
        type_value = []
        anime_name = m_form['name']
        for key in m_form.keys():
            if(m_form[key]=='type'):
                type_value.append(key)
        anime_type_insert_query = """INSERT INTO anime_type(`type`,anime_name)
VALUES"""
        for i in range(type_value.__len__()):
            if i != type_value.__len__() - 1:
                anime_type_insert_query = anime_type_insert_query + "('{}','{}'),".format(type_value[i],anime_name)
            else:
                anime_type_insert_query = anime_type_insert_query + "('{}','{}')".format(type_value[i], anime_name)
        cursor.execute(anime_type_insert_query)

        #向usr_tag_anime中插入元祖

        tags = m_form['tag'].split(' ')
        usr_tag_anime_insert_query = """INSERT INTO usr_tag_anime(usr_name,tag,anime_name,agree_num)
VALUES"""
        for i in range(len(tags)):
            if i != len(tags) - 1:
                usr_tag_anime_insert_query = usr_tag_anime_insert_query + "('{}','{}','{}',1),".format('admin',tags[i],anime_name)
            else:
                usr_tag_anime_insert_query = usr_tag_anime_insert_query + "('{}','{}','{}',1)".format('admin',tags[i],anime_name)
        cursor.execute(usr_tag_anime_insert_query)

        #向act中插入元祖
        vocals = m_form['vocal'].split(' ')
        act_insert_query = """INSERT INTO act(anime_name,vocal_name)
VALUES"""
        for i in range(len(vocals)):
            if i != len(vocals) - 1:
                act_insert_query = act_insert_query + "('{}','{}'),".format(anime_name,vocals[i])
            else:
                act_insert_query = act_insert_query + "('{}','{}')".format(anime_name,vocals[i])
        cursor.execute(act_insert_query)

        db.commit()
        db.close()
        return redirect('/')


@app.route('/type')
def type():
    db = pymysql.connect("localhost", "temp", "123456", "anime")
    #当时脑抽表名写成了classification注意不要写错了 还有type要加反引号转义
    select_query = """SELECT `type` FROM classification"""
    cursor = db.cursor()
    cursor.execute(select_query)
    types = cursor.fetchall()
    types = convert_type_to_chi(types)

    select_query = """SELECT vocal_name FROM vocal"""
    cursor.execute(select_query)
    vocals = cursor.fetchall()

    select_query = """SELECT company_name FROM company"""
    cursor.execute(select_query)
    companys = cursor.fetchall()

    select_query = """SELECT `name` FROM director"""
    cursor.execute(select_query)
    directors = cursor.fetchall()
    db.close()
    return render_template('type.html',types=types,vocals=vocals,companys=companys,directors=directors)


@app.route('/tag')
def tag():
    db = pymysql.connect("localhost", "temp", "123456", "anime")
    cursor = db.cursor()
    tag_query = """SELECT tag,COUNT(anime_name) FROM usr_tag_anime
GROUP BY tag"""
    cursor.execute(tag_query)
    tags = cursor.fetchall()
    db.close()
    return render_template('tag.html',tags=tags)


@app.route('/test',methods=['GET','POST'])
def test():
    if request.method=='POST':
        m_form = request.form
        for key in m_form.keys():
            print(key+": "+m_form[key])
        return "success"


#根本没有错误处理 太惨了
#要解决并发访问的问题 刷新页面的时候就会遇到 packet sequence number wwrong - got 1 expected 2
@app.route('/addTag')
def addTag():
    db = pymysql.connect("localhost", "temp", "123456", "anime")
    anime_name = request.args.get('name')
    a_tag = request.args.get('tag')
    tags = a_tag.split(' ')

    cursor = db.cursor()
    tag_insert_query = """INSERT INTO usr_tag_anime(usr_name,anime_name,tag,agree_num)
VALUES"""
    tag_value = """('{}','{}','{}',{})"""
    for i in range(len(tags)):
        if i != len(tags)-1:
            tag_insert_query = tag_insert_query + tag_value.format("admin",anime_name,tags[i],1)+',\n'
        else:
            tag_insert_query = tag_insert_query + tag_value.format("admin",anime_name,tags[i],1)

    cursor.execute(tag_insert_query)
    db.commit()
    db.close()
    return "success"

if __name__ == '__main__':
    app.run()
