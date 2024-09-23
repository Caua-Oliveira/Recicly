from user import User, fetch_user_by_email, save_user_to_db, delete_user_from_db, connect_to_db


class UserNode:
    def __init__(self, user):
        self.user = user
        self.next = None
        self.prev = None


class UserLinkedList:
    def __init__(self):
        self.head = None
        self.load_users_from_db()

    def load_users_from_db(self):
        db = connect_to_db()
        if not db:
            print("Failed to connect to database")
            return

        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")

        for row in cursor.fetchall():
            user = User(
                name=row['name'],
                email=row['email'],
                password=row['password'],
                cpf=row['cpf'],
                is_active=row['is_active']
            )
            self.append_user(user, save_to_db=False)

        cursor.close()
        db.close()

    def append_user(self, user, save_to_db=True):
        new_node = UserNode(user)
        if self.head is None:
            self.head = new_node
        else:
            last = self.head
            while last.next:
                last = last.next
            last.next = new_node
            new_node.prev = last

        #if save_to_db:
            #save_user_to_db(user)

    def prepend_user(self, user):
        new_node = UserNode(user)
        if self.head is None:
            self.head = new_node
        else:
            self.head.prev = new_node
            new_node.next = self.head
            self.head = new_node
        save_user_to_db(user)

    def delete_user(self, user):
        if self.head is None:
            return
        temp = self.head
        while temp and temp.user.cpf != user.cpf:
            temp = temp.next
        if temp is None:
            return
        if temp.prev:
            temp.prev.next = temp.next
        if temp.next:
            temp.next.prev = temp.prev
        if temp == self.head:
            self.head = temp.next
        delete_user_from_db(temp.user.cpf)

    def count_users(self):
        temp = self.head
        count = 0
        while temp:
            count += 1
            temp = temp.next
        return count

    def search_user_by_email(self, email):
        temp = self.head
        while temp:
            if temp.user.email == email:
                return temp.user
            temp = temp.next
        return None

    def display_users(self):
        temp = self.head
        while temp:
            print(temp.user, end=' ')
            temp = temp.next
        print()

    def display_users_reverse(self):
        temp = self.head
        if temp is None:
            return
        while temp.next:
            temp = temp.next
        while temp:
            print(temp.user, end=' ')
            temp = temp.prev
        print()

    def display_rankings(self):
        # Collect all users and their trash amount into a list
        rankings = []
        temp = self.head
        while temp:
            rankings.append((temp.user.name, temp.user.statistics.total_trash_amount))
            temp = temp.next

        # Sort the list by trash amount, highest first
        rankings.sort(key=lambda x: x[1], reverse=True)

        # Display rankings
        for i, (name, trash_amount) in enumerate(rankings, 1):
            print(f"{i}. {name} - {trash_amount} kg")
