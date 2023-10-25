import tkinter as tk
from tkinter import ttk
import sqlite3

# класс главного окна
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()
    
    #создание и работа с главным окном
    def init_main(self):
        toolbar=tk.Frame(bg='#d7d7d7',bd=2)
        toolbar.pack(side=tk.TOP,fill=tk.X)
        
        #Картинка ДОБАВИТЬ
        self.img_add=tk.PhotoImage(file='./img/icon.png')
        btn_add=tk.Button(toolbar,text='Добавить',bg='#d7d7d7',
                           bd=1,image=self.img_add,
                           command=self.open_child)
        btn_add.pack(side=tk.LEFT)

        #Картинка ОБНОВИТЬ
        self.img_upd=tk.PhotoImage(file='./img/icon1.png')
        btn_upd=tk.Button(toolbar,text='Изменить',bg='#d7d7d7',
                           bd=1,image=self.img_upd,
                           command=self.open_update_child)
        btn_upd.pack(side=tk.LEFT)

        #Картинка УДАЛЕНИЕ
        self.img_del=tk.PhotoImage(file='./img/icon2.png')
        btn_del=tk.Button(toolbar,text='Удалить',bg='#d7d7d7',
                           bd=1,image=self.img_del,
                           command=self.delete_records)
        btn_del.pack(side=tk.LEFT)

        #Картинка ПОИСК
        self.img_search=tk.PhotoImage(file='./img/icon3.png')
        btn_search=tk.Button(toolbar,text='Поиск',bg='#d7d7d7',
                           bd=1,image=self.img_search,
                           command=self.open_search)
        btn_search.pack(side=tk.LEFT)

        #Картинка ВОЗВРАТ
        self.img_refresh=tk.PhotoImage(file='./img/icon4.png')
        btn_refresh=tk.Button(toolbar,text='Удалить',bg='#d7d7d7',
                           bd=1,image=self.img_refresh,
                           command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        #Добовляем столбцы
        self.tree=ttk.Treeview(self,columns=('id','name','phone','email',),
                               height=17,show='headings')
        self.tree.column('id',width=45)
        self.tree.column('name',width=175)
        self.tree.column('phone',width=150)
        self.tree.column('email',width=150)
        
        self.tree.heading('id',text='id')
        self.tree.heading('name',text='ФИО')
        self.tree.heading('phone',text='Телефон')
        self.tree.heading('email',text='E-mail')
        
        # Упаковка
        self.tree.pack(side=tk.LEFT)

        #добавление прокрутки
        scroll=tk.Scrollbar(self,command=self.tree.yview)
        scroll.pack(side=tk.LEFT,fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

####################################################################### МЕТОДЫ
    
    #Метод добавления данных
    def records(self,name,phone,email,):
        self.db.insert_data(name,phone,email,)
        self.view_records()
    
    #отображение данных в Treeview
    def view_records(self):
        self.db.cur.execute('SELECT * FROM users')

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('','end',values=row) 
         for row in self.db.cur.fetchall()]
    
    #Обновление данных
    def update_record(self,name,phone,email):
        id=self.tree.set(self.tree.selection()[0],'#1')
        self.db.cur.execute('''
            UPDATE users
            SET name = ?, phone = ?, email = ?
            WHERE id = ?
        ''', (name,phone,email,id))
        self.db.conn.commit()
        self.view_records()

    #Удаление данных
    def delete_records(self):
        for row in self.tree.selection():
            self.db.cur.execute('DELETE from users WHERE id = ?',
                                (self.tree.set(row,'#1'),))
        self.db.conn.commit()
        self.view_records()
     
     
     #Метод поиска данных
    def search_records(self,name):
        self.db.cur.execute('SELECT * FROM users WHERE name LIKE ?',
                             ('%' + name + '%',))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('','end',values=row)
         for row in self.db.cur.fetchall()]

####################################################################

    #метод вызывающий окно обновлений
    def open_child(self):
        Child()

    #метод вызывающий дочернее окно для редактирования
    def open_update_child(self):
        Update()

    #метод вызывающий дочернее окно для поиска
    def open_search(self):
        Search()

###################################################################

#класс дочернего окна
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view=app
    
    #инициализация виджетов дочернего окна
    def init_child(self):
        self.title('Добавление контакт')
        self.geometry('400x220')
        self.resizable(False,False)
        #перехватываем все события
        self.grab_set()
        #перехватываем фокус
        self.focus_set()

        label_name=tk.Label(self,text='ФИО:')
        label_name.place(x=50,y=50)
        label_phone=tk.Label(self,text='Телефон:')
        label_phone.place(x=50,y=80)
        label_email=tk.Label(self,text='Почта:')
        label_email.place(x=50,y=110)
        
        #Поля для ввода
        self.entry_name=tk.Entry(self)
        self.entry_name.place(x=200,y=50)
        self.entry_phone=tk.Entry(self)
        self.entry_phone.place(x=200,y=80)
        self.entry_email=tk.Entry(self)
        self.entry_email.place(x=200,y=110)
        
        #Кнопка закрыть
        self.btn_cancel=tk.Button(self,text='Закрыть',command=self.destroy)
        self.btn_cancel.place(x=300,y=170)
        
        #Конпка добавления
        self.btn_add=tk.Button(self,text='Добавить')
        self.btn_add.bind('<Button-1>',lambda event:self.view.records(self.entry_name.get(),
                                                              self.entry_phone.get(),
                                                              self.entry_email.get()))
        self.btn_add.place(x=220,y=170)

####################################################################################################

#класс дочернего окна для изменения контактов
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_update()
        self.db=db
        self.default_data()

    def init_update(self):
        self.title('Редактировать позицию')
        self.btn_add.destroy()
        self.btn_upd = tk.Button(self,text='Редактировать')
        self.btn_upd.bind('<Button-1>',lambda event:self.view.update_record(self.entry_name.get(),
                                                                        self.entry_phone.get(),
                                                                        self.entry_email.get()))
        self.btn_upd.bind('<Button-1>',lambda event:self.destroy(),add='+')
        self.btn_upd.place(x=200,y=170)
        
    def default_data(self):
        id=self.view.tree.set(self.view.tree.selection()[0],'#1')
        self.db.cur.execute('SELECT * from users WHERE id = ?',(id, ))
        row=self.db.cur.fetchone()
        self.entry_name.insert(0,row[1])
        self.entry_phone.insert(0,row[2])
        self.entry_email.insert(0,row[3])

##############################################################################

#Класс окна для поиска
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_search()
        self.view=app  

    #инициализация виджетов дочернего окна
    def init_search(self):
        self.title('Поиск по контактам')
        self.geometry('300x100')
        self.resizable(False,False)
        #перехватываем все события
        self.grab_set()
        #перехватываем фокус
        self.focus_set()

        label_name=tk.Label(self,text='ФИО:')
        label_name.place(x=20,y=20)

        self.entry_name=tk.Entry(self)
        self.entry_name.place(x=70,y=20)
        
        #Кнопка закрытия
        self.btn_cancel= ttk.Button(self,text='Закрыть',command=self.destroy)
        self.btn_cancel.place(x=200,y=70)
        
        #Кнопка поиска
        self.btn_search=ttk.Button(self,text='Поиск')
        self.btn_search.bind('<Button-1>',
                          lambda event: self.view.search_records(self.entry_name.get()))
        self.btn_search.place(x=70,y=70)
        self.btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')     

############################################################################################################        

#Класс БД
class Db:
    def __init__(self):
        self.conn=sqlite3.connect('contacts.db')
        self.cur=self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY NOT NULL,
                            name TEXT,
                            phone TEXT,
                            email TEXT)''')
        self.conn.commit()

    def insert_data(self,name,phone,email):
        self.cur.execute('''
                         INSERT INTO users (name,phone,email)
                         VALUES (?,?,?)''',(name,phone,email))
        self.conn.commit()


#при запуске программы
if __name__ == '__main__':
    root=tk.Tk()
    db=Db()
    app=Main(root)
    app.pack()
    root.title('Телфоная книга')
    root.geometry('645x450')
    root.resizable(False,False)
    root.configure(bg='white')
    root.mainloop()