import razorpay
from flask import Flask, render_template, redirect, request
from funcs import *



app=Flask(__name__)
client = razorpay.Client(auth=("rzp_test_jHwZxJlL1LMmSo", "da7Adytf3jZiIAwdVcglFcAJ"))
clientsList = {}


@app.route('/')
def func_name():
    return render_template('main.html')


@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/pay', methods=["GET", "POST"])
def pay():
    if request.form.get("amount") != "":
        amount=request.form.get("amt")
        data = { "amount": amount, "currency": "INR", "receipt": "order_rcptid_11" }
        payment = client.order.create(data=data)
        pdata=[amount, payment["id"]]
        return render_template("index.html", pdata=pdata)
    return redirect("/")

@app.route('/success', methods=["POST"])
def success():
    pid=request.form.get("razorpay_payment_id")
    ordid=request.form.get("razorpay_order_id")
    sign=request.form.get("razorpay_signature")
    print(f"The payment id : {pid}, order id : {ordid} and signature : {sign}")
    params={
    'razorpay_order_id': ordid,
    'razorpay_payment_id': pid,
    'razorpay_signature': sign
    }
    final=client.utility.verify_payment_signature(params)
    if final == True:
        return redirect("/game", code=301)
    return "Something Went Wrong Please Try Again"

@app.route('/game', methods=['GET', 'POST'])
def game():
    sample_list = fetchAllCustomers()
    if request.method == 'POST':
        name = request.form['name']
        print(name, clientsList)
        id = clientsList[name]

        final = createPayout(id)
        print("Payout has been created to "+name+": "+final[1])
        return redirect('/')
    return render_template('game.html', names=sample_list)





@app.route('/customer', methods=['GET', 'POST'])
def customer():
    try:
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            contactID = createContact(name, email)
            createCustomer(name, email)
            print("Contact Had been created")
            print("Customer Has been created")
            print(contactID)
            clientsList[contactID[1]] = contactID[0]
            return redirect('/')  # Redirect to the main page after submission
    except:
        print("Name to short")
        return redirect('/')
    return render_template('customer.html')


app.run(debug=True)