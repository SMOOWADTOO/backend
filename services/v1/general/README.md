# GENERAL SERVICE
----------

The general service handles everything related to external API interfaces

-----------

> Try to follow API best practices using nouns and not verbs (POST: /user for creating new users, GET: /user for getting user info). See more at https://docs.microsoft.com/en-us/azure/architecture/best-practices/api-design 

**Port** `7008`

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

## User Types

```
USER_TYPES = {
    "normal_user": 0, 
    "business_employee": 1, 
    "business_admin": 2, 
    "system_admin": 3
}
```

## 1.1 getAddress

**Gets an address string from the OneMAP API using the postal code as a parameter**

**URL** `/general/map/address/<string:postal_code>`

**Method** `GET`

This function returns the following JSON response:

```
{
  "address": {
    "ADDRESS": "7 PEMIMPIN DRIVE SEASONS VIEW SINGAPORE 576150", 
    "BLK_NO": "7", 
    "BUILDING": "SEASONS VIEW", 
    "LATITUDE": "1.352170313", 
    "LONGITUDE": "103.84096640000001", 
    "LONGTITUDE": "103.84096640000001", 
    "POSTAL": "576150", 
    "ROAD_NAME": "PEMIMPIN DRIVE", 
    "SEARCHVAL": "SEASONS VIEW", 
    "X": "28851.1134", 
    "Y": "37141.64045"
  }, 
  "type": "success"
}
```