from flask import Flask,render_template, request
import sqlite3 as sql

app=Flask("_  _name__")

l=[]
@app.route("/")
def show():
    conn=sql.connect("shop.db")
    cur=conn.cursor()
    cur.execute("select * from buyer")
    a=cur.fetchall()
    for i in a:
        dic={"name":i[0],"mobile":i[1],"amount":i[2]}
        l.append(dic)

    return render_template("show.html",data=l)

l2=[]
@app.route("/products")
def products():
    conn=sql.connect("shop.db")
    cur=conn.cursor()
    cur.execute("select * from product")
    a=cur.fetchall()
    for i in a:
        dic={"product":i[0],"price":i[1]}
        l2.append(dic)

    return render_template("products.html",data=l2)

@app.route("/home",methods=["get","post"])
def update():
    if request.form.get("name")!=None:
        name=request.form.get("name")
        mobile=request.form.get("mobile")
        product=request.form.get("product")
        quantity=request.form.get("quantity")

        conn=sql.connect("shop.db")
        cur=conn.cursor()
        cur.execute("insert into purchase (name,mobile,product,quantity) values (?,?,?,?)",(name,mobile,product,quantity))
        conn.commit()

        cur.execute("select price from product where pname=?",(product,))
        less=cur.fetchall()
        less=less[0][0]
        quantity=int(quantity)
        less=less*quantity

        cur.execute("update buyer set amount=amount-? where mobile=?",(less,mobile))
        conn.commit()
        
        l=[]
        conn=sql.connect("shop.db")
        cur=conn.cursor()
        cur.execute("select * from buyer")
        a=cur.fetchall()
        for i in a:
            dic={"name":i[0],"mobile":i[1],"amount":i[2]}
            l.append(dic)

        return render_template("purchased.html",data=l)
    
    return render_template("index.html")


if __name__=="__main__":
    app.run(debug=True)