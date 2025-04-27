
-- import 

with source as (
   select
         "Date",
         "Close",
         "simbolo"
   from {{ source ('dbsales1', 'commodities') }}
),

-- renamed

renamed as (
      select
            cast("Date" as date) as data,
            "Close" as valor_fechamento,
            "simbolo"
      from source
)

-- select
select * from renamed