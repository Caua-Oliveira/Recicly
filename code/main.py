import urllib.request
import json
import geocoder
from geopy.distance import geodesic
from store import Store
from admin import Admin
from database_connection import *
from user import User

def initialize_global_data():
    global my_coords
    ip = geocoder.ip('me')
    my_coords = ip.latlng

initialize_global_data()

def sign_up():
    print("Cadastro")
    name = input("Nome: ")
    email = input("Email: ")
    password = input("Senha: ")
    new_user = User(name, email, password)

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
        return user_obj
    else:
        print("Email ou senha incorretos. Tente novamente.")

def admin_sign_in():
    print("Admin Login")
    admin_code = input("Admin Code: ")
    password = input("Senha: ")
    admin_obj = fetch_admin_by_code(admin_code)
    if admin_obj:
        print(f"Admin Menu")
        return admin_obj
    else:
        print("Credenciais inválidas.")
        return None

def view_statistics(user_obj):
    print(f"Estatísticas de {user_obj.name}:")
    user_obj.show_statistics()


def view_ranking(uid):
    try:
        users = fetch_all_users_from_db()
        sorted_users = sorted(users, key=lambda user: user.statistics.total_trash_amount, reverse=True)
        ranking_data = []
        user_rank = {'trash_amount': 0, 'position': 'N/A', 'name': 'N/A'}
        for rank, user in enumerate(sorted_users, start=1):
            if user.id == uid:
                user_rank = {
                    'name': user.name.title(),
                    'trash_amount': user.statistics.total_trash_amount,
                    'position': rank
                }
            user_data = {
                'rank': rank,
                'name': user.name.title(),
                'trash_amount': user.statistics.total_trash_amount,
                'id': user.id
            }
            ranking_data.append(user_data)


        return ranking_data, user_rank
    except Exception as e:
        print(f"Erro ao obter ranking: {e}")

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

def buy_coupon2(store_name, selected_coupon, uid):
    stores = fetch_all_stores_from_db()
    user_obj = fetch_user_by_id(uid)

    # Find the store by name
    for store in stores:
        if store.name.strip() == store_name.strip():
            success, code = store.redeem_coupon(selected_coupon, user_obj)
            if success:
                update_user_in_db(user_obj)  # Update the user in the database
                print(f"Cupom {selected_coupon} resgatado com sucesso!")
                return True, code
            else:
                print("Falha ao resgatar o cupom.")
            return False, None

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

    return locations_with_distances

    # print("\nLocais de Reciclagem na Cidade:\n")
    # for distance, properties, coordinates in locations_with_distances:
    #     name = properties.get('nome', 'N/A')
    #     address = properties.get('endereço', 'N/A')
    #     contact = properties.get('contato', 'N/A')
    #
    #     print(f"Nome: {name}")
    #     print(f"Endereço: {address}")
    #     print(f"Contato: {contact}")
    #     print(f"Coordenadas: {coordinates}")
    #     print(f"Distância: {distance:.2f} km\n")

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

# Main loop
def main():
    current_user = None
    while True:
        print("\n=== Recicly - Menu Principal ===")
        print("1. Cadastrar-se")
        print("2. Login")
        print("3. Admin Login")
        print("4. Entrega de lixo reciclável")
        print("5. Sair")

        choice = input("Escolha uma opção: ")

        if choice == '1':
            sign_up()

        elif choice == '2':
            user = sign_in()
            if user:
                current_user = user
                user_menu(current_user)

        elif choice == '3':
            admin = admin_sign_in()
            if admin:
                print("Acesso ao painel de administrador.")
                # Add admin-specific options here if needed

        elif choice == '4':
            user_email = input("Digite o email do usuário: ")
            user_obj = fetch_user_by_email(user_email)
            if user_obj:
                deliver_trash(user_obj)

        elif choice == '5':
            print("Saindo... Até mais!")
            break

        else:
            print("Opção inválida. Tente novamente.")

# User-specific menu
def user_menu(user_obj):
    while True:
        print(f"\n=== Bem-vindo, {user_obj.name} ===")
        print("1. Ver estatísticas")
        print("2. Ver ranking")
        print("3. Ver lojas e cupons")
        print("4. Comprar cupom")
        print("5. Ver locais de coleta")
        print("6. Logout")

        choice = input("Escolha uma opção: ")

        if choice == '1':
            view_statistics(user_obj)

        elif choice == '2':
            view_ranking()

        elif choice == '3':
            view_stores_and_coupons()

        elif choice == '4':
            buy_coupon(user_obj)

        elif choice == '5':
            display_recycling_locations()

        elif choice == '6':
            print("Logout realizado com sucesso.")
            break

        else:
            print("Opção inválida. Tente novamente.")


# Run the program
if __name__ == "__main__":
    main()