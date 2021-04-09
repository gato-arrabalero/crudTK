#Bibliotecas
from tkinter import ttk
from tkinter import *
import sqlite3

#Clase_Principal

class Product:
    #Nombre_de_la_base_datos

    dbname = 'database.db'
    
    def __init__(self,root):
        self.root = root
        self.root.title("App de Productos")
    #Creacion_del_frame

        self.frame = LabelFrame(self.root, text = "Registro de Productos")
        self.frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)
    #Nombre_Input

        Label(self.frame, text = "Nombre del Producto").grid(row = 1, column = 0)
        self.name = Entry(self.frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1)
    #Precio_Input

        Label(self.frame, text = "Precio del Producto").grid(row = 2, column = 0)
        self.price = Entry(self.frame)
        self.price.grid(row = 2, column = 1)
    #Button_Add_Product

        ttk.Button(self.frame, text = "Guardar Producto", command = self.addProducts).grid(row = 3, columnspan = 2, sticky = W + E)
    
    #Mensaje de salida

        self.mensaje = Label(text = "", fg = "green")
        self.mensaje.grid(row =3, column = 0, columnspan = 2 , sticky = W +E)
  
    #Tabla
        self.tree = ttk.Treeview(height = 10, column = 2)
        self.tree.grid(row = 4 , column = 0 , columnspan = 2)
        self.tree.heading ('#0', text = "Nombre ",  anchor = CENTER)
        self.tree.heading ('#1', text = "Precio", anchor = CENTER )
        #Buttons
        ttk.Button(text = "Borrar", command = self.deleteProduct).grid(row = 5 ,column = 0 , sticky = W + E)
        ttk.Button(text = "Editar", command = self.editProducto).grid(row= 5, column = 1 , sticky = W + E )
        #Llenando la tabla
        self.getproducts()

    #Conexion_consulta_base_datos
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.dbname) as conn:
            cursor = conn.cursor()
            result = cursor.execute (query , parameters)
            conn.commit()
        return result

    #obtener_datos
    def getproducts(self):
        #Limpiando datos
        registros = self.tree.get_children()
        for e in registros:
            self.tree.delete(e)            
        #Consultando datos
        query = 'SELECT * FROM products ORDER BY name DESC'
        dbRows = self.run_query(query)
                #Llenando datos
        for r in dbRows:
            self.tree.insert("", 0, text = r[1], value = r[2])
    
    #Validcion de datos
    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0

    #Agrear porductos
    def addProducts(self):
        if self.validation():
            query = 'INSERT INTO products VALUES (NULL,?,?)'
            parameters = (self.name.get(),self.price.get())
            self.run_query(query,parameters)
            self.mensaje['text'] = "El producto {} ha sido agregado negga!!".format(self.name.get())
            self.name.delete(0,END)
            self.price.delete(0,END)
        else:
            self.mensaje['text'] = "La cagaste nigga"
        self.getproducts()

    #Eliminar productos
    def deleteProduct(self):
        self.mensaje["text"] = ""
        try:
            self.tree.item(self.tree.selection())["text"][0]
        except IndexError as e:
            self.mensaje["text"] = "Selecciona un registro Negga"
            return
        self.mensaje["text"] = ""
        name = self.tree.item(self.tree.selection())["text"]
        query = "DELETE FROM products WHERE name = ?"
        self.run_query(query, (name,))
        self.mensaje["text"] = "El registro {} fue eliminado negga !!".format(name)
        self.getproducts()

    #Editar Registro
    def editProducto(self):
        self.mensaje["text"] = ""
        try:
            self.tree.item(self.tree.selection())["text"][0]
        except IndexError as e:
            self.mensaje["text"] = "Selecciona un registro Negga"
            return
        name = self.tree.item(self.tree.selection())["text"]
        oldPrice = self.tree.item(self.tree.selection())["values"][0]
        self.editWind = Toplevel()
        self.editWind.title = "Editar Producto"

        #Old_name
        Label(self.editWind, text = "Antiguo nombre : ").grid (row = 0 , column = 1)
        Entry(self.editWind, textvariable = StringVar(self.editWind, value = name ), state = "readonly").grid(row = 0, column = 2)

        #New_name
        Label(self.editWind, text ="Nuevo Nombre : " ).grid (row = 1, column = 1)
        newName = Entry (self.editWind)
        newName.grid(row = 1 , column = 2)

        #Old_price
        Label(self.editWind, text = "Antiguo precio : ").grid (row = 2 , column = 1)
        Entry(self.editWind, textvariable = StringVar(self.editWind, value = oldPrice ), state = "readonly").grid(row = 2, column = 2)

        #New_price
        Label(self.editWind, text ="Nuevo Precio : " ).grid (row = 3, column = 1)
        newPrice = Entry (self.editWind)
        newPrice.grid(row = 3 , column = 2)

        #button
        Button(self.editWind, text = "Update", command = lambda: self.editRegistro(newName.get(),name,newPrice.get(),oldPrice)).grid(row = 4, column = 2 , sticky = W )

    def editRegistro(self, newName, name, newPrice, oldPrice):
        query = "UPDATE products SET name = ? , price = ? WHERE name = ? AND price = ?"
        parameters = (newName, newPrice, name, oldPrice)
        self.run_query( query  ,parameters)
        self.editWind.destroy()
        self.mensaje["text"] = "El producto {} se ha actualizado ya negga !! ".format (newName)
        self.getproducts()


#Ejecucion_de_root
if __name__=='__main__': 
    root = Tk()
    app = Product(root)
    root.mainloop()      