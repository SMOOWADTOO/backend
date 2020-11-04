# PRODUCT SERVICE

---

The user service handles everything related to products:

1. Get all products

---

> Try to follow API best practices using nouns and not verbs (POST: /user for creating new users, GET: /user for getting user info). See more at https://docs.microsoft.com/en-us/azure/architecture/best-practices/api-design

**Port** `7007`

All service calls returns the following JSON response:

_Success_

```
{
    "type": "success",
    //whatever the function returns
}
```

_Warning_

```
{
    "type": "warning",
    "message": // whatever message returned
}
```

_Error_

```
{
    "type": "error",
    "message": // whatever message returned,
    "debug": // whatever is returned as Exception (exception message)
}
```

> **NOTE: Boolean values accept 0 as false, and non-zero for true when inserting into the database**

# Notification

## 1.1 Email notification for Order successful

**Email notification for Order successful**

**URL** `/notification/email`

**Method** `POST`

Request sample:

```
http://localhost:7007/notification/email
```

```

{
  "email": "ptvvo.2018@sis.smu.edu.sg",
  "firstName": "Vi",
  "lastName": "Vo",
  "orderId": "1",
  "productList": [
    {
      "itemName": "pancake",
      "qty": "1",
      "price": "3.5"
    },
    {
      "itemName": "banana",
      "qty": "1",
      "price": "1.5"
    }
  ]
}

```

This function returns the following JSON response:

```
{
    "message": "Successfully sent an email",
    "type": "success"
}
```


## 1.2 Email from customer via Contact Us

**Email from customer via Contact Us**

**URL** `/notification/contact-us`

**Method** `POST`

Request sample:

```
http://localhost:7007/notification/contact-us
```

```

{
    "email": "ptvvo.2018@sis.smu.edu.sg",
    "name": "Vi Vo",
    "subject": "Suggestion of new feature",
    "description": "To whom may I concern, I would like to suggest a new feature on CasaFair app....."
}

```

This function returns the following JSON response:

```
{
    "message": "Successfully sent an email",
    "type": "success"
}
```
