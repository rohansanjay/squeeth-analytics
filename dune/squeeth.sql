WITH oSQTH_PRICE as (
    Select 
        *
    from dex."view_token_prices" d
    left join erc20.tokens e on d.contract_address = e.contract_address
    WHERE symbol = 'oSQTH'
),

NORM_FACTOR as (
    SELECT 
        date_trunc('hour', to_timestamp(o."timestamp")) as Day, 
        (o."newNormFactor" / 1000000000000000000) as NormalizationFactor, 
        (o."oldNormFactor" / 1000000000000000000) AS OldNormalizationFactor,
        (1 - exp(ln(o."newNormFactor"/o."oldNormFactor") * 1512000 / (o."timestamp" - o."lastModificationTimestamp") / 17.5)) as funding_rate
    FROM opynfinance."Controller_evt_NormalizationFactorUpdated" o
),

JOINED as (
    Select 
        normalizationfactor, hour, median_price, funding_rate
    from 
        NORM_FACTOR
    
    RIGHT JOIN oSQTH_PRICE ON NORM_FACTOR.day=oSQTH_PRICE.hour
),

grouped as (
    select hour,
          median_price,
          normalizationfactor,
          count(normalizationfactor) over (order by hour) as _grp,
          funding_rate,
          count(funding_rate) over (order by hour) as __grp
    from JOINED
),

filled_group as (
    select hour,
        median_price,
        normalizationfactor,
       _grp,
       first_value(normalizationfactor) over (partition by _grp order by hour) as normalization_factor,
       first_value(funding_rate) over (partition by __grp order by hour) as funding_rate
    from grouped
),

CLEANED as (
    select DISTINCT (hour),
          median_price,
          normalization_factor,
          funding_rate
    from filled_group
),

COMPUTED as (
    Select 
        hour, 
        normalization_factor, 
        funding_rate,
        median_price as oSQTH_price, 
        CLEANED.median_price / CLEANED.normalization_factor * 10000 as squeeth_price
    from CLEANED
),

ETH_PRICES as (
    Select 
        hour as eth_hour, 
        median_price as eth_price, 
        d."contract_address"
    from dex."view_token_prices" d
    left join erc20.tokens e on d.contract_address = e.contract_address
    WHERE symbol = 'ETH' and d.contract_address = '\x0000000000000000000000000000000000000000'
    
    and hour > '2022-01-11 06:00'
),

COMBINED_ETH as (
    Select * from COMPUTED
    INNER JOIN ETH_PRICES on ETH_PRICES.eth_hour = COMPUTED.hour
)

select
    hour, 
    normalization_factor,
    funding_rate,
    osqth_price,
    squeeth_price,
    eth_price,
    eth_price ^ 2 as eth_sqaured_price,
    corr(funding_rate, osqth_price) OVER(ORDER BY hour
        ROWS BETWEEN 23 PRECEDING AND CURRENT ROW )
        as rolling_corr_funding_osqth,
    corr(eth_price, squeeth_price) OVER(ORDER BY hour
        ROWS BETWEEN 23 PRECEDING AND CURRENT ROW )
        as rolling_corr_eth_squeeth
from COMBINED_ETH