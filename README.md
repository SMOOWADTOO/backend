# Backend Guide

## SQL dump folder

Dump all the `.sql` script files to the ./sqldump folder

## Creating a new service

1. Create your service by copying the sample folder in the **./services/v1/sample** folder
2. Rename the folder
3. Go to **run.sh** and edit the line that says `python "$DIR/user.py"` to your service. e.g. If your service is called `product`, change it to `python "$DIR/**product**.py"`
4. Also in **run.sh**, add in your DB URL here. Once you've set them, remember to add **run.sh** to gitignore. If you added any env variables inside the **run.sh** folder, remember to send this folder through our Telegram group chat.
5. Change the Flask app name as well
6. **requirements.txt** file contains all the necessary libraries you need for your Flask app. Add and remove as needed for your application
7. Document your RESTful API parameters using the sample in **README.md**
8. In **Dockerfile**, please change the `user` to the name of your service.
9. Add your service to **install_dev.sh** and **run_dev.sh** in the root folder. These two folders is to orchestrate the running of all the services at once, rather than going to every folder and running the service individually. Remember, once you've set the API keys and DB URLs, add to `gitignore`.
10. Run **install.sh** or **install_dev.sh** on first time, or when adding new dependencies into the service. **run.sh** or **run_dev.sh** when you wanna run the service.

## Services list

**7001** `user`: [https://www.casafair.org/api/user](https://www.casafair.org/api/user)

**7002** `shop`: [https://www.casafair.org/api/shop](https://www.casafair.org/api/shop)

**7003** `order`: [https://www.casafair.org/api/order](https://www.casafair.org/api/order)

**7004** `product`: [https://www.casafair.org/api/product](https://www.casafair.org/api/product)

**7005** `review`: [https://www.casafair.org/api/review](https://www.casafair.org/api/review)

**7006** `payment`: [https://www.casafair.org/api/payment](https://www.casafair.org/api/payment)

**7007** `notification`: [https://www.casafair.org/api/notification](https://www.casafair.org/api/notification)

**7009** `search`: [https://www.casafair.org/api/search](https://www.casafair.org/api/search)

> Let's not upload API keys into GH hahaha

## Running locally

```
# Running for the first time
sh install_dev.sh

# Subsequent times
sh run_dev.sh

# When you wanna call it a day
sh stop_dev.sh
```
