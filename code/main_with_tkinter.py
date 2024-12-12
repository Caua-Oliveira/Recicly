import tkinter as tk
from tkinter import messagebox, simpledialog
from code.main import *

# Initialize global data (coordinates)
def initialize_global_data():
    global my_coords
    ip = geocoder.ip('me')
    my_coords = ip.latlng

initialize_global_data()

# Define ReciclyApp class for the GUI
class ReciclyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Recicly - Sistema de Reciclagem")
        self.main_menu()

    def main_menu(self):
        self.clear_window()

        tk.Label(self.root, text="=== Recicly - Menu Principal ===", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="Cadastrar-se", command=self.sign_up, width=20).pack(pady=5)
        tk.Button(self.root, text="Login", command=self.sign_in, width=20).pack(pady=5)
        tk.Button(self.root, text="Admin Login", command=self.admin_sign_in, width=20).pack(pady=5)
        tk.Button(self.root, text="Entrega de Lixo", command=self.deliver_trash, width=20).pack(pady=5)
        tk.Button(self.root, text="Sair", command=self.root.quit, width=20).pack(pady=5)

    def sign_up(self):
        name = simpledialog.askstring("Cadastro", "Nome:")
        email = simpledialog.askstring("Cadastro", "Email:")
        password = simpledialog.askstring("Cadastro", "Senha:", show="*")
        cpf = simpledialog.askstring("Cadastro", "CPF:")

        if all([name, email, password, cpf]):
            new_user = User(name, email, password, cpf)
            if save_user_to_db(new_user):  # Call your existing function
                messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            else:
                messagebox.showerror("Erro", "Falha ao cadastrar o usuário.")
        self.main_menu()

    def sign_in(self):
        email = simpledialog.askstring("Login", "Email:")
        password = simpledialog.askstring("Login", "Senha:", show="*")

        user = fetch_user_by_email(email)  # Call your existing function
        if user and user.verify_password(password):
            messagebox.showinfo("Sucesso", f"Bem-vindo, {user.name}!")
            self.user_menu(user)
        else:
            messagebox.showerror("Erro", "Email ou senha incorretos.")

    def admin_sign_in(self):
        code = simpledialog.askstring("Admin Login", "Admin Code:")
        password = simpledialog.askstring("Admin Login", "Senha:", show="*")

        admin = False
        if admin:
            messagebox.showinfo("Sucesso", "Acesso concedido ao painel do administrador.")
        else:
            messagebox.showerror("Erro", "Credenciais inválidas.")

    def deliver_trash(self):
        email = simpledialog.askstring("Entrega de Lixo", "Digite seu email:")
        user = fetch_user_by_email(email)  # Fetch user from the database

        if user:
            try:
                amount = float(simpledialog.askstring("Entrega", "Quantidade de lixo (kg):"))
                trash_type = simpledialog.askstring("Entrega", "Tipo de lixo (plástico, metal, papel, vidro, orgânico):").lower()

                if trash_type in user.statistics.trash_by_type:
                    user.statistics.trash_by_type[trash_type] += amount
                    user.statistics.total_trash_amount += amount
                    points = int(amount * 100)
                    user.statistics.add_points(points)

                    update_user_in_db(user)  # Update the user in the database
                    messagebox.showinfo("Sucesso", f"Lixo entregue! Você ganhou {points} pontos.")
                else:
                    messagebox.showerror("Erro", "Tipo de lixo inválido.")
            except ValueError:
                messagebox.showerror("Erro", "Quantidade inválida.")
        else:
            messagebox.showerror("Erro", "Usuário não encontrado.")

    def user_menu(self, user):
        self.clear_window()
        tk.Label(self.root, text=f"Bem-vindo, {user.name}!", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="Ver Estatísticas", command=lambda: view_statistics(user), width=20).pack(pady=5)
        tk.Button(self.root, text="Ver Ranking", command=view_ranking, width=20).pack(pady=5)
        tk.Button(self.root, text="Ver Lojas e Cupons", command=view_stores_and_coupons, width=20).pack(pady=5)
        tk.Button(self.root, text="Comprar Cupom", command=lambda: buy_coupon(user), width=20).pack(pady=5)
        tk.Button(self.root, text="Ver Locais de Coleta", command=display_recycling_locations, width=20).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.main_menu, width=20).pack(pady=5)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Run the Tkinter app
if __name__ == "__main__":
    root = tk.Tk()
    app = ReciclyApp(root)
    root.mainloop()