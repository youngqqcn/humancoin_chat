CREATE TABLE `user_integral_wallet` (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'PK',
  `user_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户ID',
  `balance` bigint DEFAULT '0' COMMENT '余额',
  `lock_balance` bigint DEFAULT '0' COMMENT '锁定余额',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `version` int DEFAULT NULL COMMENT '版本号',
  `remark` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `uid_unq` (`user_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='用户积分钱包';

CREATE TABLE `user_point_record` (
  `id` varchar(32) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'PK',
  `biz_id` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '业务ID',
  `trade_type` int DEFAULT NULL COMMENT '交易类型1活动奖励2游戏参与3游戏奖励',
  `user_id` varchar(32) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '用户ID',
  `amount` bigint DEFAULT NULL COMMENT '数量',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='用户积分记录';