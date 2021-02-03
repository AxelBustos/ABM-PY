from tkinter import ttk
from tkinter import *

import sqlite3

class Product:
    
    db_name = 'database.db'

    def __init__(self):
        self.wind=Tk()

        self.wind.title('Control de productos')
        self.wind.geometry("830x320")
        self.wind.resizable(0, 0)

        #contenedor 
        self.izq = Frame(self.wind, width=300,height=400)
        self.izq.pack(side="left")
        self.der = Frame(self.wind, width=600, height=360)
        self.der.pack(side="right")

        self.bot=Frame(self.der,width=600,height=40)
        self.bot.grid(row=1,column=0)

        #nombre 
        Label(self.izq,text="Nombre del producto",font=(16)).grid(row=0,column=0)

        self.name=Entry(self.izq,width="40")
        self.name.grid(row=1,column=0)
        self.name.focus()

        # precio
        Label(self.izq,text="Ingrese el precio",font=(16)).grid(row=2,column=0)

        self.price=Entry(self.izq,width="40")
        self.price.grid(row=3,column=0)
        #cantidad
        Label(self.izq,text="Cantidad de unidades",font=(16)).grid(row=4,column=0)

        self.cantidad=Entry(self.izq,width="40")
        self.cantidad.grid(row=5,column=0)
        
        
        #boton agregar
        Button(self.izq,text="Agregar",command = self.add_product,width="40").grid(row=6)

        Button(self.bot,text = 'Borrar', command = self.delete_product,width="25").grid(row=0,column=0)
        Button(self.bot,text = 'Editar',command = self.edit_product,width="25").grid(row=0,column=1)
        

        

        # listado
        self.lista=ttk.Treeview(self.der,columns=('precio','cantidad'))
        self.lista.grid(row=0,column=0)
        
        self.lista.column('#0')
        self.lista.column('precio')
        self.lista.column('cantidad')

        self.lista.heading('#0',text="Nombre")
        self.lista.heading('precio',text="Precio")
        self.lista.heading('cantidad',text="Cantidad")

        
        self.get_products()

   
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    
    def get_products(self):
        
        records = self.lista.get_children()
        for element in records:
            self.lista.delete(element)
        query = 'SELECT * FROM product ORDER BY name DESC'
        db_rows = self.run_query(query)
        #listarlo
        for row in db_rows:
            self.lista.insert('', 0, text = row[1], values = (row[2],row[3]))

   
    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0 and len(self.cantidad.get()) != 0

    def add_product(self):
        if self.validation():
            query = 'INSERT INTO product VALUES(NULL, ?, ?,?)'
            parameters =  (self.name.get(), self.price.get(),self.cantidad.get())
            self.run_query(query, parameters)
            
            self.name.delete(0, END)
            self.price.delete(0, END)
            self.cantidad.delete(0, END)
        self.get_products()
    def delete_product(self):
        name = self.lista.item(self.lista.selection())['text']
        query = 'DELETE FROM product WHERE name = ?'
        self.run_query(query, (name, ))
        self.get_products()
    def edit_product(self):
        
        name = self.lista.item(self.lista.selection())['text']
        old_price = self.lista.item(self.lista.selection())['values'][0]
        old_cantidad=self.lista.item(self.lista.selection())['values'][1]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Edit Product'
        # nombre anterior
        Label(self.edit_wind, text = 'Nombre a editar:').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = name), state = 'readonly').grid(row = 0, column = 2)
        # nuevo nombre
        Label(self.edit_wind, text = 'Nuevo nombre:').grid(row = 1, column = 1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row = 1, column = 2)

        # precio anterior 
        Label(self.edit_wind, text = 'Precio a editar:').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_price), state = 'readonly').grid(row = 2, column = 2)
        # nuevo precio
        Label(self.edit_wind, text = 'Nuevo precio:').grid(row = 3, column = 1)
        new_price= Entry(self.edit_wind)
        new_price.grid(row = 3, column = 2)

        # anterior cantidad 
        Label(self.edit_wind, text = 'Cantidad a editar:').grid(row = 4, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_cantidad), state = 'readonly').grid(row = 4, column = 2)
        # Nueva cantidad
        Label(self.edit_wind, text = 'Nueva cantidad:').grid(row = 5, column = 1)
        new_cantidad= Entry(self.edit_wind)
        new_cantidad.grid(row = 5, column = 2)

        Button(self.edit_wind, text = 'Guardar', command = lambda: self.edit_records(new_name.get(), name, new_price.get(), old_price,new_cantidad.get(),old_cantidad)).grid(row = 7, column = 2, sticky = W)
        self.edit_wind.mainloop()

    def edit_records(self, new_name, name, new_price, old_price,new_cantidad,old_cantidad):
        query = 'UPDATE product SET name = ?, price = ?, cantidad = ? WHERE name = ? AND price = ? AND cantidad = ?'
        parameters = (new_name, new_price,new_cantidad,name, old_price,old_cantidad)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        
        self.get_products()
        self.wind.mainloop()

pantallaPrincipal=Product()


