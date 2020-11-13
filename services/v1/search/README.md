# SEARCH SERVICE
----------

The service handles everything related to searching: 

1. Search for Products
2. Search for Shops

-----------

> Try to follow API best practices using nouns and not verbs (POST: /user for creating new users, GET: /user for getting user info). See more at https://docs.microsoft.com/en-us/azure/architecture/best-practices/api-design 

**Port** `7009`

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


# Search

## 1.1 Search for Product

**Search for products with a term query provided**

**URL** `/search/product/<string:term>`

**Method** `GET`

Request sample:

```
http://localhost:7009/search/product/yam
```

This function returns the following JSON response:

```
[
    {
        "productDesc": "Cake made from yam yum yum ah it's nice",
        "productId": 1,
        "productName": "Yam cake",
        "productPhotoURL": "https://s3.ap-southeast-1.amazonaws.com/casafair/product/1/cdd3cdf1189e4672b48b229769e8da9c.jpg",
        "shopId": 1,
        "unitPrice": 3
    }
]
```

## 1.2 Search for Shop

**Search for shops with a term query provided**

**URL** `/search/shop/<string:term>`

**Method** `GET`

Request sample:

```
http://localhost:7009/search/shop/store
```

This function returns the following JSON response:

```
[
    {
        "address": "Office of the President of the Republic of Singapore\r\nOrchard Road, Singapore 238823",
        "contactNo": "65 31234567",
        "createdAt": "Thu, 08 Oct 2020 14:50:19 GMT",
        "email": "istana_feedback@istana.gov.sg",
        "shopDesc": "The one and only Shao Rou store. You may ask, what is shao rou? It is roasted meat. Try one of our delicious shao rou today, we have chicken rice and char siew noodles, more stuff in the future ! ",
        "shopId": 2,
        "shopImageURL": "https://s3.ap-southeast-1.amazonaws.com/casafair/user/The Shao Rou Store/f3c96e34eb2e40b98182872822dbffeb.jpg",
        "shopName": "The Shao Rou Store",
        "updatedAt": "Mon, 09 Nov 2020 08:01:36 GMT",
        "username": "bossman",
        "website": "https://www.istana.gov.sg/Pages/Contact"
    },
    {
        "address": "26 JALAN BERSEH KELANTAN COURT SINGAPORE 200026",
        "contactNo": "65 123453333",
        "createdAt": "Mon, 09 Nov 2020 07:47:24 GMT",
        "email": "darrenshop@mail.com",
        "shopDesc": "dklskdl",
        "shopId": 20,
        "shopImageURL": null,
        "shopName": "darren png's store",
        "updatedAt": "Mon, 09 Nov 2020 07:47:24 GMT",
        "username": "Dorren",
        "website": "oiidjioajdadj.com"
    }
]
```