# REVIEW SERVICE

---

The review service handles everything related to reviews:

1. Get all reviews
2. Get Reviews by Shop ID
3. Add new review

---

> Try to follow API best practices using nouns and not verbs (POST: /user for creating new users, GET: /user for getting user info). See more at https://docs.microsoft.com/en-us/azure/architecture/best-practices/api-design

**Port** `7005`

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

# Review

## 1.1 Get All Reviews

**Get list of all reviews**

**URL** `/review`

**Method** `GET`

Request sample:

```
http://localhost:7005/review
```

This function returns the following JSON response:

```
{
    "reviews": [
        {
            "publishedTime": "Mon, 05 Oct 2020 11:28:19 GMT",
            "rating": 5,
            "reviewDetail": "cake is yummy, thanks shop",
            "reviewId": 1,
            "shopId": 1,
            "title": "Fabulous Cake",
            "username": "vivocity"
        },
        {
            "publishedTime": "Mon, 05 Oct 2020 11:28:19 GMT",
            "rating": 4,
            "reviewDetail": "as title",
            "reviewId": 2,
            "shopId": 2,
            "title": "Best chicken rice ever",
            "username": "johnny_chew"
        },
}
```

## 1.2 Get Reviews By Shop ID

**Get list of reviews of a specific Shop**

**URL** `/review/<shopId>`

**Method** `GET`

Request sample:

```
http://localhost:7005/review/1
```

This function returns the following JSON response:

```
{
    "reviews": [
        {
            "publishedTime": "Mon, 05 Oct 2020 11:28:19 GMT",
            "rating": 5,
            "reviewDetail": "cake is yummy, thanks shop",
            "reviewId": 1,
            "shopId": 1,
            "title": "Fabulous Cake",
            "username": "vivocity"
        },
        {
            "publishedTime": "Wed, 07 Oct 2020 20:34:59 GMT",
            "rating": 5,
            "reviewDetail": "luv the cupcake, yea u got that yummy yummy yummy",
            "reviewId": 5,
            "shopId": 1,
            "title": "Red velvet cupcake",
            "username": "sicilia"
        },
    ],
    "status": 200
}
```

## 1.3 Add new review

**A customer can add new review**

**URL** `/review/add`

**Method** `POST`
Request sample:

```
{
    "rating": 5,
    "reviewDetail": "luv the cupcake, yea u got that yummy yummy yummy",
    "shopId": 1,
    "title": "Red velvet cupcake",
    "username": "sicilia"
}
```

This function returns the following JSON response:

```
{
    "review": {
        "publishedTime": "Wed, 07 Oct 2020 20:35:56 GMT",
        "rating": 5,
        "reviewDetail": "luv the cupcake, yea u got that yummy yummy yummy",
        "reviewId": 7,
        "shopId": 1,
        "title": "Red velvet cupcake",
        "username": "sicilia"
    },
    "type": "success"
}
```

> Note: reviewId is auto-incremented, publishedTime is current timestamp when adding to database
