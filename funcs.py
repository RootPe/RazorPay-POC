import razorpay
import requests


client = razorpay.Client(auth=("rzp_test_jHwZxJlL1LMmSo", "da7Adytf3jZiIAwdVcglFcAJ"))

masterCard = "4111111111111111"



def fetchAllCustomers():
    values = client.customer.all()
    filtered = []
    for i in values['items']:
        filtered.append((i['id'], i['name']))
    return filtered

def createCustomer(name: str, email: str):
    client.customer.create({
        "name": name,
        "email": email})

def createContact(name, email):
    headers = {
        'Content-Type': 'application/json',
    }

    json_data = {
        'name': name,
        'email': email
    }

    response = requests.post(
        'https://api.razorpay.com/v1/contacts',
        headers=headers,
        json=json_data,
        auth=('rzp_test_jHwZxJlL1LMmSo', 'da7Adytf3jZiIAwdVcglFcAJ')
    )
    return (response.json()['id'], name)

def createPayout(contactID):
    import requests
    accountNumber = '2323230066978795'
    amount = 8000

    headers = {
        'Content-Type': 'application/json',
    }

    json_data = {
              "account_number": accountNumber,
              "contact": {
                "id": contactID
              },
              "amount": 4000,
              "currency": "INR",
              "purpose": "payout",
              "description": "Payout link",
              "receipt": "Receipt No. 1",
              "send_email": True
            }

    response = requests.post(
        'https://api.razorpay.com/v1/payout-links',
        headers=headers,
        json=json_data,
        auth=('rzp_test_jHwZxJlL1LMmSo', 'da7Adytf3jZiIAwdVcglFcAJ'),
    )
    return (response.json()['id'], response.json()['short_url'])

def close(contactID):
    import requests
    headers = {
        'Content-Type': 'application/json',
    }



    response = requests.post(
        'https://api.razorpay.com/v1/virtual_accounts/'+contactID+'/close',
        headers=headers,
        auth=('rzp_test_jHwZxJlL1LMmSo', 'da7Adytf3jZiIAwdVcglFcAJ'),
    )
    print(response.json())
close('cust_OOTHriTAisVF9s')