import sqlite3 as sq

class Database:

    def __init__(self, db):
        self.con = sq.connect(db)
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS recipes (recipeId INTEGER PRIMARY KEY, name TEXT, url TEXT, tag TEXT)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS ingredients (ingredientId INTEGER PRIMARY KEY, ingredient TEXT, recipeId INTEGER NOT NULL, FOREIGN KEY(recipeId) REFERENCES recipes(recipeId))")

    def insert(self, name, url, tag, ingredients):
        self.cur.execute("INSERT INTO recipes(name, url, tag) VALUES(?,?,?)",(name,url,tag))
        self.cur.execute("SELECT MAX(recipeId) FROM recipes")
        id = self.cur.fetchone()
        for i in ingredients:
            self.cur.execute("INSERT INTO ingredients(ingredient, recipeId) VALUES(?,?)",(i,id[0]))

    def view(self):
        self.cur.execute("SELECT name FROM recipes")
        rows = self.cur.fetchall()
        return rows

    def getRecipe(self, name):
        self.cur.execute("SELECT * FROM recipes WHERE name=?", (name,))
        row = self.cur.fetchone()
        self.cur.execute("SELECT ingredient FROM ingredients WHERE recipeId=?", (row[0],))
        ingredients = self.cur.fetchall()
        list = []
        for i in ingredients:
            list += i
        recipe = [row, list]
        return recipe

    def search(self, tag="", ingredients=[]):
        if ingredients == []:
            self.cur.execute("SELECT * FROM recipes WHERE tag=?", (tag,))
        else:
            for i in ingredients:
                self.cur.execute("SELECT * FROM recipes WHERE tag=? OR recipeId in (SELECT recipeId from ingredients WHERE ingredient=?)", (tag, i))
        rows = self.cur.fetchall()
        return rows

    def delete(self, id):
        self.cur.execute("DELETE FROM ingredients WHERE recipeId=?",(id,))
        self.cur.execute("DELETE FROM recipes WHERE recipeId=?", (id,))

    def update(self, id, name, url, tag, ingredients):
        self.cur.execute("DELETE FROM ingredients WHERE recipeId=?",(id,))
        for i in ingredients:
            self.cur.execute("INSERT INTO ingredients(ingredient, recipeId) VALUES(?,?)",(i,id))
        self.cur.execute("UPDATE recipes SET name=?, url=?, tag=? WHERE recipeId=?",(name, url, tag, id))

    def getTags(self):
        self.cur.execute("SELECT DISTINCT tag FROM recipes")
        rows = self.cur.fetchall()
        return rows

    def __del__(self):
        self.con.commit()
        self.con.close()
