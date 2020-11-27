# Crypto-script
## Powered by CoinGecko
This script aims to be simple and to be used for any project.
The script simply displays informations about the selected crypto.
## Dependencies
- Python (3.x)
- [coingecko API](https://www.coingecko.com/api)

## How to use
 Clone the repository and configure json settings in crypto_settings.json as follows:

- ### Required
 - `currency`: string ("eur", "usd",...)
- ### Optional
 - `polybar`: bool (set to true for 100% compatibility with polybar)
 - `balance`: int (amount of coins you have)
 - `balance_precision`: int (digits after decimal)
 - `name`: bool (true or false)
 - `image`: bool
 - `current_price`: bool
 - `price_precision`: int
 - `market_cap`: bool
 - `market_cap_rank`: bool
 - `fully_diluted_valuation`: bool
 - `total_volume`: bool
 - `high_24h`: bool
 - `low_24h`: bool
 - `price_change_24h`: bool
 - `price_change_24h_precision`: int (digits after decimal)
 - `price_change_percentage_24h`: bool
 - `price_change_percentage_24h_precision`: int (digits after decimal)
 - `market_cap_change_24h`: bool
 - `market_cap_change_percentage_24h`: bool
 - `circulating_supply`: bool
 - `total_supply`: bool
 - `max_supply`: bool
 - `ath`: bool
 - `ath_change_percentage`: bool
 - `ath_date`: bool
 - `atl`: bool
 - `atl_change_percentage`: bool
 - `atl_date`: bool
 - `roi`: bool
 - `last_updated`: bool

### Example
``` json
{
    "polybar": true,
    "url": "https://api.coingecko.com/api/v3/coins/markets?",
    "currency": "eur",
    "crypto-list":[
        {
            "id": "bitcoin",
            "symbol": true,
            "current_price": true,
            "price_precision": 0
        },
        {
            "id": "ripple",
            "symbol": true,
            "current_price": true,
            "price_precision": 3,
            "balance": 10,
            "balance_precision": 0,
            "price_change_percentage_24h": true,
            "price_change_percentage_24h_precision": 2
        }
    ]
}
```
### Use with Polybar
Set polybar value to true in crypto_settings.json and add the following config in polybar config:
``` ini
[module/crypto]
type = custom/script
interval = 1
exec = python /path/to/crypto/script
```
For more information on values(like available currencies or available crypto) or anything else, take a look [here](https://www.coingecko.com/api).
> **Important note**: keep in mind that the coingecko API has a limit of 100 requests per minute so an interval of 0.5(120 requests per minute) in polybar will not work but an interval of 1(60 requests per minute) is perfectly fine.
