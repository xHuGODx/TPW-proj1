# TPW-proj1

# Notas
```
Update ao modelo pela milesima vez.
Ja ta tudo como devia.
Se correrem o insertData.py ele vai apagar os superusers atencao.
Alterei o modelo para haver tabelas para os favoritos e cart e followers nao muda nada na implementacao só foi para ficar mais normalizado
alterei o insertdata/admin.py/settings para suportar estas mudancas
```
# Notas 2
```
add product
cart
favourites adicionei a func de remover dos favs
following
myproducts
remover um produto
detalhes de um produto
adicionar ao carrinho
```
# Notas 3
```
Falta:
Meter bonito
meter mais coisos de messages.success(request, "Order confirmed! Thank you for your purchase.") ou de message error
o log do website se calhar nao fazemos (edu: concordo)
acho que falta alguma logica tipo um user nao comprar os seus proprios produtos
fazer aquela cena da taxa de 10%
```

# Membros do Grupo

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

- Register/Login ✅ (so o da direita) ✅ ja tao os 2
- View all ads  ✅
- Search and Filter ✅

## User - com login

- All from above
- Open ads ✅
- Add ads ✅
- See their own ads ✅
- Remove their ads ✅
- Track views on their add ✅
- Edit their ads ✅
- Add ads to cart and buy ✅ 
- Follow ✅
- See products from users they follow ✅
- See who follows them ✅
- Add ads to favourites ✅
- See their favourites ✅
- Send/Receive messages ✅ 
- View profiles ✅
- Change profile info 
- Comment on profiles ✅
- View his cart ✅
- Logout ✅
- Receive notification upon selling a product ✅

## Admin

- All from above
- Remove any users ✅
- Remove any ads ✅
- Remove any comment✅
- Search users and products ✅
- View all orders ✅
- (view website log)