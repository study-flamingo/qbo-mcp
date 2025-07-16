# Exploring the Quickbooks Online Accounting API - Apideck

In this article, you'll understand how the API works, how you can connect to it, and how you can actually use it to perform various tasks, such as automatically updating accounts, invoices, bills, and more. Furthermore, you'll learn about the Apideck Unified API platform that simplifies the entire process.

## Exploring the QBO API

QuickBooks is the leading business accounting software, with a market share close to 85 percent, offering a comprehensive suite of tools, such as invoicing, estimates, instant business loans, and detailed reports.

It's quite powerful on its own, but what if you could integrate it with the rest of your tech stack? Imagine automating financial report generation with data from your sales platform or perfectly synchronized invoices and payment information between your e-commerce store and QuickBooks.

That's precisely where the QuickBooks Online Accounting API or also often referred to as the QBO API comes in, allowing you to programmatically manage your QuickBooks account, create scripts to directly interact with QuickBooks, and integrate with a selection of other services.

In this article, you'll understand how the API works, how you can connect to it, and how you can actually use it to perform various tasks, such as automatically updating accounts, invoices, bills, and more. Furthermore, you'll learn about the Accounting API offered by Apideck that simplifies the entire process.

## The QuickBooks Online Accounting API

The QuickBooks Online Accounting API uses the REST framework to provide apps with access to the customer-facing features in the software. The API is broken down into several entities that you can use to access different parts of the app. For example, the **Bill** entity has various details and fields about individual bills, such as vendor reference, currency reference, transaction date, amount, and due date.

It utilizes standard HTTP methods (GET, POST, PUT, DELETE) and returns JSON objects, making it compatible with a wide range of languages and frameworks, like Python, Java, TypeScript, and PHP. The API provides unique abilities apart from basic create, read, update, and delete (CRUD) operations, such as the following:

The API is free and has no volume limits, but there is a per-minute throttling limit (max 500 requests per minute) for sending requests. It also provides free sandbox accounts. If you want to use it with your own real QuickBooks account, you have to purchase a paid plan to create an account (the API is free regardless). Pricing for QuickBooks Online varies depending on the plan.

### Challenges with the QuickBooks Online Accounting API

It isn't all sunshine and rainbows, though, and there are numerous roadblocks you may face along the way.

One of the biggest challenges with the QuickBooks Online Accounting API is implementing proper authentication via OAuth 2.0. This ensures that your app securely accesses a user's QuickBooks account without compromising their privacy.

The authentication process requires users to grant access to their QuickBooks account, after which QuickBooks sends the developer an access token and a refresh token to get data from the user's account. However, the access token is valid for only one hour, after which you must use the refresh token to reset the access token. On top of that, the refresh token is valid for one hundred days, after which you will have to redo the entire authorization flow. However, this expiry date is rolling and extends each time it’s used to refresh an access token So, if you refresh the token before the end of this period, you won't have to go through the flow again. Still, It can be challenging to build this logic without disrupting the user experience.

Error handling is another crucial aspect that can be quite complex. It provides a variety of error codes and messages that detail why a request may have failed. For example, the following are common HTTP status code responses:

`400 Bad Request`
`401 Unauthorized`
`403 Forbidden`

Along with these, the QuickBooks response also includes a separate error code that may be mapped to specific issues, as seen in their documentation. You must establish a well-defined error-handling strategy that interprets and captures these error codes and their details.

You must also familiarize yourself with the request and response structures to use the API effectively. It has many different endpoints for each feature, such as invoices, accounts, bills, customers, and employees; and each endpoint has different requirements. Use their documentation to look up the requirements for each one of them and ensure you don't send bad requests.

It can also become difficult to parse the API responses or create the JSON payloads, which often contain many complex nested objects. Since many API operations require asynchronous operations and handling, especially when dealing with long-running operations, a clear understanding of managing promise chains and callbacks is necessary.

Lastly, while the sandbox environment provides a useful platform for testing, it offers only a limited data set. This limitation means that it cannot fully replicate the myriad errors and scenarios you may encounter in a live environment. Real-world testing is essential for developing a comprehensive understanding of how to address various issues that may arise during actual use.

## Authentication and Integration with the QuickBooks Online Accounting API

In this section, you'll learn how to authenticate the QuickBooks Online Accounting API and get your access and refresh tokens.

Head over to https://developer.intuit.com/ and click the **Sign Up** button.

Fill in your account details, and then navigate to the **Sandbox** option from the profile menu. If you don't find a sandbox company already created, click the **Add a sandbox company** button:

Next, go to the **Dashboard** tab and click **Create an app**. Select **QuickBooks Online and Payments** as the platform you want to develop for:

Give your app a name and tick only the `com.intuit.quickbooks.accounting` option for the scope:

`com.intuit.quickbooks.accounting`

Now, navigate to the **Keys & credentials** within the **Development Settings** option and get the **Client ID** and **Client Secret**:

If you're interested, you can find the GitHub repo for the full code here.

You'll use the following libraries in your code, so you need to download them with npm or another package manager:

`.env`
`process.env`

This tutorial uses Visual Studio Code, which you can download from their official page.

You can store sensitive data like the client ID, secret, and redirect URI in a `.env file`, as in the following snippet:

`.env file`
`# .env
CLIENT_ID="YOUR_CLIENT_SECRET_COPIED_EARLIER"
CLIENT_SECRET="YOUR_CLIENT_SECRET_COPIED_EARLIER"
REDIRECT_URI="http://localhost:3000/callback"`

Navigate to the **Keys** page in your Intuit Developer account and update the **Redirect URIs > LINK** field with the value `http://localhost:3000/callback`. Ensure that this value exactly matches both your `.env` and your Intuit Developer account:

`http://localhost:3000/callback`
`.env`

Before getting into the actual code, let's briefly review how the authorization process works:

As seen in this diagram, you first send a GET request to a QuickBooks endpoint where the user authorizes access to their account. Then, that page redirects you to the `redirect_uri` specified in your `.env` file and includes the authorization code.

`redirect_uri`
`.env`

Next, you send a POST request to another endpoint that allows you to exchange this authorization code with the access and refresh tokens used to access user data.

The first thing you must do is visit the QuickBooks authorization page:

```python
from flask import Flask, redirect, request, jsonify
import os
import requests
import base64
from urllib.parse import quote_plus

app = Flask(__name__)

# Global variables to store tokens (for demonstration purposes)
accessToken = None
refreshToken = None
BASE_URL = None

@app.route('/auth')
def auth():
    redirect_uri = quote_plus(os.environ.get('REDIRECT_URI'))
    auth_url = f"https://appcenter.intuit.com/connect/oauth2?client_id={os.environ.get('CLIENT_ID')}&response_type=code&scope=com.intuit.quickbooks.accounting&redirect_uri={redirect_uri}&state=demo-app"
    return redirect(auth_url)
```

Here, you retrieve the redirect URI from the environment variables and encode it to ensure it's correctly formatted. Next, the `authUrl` is constructed with crucial data, such as the `client_id`, `client_secret`, `response_type`, and `state`, encoded as URL query parameters.

`authUrl`
`client_id`
`client_secret`
`response_type`
`state`

Refer to the QuickBooks documentation for a primer on what all these terms mean.

Finally, you're instructing the browser to redirect you to the constructed `authUrl`.

`authUrl`

The following code handles the callback, retrieves the authorization code, and exchanges it for the access and refresh tokens:

```python
@app.route('/callback')
def callback():
    global accessToken, refreshToken, BASE_URL
    auth_code = request.args.get('code')
    realm_id = request.args.get('realmId')

    BASE_URL = f"https://sandbox-quickbooks.api.intuit.com/v3/company/{realm_id}"

    if not auth_code:
        return jsonify({'error': 'No authorization code received'}), 400

    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')
    redirect_uri = os.environ.get('REDIRECT_URI')

    headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic ' + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode(),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': redirect_uri
    }

    try:
        response = requests.post('https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer', headers=headers, data=data)
        response.raise_for_status() # Raise an exception for HTTP errors
        token_data = response.json()
        accessToken = token_data['access_token']
        refreshToken = token_data['refresh_token']
        print(f"Access Token: {accessToken}, Refresh Token: {refreshToken}")
        return jsonify({'accessToken': accessToken, 'refreshToken': refreshToken})
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
```

Here, you're making a POST request to the endpoint, passing in the body object and the headers. The `try-catch` block assists with error handling and fixing any possible issues. Similarly, you can implement the refresh token logic to refresh the access code every sixty minutes:

`try-catch`
```python
def refresh_access_token():
    global accessToken, refreshToken
    if not refreshToken:
        print('No refresh token available to refresh access token')
        return

    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')

    headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic ' + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode(),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refreshToken
    }

    try:
        response = requests.post('https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer', headers=headers, data=data)
        response.raise_for_status()
        token_data = response.json()
        accessToken = token_data['access_token']
        refreshToken = token_data['refresh_token']
        print(f"Access token refreshed: {accessToken}")
        print(f"Refresh token: {refreshToken}")
        # Here, store the new tokens in your database or persistent storage if needed
    except requests.exceptions.RequestException as e:
        print(f"Error refreshing token: {e}")

# In a real application, you would use a scheduler like APScheduler or a background task
# to call refresh_access_token periodically. For a simple Flask app, this might be
# handled differently or as part of a long-running process.
# For demonstration, we'll just define the function.
```

In this code snippet, you're first checking if a refresh token exists. Then, you're sending a request to the same endpoint as the callback logic with the only difference being that this time, `grant_type` is now `refresh_token` instead of `authorization_code`, as seen in the previous code block.

`grant_type`
`refresh_token`
`authorization_code`

The `setInterval` function triggers this function every 60 hours or 3,600,000 milliseconds.

`setInterval`

## Using the API

Once you're done with the authentication and have the access token, you can use the API to manipulate the sandbox QuickBooks account.

### Create, Get, and Update Accounts

Accounts refer to categories that can track a business's money in and money out.

To create an account, you send a POST request, as follows:

```python
# Example of creating an account
# In a real Flask app, this would be an endpoint
# @app.route('/create-account', methods=['POST'])
# def create_account():
account_data = {
    "Name": "Test_Account",
    "AccountType": "Accounts Receivable"
}
headers = {
    'Authorization': f'Bearer {accessToken}',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}
try:
    response = requests.post(f"{BASE_URL}/account", json=account_data, headers=headers)
    response.raise_for_status()
    # return jsonify(response.json()), 201
    print(response.json())
except requests.exceptions.RequestException as e:
    # return jsonify({'error': str(e)}), 500
    print(f"Error creating account: {e}")
```

### Create, Get, and Update Invoices

To create an invoice using the QuickBooks Online Accounting API, you set up an endpoint called `/create-invoice` and send a POST request with the required invoice data. Here's how that works:

`/create-invoice`
```python
# Example of creating an invoice
# @app.route('/create-invoice', methods=['POST'])
# def create_invoice():
invoice_data = {
    "CustomerRef": {
        "value": "1" # Replace with the appropriate customer ID
    },
    "Line": [
        {
            "Amount": 100.00,
            "DetailType": "SalesItemLineDetail",
            "SalesItemLineDetail": {
                "ItemRef": {
                    "value": "1", # Replace with the appropriate item ID
                    "name": "Item Name"
                },
                "UnitPrice": 100.00,
                "Qty": 1
            }
        }
    ],
    "BillAddr": {
        "Line1": "123 Main St",
        "City": "Anytown",
        "CountrySubDivisionCode": "CA",
        "PostalCode": "12345"
    },
    "CurrencyRef": {
        "value": "USD"
    }
}
headers = {
    'Authorization': f'Bearer {accessToken}',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}
try:
    response = requests.post(f"{BASE_URL}/invoice", json=invoice_data, headers=headers)
    response.raise_for_status()
    # return jsonify(response.json()), 201
    print(response.json())
except requests.exceptions.RequestException as e:
    # return jsonify({'error': str(e)}), 500
    print(f"Error creating invoice: {e}")
```

In this code snippet, you define the data for the invoice in the `invoiceData` object, consisting of the following components:

`invoiceData`

**`CustomerRef`** identifies the customer for whom the invoice is created. The value field must contain the ID of an existing customer in your QuickBooks account.

`CustomerRef`

**`Line`** is an array of line items for the invoice. Each object in the array represents an individual item being billed:

`Line`
`Amount`
`DetailType`
`SalesItemLineDetail`
`SalesItemLineDetail`
`ItemRef`
`value`
`name`
`UnitPrice`
`Qty`

**`BillAddr`** is an optional object for the billing address details for the customer, helping to clarify where the invoice is to be sent.

`BillAddr`

**`CurrencyRef`** identifies the currency in which the invoice is issued. The value `USD` signifies that the invoice is in US dollars.

`CurrencyRef`
`USD`

To read or retrieve a specific invoice, you send a GET request to the URL specified with the invoice ID: `BASE_URL/invoice/invoice_id`. Here's an example of how that might look:

`BASE_URL/invoice/invoice_id`
```python
# Example of getting an invoice
# @app.route('/invoice/<string:invoice_id>', methods=['GET'])
# def get_invoice(invoice_id):
headers = {
    'Authorization': f'Bearer {accessToken}',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}
try:
    response = requests.get(f"{BASE_URL}/invoice/{invoice_id}", headers=headers)
    response.raise_for_status()
    # return jsonify(response.json()), 200
    print(response.json())
except requests.exceptions.RequestException as e:
    # return jsonify({'error': str(e)}), 500
    print(f"Error getting invoice: {e}")
```

Upon a successful request, you receive the invoice details in JSON format, including all information about the customer, line items, and billing address.

To update an existing invoice, you send a POST request to the URL `BASE_URL/invoice` with a JSON object containing the updates. The `sparse:true` field indicates that it's a sparse update where other fields are left untouched except the ones being updated.

`BASE_URL/invoice`
`sparse:true`

You need to include the invoice's `Id` and `SyncToken` in the request. Here's how you can structure the update:

`Id`
`SyncToken`
```python
# Example of updating an invoice
# @app.route('/update-invoice', methods=['POST'])
# def update_invoice():
invoice_data = {
    "Id": "145", # Replace with the invoice ID you want to update
    "SyncToken": "0", # Must be the current SyncToken for the invoice
    "Line": [
        {
            "Amount": 150.00,
            "DetailType": "SalesItemLineDetail",
            "SalesItemLineDetail": {
                "ItemRef": {
                    "value": "1", # ID of the item
                    "name": "Updated Item Name" # Optional updated item name
                },
                "UnitPrice": 150.00,
                "Qty": 1
            }
        }
    ]
}
headers = {
    'Authorization': f'Bearer {accessToken}',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}
try:
    response = requests.post(f"{BASE_URL}/invoice", json=invoice_data, headers=headers)
    response.raise_for_status()
    # return jsonify(response.json()), 200
    print(response.json())
except requests.exceptions.RequestException as e:
    # return jsonify({'error': str(e)}), 500
    print(f"Error updating invoice: {e}")
```

In return, you get this object:

```json
{
  "Account": {
    "Name": "Test_Account_Updated",
    "SubAccount": false,
    "FullyQualifiedName": "Test_Account_Updated",
    "Active": true,
    "Classification": "Asset",
    "AccountType": "Accounts Receivable",
    "AccountSubType": "AccountsReceivable",
    "CurrentBalance": 0,
    "CurrentBalanceWithSubAccounts": 0,
    "CurrencyRef": {
      "value": "USD",
      "name": "United States Dollar"
    },
    "domain": "QBO",
    "sparse": false,
    "Id": "91",
    "SyncToken": "1",
    "MetaData": {
      "CreateTime": "2024-08-12T09:37:38-07:00",
      "LastUpdatedTime": "2024-08-12T11:17:56-07:00"
    }
  },
  "time": "2024-08-12T11:17:56.425-07:00"
}
```

### Create, Get, and Update Bills

To create a bill, set up an endpoint called `/create-bill` and send a POST request with the required bill data. Here's how that works:

`/create-bill`
```python
# Example of creating a bill
# @app.route('/create-bill', methods=['POST'])
# def create_bill():
bill_data = {
    "VendorRef": {
        "value": "56"
    },
    "Line": [
        {
            "Amount": 100.00,
            "DetailType": "AccountBasedExpenseLineDetail",
            "AccountBasedExpenseLineDetail": {
                "AccountRef": {
                    "value": "7",
                }
            }
        }
    ],
    "CurrencyRef": {
        "value": "USD"
    }
}
headers = {
    'Authorization': f'Bearer {accessToken}',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}
try:
    response = requests.post(f"{BASE_URL}/bill", json=bill_data, headers=headers)
    response.raise_for_status()
    # return jsonify(response.json()), 201
    print(response.json())
except requests.exceptions.RequestException as e:
    # return jsonify({'error': str(e)}), 500
    print(f"Error creating bill: {e}")
```

In this code snippet, you define the data for the bill in the `billData` object, which includes these components:

`billData`

**`VendorRef`** identifies the vendor to whom the bill is addressed. The `value` field must contain the ID of an existing vendor in your QuickBooks account.

`VendorRef`
`value`

**`Line`** is an array of line items for the bill. Each object in the array represents an individual expense being billed:

`Line`
`Amount`
`DetailType`
`ExpenseLineDetail`
`ExpenseLineDetail`
`AccountRef`
`value`
`name`
`Amount`
`Qty`

**`CurrencyRef`** identifies the currency in which the bill is issued. The value `USD` signifies that the bill is in US dollars.

`CurrencyRef`
`USD`

To read or retrieve a specific bill, you send a GET request to the URL specified with the bill ID: `BASE_URL/bill/bill_id`. Here's an example of how that might look:

`BASE_URL/bill/bill_id`
```python
# Example of getting a bill
# @app.route('/bill/<string:bill_id>', methods=['GET'])
# def get_bill(bill_id):
headers = {
    'Authorization': f'Bearer {accessToken}',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}
try:
    response = requests.get(f"{BASE_URL}/bill/{bill_id}", headers=headers)
    response.raise_for_status()
    # return jsonify(response.json()), 200
    print(response.json())
except requests.exceptions.RequestException as e:
    # return jsonify({'error': str(e)}), 500
    print(f"Error getting bill: {e}")
```

To update an existing bill, you send a POST request to the URL `${BASE_URL}/bill` with a JSON object containing the updates. Remember to include the bill's `Id` and `SyncToken` in the request.

`${BASE_URL}/bill`
`Id`
`SyncToken`

Also, since it's a full update, any fields not included in the request are changed to `NULL`.

`NULL`

Here's how you can structure the update:

```python
# Example of updating a bill
# @app.route('/update-bill', methods=['POST'])
# def update_bill():
bill_data = {
    "Id": "146", # Replace with the bill ID you want to update
    "SyncToken": "0",
    "DueDate": "2024-08-12",
    "TotalAmt": 150,
    # Other fields as necessary
}
headers = {
    'Authorization': f'Bearer {accessToken}',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}
try:
    response = requests.post(f"{BASE_URL}/bill", json=bill_data, headers=headers)
    response.raise_for_status()
    # return jsonify(response.json()), 200
    print(response.json())
except requests.exceptions.RequestException as e:
    # return jsonify({'error': str(e)}), 500
    print(f"Error updating bill: {e}")
```

### Create, Get, and Update Payments

Payments are essential for tracking monetary transactions made toward invoices or outstanding balances.

QuickBooks has specific features and requirements for payments, which include the following:

`Line`

To create a payment, set up an endpoint called `/create-payment` that sends a POST request with the required payment data:

`/create-payment`
```python
# Example of creating a payment
# @app.route('/create-payment', methods=['POST'])
# def create_payment():
payment_data = {
    "CustomerRef": {
        "value": "1" # Replace with the appropriate customer ID
    },
    "TotalAmt": 100,
    "Line": [
        {
            "Amount": 100.00, # Total payment amount for this line
            "LinkedTxn": [
                {
                    "TxnId": "1", # Replace with the ID of the invoice being paid
                    "TxnType": "Invoice" # The type of transaction
                }
            ]
        }
    ],
    "CurrencyRef": {
        "value": "USD" # Currency code for the payment
    }
}
headers = {
    'Authorization': f'Bearer {accessToken}',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}
try:
    response = requests.post(f"{BASE_URL}/payment", json=payment_data, headers=headers)
    response.raise_for_status()
    # return jsonify(response.json()), 201
    print(response.json())
except requests.exceptions.RequestException as e:
    # return jsonify({'error': str(e)}), 500
    print(f"Error creating payment: {e}")
```

The code snippet includes the following fields:

**`CustomerRef`** identifies the customer making the payment.

`CustomerRef`

**`Line`** contains details about the payment, including the following:

`Line`
`Amount`
`LinkedTxn`
`TxnId`
`TxnType`

**`PaymentMethodRef`** identifies how the payment is made (*eg* cash, credit card).

`PaymentMethodRef`

**`CurrencyRef`** specifies the currency in which the payment is made.

`CurrencyRef`

To read or retrieve a specific payment, send a GET request to the URL specified with the payment ID `BASE_URL/payment/payment_id`:

`BASE_URL/payment/payment_id`
```python
# Example of getting a payment
# @app.route('/payment/<string:payment_id>', methods=['GET'])
# def get_payment(payment_id):
headers = {
    'Authorization': f'Bearer {accessToken}',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}
try:
    response = requests.get(f"{BASE_URL}/payment/{payment_id}", headers=headers)
    response.raise_for_status()
    # return jsonify(response.json()), 200
    print(response.json())
except requests.exceptions.RequestException as e:
    # return jsonify({'error': str(e)}), 500
    print(f"Error getting payment: {e}")
```

This code gets the payment ID from the request parameters and retrieves the payment details in JSON format.

To update an existing payment, send a POST request to the `${BASE_URL}/payment` URL with a JSON object for the updates. Include the payment's `Id` and `SyncToken`.

`${BASE_URL}/payment`
`Id`
`SyncToken`

### Create, Get, and Update Transfers

Transfers represent the movement of money between bank accounts. To create a transfer, set up an endpoint called `/create-transfer` and send a POST request with the required transfer data:

`/create-transfer`
```python
# Example of creating a transfer
# @app.route('/create-transfer', methods=['POST'])
# def create_transfer():
transfer_data = {
    "FromAccountRef": {
        "value": "1" # Replace with the source account ID
    },
    "ToAccountRef": {
        "value": "2" # Replace with the destination account ID
    },
    "Amount": 100.00, # Amount to be transferred
    "TxnDate": "2024-01-01" # Date of the transfer
}
headers = {
    'Authorization': f'Bearer {accessToken}',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}
try:
    response = requests.post(f"{BASE_URL}/transfer", json=transfer_data, headers=headers)
    response.raise_for_status()
    # return jsonify(response.json()), 201
    print(response.json())
except requests.exceptions.RequestException as e:
    # return jsonify({'error': str(e)}), 500
    print(f"Error creating transfer: {e}")
```

Here are the important attributes of the JSON object in this code snippet:

`FromAccountRef`
`ToAccountRef`
`Amount`
`CurrencyRef`
`PaymentMethodRef`
`Date`

To read or retrieve a specific transfer, send a GET request to the URL specified with the transfer ID `BASE_URL/transfer/transfer_id`:

`BASE_URL/transfer/transfer_id`
```python
# Example of getting a transfer
# @app.route('/transfer/<string:transfer_id>', methods=['GET'])
# def get_transfer(transfer_id):
headers = {
    'Authorization': f'Bearer {accessToken}',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}
try:
    response = requests.get(f"{BASE_URL}/transfer/{transfer_id}", headers=headers)
    response.raise_for_status()
    # return jsonify(response.json()), 200
    print(response.json())
except requests.exceptions.RequestException as e:
    # return jsonify({'error': str(e)}), 500
    print(f"Error getting transfer: {e}")
```

This code retrieves the transfer details using the transfer ID provided in the request parameters.

To update an existing transfer, send a POST request to the `${BASE_URL}/transfer` URL with a JSON object for the updates. Include the transfer `Id` and `SyncToken`. Since transfers support sparse updates, you'll see a code snippet for that later, but you may do a full update, too.

`${BASE_URL}/transfer`
`Id`
`SyncToken`

Here's how you could structure the update:

```python
# Example of updating a transfer
# @app.route('/update-transfer', methods=['POST'])
# def update_transfer():
transfer_data = {
    "Id": "145", # Replace with the transfer ID you want to update
    "SyncToken": "0", # Must be the current SyncToken for the transfer
    "Amount": 150.00, # Updated transfer amount
    "FromAccountRef": {
        "value": "1" # Source account ID
    },
    "ToAccountRef": {
        "value": "2" # Destination account ID
    },
    "sparse": True
}
headers = {
    'Authorization': f'Bearer {accessToken}',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}
try:
    response = requests.post(f"{BASE_URL}/transfer", json=transfer_data, headers=headers)
    response.raise_for_status()
    # return jsonify(response.json()), 200
    print(response.json())
except requests.exceptions.RequestException as e:
    # return jsonify({'error': str(e)}), 500
    print(f"Error updating transfer: {e}")
```

### Create, Get, and Update Vendors

The QuickBooks Online Accounting API has some specific rules for setting up vendors:

`DisplayName`
`PrimaryEmailAddress`
`@`
`.`

To create a vendor, set up an endpoint called `/create-vendor` and send a POST request with the required vendor data:

`/create-vendor`
```python
# Example of creating a vendor
# @app.route('/create-vendor', methods=['POST'])
# def create_vendor():
vendor_data = {
    "DisplayName": "Vendor Name", # Required: Name of the vendor
    "PrimaryEmailAddr": {
        "Address": "vendor@example.com" # Vendor's email address
    },
    "PrimaryPhone": {
        "FreeFormNumber": "(123) 456-7890" # Vendor's phone number
    },
    "BillAddr": { # Optional billing address details
        "Line1": "123 Vendor St",
        "City": "Vendor City",
        "CountrySubDivisionCode": "CA", # State abbreviation
        "PostalCode": "12345" # Postal code
    },
    "Suffix": "Sr.",
    "Title": "Mr.",
    "GivenName": "Example 1",
    "PrintOnCheckName": "Example Vendor Name"
}
headers = {
    'Authorization': f'Bearer {accessToken}',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}
try:
    response = requests.post(f"{BASE_URL}/vendor", json=vendor_data, headers=headers)
    response.raise_for_status()
    # return jsonify(response.json()), 201
    print(response.json())
except requests.exceptions.RequestException as e:
    # return jsonify({'error': str(e)}), 500
    print(f"Error creating vendor: {e}")
```

To read or retrieve a specific vendor, send a GET request to the URL specified with the vendor ID `BASE_URL/vendor/vendor_id`:

`BASE_URL/vendor/vendor_id`
```python
# Example of getting a vendor
# @app.route('/vendor/<string:vendor_id>', methods=['GET'])
# def get_vendor(vendor_id):
headers = {
    'Authorization': f'Bearer {accessToken}',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}
try:
    response = requests.get(f"{BASE_URL}/vendor/{vendor_id}", headers=headers)
    response.raise_for_status()
    # return jsonify(response.json()), 200
    print(response.json())
except requests.exceptions.RequestException as e:
    # return jsonify({'error': str(e)}), 500
    print(f"Error getting vendor: {e}")
```

This code retrieves the vendor details using the vendor ID provided in the request parameters.

To update an existing vendor, send a POST request to the `${BASE_URL}/vendor` URL with a JSON object for the updates. Include the vendor's `Id` and `SyncToken`. The structure is the same as the earlier full update requests.

`${BASE_URL}/vendor`
`Id`
`SyncToken`

### Webhooks

Webhooks act as instant messengers, delivering information in real-time straight to your app whenever an event occurs in your end user’s QuickBooks account. You can use this data to perform further actions or logic. For example, if your user creates a new invoice, vendor, or customer, you can instantly get a notification, which can be used for actions such as automatically updating your accounting system, sending a confirmation email, or triggering a workflow to approve or review the new entry.

Using webhooks with QuickBooks is quite simple. First, setup OAuth 2.0 authentication for your app using the steps outlined above. Then, you can specify webhook events you want to listen for and the endpoint URL where you want to receive the data in the Intuit Developer dashboard.

Once the webhook's data is validated, you can process it and perform additional logical operations. For more detailed guidance, refer to the documentation and explore code samples here.

## Conclusion

This article covered the fundamental processes involved with the QuickBooks Online Accounting API, such as authorization, account creation, invoices, bills, and payments. By now, you should have a solid understanding of the request and response structure as well as how you can integrate it in your own apps.

To further simplify the process, you should check out Apideck. It's a powerful unified APIs solution that allows business-to-business software-as-a-service (B2B SaaS) companies to scale their integrations effortlessly. The Apideck Unified API enables you to create a single integration that interacts with multiple accounting systems, including QuickBooks, Xero, and Sage, as well as customer relationship management (CRM) and human resources information systems (HRIS), eliminating the need for separate point-to-point integrations. However, its main differentiator is its real-time data access, ensuring minimal delays and robust security with its no-data-storage model and SOC 2 type 2 compliance.

Get started with a free trial today.

## Ready to get started?

Scale your integration strategy and deliver the integrations your customers need in record time.

##### Trusted by

# Insights, guides, and updates from Apideck

Discover company news, API insights, and expert blog posts. Explore practical integration guides and tech articles to make the most of Apideck's platform.

Understanding Local and Remote Model Context Protocols

Curious about where your Model Context Protocol (MCP) server should live—on your machine or in the cloud? This article breaks down the core differences between local and remote MCP setups, including speed, privacy, ease of use, and scalability. Whether you're a developer building new AI tools or deploying services for end users, this guide will help you choose the right MCP setup for your use case.

Saurabh Rai

Breaking Down Unified API Pricing: Why API-Call Pricing Stands Out

In this post, we’ll explore the most common pricing models for unified APIs, examine their pros and cons, and help you determine which one best fits your integration strategy. From account-based to API-call-based and hybrid pricing models like those offered by Apideck, we’ll unpack the business and technical tradeoffs to help you make informed decisions.

Sooter Saalu

Building a Local RAG Chat App with Reflex, LangChain, Huggingface, and Ollama

Learn how to create a fully local, privacy-friendly RAG-powered chat app using Reflex, LangChain, Huggingface, FAISS, and Ollama. This step-by-step guide walks you through building an interactive chat UI, embedding search, and local LLM integration—all without needing frontend skills or cloud dependencies.

Saurabh Rai