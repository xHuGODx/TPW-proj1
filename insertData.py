import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webproj.settings")
django.setup()

from app.models import User, Product, Comment, Order, Message
from django.contrib.auth import authenticate, login as auth_login

User.objects.all().delete()
Product.objects.all().delete()
Comment.objects.all().delete()
Order.objects.all().delete()
Message.objects.all().delete()

user1 = User.objects.create(
    id=1,
    username="joao",
    name="João Carlos Rodrigues",
    email="joao@example.com",
    password="password1",
    admin=False,
    image="profile_images/joao.jpg",
    description="Sigma Sigma on the wall, whos the skibidiest of them all?",
    sold=0,
)

user2 = User.objects.create(
    id=2,
    username="maria",
    name="Maria Ferreira Silva",
    email="maria@example.com",
    password="password2",
    admin=False,
    image="profile_images/maria.jpg",
    description="Amante de livros e colecionadora de action figures.",
    sold=0,
)

user3 = User.objects.create(
    id=3,
    username="ricardo",
    name="Ricardo Nogueira",
    email="ricardo@example.com",
    password="password3",
    admin=False,
    image="profile_images/ricardo.jpg",
    description="Nerd que gosta de Pilates e de jogar SONIC.",
    sold=0,
)

user4 = User.objects.create(
    id=4,
    username="ana",
    name="Ana Paula Mendes",
    email="ana@example.com",
    password="password4",
    admin=False,
    image="profile_images/ana.jpg",
    description="Administradora dedicada com paixão por Star Wars.",
    sold=2,
)

user5 = User.objects.create(
    id=5,
    username="tiago",
    name="Tiago Lopes",
    email="tiago@example.com",
    password="password5",
    admin=False,
    image="profile_images/tiago.jpg",
    description="Colecionador de figuras raras e fã de cosplay.",
    sold=1,
)

useradmin = User.objects.create(
    id=6,
    username="mateus",
    name="Mateus Reis Silva",
    email="mateus@example.com",
    password="password123",
    admin=True,
    image="profile_images/mateus.jpg",
    description="Desenvolvedor de software e entusiasta de tecnologia.",
    sold=0,
)


authenticate(username='joao', password='password1')
authenticate(username='maria', password='password2')
authenticate(username='ricardo', password='password3')
authenticate(username='ana', password='password4')
authenticate(username='tiago', password='password5')
authenticate(username='mateus', password='password123')


products = [
    Product.objects.create(
        id=1,
        name="Lego Death Star",
        description="Lego Star Wars Death Star 2016 Edition, 4016 pieces, brand new. Includes all minifigures and instructions. Box is slightly damaged.",
        price=299.99,
        user=user1,
        brand="LEGO",
        category="LEGO",
        color="Grey",
        seen=10,
        image="product_images/lego_death_star.jpg",
    ),
    Product.objects.create(
        id=2,
        name="Lego Millennium Falcon",
        description="Lego Star Wars Millennium Falcon 2017 Edition, 7541 pieces, brand new. Includes all minifigures and instructions. Box is slightly damaged.",
        price=399.99,
        user=user2,
        brand="LEGO",
        category="LEGO",
        color="Grey",
        seen=20,
        image="product_images/lego_millennium_falcon.jpg",
    ),
    Product.objects.create(
        id=3,
        name="Lightsaber Replica",
        description="High-quality replica of Luke Skywalker’s lightsaber from Star Wars: A New Hope. Full metal hilt with removable blade and sound effects.",
        price=199.99,
        user=user3,
        brand="Hasbro",
        category="WEAPON",
        color="Silver",
        seen=30,
        image="product_images/lightsaber_replica.jpg",
    ),
    Product.objects.create(
        id=4,
        name="Darth Vader Action Figure",
        description="12-inch Darth Vader action figure with real fabric cape and light-up lightsaber. Limited edition collectible from the 40th Anniversary of Star Wars.",
        price=89.99,
        user=user4,
        brand="Hot Toys",
        category="FIGURES",
        color="Black",
        seen=40,
        image="product_images/darth_vader_figure.jpg",
    ),
    Product.objects.create(
        id=5,
        name="Star Wars: A New Hope Poster",
        description="Original 1977 Star Wars: A New Hope movie poster, rolled and in excellent condition. A rare find for collectors.",
        price=249.99,
        user=user5,
        brand="Lucasfilm",
        category="POSTER",
        color="Multi",
        seen=15,
        image="product_images/star_wars_poster.jpg",
    ),
    Product.objects.create(
        id=6,
        name="Yoda Bust",
        description="Limited edition Yoda bust made of resin, hand-painted and signed by the sculptor. A must-have for Star Wars collectors.",
        price=349.99,
        user=user1,
        brand="Gentle Giant",
        category="COLLECTIBLE",
        color="Green",
        seen=25,
        image="product_images/yoda_bust.jpg",
    ),
    Product.objects.create(
        id=7,
        name="R2-D2 Phone Charger",
        description="Portable R2-D2 phone charger with sound effects. Compatible with most smartphones and includes a USB charging cable.",
        price=29.99,
        user=user2,
        brand="ThinkGeek",
        category="OTHER",
        color="White",
        seen=50,
        image="product_images/r2d2_charger.jpg",
    ),
    Product.objects.create(
        id=8,
        name="Kylo Ren Lightsaber",
        description="Kylo Ren’s crossguard lightsaber replica with glowing red blades and sound effects. Made of durable metal and plastic, ideal for cosplay.",
        price=179.99,
        user=user3,
        brand="Disney",
        category="WEAPON",
        color="Red",
        seen=35,
        image="product_images/kylo_ren_lightsaber.jpg",
    ),
    Product.objects.create(
        id=9,
        name="Lego Imperial Star Destroyer",
        description="Lego Star Wars Imperial Star Destroyer 2019 Edition, 4784 pieces, in perfect condition. Includes stand and mini Tantive IV.",
        price=699.99,
        user=user1,
        brand="LEGO",
        category="LEGO",
        color="Grey",
        seen=60,
        image="product_images/lego_star_destroyer.jpg",
    ),
    Product.objects.create(
        id=10,
        name="Boba Fett Action Figure",
        description="Highly detailed Boba Fett action figure with removable helmet and blaster rifle. Part of the Black Series collection.",
        price=99.99,
        user=user4,
        brand="Hasbro",
        category="FIGURES",
        color="Green",
        seen=45,
        image="product_images/boba_fett_figure.jpg",
    ),
    Product.objects.create(
        id=11,
        name="The Empire Strikes Back Poster",
        description="Original 1980 Star Wars: The Empire Strikes Back movie poster in excellent condition. Rolled and stored properly, perfect for collectors.",
        price=299.99,
        user=user5,
        brand="Lucasfilm",
        category="POSTER",
        color="Blue",
        seen=20,
        image="product_images/empire_strikes_back_poster.jpg",
    ),
    Product.objects.create(
        id=12,
        name="Han Solo in Carbonite Statue",
        description="Life-size replica of Han Solo frozen in carbonite, made from fiberglass and resin. A centerpiece for any Star Wars collection.",
        price=999.99,
        user=user2,
        brand="Sideshow Collectibles",
        category="COLLECTIBLE",
        color="Grey",
        seen=70,
        image="product_images/han_solo_carbonite.jpg",
    ),
    Product.objects.create(
        id=13,
        name="Star Wars Monopoly",
        description="Star Wars-themed Monopoly board game, featuring custom pieces and locations from the original trilogy. Sealed and brand new.",
        price=59.99,
        user=user1,
        brand="Hasbro",
        category="OTHER",
        color="Multi",
        seen=40,
        image="product_images/star_wars_monopoly.jpg",
    ),
    Product.objects.create(
        id=14,
        name="Darth Maul Double-Bladed Lightsaber",
        description="Full-scale replica of Darth Maul’s iconic double-bladed lightsaber with red LED blades and sound effects. Perfect for cosplay or display.",
        price=249.99,
        user=user3,
        brand="Master Replicas",
        category="WEAPON",
        color="Red",
        seen=55,
        image="product_images/darth_maul_lightsaber.jpg",
    ),
    Product.objects.create(
        id=15,
        name="Lego X-Wing Starfighter",
        description="Lego Star Wars X-Wing Starfighter, 731 pieces, featuring Luke Skywalker and R2-D2 minifigures. Comes with instructions and box.",
        price=79.99,
        user=user5,
        brand="LEGO",
        category="LEGO",
        color="White",
        seen=65,
        image="product_images/lego_xwing.jpg",
    ),
    Product.objects.create(
        id=16,
        name="Stormtrooper Helmet",
        description="Wearable Stormtrooper helmet with voice-changing technology. Highly detailed replica from Star Wars: A New Hope.",
        price=159.99,
        user=user2,
        brand="Anovos",
        category="FIGURES",
        color="White",
        seen=50,
        image="product_images/stormtrooper_helmet.jpg",
    ),
    Product.objects.create(
        id=17,
        name="Return of the Jedi Poster",
        description="Original 1983 Star Wars: Return of the Jedi movie poster, in excellent condition. A rare piece for serious collectors.",
        price=189.99,
        user=user4,
        brand="Lucasfilm",
        category="POSTER",
        color="Green",
        seen=30,
        image="product_images/return_of_jedi_poster.jpg",
    ),
    Product.objects.create(
        id=18,
        name="Mandalorian Helmet Collectible",
        description="Life-size Mandalorian helmet made from beskar steel replica. Officially licensed and perfect for display.",
        price=399.99,
        user=user1,
        brand="Efx Collectibles",
        category="COLLECTIBLE",
        color="Silver",
        seen=85,
        image="product_images/mandalorian_helmet.jpg",
    ),
    Product.objects.create(
        id=19,
        name="BB-8 Remote Control Droid",
        description="Remote-controlled BB-8 droid with full motion control and authentic sounds. A fun gadget for all Star Wars fans.",
        price=129.99,
        user=user5,
        brand="Sphero",
        category="OTHER",
        color="Orange and White",
        seen=40,
        image="product_images/bb8_droid.jpg",
    ),
    Product.objects.create(
        id=20,
        name="Lego Y-Wing Starfighter",
        description="Lego Star Wars Y-Wing Starfighter, 1967 pieces. Includes Y-Wing pilot minifigure and display stand. Perfect for collectors.",
        price=199.99,
        user=user2,
        brand="LEGO",
        category="LEGO",
        color="Yellow",
        seen=75,
        image="product_images/lego_ywing.jpg",
    ),
]

for p in products:
    p.save()


user1.favorites.add(products[0], products[4])
user2.favorites.add(products[1], products[5], products[12])
user3.favorites.add(products[2], products[13])
user4.favorites.add(products[3], products[9], products[0])
user5.favorites.add(products[8], products[11], products[18])

user1.followers.add(user2)
user1.followers.add(user3)
user2.followers.add(user4)
user3.followers.add(user1)
user3.followers.add(user5)
user4.followers.add(user5)
user5.followers.add(user2)


user1.save()
user2.save()
user3.save()
user4.save()
user5.save()



comments = [
    Comment.objects.create(
        text="Great seller! The product arrived quickly and was exactly as described. Highly recommend!",
        rating=5,
        user=user2,  
        seller=user1  
    ),
    Comment.objects.create(
        text="The item was in good condition, but the shipping took longer than expected.",
        rating=4,
        user=user3,  
        seller=user1  
    ),
    Comment.objects.create(
        text="Seller was very helpful and answered all my questions promptly. I’m happy with the purchase!",
        rating=5,
        user=user4,  
        seller=user2  
    ),
    Comment.objects.create(
        text="Received a damaged box, but the item inside was fine. Could be packaged better.",
        rating=3,
        user=user1,  
        seller=user3  
    ),
    Comment.objects.create(
        text="Fantastic service! The seller even included a small gift with my order. Will buy again.",
        rating=5,
        user=user5,  
        seller=user4  
    ),
    Comment.objects.create(
        text="Communication with the seller was difficult. The product was good, but not the experience.",
        rating=2,
        user=user3,  
        seller=user5  
    ),
    Comment.objects.create(
        text="Item didn’t match the description and the seller was unresponsive. Very disappointed.",
        rating=1,
        user=user4,  
        seller=user3  
    ),
    Comment.objects.create(
        text="Amazing product and great seller! Everything went smoothly from start to finish.",
        rating=5,
        user=user2,  
        seller=user5  
    ),
    Comment.objects.create(
        text="Decent experience, but the product had some minor issues that weren’t mentioned in the listing.",
        rating=3,
        user=user1,  
        seller=user4  
    ),
    Comment.objects.create(
        text="Fast shipping and excellent communication! Highly recommend this seller.",
        rating=5,
        user=user5,  
        seller=user1  
    )
]


for c in comments:
    c.save()

messages = [
    Message.objects.create(
        sender=user1,  # João
        receiver=user2,  # Maria
        text="Hi Maria! I just wanted to check if you received the Lego Death Star. Let me know!"
    ),
    Message.objects.create(
        sender=user2,  # Maria
        receiver=user1,  # João
        text="Hey João! Yes, I received it yesterday. Thanks for the quick shipping!"
    ),
    Message.objects.create(
        sender=user3,  # Ricardo
        receiver=user4,  # Ana
        text="Hi Ana! I saw your Boba Fett figure. Is it still available?"
    ),
    Message.objects.create(
        sender=user4,  # Ana
        receiver=user3,  # Ricardo
        text="Yes, it is! Let me know if you're interested in buying it."
    ),
    Message.objects.create(
        sender=user5,  # Tiago
        receiver=user1,  # João
        text="João, can you send me more pictures of the Lego Star Destroyer?"
    ),
    Message.objects.create(
        sender=user1,  # João
        receiver=user5,  # Tiago
        text="Sure, Tiago! I'll send them right away."
    ),
    Message.objects.create(
        sender=user2,  # Maria
        receiver=user3,  # Ricardo
        text="Ricardo, did you receive the Han Solo figure I sent you?"
    ),
    Message.objects.create(
        sender=user3,  # Ricardo
        receiver=user2,  # Maria
        text="Not yet, but I'm looking forward to it! Thanks for sending it."
    ),
    Message.objects.create(
        sender=user4,  # Ana
        receiver=user5,  # Tiago
        text="Tiago, are you going to the Star Wars convention next month?"
    ),
    Message.objects.create(
        sender=user5,  # Tiago
        receiver=user4,  # Ana
        text="Yes! I'm really excited. Are you coming too?"
    )
]

for m in messages:
    m.save()