# TPW-proj1

# Introduction

Olx clone, where users can buy and sell star wars themed items.

# How to run localy

    Start a venv if you want.

    pip install -r requirements.txt

    python3 manage.py makemigrations

    python3 manage.py migrate

    python3 insertData.py

    python3 manage.py runserver

# Acess this link to view the website deployed

# Users 

| User    | Password     | Admin |
|:--------|:-------------|:------|
| joao    | password1    | False |
| maria   | password2    | False |
| ricardo | password3    | False |
| ana     | password4    | False |
| tiago   | password5    | False |
| mateus  | password123  | True  |

# Members of the Group

| Nome | NMec |
|:---|:---:|
| Inês Ferreira | 104415 |
| Hugo Ribeiro | 113402 |
| Eduardo Lopes | 103070 |

| Superuser | Password |
|:---|:---:|
| admin | admin123 |

# Funcionalities 

## User - Not logged

- Register/Login 
- View all ads  
- Search and Filter 

## User - com login

- All from above
- Open ads 
- Add ads 
- See their own ads 
- Remove their ads 
- Track views on their add 
- Edit their ads 
- Add ads to cart and buy 
- Follow 
- See products from users they follow 
- See who follows them 
- Add ads to favourites 
- See their favourites 
- Send/Receive messages 
- View profiles 
- Change profile info 
- Comment on profiles 
- View his cart 
- Logout 
- Receive notification upon selling a product 

## Admin

- All from above
- Remove any users 
- Remove any ads 
- Remove any comment
- Search users and products 
- View all orders 


# How to add a new admin

Create a super user, and give the admin flag in the default admin django page.