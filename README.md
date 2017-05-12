# Pizza-Menu-Ordering-System

## Architecture
![picture alt](img/architecture.png)


## Rest Endpoint Screenshots
### Menu POST https://p80jhqkrq7.execute-api.us-west-1.amazonaws.com/prod/menu
![picture alt](img/Menu-POST.png)

### Menu PUT https://p80jhqkrq7.execute-api.us-west-1.amazonaws.com/prod/menu/121-232-343-544
![picture alt](img/Menu-PUT.png)

### Menu GET https://p80jhqkrq7.execute-api.us-west-1.amazonaws.com/prod/menu/121-232-343-544
![picture alt](img/MENU-GET.png)

### Menu DELETE https://p80jhqkrq7.execute-api.us-west-1.amazonaws.com/prod/menu/121-232-343-544
![picture alt](img/MENU-DELETE.png)

### Order POST https://p80jhqkrq7.execute-api.us-west-1.amazonaws.com/prod/order/
#### Posting a new order
![picture alt](img/ORDER-POST.png)

### ORDER PUT https://p80jhqkrq7.execute-api.us-west-1.amazonaws.com/prod/order/12111110001
#### 1st put is for chosing one of the offered selection
![picture alt](img/ORDER-PUT-1.png)

### ORDER PUT https://p80jhqkrq7.execute-api.us-west-1.amazonaws.com/prod/order/12111110001
#### 2nd put is for chosing one of the offered size
![picture alt](img/ORDER-PUT-2.png)

### ORDER GET https://p80jhqkrq7.execute-api.us-west-1.amazonaws.com/prod/order/12111110001
#### This is to see your order summary, status etc
![picture alt](img/ORDER-GET.png)
