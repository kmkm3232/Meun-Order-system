from flask import Flask, render_template, request, session, redirect, flash, url_for
import cx_Oracle
from datetime import *
import time

app = Flask(__name__)
app.secret_key = " "
conn = cx_Oracle.connect('G2_team02/ceG2_team02@144.214.177.102/xe')

@app.route("/layout")
def layout():
	return render_template("layout.html")
    
@app.route("/login", methods=['POST', 'GET'])
def login():
	# error = None
	if request.method == 'POST':
		pyuserid= request.form["userid"]
		pypw = request.form["password"]
		cursor = conn.cursor()
		sql1 = ("SELECT USER_ID, USER_PASSWORD  FROM USERS WHERE USER_ID = '"+pyuserid+"'AND USER_PASSWORD = '"+pypw+"'" )
		cursor.execute(sql1)
		conn.commit()
		results = cursor.fetchall()
		for row in results:
			ffuserid = row[0]
			session['usern'] = ffuserid
			if cursor.execute(sql1):
				flash('logged in')
				return redirect(url_for("login"))
		else:
			flash('Incorrect username or password')
			return redirect(url_for("login"))

	return render_template("login.html")


@app.route("/orders", methods=['POST','GET'])
def orders():

    cursor = conn.cursor()
    cursor.execute("""SELECT a.PRODUCT_NAME, b.* FROM PRODUCT a, ORDER_ITEMS b WHERE a.PRODUCT_ID = b.PRODUCT_ID AND ORDER_ID = (SELECT MAX(ORDER_ID) FROM ORDER_ITEMS)""")
    orders_results = cursor.fetchall()

    cursor = conn.cursor()
    cursor.execute("""SELECT TOTALPRICE FROM ORDERS WHERE ORDER_ID = (SELECT MAX(ORDER_ID) FROM ORDER_ITEMS)""")
    price_results = cursor.fetchall()

    return render_template('orders.html', orders_results=orders_results)

@app.route("/logout")
def logout():
	session.pop('usern', None)
	flash('logged out')
	return redirect(url_for("login"))

@app.route("/index")
def index():
	return render_template("index.html")

@app.route('/drinks')
def drinks():
    if "cart" not in session:
        session['cart'] = []
    if "usern" in session:
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM Product WHERE PRODUCT_TYPE = 'Drink' """)
        drink_results = cursor.fetchall()
        cursor = conn.cursor()
        cursor.execute("""SELECT DISTINCT Product_type FROM Product """)
        distinct_product_type = cursor.fetchall()
        return render_template('drinks.html', drink_results=drink_results, distinct_product_type=distinct_product_type)
    elif "usern" not in session:
        flash  ('login fisrt!')
        return redirect(url_for("login"))

@app.route('/pizza')
def pizza():
    if "cart" not in session:
        session['cart'] = []
    if "usern" in session:
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM Product WHERE PRODUCT_TYPE = 'Pizza' """)
        pizza_results = cursor.fetchall()
        cursor = conn.cursor()
        cursor.execute("""SELECT DISTINCT Product_type FROM Product """)
        pizza_product_type = cursor.fetchall()
        return render_template('pizza.html', pizza_results=pizza_results, pizza_product_type=pizza_product_type)
    elif "usern" not in session:
        flash  ('login fisrt!')
        return redirect(url_for("login"))

@app.route('/snack')
def snack():
    if "cart" not in session:
        session['cart'] = []
    if "usern" in session:
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM Product WHERE PRODUCT_TYPE = 'Snack' """)
        snack_results = cursor.fetchall()
        cursor = conn.cursor()
        cursor.execute("""SELECT DISTINCT Product_type FROM Product """)
        snack_product_type = cursor.fetchall()
        return render_template('snack.html', snack_results=snack_results, snack_product_type=snack_product_type)
    elif "usern" not in session:
        flash  ('login fisrt!')
        return redirect(url_for("login"))
@app.route('/set')
def combo():
    if "cart" not in session:
        session['cart'] = []
    if "usern" in session:
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM Product WHERE PRODUCT_TYPE = 'Set' """)
        set_results = cursor.fetchall()
        cursor = conn.cursor()
        cursor.execute("""SELECT DISTINCT Product_type FROM Product """)
        set_product_type = cursor.fetchall()
        return render_template('set.html', set_results=set_results, set_product_type=set_product_type)
    elif "usern" not in session:
        flash  ('login fisrt!')
        return redirect(url_for("login"))

@app.route('/rice&spaghetti')
def maincourses():
    if "cart" not in session:
        session['cart'] = []
    if "usern" in session:
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM Product WHERE PRODUCT_TYPE = 'Rice & Spaghetti' """)
        rice_results = cursor.fetchall()
        cursor = conn.cursor()
        cursor.execute("""SELECT DISTINCT Product_type FROM Product """)
        rice_product_type = cursor.fetchall()
        return render_template('rice_spaghetti.html', rice_results=rice_results, rice_product_type=rice_product_type)
    elif "usern" not in session:
        flash  ('login fisrt!')
        return redirect(url_for("login"))

@app.route('/addtocart', methods=['POST', 'GET'])
def atc():
    added = False
    targetPid = request.form["productid"]
    targetpName = request.form["productname"]
    targetpPrice = request.form["productprice"]
    targetpQuantity = request.form["addtocartquantity"]
    targetpnum = request.form["productnum"]
    index = time.localtime()
    if session['cart'] == []:
        session['cart'].append([targetPid, targetpName, targetpPrice, targetpQuantity, targetpnum,'single', index])
        session.modified = True
    else:
        for i in session['cart']:
            if targetPid == i[0]:
                if i[5] == 'single':
                    a = int(i[3])
                    b = int(targetpQuantity)
                    newq = a + b
                    i[3] = newq
                    session.modified = True
                    added = True
                    break
        if not added:
            session['cart'].append([targetPid, targetpName, targetpPrice, targetpQuantity, targetpnum, 'single', index])
            session.modified = True
    flash('Added ' + targetpQuantity + ' ' + targetpName + ' ' + 'to shopping cart.')
    return redirect(request.referrer)

@app.route('/addtocart2', methods=['POST', 'GET'])
def atc2():
    cursor = conn.cursor()
    cursor.execute(""" SELECT COUNT(*) from product""")
    totalproductnum = cursor.fetchone()
    setid = request.form["set_id_py"]
    setname = request.form["set_name_py"]
    setprice = request.form["set_price_py"]
    setqty = request.form["set_qty_py"]
    setnum = request.form["set_num_py"]
    index = time.localtime()
    session['cart'].append([setid, setname, setprice, '1', setnum, 'set', index])
    for i in range(1,21):
        if "py_id"+str(i) in request.form:
            if int(request.form["py_qty"+str(i)]) >0:
                targetPid = request.form["py_id"+ str(i)]
                targetpName = request.form["py_name"+str(i)]
                targetpQuantity = request.form["py_qty"+str(i)]
                targetpnum = request.form["py_num"+str(i)]
                session['cart'].append([targetPid, targetpName, '0', targetpQuantity, targetpnum, 'setitem', index])
                session.modified = True
        else:
            continue
    flash('Added'+' '+setname+' to shopping cart.')
    return redirect('http://localhost:8000/set')

@app.route('/remove', methods=['POST', 'GET'])
def remove():
    removeitem = request.form["removeitem"]
    removeitemname = request.form["productname"]
    indexx = request.form["index"]
    for i in reversed(session['cart']):
        if str(i[6]) == indexx:
            session['cart'].remove(i)
            session.modified = True
    if request.referrer == "http://localhost:8000/addtocart_set":
        return redirect("http://localhost:8000/set")
    flash('Removed ' + ' ' + removeitemname + ' ' + 'from shopping cart.')
    return redirect(request.referrer)


@app.route('/update', methods=['POST', 'GET'])
def update():
    updateitem = request.form["updateitem"]
    updatequantity = request.form["qt"]
    for i in session['cart']:
        if updateitem == i[0]:
            if i[5] == 'single':
                i[3] = updatequantity
                session.modified = True
                break
    flash('Updated!')
    if request.referrer == "http://localhost:8000/addtocart_set":
        return redirect("http://localhost:8000/set")
    return redirect(request.referrer)

@app.route('/insert', methods=['POST', 'GET'])
def insert():
    x = date.today()
    total = 0
    for i in session['cart']:
        if i[5] == 'single':
            total += float(i[2]) * float(i[3])
        if i[5] == 'set':
            print (i[2],i[3])
            total += float(i[2]) * float(i[3])
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO INVOICE (USER_ID, INVOICE_DATE) VALUES('{0}','{1}')""".format(session['usern'],x.strftime("%d-%b-%Y")))
    insert_results = conn.commit()

    cursor = conn.cursor()
    cursor.execute("""INSERT INTO ORDERS (INVOICE_ID) SELECT INVOICE_ID FROM INVOICE WHERE ROWNUM<=1 ORDER BY INVOICE_ID DESC""")
    insert_results = conn.commit()

    cursor = conn.cursor()
    cursor.execute("""UPDATE ORDERS SET TOTALPRICE = ('{0}'), ORDER_DATE = ('{1}') WHERE ORDER_ID = (SELECT MAX (ORDER_ID) FROM ORDERS)""".format(total,x.strftime("%d-%b-%Y")))
    insert_results = conn.commit()

    for i in session['cart']:
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO ORDER_ITEMS (ORDER_ID, PRODUCT_ID,   QUANTITY, PRICE, ITEM_REMARK) VALUES((SELECT MAX(ORDER_ID) FROM ORDERS), '{0}','{1}','{2}','{3}')""".format(i[0],i[3],i[2],i[6]))
        insert_results = conn.commit()

    session['cart'] = []
    session.modified = True
    if request.referrer == "http://localhost:8000/addtocart_set":
        return redirect("http://localhost:8000/set")

    return redirect(request.referrer)
@app.route('/addtocart_set', methods=['POST', 'GET'])
def addtocartset():
    targetPid = request.form["productid"]
    targetpName = request.form["productname"]
    targetpPrice = request.form["productprice"]
    targetpQty = request.form["asetqty"]
    targetpnum = request.form["productnum"]
    cursor = conn.cursor()
    cursor.execute(
        """ SELECT product_id, set_product_quantity from product_set where set_id = '{0}' """.format(targetPid))
    setitem = cursor.fetchall()
    setitem_results_pizza = []
    setitem_results_drinks = []
    setitem_results_snack = []
    setitem_results_rice = []
    for i in setitem:
        cursor = conn.cursor()
        cursor.execute(""" SELECT remark from product where product_id = '{0}' """.format(i[0]))
        checkremark = cursor.fetchone()

        if checkremark[0] == 'a':
            cursor = conn.cursor()
            cursor.execute(""" SELECT * from product where product_id = '{0}' """.format(i[0]))
            results = cursor.fetchall()
            cursor = conn.cursor()
            cursor.execute(""" SELECT product_type from product where product_id = '{0}' """.format(i[0]))
            results_type = cursor.fetchone()
            if results_type[0] == 'Pizza':
                setitem_results_pizza.append(results[0]+i)
            if results_type[0] == 'Drink':
                setitem_results_drinks.append(results[0]+i)
            if results_type[0] == 'Snack':
                setitem_results_snack.append(results[0]+i)
            if results_type[0] == 'Rice & Spaghetti':
                setitem_results_rice.append(results[0]+i)
        else:
            cursor = conn.cursor()
            cursor.execute(""" SELECT * from product where product_type = '{0}' """.format(checkremark[0]))
            results = cursor.fetchall()
            for x in results:
                if checkremark[0] == 'Pizza':
                    setitem_results_pizza.append(x+i)
                if checkremark[0] == 'Drink':
                    setitem_results_drinks.append(x+i)
                if checkremark[0] == 'Snack':
                    setitem_results_snack.append(x+i)
                if checkremark[0] == 'Rice & Spaghetti':
                    setitem_results_rice.append(x+i)
    return render_template('set_detail.html', setitem_results_pizza=setitem_results_pizza,
                           setitem_results_drinks=setitem_results_drinks, setitem_results_snack=setitem_results_snack,
                           setitem_results_rice=setitem_results_rice, targetpName=targetpName, targetpPrice=targetpPrice, targetPid=targetPid, targetpnum=targetpnum)

@app.route('/seeorder', methods=['POST', 'GET'])
def seeorder():
    if "usern" in session:
        cursor = conn.cursor()
        cursor.execute(""" SELECT * from Orders""")
        orders = cursor.fetchall()
        return render_template('seeorder.html',orders=orders)
    elif "usern" not in session:
        flash  ('login fisrt!')
        return redirect(url_for("login"))
        
@app.route('/removeorders', methods=['POST', 'GET'])
def removeorder():
    removeoid = request.form["remove_oid"]
    cursor = conn.cursor()
    cursor.execute(""" DELETE FROM Order_items where order_id = '{0}'""".format(removeoid))
    a = conn.commit()
    cursor = conn.cursor()
    cursor.execute(""" DELETE FROM Orders where order_id = '{0}'""".format(removeoid))
    a = conn.commit()
    cursor = conn.cursor()
    cursor.execute(""" SELECT * from Orders""")
    orders = cursor.fetchall()
    return render_template('seeorder.html',orders=orders)    

@app.route('/editorders',methods=['POST', 'GET'])
def editorders():
    editoid = request.form["edit_oid"]
    cursor = conn.cursor()
    cursor.execute(""" SELECT * from Orders WHERE Order_id = '{0}'""".format(editoid))
    order_detail = cursor.fetchall()

    cursor = conn.cursor()
    cursor.execute(""" SELECT * from Order_items WHERE Order_id = '{0}' """.format(editoid))
    x = cursor.fetchall()
    order_items_detail =[] 
    for i in x:
        cursor = conn.cursor()
        cursor.execute(""" SELECT Product_type from product where product_id ='{0}' """.format(i[1]))
        type1 = cursor.fetchone()
        print(type1)
        if type1[0] == 'Set':
            cursor = conn.cursor()
            cursor.execute(""" SELECT Product_name, price, Product_id from product where product_id ='{0}' """.format(i[1]))
            product = cursor.fetchone()
            order_items_detail.append([product[2], product[0], i[2], product[1], 'set', i[4], editoid])
            continue
        elif i[3] > 0:
            cursor = conn.cursor()
            cursor.execute(""" SELECT Product_name, price, Product_id from product where product_id ='{0}' """.format(i[1]))
            product = cursor.fetchone()
            order_items_detail.append([product[2], product[0], i[2], product[1], 'single', i[4], editoid]) 
        else:
            cursor = conn.cursor()
            cursor.execute(""" SELECT Product_name, price, Product_id from product where product_id ='{0}' """.format(i[1]))
            product = cursor.fetchone()
            order_items_detail.append([product[2], product[0], i[2], '0', 'setitem', i[4], editoid])
    return render_template('editorder.html',order_detail=order_detail, order_items_detail=order_items_detail)

@app.route('/updateitem', methods=['POST','GET'])
def updateitem():
    oid        = request.form["order"]
    itemremark = request.form["updateitem"]
    qty        = request.form["qty"]
    newtotal = 0
    print (oid, 'idddddd' , itemremark, 'remarkkkkk' , qty, 'qtyyyyyyy')
    cursor = conn.cursor()
    cursor.execute(""" UPDATE order_items SET quantity = '{0}' where item_remark = '{1}' """. format(qty, itemremark))
    a = conn.commit()

    cursor = conn.cursor()
    cursor.execute(""" SELECT price, quantity from order_items where order_id = '{0}'""".format(oid))
    itemlist = cursor.fetchall()
    for i in itemlist:
        newtotal +=i[0]*i[1]

    cursor = conn.cursor()
    cursor.execute(""" UPDATE orders set totalprice = '{0}' where order_id = '{1}' """.format(newtotal, oid))
    a = conn.commit()

    cursor = conn.cursor()
    cursor.execute(""" SELECT * from Orders""")
    orders = cursor.fetchall()

    return render_template('seeorder.html',orders=orders)

@app.route('/delitem', methods=['POST','GET'])
def delitem():
    oid        = request.form["order"]
    itemremark = request.form["delitem"]
    newtotal = 0
    cursor = conn.cursor()
    cursor.execute(""" SELECT item_remark, price, quantity from order_items where order_id = '{0}'""".format(oid))
    itemlist = cursor.fetchall()
    for i in itemlist:
        if i[0] == itemremark:
            continue 
        else:
            newtotal +=int(i[1])*int(i[2])

    cursor = conn.cursor()
    cursor.execute(""" DELETE From order_items where item_remark = '{0}' """. format(itemremark))
    a = conn.commit()

    cursor = conn.cursor()
    cursor.execute(""" UPDATE orders set totalprice = '{0}' where order_id = '{1}' """.format(newtotal, oid))
    a = conn.commit()

    if newtotal == 0:
        cursor = conn.cursor()
        cursor.execute(""" DELETE From orders where order_id = '{0}' """. format(oid))
        a = conn.commit()

    cursor = conn.cursor()
    cursor.execute(""" SELECT * from Orders""")
    orders = cursor.fetchall()

    return render_template('seeorder.html',orders=orders)

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=8000)
