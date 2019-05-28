/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80015
 Source Host           : localhost:3306
 Source Schema         : anime

 Target Server Type    : MySQL
 Target Server Version : 80015
 File Encoding         : 65001

 Date: 28/05/2019 20:44:09
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `act`;
CREATE TABLE `act`  (
  `anime_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `vocal_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`anime_name`, `vocal_name`) USING BTREE,
  INDEX `vocal_anime_fk`(`vocal_name`) USING BTREE,
  CONSTRAINT `anime_vocal_fk` FOREIGN KEY (`anime_name`) REFERENCES `anime` (`name`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;
-- ----------------------------
-- Records of act
-- ----------------------------
INSERT INTO `act` VALUES ('我的英雄学院', '三宅健太');
INSERT INTO `act` VALUES ('混沌武士', '三木真一郎');
INSERT INTO `act` VALUES ('新世纪福音战士', '三石琴乃');
INSERT INTO `act` VALUES ('CAROLE & TUESDAY', '上坂堇');
INSERT INTO `act` VALUES ('少女与战车', '中上育实');
INSERT INTO `act` VALUES ('混沌武士', '中井和哉');
INSERT INTO `act` VALUES ('樱花庄的宠物女孩', '中津真莉');
INSERT INTO `act` VALUES ('魔卡少女樱', '丹下樱');
INSERT INTO `act` VALUES ('魔卡少女樱', '久川绫');
INSERT INTO `act` VALUES ('NO GAME NO LIFE 游戏人生', '井口裕香');
INSERT INTO `act` VALUES ('少女与战车', '井口裕香');
INSERT INTO `act` VALUES ('命运石之门', '今井麻美');
INSERT INTO `act` VALUES ('攻壳机动队 S.A.C. 2nd GIG', '仲野裕');
INSERT INTO `act` VALUES ('攻壳机动队STAND ALONE COMPLEX', '仲野裕');
INSERT INTO `act` VALUES ('刀剑神域', '伊藤加奈惠');
INSERT INTO `act` VALUES ('我的英雄学院', '佐仓绫音');
INSERT INTO `act` VALUES ('太空丹迪', '佐武宇绮');
INSERT INTO `act` VALUES ('混沌武士', '佐藤银平');
INSERT INTO `act` VALUES ('CAROLE & TUESDAY', '入野自由');
INSERT INTO `act` VALUES ('邻家的吸血鬼小妹', '内田彩');
INSERT INTO `act` VALUES ('太空丹迪', '内藤千晶');
INSERT INTO `act` VALUES ('会长是女仆大人', '冈本信彦');
INSERT INTO `act` VALUES ('爆漫王。', '冈本信彦');
INSERT INTO `act` VALUES ('爆漫王。', '利根健太朗');
INSERT INTO `act` VALUES ('数码兽大冒险', '前田爱');
INSERT INTO `act` VALUES ('强袭魔女', '千叶纱子');
INSERT INTO `act` VALUES ('机动警察 和平保卫战', '古川登志夫');
INSERT INTO `act` VALUES ('太空丹迪', '吉野裕行');
INSERT INTO `act` VALUES ('强袭魔女', '名冢佳织');
INSERT INTO `act` VALUES ('邻家的吸血鬼小妹', '和气杏未');
INSERT INTO `act` VALUES ('NEW GAME!', '喜多村英梨');
INSERT INTO `act` VALUES ('强袭魔女', '园崎未惠');
INSERT INTO `act` VALUES ('数码兽大冒险', '坂本千夏');
INSERT INTO `act` VALUES ('星际牛仔', '坂本真绫');
INSERT INTO `act` VALUES ('CAROLE & TUESDAY', '堀内贤雄');
INSERT INTO `act` VALUES ('樱花庄的宠物女孩', '堀江由衣');
INSERT INTO `act` VALUES ('星际牛仔', '多田葵');
INSERT INTO `act` VALUES ('CAROLE & TUESDAY', '大冢明夫');
INSERT INTO `act` VALUES ('攻壳机动队 S.A.C. 2nd GIG', '大冢明夫');
INSERT INTO `act` VALUES ('攻壳机动队STAND ALONE COMPLEX', '大冢明夫');
INSERT INTO `act` VALUES ('混沌武士', '大冢芳忠');
INSERT INTO `act` VALUES ('攻壳机动队 S.A.C. 2nd GIG', '大川透');
INSERT INTO `act` VALUES ('攻壳机动队STAND ALONE COMPLEX', '大川透');
INSERT INTO `act` VALUES ('机动警察 和平保卫战', '大林隆介');
INSERT INTO `act` VALUES ('珈百璃的堕落', '大空直美');
INSERT INTO `act` VALUES ('珈百璃的堕落', '大西沙织');
INSERT INTO `act` VALUES ('数码兽大冒险', '天神有海');
INSERT INTO `act` VALUES ('新世纪福音战士', '宫村优子');
INSERT INTO `act` VALUES ('CAROLE & TUESDAY', '宫野真守');
INSERT INTO `act` VALUES ('命运石之门', '宫野真守');
INSERT INTO `act` VALUES ('CAROLE & TUESDAY', '宮寺智子');
INSERT INTO `act` VALUES ('机动警察 和平保卫战', '富永美衣奈');
INSERT INTO `act` VALUES ('珈百璃的堕落', '富田美忧');
INSERT INTO `act` VALUES ('邻家的吸血鬼小妹', '富田美忧');
INSERT INTO `act` VALUES ('神的记事本', '小仓唯');
INSERT INTO `act` VALUES ('会长是女仆大人', '小林优');
INSERT INTO `act` VALUES ('强袭魔女', '小清水亚美');
INSERT INTO `act` VALUES ('数码兽大冒险', '小西宽子');
INSERT INTO `act` VALUES ('攻壳机动队 S.A.C. 2nd GIG', '小野冢贵志');
INSERT INTO `act` VALUES ('攻壳机动队STAND ALONE COMPLEX', '小野冢贵志');
INSERT INTO `act` VALUES ('神的记事本', '小野大辅');
INSERT INTO `act` VALUES ('少女与战车', '尾崎真实');
INSERT INTO `act` VALUES ('NEW GAME!', '山口爱');
INSERT INTO `act` VALUES ('新世纪福音战士', '山口由里子');
INSERT INTO `act` VALUES ('刀剑神域', '山寺宏一');
INSERT INTO `act` VALUES ('攻壳机动队 S.A.C. 2nd GIG', '山寺宏一');
INSERT INTO `act` VALUES ('攻壳机动队STAND ALONE COMPLEX', '山寺宏一');
INSERT INTO `act` VALUES ('新世纪福音战士', '山寺宏一');
INSERT INTO `act` VALUES ('星际牛仔', '山寺宏一');
INSERT INTO `act` VALUES ('混沌武士', '山寺宏一');
INSERT INTO `act` VALUES ('CAROLE & TUESDAY', '岛袋美由利');
INSERT INTO `act` VALUES ('魔卡少女樱', '岩男润子');
INSERT INTO `act` VALUES ('樱花庄的宠物女孩', '川澄绫子');
INSERT INTO `act` VALUES ('混沌武士', '川澄绫子');
INSERT INTO `act` VALUES ('CAROLE & TUESDAY', '市之濑加那');
INSERT INTO `act` VALUES ('我的英雄学院', '悠木碧');
INSERT INTO `act` VALUES ('刀剑神域', '户松遥');
INSERT INTO `act` VALUES ('NEW GAME!', '户田惠');
INSERT INTO `act` VALUES ('强袭魔女', '斋藤千和');
INSERT INTO `act` VALUES ('NEW GAME!', '日笠阳子');
INSERT INTO `act` VALUES ('NO GAME NO LIFE 游戏人生', '日笠阳子');
INSERT INTO `act` VALUES ('爆漫王。', '日野聪');
INSERT INTO `act` VALUES ('混沌武士', '日高法子');
INSERT INTO `act` VALUES ('邻家的吸血鬼小妹', '日高里菜');
INSERT INTO `act` VALUES ('刀剑神域', '早见沙织');
INSERT INTO `act` VALUES ('爆漫王。', '早见沙织');
INSERT INTO `act` VALUES ('NEW GAME!', '朝日奈丸佳');
INSERT INTO `act` VALUES ('NO GAME NO LIFE 游戏人生', '松冈祯丞');
INSERT INTO `act` VALUES ('刀剑神域', '松冈祯丞');
INSERT INTO `act` VALUES ('樱花庄的宠物女孩', '松冈祯丞');
INSERT INTO `act` VALUES ('神的记事本', '松冈祯丞');
INSERT INTO `act` VALUES ('轮回的拉格朗日', '松冈祯丞');
INSERT INTO `act` VALUES ('新世纪福音战士', '林原惠美');
INSERT INTO `act` VALUES ('星际牛仔', '林原惠美');
INSERT INTO `act` VALUES ('太空丹迪', '桑岛法子');
INSERT INTO `act` VALUES ('NEW GAME!', '森永千才');
INSERT INTO `act` VALUES ('会长是女仆大人', '椎桥和义');
INSERT INTO `act` VALUES ('机动警察 和平保卫战', '榊原良子');
INSERT INTO `act` VALUES ('樱花庄的宠物女孩', '樱井孝宏');
INSERT INTO `act` VALUES ('神的记事本', '樱井孝宏');
INSERT INTO `act` VALUES ('珈百璃的堕落', '水濑祈');
INSERT INTO `act` VALUES ('数码兽大冒险', '水谷优子');
INSERT INTO `act` VALUES ('NO GAME NO LIFE 游戏人生', '泽城美雪');
INSERT INTO `act` VALUES ('强袭魔女', '泽城美雪');
INSERT INTO `act` VALUES ('混沌武士', '涉谷茂');
INSERT INTO `act` VALUES ('少女与战车', '渊上舞');
INSERT INTO `act` VALUES ('珈百璃的堕落', '渊上舞');
INSERT INTO `act` VALUES ('我的英雄学院', '渡边明乃');
INSERT INTO `act` VALUES ('轮回的拉格朗日', '濑户麻沙美');
INSERT INTO `act` VALUES ('魔卡少女樱', '熊井统子');
INSERT INTO `act` VALUES ('攻壳机动队 S.A.C. 2nd GIG', '玉川砂记子');
INSERT INTO `act` VALUES ('神的记事本', '生天目仁美');
INSERT INTO `act` VALUES ('攻壳机动队 S.A.C. 2nd GIG', '田中敦子');
INSERT INTO `act` VALUES ('攻壳机动队STAND ALONE COMPLEX', '田中敦子');
INSERT INTO `act` VALUES ('强袭魔女', '田中理惠');
INSERT INTO `act` VALUES ('NO GAME NO LIFE 游戏人生', '田村由香里');
INSERT INTO `act` VALUES ('太空丹迪', '畠山航辅');
INSERT INTO `act` VALUES ('魔卡少女樱', '皆口裕子');
INSERT INTO `act` VALUES ('星际牛仔', '石冢运升');
INSERT INTO `act` VALUES ('混沌武士', '石冢运升');
INSERT INTO `act` VALUES ('轮回的拉格朗日', '石原夏织');
INSERT INTO `act` VALUES ('太空丹迪', '石塚 運昇');
INSERT INTO `act` VALUES ('我的英雄学院', '石川界人');
INSERT INTO `act` VALUES ('新世纪福音战士', '石田彰');
INSERT INTO `act` VALUES ('CAROLE & TUESDAY', '神谷浩史');
INSERT INTO `act` VALUES ('强袭魔女', '福圆美里');
INSERT INTO `act` VALUES ('新世纪福音战士', '立木文彦');
INSERT INTO `act` VALUES ('机动警察 和平保卫战', '竹中直人');
INSERT INTO `act` VALUES ('NEW GAME!', '竹尾步美');
INSERT INTO `act` VALUES ('刀剑神域', '竹达彩奈');
INSERT INTO `act` VALUES ('太空丹迪', '竹达彩奈');
INSERT INTO `act` VALUES ('邻家的吸血鬼小妹', '筱原侑');
INSERT INTO `act` VALUES ('新世纪福音战士', '绪方惠美');
INSERT INTO `act` VALUES ('魔卡少女樱', '绪方惠美');
INSERT INTO `act` VALUES ('NO GAME NO LIFE 游戏人生', '能登麻美子');
INSERT INTO `act` VALUES ('会长是女仆大人', '花泽香菜');
INSERT INTO `act` VALUES ('命运石之门', '花泽香菜');
INSERT INTO `act` VALUES ('珈百璃的堕落', '花泽香菜');
INSERT INTO `act` VALUES ('星际牛仔', '若本规夫');
INSERT INTO `act` VALUES ('NEW GAME!', '茅野爱衣');
INSERT INTO `act` VALUES ('NO GAME NO LIFE 游戏人生', '茅野爱衣');
INSERT INTO `act` VALUES ('少女与战车', '茅野爱衣');
INSERT INTO `act` VALUES ('樱花庄的宠物女孩', '茅野爱衣');
INSERT INTO `act` VALUES ('神的记事本', '茅野爱衣');
INSERT INTO `act` VALUES ('轮回的拉格朗日', '茅野爱衣');
INSERT INTO `act` VALUES ('数码兽大冒险', '荒木香衣');
INSERT INTO `act` VALUES ('数码兽大冒险', '菊池正美');
INSERT INTO `act` VALUES ('会长是女仆大人', '藤村步');
INSERT INTO `act` VALUES ('爆漫王。', '藤村步');
INSERT INTO `act` VALUES ('轮回的拉格朗日', '藤村步');
INSERT INTO `act` VALUES ('数码兽大冒险', '藤田淑子');
INSERT INTO `act` VALUES ('太空丹迪', '诹访部顺一');
INSERT INTO `act` VALUES ('爆漫王。', '诹访部顺一');
INSERT INTO `act` VALUES ('强袭魔女', '野川樱');
INSERT INTO `act` VALUES ('轮回的拉格朗日', '野水伊织');
INSERT INTO `act` VALUES ('轮回的拉格朗日', '金元寿子');
INSERT INTO `act` VALUES ('NO GAME NO LIFE 游戏人生', '钉宫理惠');
INSERT INTO `act` VALUES ('会长是女仆大人', '铃村健一');
INSERT INTO `act` VALUES ('神的记事本', '铃村健一');
INSERT INTO `act` VALUES ('攻壳机动队 S.A.C. 2nd GIG', '阪修');
INSERT INTO `act` VALUES ('攻壳机动队STAND ALONE COMPLEX', '阪修');
INSERT INTO `act` VALUES ('爆漫王。', '阿部敦');
INSERT INTO `act` VALUES ('数码兽大冒险', '风间勇刀');
INSERT INTO `act` VALUES ('星际牛仔', '高岛雅罗');
INSERT INTO `act` VALUES ('少女与战车', '高桥美佳子');
INSERT INTO `act` VALUES ('樱花庄的宠物女孩', '高森奈津美');
INSERT INTO `act` VALUES ('NEW GAME!', '高田忧希');
INSERT INTO `act` VALUES ('混沌武士', '鹤弘美');

SET FOREIGN_KEY_CHECKS = 1;