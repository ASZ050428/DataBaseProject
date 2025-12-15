-- 创建用户表
CREATE TABLE `users` (
  `USER_ID` int unsigned NOT NULL AUTO_INCREMENT,
  `USER_NAME` varchar(32) COLLATE utf8mb4_general_ci NOT NULL,
  `PASSWORD` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`USER_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 创建歌手表
CREATE TABLE `artists` (
  `ARTIST_ID` int unsigned NOT NULL AUTO_INCREMENT,
  `ARTIST_NAME` varchar(32) COLLATE utf8mb4_general_ci NOT NULL,
  `REGION` varchar(32) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `BIO` text COLLATE utf8mb4_general_ci,
  PRIMARY KEY (`ARTIST_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 创建专辑表
CREATE TABLE `albums` (
  `ALBUM_ID` int unsigned NOT NULL AUTO_INCREMENT,
  `TITLE` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `RELEASE_DATE` date DEFAULT NULL,
  PRIMARY KEY (`ALBUM_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 创建歌曲表
CREATE TABLE `songs` (
  `SONG_ID` int unsigned NOT NULL AUTO_INCREMENT,
  `ALBUM_ID` int unsigned DEFAULT NULL,
  `SONG_NAME` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `DURATION` int unsigned NOT NULL,
  `AUDIO_URL` int unsigned NOT NULL,
  `LYRICS` text COLLATE utf8mb4_general_ci,
  `RELEASE_DATE` date DEFAULT NULL,
  PRIMARY KEY (`SONG_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 创建歌曲-歌手关联表（多对多关系）
CREATE TABLE `artist_song_relation` (
  `SONG_ID` int unsigned NOT NULL,
  `ARTIST_ID` int unsigned NOT NULL,
  PRIMARY KEY (`SONG_ID`,`ARTIST_ID`)
) ENGINE=InnoDB
 DEFAULT CHARSET=utf8mb4 
 COLLATE=utf8mb4_general_ci;

-- 创建收藏列表表
CREATE TABLE `user_favourite_songs_list` (
  `LIST_ID` int unsigned NOT NULL AUTO_INCREMENT,
  `LIST_NAME` varchar(32) COLLATE utf8mb4_general_ci NOT NULL,
  `CREATE_TIME` datetime NOT NULL,
  PRIMARY KEY (`LIST_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 创建评论表
CREATE TABLE `comments` (
  `COMMENTS_ID` int unsigned NOT NULL AUTO_INCREMENT,
  `USER_ID` int unsigned NOT NULL,
  `RELEASE_TIME` datetime NOT NULL,
  `SONG_ID` int unsigned NOT NULL,
  `CONTENTS` text COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`COMMENTS_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 创建收藏列表，歌曲关联表
CREATE TABLE `user_song_list_relation` (
  `LIST_ID` int unsigned NOT NULL,
  `SONG_ID` int unsigned NOT NULL,
  `ADD_TIME` datetime NOT NULL,
  PRIMARY KEY (`LIST_ID`,`SONG_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 创建用户，收藏列表关联表
CREATE TABLE `user_list_relation` (
  `USER_ID` int unsigned NOT NULL,
  `LIST_ID` int unsigned NOT NULL,
  PRIMARY KEY (`USER_ID`,`LIST_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 创建用户，评论关联表
CREATE TABLE `user_comment_relation` (
  `USER_ID` int unsigned NOT NULL,
  `COMMENT_ID` int unsigned NOT NULL,
  PRIMARY KEY (`USER_ID`,`COMMENT_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 创建用户关注歌手关联表
CREATE TABLE `user_follow_artists` (
  `USER_ID` int unsigned NOT NULL,
  `ARTIST_ID` int unsigned NOT NULL,
  `FOLLOW_TIME` datetime NOT NULL,
  PRIMARY KEY (`USER_ID`,`ARTIST_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 创建用户收藏专辑关联表
CREATE TABLE `user_favourite_albums` (
  `USER_ID` int unsigned NOT NULL,
  `ALBUM_ID` int unsigned NOT NULL,
  `COLLECT_TIME` datetime NOT NULL,
  PRIMARY KEY (`USER_ID`,`ALBUM_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 创建歌手专辑关联表
CREATE TABLE `artist_album_relation` (
  `ARTIST_ID` int unsigned NOT NULL,
  `ALBUM_ID` int unsigned NOT NULL,
  PRIMARY KEY (`ARTIST_ID`,`ALBUM_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 用户称为歌手关联表
CREATE TABLE `user_become_artist` (
  `USER_ID` int unsigned NOT NULL,
  `ARTIST_ID` int unsigned NOT NULL,
  PRIMARY KEY (`USER_ID`,`ARTIST_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;