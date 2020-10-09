# USER SERVICE
----------

The user service handles everything related to users: 

1. User Login
2. User Profile

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


# Login

## 1.1 authenticate

**Authenticates a user requesting to login**

**URL** `/user/authentication`

**Method** `POST`

Request sample:

```
{
	"email": "a@a.com",
	"password": "sfz5466z"
}
```

This function returns the following JSON response:

```
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1MCwiZW1haWwiOiJhQGEuY29tIiwiZW1haWxfdmVyaWZpZWRfYXQiOm51bGwsImlzX2FkbWluIjpudWxsLCJyZW1lbWJlcl90b2tlbiI6bnVsbCwibnJpYyI6bnVsbCwiZmlyc3RfbmFtZSI6IldlaW1pbmciLCJsYXN0X25hbWUiOiJTaXR1IiwiZHJpdmluZ19saWNlbmNlX3ZhbGlkaXR5IjpudWxsLCJwcm9maWxlX3Bob3RvX3VybCI6IiIsImFkZHJlc3NfbGluZTEiOiI3IFBFTUlNUElOIERSSVZFIiwiYWRkcmVzc19saW5lMiI6IlNFQVNPTlMgVklFVyIsInBvc3RhbF9jb2RlIjoiNTc2MTUwIiwibW9iaWxlX25vIjpudWxsLCJ0ZWxlZ3JhbV90b2tlbiI6bnVsbCwiZXhwIjoxNjAxODc1NTcwfQ.v8vubk3UY_NU8W1afdDPp6DVYP_n87BFDC_UuHK5XHc",
    "type": "success"
}
```

## 1.2 createUserProfile

**Get user profile from specific ID**

**URL** `/user/profile`

**Method** `POST`

Request sample:

```
{
	"first_name": "Emmanuel",
    "last_name": "Rayendra",
    "mobile_no": "91829191",
    "nric": "S2710291E"
}
```

This function returns the following JSON response:

```
{
    "type": "success",
    "user": {
        "first_name": "Emmanuel",
        "last_name": "Rayendra",
        "mobile_no": "91829191",
        "nric": "S2710291E",
        "user_id": 4
    }
}
```

## 1.3 getUserProfile

**Get user profile from specific ID**

**URL** `/user/profile/<int:id>`

**Method** `GET`

This function returns the following JSON response:

```
{
    "type": "success",
    "user": {
        "first_name": "Emmanuel",
        "last_name": "Rayendra",
        "mobile_no": "91829191",
        "nric": "S2710291E",
        "user_id": 4
    }
}
```