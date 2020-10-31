# PAYMENT SERVICE
----------

The payment service handles everything related to payments:

1. Calculating orders
2. Start payment session
3. Process Stripe payment transaction

-----------

> Try to follow API best practices using nouns and not verbs (POST: /user for creating new users, GET: /user for getting user info). See more at https://docs.microsoft.com/en-us/azure/architecture/best-practices/api-design 

**Port** `7006`

All service calls returns the following JSON response:

*Success*

```
{
    "type": "success",
    //whatever the function returns
}
```

*Warning*

```
{
    "type": "warning",
    "message": // whatever message returned
}
```

*Error*

```
{
    "type": "error",
    "message": // whatever message returned,
    "debug": // whatever is returned as Exception (exception message)
}
```

> **NOTE: Boolean values accept 0 as false, and non-zero for true when inserting into the database**

# Calculation

## 1.1 calculatePayment

**Calculates payment of all objects with GST. Accepts either function call or through API calls.**

**URL** `/payment/calculate`

**Method** `POST`

**Parameters** `api_call=True`, `products=""`

Request sample:

```
{
    "products": [
        {
            "productDesc": "cake made from kopi",
            "productId": 8,
            "productName": "coffee cake",
            "shopId": 1,
            "unitPrice": 2.5,
            "quantity": 5
        }
    ]
}
```

This function returns the following JSON response:

```
{
    "amount": 13.375,
    "gst": 0.875,
    "preTax": 12.5
}
```

# Payment

## 1.1 beginPaymentSession

**Begins a payment session that is time-limited.**

**URL** `/payment/session`

**Method** `POST`

Request sample:

```
{
    "products": [
        {
            "productDesc": "cake made from kopi",
            "productId": 8,
            "productName": "coffee cake",
            "shopId": 1,
            "unitPrice": 2.5,
            "quantity": 5
        },
        ...
    ]
}
```

This function returns the following JSON response:

```
{
    "paymentToken": "eyJwcm9kdWN0cyI6IFt7InByb2R1Y3REZXNjIjogImNha2UgbWFkZSBmcm9tIGtvcGkiLCAicHJvZHVjdElkIjogOCwgInByb2R1Y3ROYW1lIjogImNvZmZlZSBjYWtlIiwgInNob3BJZCI6IDEsICJ1bml0UHJpY2UiOiAyLjUsICJxdWFudGl0eSI6IDV9XX0=",
    "type": "success"
}
```

> NOTE: Use this token for payment intent creation

## 1.2 createIntent

**Creates a payment intent from the Stripe API**

> This processes a payment

**URL** `/payment/intent`

**Method** `POST`

Request sample:

```
{
	"paymentToken": "eyJwcm9kdWN0cyI6IFt7InByb2R1Y3REZXNjIjogImNha2UgbWFkZSBmcm9tIGtvcGkiLCAicHJvZHVjdElkIjogOCwgInByb2R1Y3ROYW1lIjogImNvZmZlZSBjYWtlIiwgInNob3BJZCI6IDEsICJ1bml0UHJpY2UiOiAyLjUsICJxdWFudGl0eSI6IDV9XX0="
}
```

This function returns the following JSON response:

```
{
    "amount": 2.14, 
    "gst": 0.14000000000000012, 
    "iat": "Sat, 31 Oct 2020 14:40:45 GMT", 
    "paymentIntentID": "pi_1HiLG5BuBqXcJvpBNwLCXpMl", 
    "pretax": 2.0, 
    "purchasedProducts": [
        {
        "productDesc": "Cake made from yam", 
        "productId": 1, 
        "productName": "Yam Cake", 
        "quantity": 1, 
        "shopId": 1, 
        "unitPrice": 2
        }
    ], 
    "type": "success"
}
```