# USER SERVICE
----------

The user service handles everything related to users: 

1. User Login
2. User Profile

This service uses the JWT authentication flow for protected APIs. If you see the **:warning: PROTECTED API** label, include the JWT token in the response headers like below:

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MywiZW1haWwiOiJlckBob21lYml6LmFwcCIsInR5cGUiOiJub3JtYWxfdXNlciIsInVzZXJJRCI6MywibnJpYyI6bnVsbCwiZmlyc3ROYW1lIjoiRW1tYW51ZWwiLCJsYXN0TmFtZSI6IlJheWVuZHJhIiwiYmlydGhkYXkiOm51bGwsImdlbmRlciI6bnVsbCwiZGVzY3JpcHRpb24iOm51bGwsImFkZHJlc3NMaW5lMSI6bnVsbCwiYWRkcmVzc0xpbmUyIjpudWxsLCJwb3N0YWxDb2RlIjpudWxsLCJwaG9uZU5vIjpudWxsLCJ0ZWxlZ3JhbVRva2VuIjpudWxsLCJleHAiOjE2MDE4OTUwODF9.mNRpLpezI78pcfPKv-p8gFdt_TkAY21Kfyd2gB_EJb4
```

-----------

> Try to follow API best practices using nouns and not verbs (POST: /user for creating new users, GET: /user for getting user info). See more at https://docs.microsoft.com/en-us/azure/architecture/best-practices/api-design 

**Port** `7001`

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

## 1.1 authenticate

**Authenticates a user requesting to login**

**URL** `/user/authentication`

**Method** `POST`

Request sample:

```
{
    "email": "er@homebiz.app", 
    "password": "la_chinata"
}
```

This function returns the following JSON response:

```
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MywiZW1haWwiOiJlckBob21lYml6LmFwcCIsInR5cGUiOiJub3JtYWxfdXNlciIsInVzZXJJRCI6MywibnJpYyI6bnVsbCwiZmlyc3ROYW1lIjoiRW1tYW51ZWwiLCJsYXN0TmFtZSI6IlJheWVuZHJhIiwiYmlydGhkYXkiOm51bGwsImdlbmRlciI6bnVsbCwiZGVzY3JpcHRpb24iOm51bGwsImFkZHJlc3NMaW5lMSI6bnVsbCwiYWRkcmVzc0xpbmUyIjpudWxsLCJwb3N0YWxDb2RlIjpudWxsLCJwaG9uZU5vIjpudWxsLCJ0ZWxlZ3JhbVRva2VuIjpudWxsLCJleHAiOjE2MDE4OTUwODF9.mNRpLpezI78pcfPKv-p8gFdt_TkAY21Kfyd2gB_EJb4",
    "type": "success",
    "user": {
        "created": "Mon, 05 Oct 2020 05:54:04 GMT",
        "email": "er@homebiz.app",
        "firstName": "Emmanuel",
        "gender": null,
        "id": 3,
        "lastName": "Rayendra",
        "phoneNo": null,
        "type": "normal_user",
        "updated": null
    }
}
```

> Important: Use the `token` parameter for protected APIs through the headers, e.g. `Authorization: Bearer <JWT token>`

## 1.2 createUser

**Creates a new user using the specified `user_type` parameter.**

For example, if URL is `/user/normal_user`, this function will create a user account of `userType` value `normal_user`.

**URL** `/user/<string:user_type>`

**Method** `POST`

Request sample:

```
{
    "email": "hs@homebiz.app", 
    "password": "shepherdspie",
    "firstName": "Hong Seng",
    "lastName": "Ong"
}
```

This function returns the following JSON response:

```
{
    "type": "success",
    "user": {
        "created": "Mon, 05 Oct 2020 08:41:13 GMT",
        "email": "hs@homebiz.app",
        "id": 18,
        "type": "normal_user",
        "updated": null
    }
}
```

## 1.3 getFullUserProfile

### :warning: PROTECTED API

**Get user profile from specific ID**

**URL** `/user/profile/me`

**Method** `GET`

This function returns the following JSON response:

```
{
    "type": "success",
    "user": {
        "addressLine1": null,
        "addressLine2": null,
        "birthday": null,
        "created": "Mon, 05 Oct 2020 05:54:04 GMT",
        "description": null,
        "email": "er@homebiz.app",
        "firstName": "Emmanuel",
        "gender": null,
        "id": 3,
        "lastName": "Rayendra",
        "nric": null,
        "phoneNo": null,
        "postalCode": null,
        "telegramToken": null,
        "type": "normal_user",
        "updated": null
    }
}
```

## 1.4 checkEmailExists

**This function checks if the email exists in the database. You might want to use this for validating registration forms.**

**URL** `/user/check/<string:email>`

**Method** `GET`

This function returns the following JSON response:

```
{
    "type": "success",
    "user": {
        "email": "er@homebiz.app",
        "id": 3,
        "type": "normal_user"
    }
}
```