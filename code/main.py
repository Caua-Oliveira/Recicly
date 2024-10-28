import urllib.request
import json
import geocoder
from geopy.distance import geodesic
from store import Store
from admin import Admin
from database_connection import *
from user import User

# Inicializar variáveis globais
def initialize_global_data():
    global my_coords
    ip = geocoder.ip('me')
    my_coords = ip.latlng

    global stores
    stores = []


initialize_global_data()

def initialize_stores():
    store1 = Store("Green Store", "A store for eco-friendly products")
    store1.add_coupon("10% Off", "10% off on all items", 50, "GREEN10")
    store1.add_coupon("Free Shipping", "Free shipping on orders over $50", 30, "FREESHIP")

    store2 = Store("Tech Recycle", "Recycle your old electronics")
    store2.add_coupon("15% Off", "15% off on electronics", 75, "TECH15")
    store2.add_coupon("Buy 1 Get 1", "Buy one get one free on selected items", 100, "B1G1")

    stores.extend([store1, store2])


initialize_stores()


def sign_up():
    print("Cadastro")
    name = input("Nome: ")
    email = input("Email: ")
    password = input("Senha: ")
    cpf = input("CPF: ")
    new_user = User(name, email, password, cpf)

    if save_user_to_db(new_user):
        print("Usuário salvo com sucesso.")
    else:
        print("Falha ao salvar o usuário. Por favor, tente novamente.")

def sign_in():
    print("Login")
    email = input("Email: ")
    password = input("Senha: ")
    user_obj = fetch_user_by_email(email)
    if user_obj and user_obj.verify_password(password):
        print(f"Bem-vindo de volta, {user_obj.name}!")
        return user_obj
    else:
        print("Credenciais inválidas.")
        return None

def deliver_trash(user_obj):
    print("Entrega de Lixo")
    try:
        amount = float(input("Digite a quantidade de lixo entregue (kg): "))
        trash_type = input("Digite o tipo de lixo (plástico/metal/papel/vidro/orgânico): ").lower()
        if trash_type in user_obj.statistics.trash_by_type:
            user_obj.statistics.trash_by_type[trash_type] += amount
            user_obj.statistics.total_trash_amount += amount
            points_earned = int(amount * 100)
            user_obj.statistics.add_points(points_earned)
            update_user_in_db(user_obj)
            print(f"Lixo entregue com sucesso! Você ganhou {points_earned} pontos.")
        else:
            print("Tipo de lixo inválido.")
    except ValueError:
        print("Quantidade inválida.")

def view_statistics(user_obj):
    print(f"Estatísticas de {user_obj.name}:")
    user_obj.show_statistics()

def view_ranking_by_trash_amount():
    print("Ranking de Usuários:")
    # Implementação necessária para obter ranking dos usuários

def fetch_recycling_locations():
    url = "https://geo.salvador.ba.gov.br/arcgis/rest/services/Hosted/cooperativas_p/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"
    try:
        with urllib.request.urlopen(url) as response:
            return json.load(response)['features']
    except Exception as e:
        print(f"Erro ao buscar locais de reciclagem: {e}")
        return []

def display_recycling_locations():
    features = fetch_recycling_locations()

    locations_with_distances = []
    for feature in features:
        properties = feature['properties']
        geometry = feature['geometry']
        coordinates = geometry.get('coordinates', [0, 0])
        location_coords = (coordinates[1], coordinates[0])
        distance = geodesic(my_coords, location_coords).kilometers

        locations_with_distances.append((distance, properties, coordinates))

    locations_with_distances.sort(key=lambda x: x[0])

    print("\nLocais de Reciclagem na Cidade:\n")
    for distance, properties, coordinates in locations_with_distances:
        name = properties.get('nome', 'N/A')
        address = properties.get('endereço', 'N/A')
        contact = properties.get('contato', 'N/A')

        print(f"Nome: {name}")
        print(f"Endereço: {address}")
        print(f"Contato: {contact}")
        print(f"Coordenadas: {coordinates}")
        print(f"Distância: {distance:.2f} km\n")

def view_stores_and_coupons():
    try:
        stores = fetch_all_stores_from_db()
        for store in stores:
            print(store)
            for coupon in store.coupons.values():
                print(coupon)
            print("\n")
    except Exception as e:
        print(f"Erro ao obter lojas e cupons: {e}")

def buy_coupon(user_obj):
    stores = fetch_all_stores_from_db()
    store_name = input("Digite o nome da loja: ")

    # Find the store by name
    for store in stores:
        if store.name.strip() == store_name.strip():
            print(f"Cupons disponíveis em {store_name}:")

            # Display available coupons
            for coupon_code, coupon_data in store.coupons.items():
                print(f"{coupon_data.name.strip()} - {coupon_data.price} pontos")

            # Get the coupon name from the user
            selected_coupon = input("Digite o nome do cupom: ")

            # Attempt to redeem the coupon
            if store.redeem_coupon(selected_coupon, user_obj):
                update_user_in_db(user_obj)  # Update the user in the database
                print(f"Cupom {selected_coupon} resgatado com sucesso!")
            else:
                print("Falha ao resgatar o cupom.")
            return

    print("Loja não encontrada.")


def admin_actions():
    print("Credenciais inválidas.")

def main():
    while True:
        action = input(
            "1. Cadastro\n2. Login\n3. Login Admin\n4. Ver Locais de Reciclagem\n5. Sair\nEscolha uma ação: ")
        if action == "1":
            sign_up()
        elif action == "2":
            user_obj = sign_in()
            if user_obj:
                while True:
                    user_action = input(
                        "1. Entregar Lixo\n2. Ver Estatísticas\n3. Ver Ranking\n4. Ver Lojas e Cupons\n5. Resgatar Cupom\n6. Sair\nEscolha uma ação: ")
                    if user_action == "1":
                        deliver_trash(user_obj)
                    elif user_action == "2":
                        view_statistics(user_obj)
                    elif user_action == "3":
                        view_ranking_by_trash_amount()
                    elif user_action == "4":
                        view_stores_and_coupons()
                    elif user_action == "5":
                        buy_coupon(user_obj)
                    elif user_action == "6":
                        print("Saindo...")
                        break
        elif action == "3":
            admin_actions()
        elif action == "4":
            display_recycling_locations()
        elif action == "5":
            print("Saindo...")
            break

if __name__ == "__main__":
    main()
