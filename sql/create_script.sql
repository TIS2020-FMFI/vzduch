DROP TABLE IF EXISTS si;
CREATE TABLE si(
    id int(10) PRIMARY KEY NOT NULL,
    ci smallint(6) NOT NULL,
    ii bigint(20) NOT NULL,
    name varchar(80),
    cccc char(4),
    cc char(2),
    iso_cc int(11),
    lat double,
    lon double,
    elev double,
    info char(32),
    vtime datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
    mtime datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
    changed_id int(11),
    changes varchar(32),
    ue tinyint(1) DEFAULT 0
);

DROP TABLE IF EXISTS obs_nmsko_1h;
CREATE TABLE obs_nmsko_1h(
    obs_id bigint(20) NOT NULL,
    si_id bigint(20)  NOT NULL,
    date datetime  NOT NULL,
    ta_2m float,
    pa_avg float,
    rh_avg float,
    ws_avg float,
    wd_avg float,
    ws_max float,
    wd_ws_max float,
    pr_sum float,
    HG float,
    PM10 float,
    PM2_5 float,
    SO2 float,
    NO float,
    NO2 float,
    NOx float,
    CO float,
    BEN float,
    H2S float,
    O3 float,
    CONSTRAINT PK PRIMARY KEY (si_id, date),
    FOREIGN KEY (si_id) REFERENCES si(id)
);