-- 创建股票池表
CREATE TABLE IF NOT EXISTS `stock_pool` (
    `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
    `security_code` varchar(20) NOT NULL COMMENT '股票代码',
    `security_name` varchar(50) NOT NULL COMMENT '股票名称',
    `year_start_price` decimal(10,2) NOT NULL COMMENT '年初价格',
    `current_price` decimal(10,2) NOT NULL COMMENT '当前价格',
    `year_change_rate` decimal(10,2) NOT NULL COMMENT '年度涨跌幅(%)',
    `created_at` datetime NOT NULL COMMENT '创建时间',
    `updated_at` datetime NOT NULL COMMENT '更新时间',
    `deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除(0-未删除，1-已删除)',
    PRIMARY KEY (`id`),
    KEY `idx_security_code` (`security_code`),
    KEY `idx_year_change_rate` (`year_change_rate`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='股票池表';