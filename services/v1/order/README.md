# ORDER SERVICE
----------

The order service handles everything related to orders: 

1. Get all orders
2. Get orders By shopId
3. Get orders By username
4. Create new order
5. Edit order

-----------

> Try to follow API best practices using nouns and not verbs (POST: /user for creating new users, GET: /user for getting user info). See more at https://docs.microsoft.com/en-us/azure/architecture/best-practices/api-design 

**Port** `7003`

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


# Order

## 1.1 Get All Orders

**Get list of all orders**

**URL** `/order/all`

**Method** `GET`

Request sample:

```
http://localhost:7003/order/all
```

This function returns the following JSON response:

```
{
  "orderDetails": [
    {
        "createdAt": "Fri, 09 Oct 2020 15:37:35 GMT", 
        "orderDetailId": 1, 
        "orderId": 1, 
        "price": 2.5, 
        "productId": 1, 
        "quantity": 3, 
        "total": 7.5
    }
  ], 
  "orders": [
    {
        "completed": false, 
        "createdAt": "Fri, 09 Oct 2020 15:35:22 GMT", 
        "deliveryAddress": "SMU SIS", 
        "orderId": 1, 
        "paid": false, 
        "pickupAddress": "pickup", 
        "username": "user1"
    }
  ],
  "type": "success"
}
```

## 1.2 Get order By Shop ID

**Get all order details for a specific shop**

**URL** `/order/<shopId>`

**Method** `GET`

Request sample:

```
http://localhost:7003/order/1
```

This function returns the following JSON response:

```
{
  "orderDetails": [
    {
        "createdAt": "Fri, 09 Oct 2020 15:37:35 GMT", 
        "orderDetailId": 1, 
        "orderId": 1, 
        "price": 2.5, 
        "productId": 1, 
        "quantity": 3, 
        "total": 7.5
    }
  ], 
  "orders": [
    {
        "completed": false, 
        "createdAt": "Fri, 09 Oct 2020 15:35:22 GMT", 
        "deliveryAddress": "SMU SIS", 
        "orderId": 1, 
        "paid": false, 
        "pickupAddress": "pickup", 
        "username": "user1"
    }
  ],
  "type": "success"
}
```

## 1.3 Get Order By User

**Get order details for a specific user**

**URL** `/order/user/<username>`

**Method** `GET`

Request sample:
```
http://localhost:7003/order/user/user1
```

This function returns the following JSON response:

```
{
  "orderDetails": [
    {
        "createdAt": "Fri, 09 Oct 2020 15:37:35 GMT", 
        "orderDetailId": 1, 
        "orderId": 1, 
        "price": 2.5, 
        "productId": 1, 
        "quantity": 3, 
        "total": 7.5
    }
  ], 
  "orders": [
    {
        "completed": false, 
        "createdAt": "Fri, 09 Oct 2020 15:35:22 GMT", 
        "deliveryAddress": "SMU SIS", 
        "orderId": 1, 
        "paid": false, 
        "pickupAddress": "pickup", 
        "username": "user1"
    }
  ],
  "type": "success"
}
```

## 1.4 Create new order

**creating a new order**

**URL** `/order/create`

**Method** `POST`
Request sample:
```
http://localhost:7003/order/create
```

```
{
    "completed": false, 
    "deliveryAddress": "SMU SIS", 
    "order_details": [
      {
        "price": 2.5, 
        "productId": 1, 
        "quantity": 3, 
        "total": 7.5
      }
    ], 
    "paid": false, 
    "pickupAddress": "Istana", 
    "username": "jrchew"
}
```
This function returns the following JSON response:

```
{
    "order": {
        "completed": false,
        "createdAt": "Sat, 10 Oct 2020 01:53:35 GMT",
        "deliveryAddress": "SMU SIS",
        "orderId": 9,
        "order_details": [
            {
                "createdAt": "Sat, 10 Oct 2020 01:53:35 GMT",
                "orderDetailId": 16,
                "orderId": 9,
                "price": 2.5,
                "productId": 1,
                "quantity": 3,
                "total": 7.5
            }
        ],
        "paid": false,
        "pickupAddress": "Istana",
        "total": 12.5,
        "username": "jrchew"
    },
    "type": "success"
}
```

## 1.5 Edit order

**User can edit a order details**

**URL** `/order/edit`

**Method** `POST`
Request sample:
```
http://localhost:7003/order/edit
```
```
{
    "completed": false, 
    "deliveryAddress": "SMU SIS", 
    "orderId": 1,
    "paid": false, 
    "pickupAddress": "SMU SOE", 
    "total": 12.5, 
    "username": "jrchew"
}
```
Compulsory fields: orderId, username

Non-editable fields: orderId, username, createdAt, updatedAt

This function returns the following JSON response:

```
{
    "order": {
        "completed": false,
        "createdAt": "Fri, 09 Oct 2020 15:35:22 GMT",
        "deliveryAddress": "SMU SIS",
        "orderId": 1,
        "paid": false,
        "pickupAddress": "SMU SOE",
        "username": "jrchew"
    },
    "type": "success"
}
```
Note: orderId is auto-incremented