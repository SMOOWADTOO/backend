# SHOP SERVICE
----------

The shop service handles everything related to shops: 

1. Get all shops
2. Get Shop By Shop ID
3. Create new shop
4. Edit shop

-----------

> Try to follow API best practices using nouns and not verbs (POST: /user for creating new users, GET: /user for getting user info). See more at https://docs.microsoft.com/en-us/azure/architecture/best-practices/api-design 

**Port** `7002`

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


# Shop

## 1.1 Get All Shops

**Get list of all shops**

**URL** `/shop/all`

**Method** `GET`

Request sample:

```
http://localhost:7002/shop/all
```

This function returns the following JSON response:

```
{
  "shops": [
    {
      "address": "address", 
      "contactNo": "91234567", 
      "createdAt": "Thu, 08 Oct 2020 22:45:31 GMT", 
      "email": "test@email.com", 
      "shopDesc": "Description", 
      "shopId": 1, 
      "shopImageURL": "hello.url.com", 
      "shopName": "Hello", 
      "updatedAt": "Fri, 09 Oct 2020 17:50:54 GMT", 
      "username": "user1", 
      "website": "abc.com"
    }
  ]
}
```

## 1.2 Get Shop By Shop ID

**Get shop details of a specific shop**

**URL** `/shop/<shopId>`

**Method** `GET`

Request sample:

```
http://localhost:7002/shop/1
```

This function returns the following JSON response:

```
{
  "shop": {
      "address": "address", 
      "contactNo": "91234567", 
      "createdAt": "Thu, 08 Oct 2020 22:45:31 GMT", 
      "email": "test@email.com", 
      "shopDesc": "Description", 
      "shopId": 1, 
      "shopImageURL": "hello.url.com", 
      "shopName": "Hello", 
      "updatedAt": "Fri, 09 Oct 2020 17:50:54 GMT", 
      "username": "user1", 
      "website": "abc.com"
    }, 
  "type": "success"
}
```

## 1.3 Create new shop

**User create a new shop**

**URL** `/shop/create`

**Method** `POST`
Request sample:
```
http://localhost:7002/shop/create
```

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

## 1.4 Edit shop details

**User can edit a shop details**

**URL** `/shop/edit`

**Method** `POST`
Request sample:
```
http://localhost:7002/shop/edit
```
```
{
	"shopId": 1,
    "username": "abc",
    "shopName": "hello",
    "address": "address", 
    "contactNo": "91234567", 
    "email": "test@email.com", 
    "shopDesc": "Description", 
    "shopImageURL": "hello.url.com", 
    "shopName": "Hello", 
    "username": "user1", 
    "website": "abc.com"
}
```
Compulsory fields: shopId, username

Non-editable fields: shopId, username, createdAt, updatedAt

This function returns the following JSON response:

```
{
    "shop": {
        "shopId": 1,
        "username": "abc",
        "shopName": "hello",
        "address": "address", 
        "contactNo": "91234567", 
        "createdAt": "Thu, 08 Oct 2020 22:45:31 GMT", 
        "email": "test@email.com", 
        "shopDesc": "Description", 
        "shopImageURL": "hello.url.com", 
        "shopName": "Hello", 
        "updatedAt": "Fri, 09 Oct 2020 17:50:54 GMT", 
        "username": "user1", 
        "website": "abc.com"
    },
    "type": "success"
}
```
Note: shopId is auto-incremented