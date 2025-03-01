## 题目

有如下数据记录直播平台主播上播及下播时间，根据该数据计算出平台每分钟最大直播人数。

```text
+----------+----------------------+----------------------+
| user_id  |      start_time      |       end_time       |
+----------+----------------------+----------------------+
| 1        | 2024-04-29 01:00:00  | 2024-04-29 02:01:05  |
| 2        | 2024-04-29 01:05:00  | 2024-04-29 02:03:18  |
| 3        | 2024-04-29 02:00:00  | 2024-04-29 04:03:22  |
| 4        | 2024-04-29 03:15:07  | 2024-04-29 04:33:21  |
| 5        | 2024-04-29 03:34:16  | 2024-04-29 06:10:45  |
| 6        | 2024-04-29 05:22:00  | 2024-04-29 07:01:08  |
| 7        | 2024-04-29 06:11:03  | 2024-04-29 09:26:05  |
| 3        | 2024-04-29 08:00:00  | 2024-04-29 12:34:27  |
| 1        | 2024-04-29 11:00:00  | 2024-04-29 16:03:18  |
| 8        | 2024-04-29 15:00:00  | 2024-04-29 17:01:05  |
+----------+----------------------+----------------------+
```

## 处理逻辑

查询每分钟最大在线人数，那么我们就需要得到主播在时间内的波动情况。也就是说，我们需要知道每个时间正在进行直播的主播数量。

 我们可以新开一数据列`act` 。观察数据不难发现，在`start_time`表示主播开始直播，那么`act`可以赋值为`1`，`end_time`表示主播不直播，`act`可以赋值为`-1`，这样就可以知道主播人数的波动情况。

但这里我们**需要注意**的是，如果某一个分钟内无任何操作记录，则不会出现该分钟的数据，那么我们自然就统计不到，所以我们需要额外的生成这些记录。然后将这些记录的数据列`user_id,act` 赋值为`0`，保证不会污染到真实的数据。

操作如下：

1. 首先对原始数据进行处理，生成主播上下播的日志数据，同时增加人数变化字段，主播上播为1，主播下播-1。新数据包含` user_id`,`action_time`,`act`

2. 生成`0~24*60-1`条记录数据

3. 根据2生成每分钟一条记录的心跳记录，心跳记录`act_cnt= 0`,代表没有主播上播，也没有主播下播。

   ```sql
   with t1 as (
     select
       user_id,
       start_time as act_time,
       1 as act
     from
       t4_livestream_log
     union all
     select
       user_id,
       end_time as act_time,
       -1 as act
     from
       t4_livestream_log
     union all
     select 
       0 as user_id,
       -- 要注意如何生成数据：24*60*60，要精确到秒级
       from_unixtime(unix_timestamp('2024-04-29', 'yyyy-MM-dd') + id*60, 'yyyy-MM-dd HH:mm:ss') as act_time,
       0 as act
       -- 需要注意posexplode的用法
       from (select posexplode(split(space(24*60), ' ' )) as (id, value)) t
   )
   ```

4. 汇总所有数据之后，对`act_cnt`累积求和，然后求出每分钟的最大值即可

需要注意到的是：原始记录的时间粒度是秒级，那么我们最后求每分钟最大值时，需要改变时间颗粒度, 改为分钟级

```sql
t2 as (
select
   user_id,
   act_time,
   act,
   sum(act) over(order by act_time) as people_num
   from t1
)
select  date_format(act_time,'yyyy-MM-dd HH:mm'), max(people_num)
from t2
group by date_format(act_time,'yyyy-MM-dd HH:mm');
```

全部语句如下：

```SQL
with t1 as (
  select
    user_id,
    start_time as act_time,
    1 as act
  from
    t4_livestream_log
  union all
  select
    user_id,
    end_time as act_time,
    -1 as act
  from
    t4_livestream_log
  union all
  select 
    0 as user_id,
    from_unixtime(unix_timestamp('2024-04-29', 'yyyy-MM-dd') + id*60, 'yyyy-MM-dd HH:mm:ss') as act_time,
    0 as act
    from (select posexplode(split(space(24*60), ' ' )) as (id, value)) t
),
t2 as (
select
   user_id,
   act_time,
   act,
   sum(act) over(order by act_time) as people_num
   from t1
)
select  date_format(act_time,'yyyy-MM-dd HH:mm'), max(people_num)
from t2
group by date_format(act_time,'yyyy-MM-dd HH:mm');
```

## 插入语句

```sql
CREATE TABLE IF NOT EXISTS t4_livestream_log (
    user_id INT, -- 主播ID
    start_time STRING, -- 开始时间
    end_time STRING -- 结束时间
);

insert into t4_livestream_log(user_id, start_time, end_time) values 
(1,'2024-04-29 01:00:00','2024-04-29 02:01:05'),
(2,'2024-04-29 01:05:00','2024-04-29 02:03:18'),
(3,'2024-04-29 02:00:00','2024-04-29 04:03:22'),
(4,'2024-04-29 03:15:07','2024-04-29 04:33:21'),
(5,'2024-04-29 03:34:16','2024-04-29 06:10:45'),
(6,'2024-04-29 05:22:00','2024-04-29 07:01:08'),
(7,'2024-04-29 06:11:03','2024-04-29 09:26:05'),
(3,'2024-04-29 08:00:00','2024-04-29 12:34:27'),
(1,'2024-04-29 11:00:00','2024-04-29 16:03:18'),
(8,'2024-04-29 15:00:00','2024-04-29 17:01:05');
```

