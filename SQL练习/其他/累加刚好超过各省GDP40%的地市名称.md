# 题目

现有各省地级市的gdp数据,求从高到底累加刚好超过各省GDP40%的地市名称，临界地市也需要。 例如:

浙江省的杭州24% 宁波 20% ,杭州+宁波=44% 大于40% 取出杭州、宁波

江苏省的苏州19% 南京 14% 无锡 12%，苏州+南京=33% ，苏州+南京+无锡=45%，取出 苏州、南京、无锡

```text
+-------+-------+-----------+
| prov  | city  |  gdp_amt  |
+-------+-------+-----------+
| 浙江    | 杭州    | 20059.00  |
| 浙江    | 宁波    | 16452.80  |
| 浙江    | 温州    | 8730.60   |
| 浙江    | 绍兴    | 7791.00   |
| 浙江    | 嘉兴    | 7062.45   |
| 浙江    | 台州    | 6240.68   |
| 浙江    | 金华    | 6011.27   |
| 浙江    | 湖州    | 4015.10   |
| 浙江    | 衢州    | 2125.20   |
| 浙江    | 舟山    | 2100.80   |
| 浙江    | 丽水    | 1964.40   |
| 江苏    | 苏州    | 24653.37  |
| 江苏    | 南京    | 17421.40  |
| 江苏    | 无锡    | 15456.19  |
| 江苏    | 南通    | 11813.27  |
| 江苏    | 常州    | 10116.36  |
| 江苏    | 徐州    | 8900.44   |
| 江苏    | 扬州    | 7423.26   |
| 江苏    | 盐城    | 7403.87   |
| 江苏    | 泰州    | 6731.66   |
| 江苏    | 镇江    | 5264.07   |
| 江苏    | 淮安    | 5015.06   |
| 江苏    | 宿迁    | 4398.07   |
| 江苏    | 连云港   | 4363.61   |
+-------+-------+-----------+
```

# 思路

我们可以求每个城市在自己省份的GDP占比和每个城市从低到高累加起来的GDP占比。

```sql
select prov,
       city,
       gdp_amt,
       total_gpd_amt,
       ord_sum_gdp_amt,
       round(gdp_amt / total_gpd_amt,2) as city_percnt,
       round(ord_sum_gdp_amt / total_gpd_amt,2) as lj_city_percent
from (select prov,
             city,
             gdp_amt,
             sum(gdp_amt) over (partition by prov)                       as total_gpd_amt,
             sum(gdp_amt) over (partition by prov order by gdp_amt desc) as ord_sum_gdp_amt
      from t1_gdp) t
```

由于要求包含临界值，直接求取十分不方便，所以可以改变策略，求取从低到高累加求和`< 60%`的记录，然后和原表连接取补集，就能够用得到结果。
为什么要求补集？
因为如果直接筛选出累计GDP超过40%的城市，在实际操作中会有点复杂，因为**需要同时包含累计值刚好超过40%的那个临界城市。**
所以我们**先找出累计GDP占比小于60%的城市**：这样做的原因是，如果累计占比小于60%，**那么剩下的部分必然超过40%。**
也就是说，那些不在累计占比小于60%列表中的城市，就是我们需要的累计GDP超过40%的城市。

```SQL
-- 计算每个省份的总GDP和每个城市的累加GDP
with t1 as (
     select 
        prov,
        city,
        gdp_amt,
        sum(gdp_amt) over(partition by prov) as total_amt, -- 省份总GDP
        sum(gdp_amt) over(partition by prov order by gdp_amt desc) as accum_amt -- 按GDP降序累加
     from t0_gdp
),
-- 筛选累加占比小于60%的城市
t2 as (
     select
        prov,
        city,
        gdp_amt,
        -- 单城市占比
        round(gdp_amt / total_amt,2) as city_percent, 
        -- 累加占比
        round(accum_amt / total_amt,2) as accum_percent 
     from t1
    -- 累加占比小于60%
     where round(accum_amt / total_amt,2) < 0.6 
)
-- 通过补集获取累加占比超过40%的城市
select 
    t0.prov,
    t0.city 
from t0_gdp t0
left join t2 
on t0.prov = t2.prov
and t0.city = t2.city
where t2.city is null; -- 累加占比超过40%的城市
```

# 结果

| prov | city |
| ---- | ---- |
| 浙江 | 杭州 |
| 浙江 | 宁波 |
| 江苏 | 苏州 |
| 江苏 | 南京 |
| 江苏 | 无锡 |