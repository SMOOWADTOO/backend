# USER SERVICE
----------

The user service handles everything related to products: 

1. Get all products

-----------

> Try to follow API best practices using nouns and not verbs (POST: /user for creating new users, GET: /user for getting user info). See more at https://docs.microsoft.com/en-us/azure/architecture/best-practices/api-design 

**Port** `7004`

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


# Product

## 1.1 Get All Products

**Get list of all products**

**URL** `/product`

**Method** `GET`

Request sample:

```
{

}
```

This function returns the following JSON response:

```
{

}
```

## 1.2 Get Products By Shop ID

**Get list of products of a specific Shop**

**URL** `/product/<shopId>`

**Method** `GET`

Request sample:

```
{
	"shopId": 1,
}
```

This function returns the following JSON response:

```
{
<!-- TODO -->
}
```

## 1.3 Add new product

**A Shop can add new product**

**URL** `/product/add`

**Method** `POST`
Request sample:

```
{
	"shopId": 1,
    "productName": "coffee cake",
    "productDesc": "cake made from kopi",
    "unitPrice": 2.5
}
```
This function returns the following JSON response:

```
{
    "type": "success",
    "product": {
        "shopId": 1,
        "productId": 10 
        "productName": "coffee cake",
        "productDesc": "cake made from kopi",
        "unitPrice": 2.5
    }
}
```
Note: productId is auto-incremented