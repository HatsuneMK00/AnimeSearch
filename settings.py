class anime:
    def __init__(self, name, describe, year, score, image, episode_num, link=""):
        self.name = name
        self.describe = describe
        self.year = year
        self.score = score
        self.image = image
        self.episode_num = episode_num
        self.link = link

    def info(self):
        return {'name': self.name, 'describe': self.describe, 'year': self.year, 'score': self.score,
                'image': self.image, 'episode_num': self.episode_num, 'link': self.link}


def convert_type_to_chi(type_names):
    result = []
    for type_name in type_names:
        if type_name[0]=='zhandou':
            result.append(['战斗','zhandou'])
        elif type_name[0]=='yishijie':
            result.append(['爱情','aiqing'])
        elif type_name[0]=='aiqing':
            result.append(['异世界','yishijie'])
    return result