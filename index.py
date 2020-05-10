from tkinter import ttk
from tkinter import *

import sqlite3

class Product:

  db_name = 'database.db'


  def __init__(self, window):
    self.wind = window
    self.wind.title('Product Application')

    #Se crea el contenedor
    frame = LabelFrame(self.wind, text = 'Register a new product')
    frame.grid(row = 0 , column  = 0 , columnspan = 3 , pady = 20)

    #Name input
    Label(frame, text = 'Name: ').grid(row = 1, column = 0)
    self.name = Entry(frame )
    self.name.focus()
    self.name.grid(row = 1, column = 1)

    #Price input
    Label(frame, text = 'Price: ').grid(row = 2, column = 0)
    self.price = Entry(frame )
    self.price.grid(row = 2, column = 1)

    #Button Add
    ttk.Button(frame, text = 'Save product', command = self.add_product).grid(row = 3, columnspan = 2, sticky = W + E)

    #Output message
    self.message = Label(text = '', fg = 'red')
    self.message.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)

    #Table
    self.tree = ttk.Treeview( height = 10 , columns = 2 )
    self.tree.grid(row = 4 , column = 0 , columnspan = 2 )
    self.tree.heading('#0', text = 'Name', anchor = CENTER)
    self.tree.heading('#1', text = 'Price', anchor = CENTER)
    
    #Buttons
    ttk.Button(text = 'Delete', command = self.delete_product).grid(row = 5, column = 0, sticky = W + E)
    ttk.Button(text = 'Update', command = self.update_product).grid(row = 5, column = 1, sticky = W + E)
    
    
    self.get_products()

  def run_query(self, query, parameters = ()):
    with sqlite3.connect(self.db_name) as conn:
      cursor = conn.cursor()
      result = cursor.execute(query, parameters)
      conn.commit()
    return result 

  def get_products(self):
    #Cleaning the table
    records = self.tree.get_children()
    for element in records:
      self.tree.delete(element)
    #Quering data
    query = 'SELECT * FROM product ORDER BY price DESC'
    db_rows = self.run_query(query)
    for row in db_rows:
      self.tree.insert('', 0, text = row[1] ,value = row[2] )

  def validation(self):
    return len(self.name.get()) and len(self.price.get())
  
  def add_product(self):
    print(self.validation)
    if self.validation():
      query = 'INSERT INTO product VALUES(NULL, ?, ?)'
      parameters = (self.name.get(), self.price.get())
      self.run_query(query, parameters)
      self.message['text'] = 'Product {} saved successfully'.format(self.name.get())
      self.name.delete(0, END)
      self.price.delete(0, END)
    else:
      self.message['text'] = 'Name and Price are required'
    self.get_products()

  def delete_product(self):
    self.message['text'] = ''
    try:
      self.tree.item(self.tree.selection())['text'][0]
    except IndexError as e:
      self.message['text'] = 'First, select a record'
      return
    self.message['text'] = ''
    name = self.tree.item(self.tree.selection())['text']
    query = 'DELETE FROM product WHERE name = ?'
    self.run_query(query, (name,))
    self.message['text'] = 'Record {} has been deleted succesfully'.format(name)
    self.get_products()
    
  def update_product(self):
    self.message['text'] = ''
    try:
      self.tree.item(self.tree.selection())['text'][0]
    except IndexError as e:
      self.message['text'] = 'First, select a record'
      return
    name = self.tree.item(self.tree.selection())['text']
    old_price = self.tree.item(self.tree.selection())['values'][0]
    self.edit_window = Toplevel()
    self.edit_window.title = 'Edit Product'
    
    #Old data
    Label(self.edit_window, text = 'Old name: ').grid(row = 0, column = 1)
    Entry(self.edit_window, textvariable = StringVar(self.edit_window, value = name), state = 'readonly').grid(row = 0, column = 2)
    #New data
    Label(self.edit_window, text = 'New name: ').grid(row = 1, column = 1)
    new_name = Entry(self.edit_window)
    new_name.grid(row = 1, column = 2)
    
    #Old Price
    Label(self.edit_window, text = 'Old price: ').grid(row = 2, column = 1)
    Entry(self.edit_window, textvariable = StringVar(self.edit_window, value = old_price), state = 'readonly').grid(row = 2, column = 2)
    #New Price
    Label(self.edit_window, text = 'New price: ').grid(row = 3, column = 1)
    new_price = Entry(self.edit_window)
    new_price.grid(row = 3, column = 2)
    
    Button(self.edit_window, text = 'Update', command = lambda: self.edit_records(new_name.get(), name, new_price.get(), old_price)).grid(row = 4, column = 2, sticky = W + E)
    
  def edit_records(self, new_name, name, new_price, old_price):
    query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'
    parameters = (new_name, new_price, name, old_price)
    self.run_query(query, parameters)
    self.edit_window.destroy
    self.message['text'] = 'Record {} updated succesfully'.format(name)
    self.get_products()
    
if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()