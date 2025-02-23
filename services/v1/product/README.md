# PRODUCT SERVICE
----------

The user service handles everything related to products: 

1. Get all products
2. Get Products By Shop ID
3. Add new product
4. Edit a product

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
http://localhost:7004/product
```

This function returns the following JSON response:

```
{
    "products": [
        {
            "productDesc": "Cake made from yam yum yum ah it's nice",
            "productId": 1,
            "productName": "Yam cake",
            "productPhotoURL": "https://s3.ap-southeast-1.amazonaws.com/casafair/product/1/cdd3cdf1189e4672b48b229769e8da9c.jpg",
            "shopId": 1,
            "unitPrice": 3
        },
        {
            "productDesc": "Cake made from pandan leaf",
            "productId": 2,
            "productName": "Pandan Cake",
            "productPhotoURL": "https://s3.ap-southeast-1.amazonaws.com/casafair/product/2/fc84b45d287f426290ceb29246735e30.jpg",
            "shopId": 1,
            "unitPrice": 3
        },
        ...
    ]
}
```

## 1.2 Get Products By Shop ID

**Get list of products of a specific Shop**

**URL** `/product/<shopId>`

**Method** `GET`

Request sample:

```
http://localhost:7004/product/1
```

This function returns the following JSON response:

```
{
"products": [
    {
        "productDesc": "Cake made from yam",
        "productId": 1,
        "productName": "Yam Cake",
        "shopId": 1,
        "unitPrice": 2
    },
    {
        "productDesc": "Cake made from pandan leaf",
        "productId": 2,
        "productName": "Pandan Cake",
        "shopId": 1,
        "unitPrice": 3
    }
],
"status": 200
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
    "product": {
        "productDesc": "cake made from kopi",
        "productId": 8,
        "productName": "coffee cake",
        "shopId": 1,
        "unitPrice": 2.5
    },
    "type": "success"
}
```
> Note: productId is auto-incremented

## 1.4 Edit a product

**Edit an existing product**

**URL** `/product/edit`

**Method** `POST`

Request sample:
```
{
    "productDesc": "Cake made from yam you've got the yummy yum yum",
    "productId": 1,
    "productName": "Yam cake lah!",
    "unitPrice": 3.5
}
```
This function returns the following JSON response:

```
{
    "message": "Successfully updated your product!",
    "product": {
        "productDesc": "Cake made from yam you've got the yummy yum yum",
        "productId": 1,
        "productName": "Yam cake lah!",
        "productPhotoURL": null,
        "shopId": 1,
        "unitPrice": 3.5
    },
    "type": "success"
}
```