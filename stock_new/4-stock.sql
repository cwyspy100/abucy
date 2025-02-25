-- 创建数据库
CREATE DATABASE IF NOT EXISTS wealth_data DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE wealth_data;

-- 证券类型维护表
CREATE TABLE security_type (
    id BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
    type_code VARCHAR(2) NOT NULL COMMENT '类型代码',
    type_name VARCHAR(50) NOT NULL COMMENT '类型名称',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted TINYINT(1) NOT NULL DEFAULT 0 COMMENT '删除标记',
    PRIMARY KEY (id),
    UNIQUE KEY uk_type_code (type_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='证券类型维护表';

-- 市场维护表
CREATE TABLE market (
    id BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
    market_code VARCHAR(2) NOT NULL COMMENT '市场代码',
    market_name VARCHAR(50) NOT NULL COMMENT '市场名称',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted TINYINT(1) NOT NULL DEFAULT 0 COMMENT '删除标记',
    PRIMARY KEY (id),
    UNIQUE KEY uk_market_code (market_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='市场维护表';

-- 行业分类表
CREATE TABLE industry (
    id BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
    industry_l1_code VARCHAR(3) NOT NULL COMMENT '一级行业代码',
    industry_l1_name VARCHAR(50) NOT NULL COMMENT '一级行业名称',
    industry_l2_code VARCHAR(6) NOT NULL COMMENT '二级行业代码',
    industry_l2_name VARCHAR(50) NOT NULL COMMENT '二级行业名称',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted TINYINT(1) NOT NULL DEFAULT 0 COMMENT '删除标记',
    PRIMARY KEY (id),
    UNIQUE KEY uk_industry_l2_code (industry_l2_code),
    KEY idx_industry_l1 (industry_l1_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='行业分类表';

-- 证券基本信息表
drop table security_info;
-- 证券基本信息表
CREATE TABLE security_info (
    id BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
    security_code VARCHAR(20) NOT NULL COMMENT '证券代码',
    security_name VARCHAR(100) NOT NULL COMMENT '证券名称',
    market_code VARCHAR(2) NOT NULL COMMENT '市场代码',
    type_code VARCHAR(2) NOT NULL COMMENT '证券类型代码',
		industry_1 VARCHAR(50) COMMENT '所属行业',
    industry_2 VARCHAR(50) COMMENT '细分行业',
    listing_date DATE COMMENT '上市日期',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted TINYINT(1) NOT NULL DEFAULT 0 COMMENT '删除标记',
    PRIMARY KEY (id),
    UNIQUE KEY uk_security_code (security_code),
    KEY idx_market_type (market_code, type_code),
    KEY idx_industry (industry_1)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='证券基本信息表';

-- 证券日线行情表
CREATE TABLE stock_daily (
    id BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
    security_code VARCHAR(20) NOT NULL COMMENT '证券代码',
    trade_date DATE NOT NULL COMMENT '交易日期',
    open_price DECIMAL(20,4) NOT NULL COMMENT '开盘价',
    close_price DECIMAL(20,4) NOT NULL COMMENT '收盘价',
    high_price DECIMAL(20,4) NOT NULL COMMENT '最高价',
    low_price DECIMAL(20,4) NOT NULL COMMENT '最低价',
    volume BIGINT NOT NULL COMMENT '成交量',
    amount DECIMAL(20,4) NOT NULL COMMENT '成交额',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted TINYINT(1) NOT NULL DEFAULT 0 COMMENT '删除标记',
    PRIMARY KEY (id),
    UNIQUE KEY uk_security_trade (security_code, trade_date),
    KEY idx_trade_date (trade_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
PARTITION BY LIST COLUMNS(security_code) COMMENT='证券日线行情表';

-- 财务数据表
CREATE TABLE stock_financial (
    id BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
    security_code VARCHAR(20) NOT NULL COMMENT '证券代码',
    report_date DATE NOT NULL COMMENT '报告期',
    revenue DECIMAL(20,4) COMMENT '营业收入(元)',
    net_profit DECIMAL(20,4) COMMENT '净利润(元)',
    eps DECIMAL(10,4) COMMENT '每股收益(元)',
    roe DECIMAL(10,4) COMMENT '净资产收益率(%)',
    pe_ratio DECIMAL(10,4) COMMENT '市盈率',
    pb_ratio DECIMAL(10,4) COMMENT '市净率',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted TINYINT(1) NOT NULL DEFAULT 0 COMMENT '删除标记',
    PRIMARY KEY (id),
    UNIQUE KEY uk_security_report (security_code, report_date),
    KEY idx_report_date (report_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='财务数据表';

-- 技术指标表
CREATE TABLE technical_indicator (
    id BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
    security_code VARCHAR(20) NOT NULL COMMENT '证券代码',
    trade_date DATE NOT NULL COMMENT '交易日期',
    ma5 DECIMAL(20,4) COMMENT '5日均线',
    ma10 DECIMAL(20,4) COMMENT '10日均线',
    ma20 DECIMAL(20,4) COMMENT '20日均线',
    ma60 DECIMAL(20,4) COMMENT '60日均线',
    ma120 DECIMAL(20,4) COMMENT '120日均线',
    rsi6 DECIMAL(10,4) COMMENT '6日RSI',
    rsi12 DECIMAL(10,4) COMMENT '12日RSI',
    rsi24 DECIMAL(10,4) COMMENT '24日RSI',
    volume_ma5 BIGINT COMMENT '5日成交量均线',
    volume_ma10 BIGINT COMMENT '10日成交量均线',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted TINYINT(1) NOT NULL DEFAULT 0 COMMENT '删除标记',
    PRIMARY KEY (id),
    UNIQUE KEY uk_security_trade (security_code, trade_date),
    KEY idx_trade_date (trade_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='技术指标表';

drop table stock_pool
-- 创建股票池表
CREATE TABLE IF NOT EXISTS `stock_pool` (
    `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
    `security_code` varchar(20) NOT NULL COMMENT '股票代码',
    `security_name` varchar(50) NOT NULL COMMENT '股票名称',
    `year_start_price` decimal(10,2) NOT NULL COMMENT '年初价格',
    `current_price` decimal(10,2) default 0.00 COMMENT '当前价格',
    `year_change_rate` decimal(10,2) default 0.00 COMMENT '年度涨跌幅(%)',
    `created_at` datetime NOT NULL COMMENT '创建时间',
    `updated_at` datetime NOT NULL COMMENT '更新时间',
    `deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除(0-未删除，1-已删除)',
    PRIMARY KEY (`id`),
    KEY `idx_security_code` (`security_code`),
    KEY `idx_year_change_rate` (`year_change_rate`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='股票池表';

-- 插入基础数据
INSERT INTO security_type (type_code, type_name) VALUES
('01', '股票'),
('02', '基金'),
('03', '期货'),
('04', 'ETF');

INSERT INTO market (market_code, market_name) VALUES
('CN', 'A股市场'),
('HK', '港股市场'),
('US', '美股市场');

INSERT INTO industry (industry_l1_code, industry_l1_name, industry_l2_code, industry_l2_name) VALUES
('A01', '信息技术', 'A0101', '软件服务'),
('A01', '信息技术', 'A0102', '硬件设备'),
('B01', '金融', 'B0101', '银行'),
('B01', '金融', 'B0102', '证券');