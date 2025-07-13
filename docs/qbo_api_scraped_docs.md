# QuickBooks Online API Documentation (Scraped)

## Account
Accounts are what businesses use to track transactions. Accounts can track money coming in (income or revenue) and going out (expenses). They can also track the value of things (assets), like vehicles and equipment. There are five basic account types: asset, liability, income, expense, and equity.
Accounts are part of the chart of accounts, the unique list of accounts each business puts together to do their accounting. Accountants often call accounts "ledgers". Learn more about accounts and the chart of accounts.
The account object is what you'll use to do actions with the end-users accounts.


### Account Object Attributes

- Id: Unique identifier for this object. Required for update.

- Name: User recognizable name for the Account. Max 100 characters. Must not contain double quotes (") or colon (:). Required.

- SyncToken: Version number of the object. Required for update.

- AcctNum: User-defined account number. Must not contain colon (:). Conditionally required.
  - Name must be unique.
  - For French Locales: Length must be between 6 and 20 characters, must start with the account number from the master category list, name limited to alpha-numeric characters.
  - Max length for Account.AcctNum: AU & CA: 20 characters; US, UK & IN: 7 characters.

- CurrencyRef: Reference to the currency in which this account holds amounts. Optional.
- ParentRef: Specifies the Parent AccountId if this represents a SubAccount. Optional.
- Description: User entered description for the account. Max 100 characters. Optional.

- Active: Whether or not active inactive accounts may be hidden from most display purposes and may not be posted to. Optional.

- MetaData: Descriptive information about the object. Read only. Optional.

- SubAccount: Specifies whether this object represents a parent (false) or subaccount (true). Read only.

- Classification: The classification of an account. Not supported for non-posting accounts. Valid values: Asset, Equity, Expense, Liability, Revenue. Read only.

- FullyQualifiedName: Fully qualified name of the object; derived from Name and ParentRef. System generated. Limited to 5 levels. Read only.

- TxnLocationType: The account location. Valid values: WithinFrance, FranceOverseas, OutsideFranceWithEU, OutsideEU. For France locales, only.

- AccountType: A detailed account classification that specifies the use of this account. The type is based on the Classification.

- CurrentBalanceWithSubAccounts: Specifies the cumulative balance amount for the current Account and all its sub-accounts. Read only.

- AccountAlias: A user friendly name for the account. It must be unique across all account categories. For France locales, only.

- TaxCodeRef: Reference to the default tax code used by this account. Tax codes are referenced by the TaxCode.Id in the TaxCode object. Available when endpoint is invoked with the minorversion=3 query parameter. For global locales, only.

- AccountSubType: The account sub-type classification and is based on the AccountType value.

- CurrentBalance: Specifies the balance amount for the current Account. Valid for Balance Sheet accounts. Read only.
}## Create an account

### Create an Account

#### Request Body Attributes

- Name: User recognizable name for the Account. Max 100 characters. Must not contain double quotes (") or colon (:). Required.
- AcctNum: User-defined account number. Must not contain colon (:). Conditionally required.
  - For France locales: Name must be unique. Length must be between 6 and 20 characters. Must start with the account number from the master category list. Name limited to alpha-numeric characters. Required for France locales.
- TaxCodeRef: Reference to the default tax code used by this account. Tax codes are referenced by the TaxCode.Id in the TaxCode object. Available when endpoint is invoked with the minorversion=3 query parameter. For global locales, only. Conditionally required for France locales.
- AccountType: A detailed account classification that specifies the use of this account. The type is based on the Classification. Conditionally required if AccountSubType is not specified.
- AccountSubType: The account sub-type classification and is based on the AccountType value. Conditionally required if AccountType is not specified.

### Returns

Returns the newly created Account object.

#### Request URL

`POST /v3/company/<realmID>/account`
`Content-Type: application/json`
`ProductionBaseURL: https://quickbooks.api.intuit.com`
`SandboxBaseURL: https://sandbox-quickbooks.api.intuit.com`

#### Request Body

```json
{
  "Name": "MyJobs_test",
  "AccountType": "Accounts Receivable"
}
```

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

#### Returns

```json
{
  "Account": {
    "FullyQualifiedName": "MyJobs",
    "domain": "QBO",
    "Name": "MyJobs",
    "Classification": "Asset",
    "AccountSubType": "AccountsReceivable",
    "CurrencyRef": {
      "name": "United States Dollar",
      "value": "USD"
    },
    "CurrentBalanceWithSubAccounts": 0,
    "sparse": false,
    "MetaData": {
      "CreateTime": "2014-12-31T09:29:05-08:00",
      "LastUpdatedTime": "2014-12-31T09:29:05-08:00"
    },
    "AccountType": "Accounts Receivable",
    "CurrentBalance": 0,
    "Active": true,
    "SyncToken": "0",
    "Id": "94",
    "SubAccount": false
  },
  "time": "2014-12-31T09:29:05.717-08:00"
}
```

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

## Query an account

### Returns

Returns the results of the query.

#### Request URL

`GET /v3/company/<realmID>/query?query=<selectStatement>`
`Content-Type: text/plain`
`ProductionBaseURL: https://quickbooks.api.intuit.com`
`SandboxBaseURL: https://sandbox-quickbooks.api.intuit.com`

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

;

#### Sample Query

```sql
select * from Account where Metadata.CreateTime > '2014-12-31'
```

Try it

### **Sign in to explore our APIs**

You must be signed in with your developer credentials and have an active test company to explore our APIs. Once you sign in you can create a test company if you don’t have one already.Sign in

Copied!

Returns

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

66

67

68

69

70

71

72

73

74

75

76

77

78

{

"QueryResponse": {

"startPosition": 1,

"Account": \[\
\
{\
\
"FullyQualifiedName": "Canadian Accounts Receivable",\
\
"domain": "QBO",\
\
"Name": "Canadian Accounts Receivable",\
\
"Classification": "Asset",\
\
"AccountSubType": "AccountsReceivable",\
\
"CurrencyRef": {\
\
"name": "United States Dollar",\
\
"value": "USD"\
\
},\
\
"CurrentBalanceWithSubAccounts": 0,\
\
"sparse": false,\
\
"MetaData": {\
\
"CreateTime": "2015-06-23T09:38:18-07:00",\
\
"LastUpdatedTime": "2015-06-23T09:38:18-07:00"\
\
},\
\
"AccountType": "Accounts Receivable",\
\
"CurrentBalance": 0,\
\
"Active": true,\
\
"SyncToken": "0",\
\
"Id": "92",\
\
"SubAccount": false\
\
},\
\
{\
\
"FullyQualifiedName": "MyClients",\
\
"domain": "QBO",\
\
"Name": "MyClients",\
\
"Classification": "Asset",\
\
"AccountSubType": "AccountsReceivable",\
\
"CurrencyRef": {\
\
"name": "United States Dollar",\
\
"value": "USD"\
\
},\
\
"CurrentBalanceWithSubAccounts": 0,\
\
"sparse": false,\
\
"MetaData": {\
\
"CreateTime": "2015-07-13T12:34:47-07:00",\
\
"LastUpdatedTime": "2015-07-13T12:34:47-07:00"\
\
},\
\
"AccountType": "Accounts Receivable",\
\
"CurrentBalance": 0,\
\
"Active": true,\
\
"SyncToken": "0",\
\
"Id": "93",\
\
"SubAccount": false\
\
},\
\
{\
\
"FullyQualifiedName": "MyJobs",\
\
"domain": "QBO",\
\
"Name": "MyJobs",\
\
"Classification": "Asset",\
\
"AccountSubType": "AccountsReceivable",\
\
"CurrencyRef": {\
\
"name": "United States Dollar",\
\
"value": "USD"\
\
},\
\
"CurrentBalanceWithSubAccounts": 0,\
\
"sparse": false,\
\
"MetaData": {\
\
"CreateTime": "2015-01-13T10:29:27-08:00",\
\
"LastUpdatedTime": "2015-01-13T10:29:27-08:00"\
\
},\
\
"AccountType": "Accounts Receivable",\
\
"CurrentBalance": 0,\
\
"Active": true,\
\
"SyncToken": "0",\
\
"Id": "91",\
\
"SubAccount": false\
\
}\
\
\],

"maxResults": 3

},

"time": "2015-07-13T12:35:57.651-07:00"

}

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

## Read an account

Retrieves the details of an Account object that has been previously created.

### Returns

Returns the Account object.

Copied!

Request URL

1

2

3

4

GET /v3/company/<realmID>/account/<accountId>

ProductionBaseURL:https://quickbooks.api.intuit.com

SandboxBaseURL:https://sandbox-quickbooks.api.intuit.com

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

;

Try it

### **Sign in to explore our APIs**

You must be signed in with your developer credentials and have an active test company to explore our APIs. Once you sign in you can create a test company if you don’t have one already.Sign in

Copied!

Returns

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

{

"Account": {

"FullyQualifiedName": "Accounts Payable (A/P)",

"domain": "QBO",

"Name": "Accounts Payable (A/P)",

"Classification": "Liability",

"AccountSubType": "AccountsPayable",

"CurrentBalanceWithSubAccounts": -1091.23,

"sparse": false,

"MetaData": {

"CreateTime": "2014-09-12T10:12:02-07:00",

"LastUpdatedTime": "2015-06-30T15:09:07-07:00"

},

"AccountType": "Accounts Payable",

"CurrentBalance": -1091.23,

"Active": true,

"SyncToken": "0",

"Id": "33",

"SubAccount": false

},

"time": "2015-07-13T12:50:36.72-07:00"

}

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

## Full update an account

Use this operation to update any of the writable fields of an existing account object. The request body must include all writable fields of the existing object as returned in a read response. Writable fields omitted from the request body are set to NULL. The ID of the object to update is specified in the request body.

### Request Body

### Account Object Attributes

- Id
\* Required for update
read only
system defined
String, filterable, sortable
Unique identifier for this object.
Sort order is ASC by default.

- Name
\* Required
max character: max 100 characters
String, filterable, sortable
User recognizable name for the Account.
Account.Name attribute must not contain double quotes (") or colon (:).

- SyncToken
\* Required for update
read only
system defined
String
Version number of the object. It is used to lock an object for use by one app at a time. As soon as an application modifies an object, its SyncToken is incremented. Attempts to modify an object specifying an older SyncToken fails. Only the latest version of the object is maintained by QuickBooks Online.

- AcctNum
\* Conditionally required

String
User-defined account number to help the user in identifying the account within the chart-of-accounts and in deciding what should be posted to the account. The Account.AcctNum attribute must not contain colon (:).

- Name must be unique.

For French Locales:

Length must be between 6 and 20 characters
Must start with the account number from the master category list.
Name limited to alpha-numeric characters.

Max length for Account.AcctNum:

- AU & CA: 20 characters.
- US, UK & IN: 7 characters

- CurrencyRef
Optional
read only
CurrencyRefReference to the currency in which this account holds amounts.

Show child attributes

- ParentRef
Optional
ReferenceType, filterable, sortableSpecifies the Parent AccountId if this represents a SubAccount.

Show child attributes

- Description
Optional
max character: maximum of 100 chars
String, filterable, sortable
User entered description for the account, which may include user entered information to guide bookkeepers/accountants in deciding what journal entries to post to the account.

- Active
Optional
Boolean, filterable
Whether or not active inactive accounts may be hidden from most display purposes and may not be posted to.

- MetaData
Optional
ModificationMetaDataDescriptive information about the object. The MetaData values are set by Data Services and are read only for all applications.

Show child attributes

- SubAccount
read only
system defined
Boolean, filterable, sortable
Specifies whether this object represents a parent (false) or subaccount (true). Please note that accounts of these types - OpeningBalanceEquity, UndepositedFunds, RetainedEarnings, CashReceiptIncome, CashExpenditureExpense, ExchangeGainOrLoss cannot have a sub account and cannot be a sub account of another account.

- Classification
read only
system defined
String, filterable
The classification of an account. Not supported for non-posting accounts.
Valid values include: Asset, Equity, Expense, Liability, Revenue

- FullyQualifiedName
read only
system defined
String, filterable, sortable
Fully qualified name of the object; derived from Name and ParentRef. The fully qualified name prepends the topmost parent, followed by each subaccount separated by colons and takes the form of
Parent:Account1:SubAccount1:SubAccount2. System generated. Limited to 5 levels.

- TxnLocationType
minorVersion: 5![](https://uxfabric.intuitcdn.net/developer-homepage-ui/597e2ebf6899d127.png)String
The account location. Valid values include:

- WithinFrance
- FranceOverseas
- OutsideFranceWithEU
- OutsideEU

For France locales, only.

AccountType

AccountTypeEnum, filterable

A detailed account classification that specifies the use of this account. The type is based on the Classification.

Show child attributes

CurrentBalanceWithSubAccounts

read only

Decimal, filterable, sortable

Specifies the cumulative balance amount for the current Account and all its sub-accounts.

AccountAlias

minorVersion: 5

![](https://uxfabric.intuitcdn.net/developer-homepage-ui/597e2ebf6899d127.png)

String

A user friendly name for the account. It must be unique across all account categories. For France locales, only.
For example, if an account is created under category 211 with AccountAlias of Terrains, then the system does not allow creation of an account with same AccountAlias of Terrains for any other category except 211. In other words, 211001 and 215001 accounts cannot have same AccountAlias because both belong to different account category.
For France locales, only.

TaxCodeRef

minorVersion: 3

![](https://uxfabric.intuitcdn.net/developer-homepage-ui/5cd866378f4464a0.png)

![](https://uxfabric.intuitcdn.net/developer-homepage-ui/4d92c03e306bedd2.png)

![](https://uxfabric.intuitcdn.net/developer-homepage-ui/822d5e6fe32a9ee4.png)

![](https://uxfabric.intuitcdn.net/developer-homepage-ui/c6c67c6deb464402.png)

![](https://uxfabric.intuitcdn.net/developer-homepage-ui/597e2ebf6899d127.png)

ReferenceType

Reference to the default tax code used by this account. Tax codes are referenced by the TaxCode.Id in the TaxCode object. Available when endpoint is invoked with the minorversion=3 query parameter. For global locales, only.

Show child attributes

AccountSubType

String, filterable

The account sub-type classification and is based on the AccountType value.

Show child attributes

CurrentBalance

read only

Decimal, filterable, sortable

Specifies the balance amount for the current Account. Valid for Balance Sheet accounts.

### Returns

The account response body.

Copied!

Request URL

1

2

3

4

5

POST /v3/company/<realmID>/account

Contenttype:application/json

ProductionBaseURL:https://quickbooks.api.intuit.com

SandboxBaseURL:https://sandbox-quickbooks.api.intuit.com

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

;

Copied!

Request Body

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

{

"FullyQualifiedName": "Accounts Payable (A/P)",

"domain": "QBO",

"SubAccount": false,

"Description": "Description added during update.",

"Classification": "Liability",

"AccountSubType": "AccountsPayable",

"CurrentBalanceWithSubAccounts": -1091.23,

"sparse": false,

"MetaData": {

"CreateTime": "2014-09-12T10:12:02-07:00",

"LastUpdatedTime": "2015-06-30T15:09:07-07:00"

},

"AccountType": "Accounts Payable",

"CurrentBalance": -1091.23,

"Active": true,

"SyncToken": "0",

"Id": "33",

"Name": "Accounts Payable (A/P)"

}

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Try it

### **Sign in to explore our APIs**

You must be signed in with your developer credentials and have an active test company to explore our APIs. Once you sign in you can create a test company if you don’t have one already.Sign in

Copied!

Returns

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

{

"Account": {

"FullyQualifiedName": "Accounts Payable (A/P)",

"domain": "QBO",

"SubAccount": false,

"Description": "Description added during update.",

"Classification": "Liability",

"AccountSubType": "AccountsPayable",

"CurrentBalanceWithSubAccounts": -1091.23,

"sparse": false,

"MetaData": {

"CreateTime": "2014-09-12T10:12:02-07:00",

"LastUpdatedTime": "2015-07-13T15:35:13-07:00"

},

"AccountType": "Accounts Payable",

"CurrentBalance": -1091.23,

"Active": true,

"SyncToken": "1",

"Id": "33",

"Name": "Accounts Payable (A/P)"

},

"time": "2015-07-13T15:31:25.618-07:00"

}

## Bill
A Bill object is an AP transaction representing a request-for-payment from a third party for goods/services rendered, received, or both.

## The bill object

### Account Object Attributes

- Id
\* Required for update
read only
system defined
String, filterable, sortable
Unique identifier for this object.
Sort order is ASC by default.

- VendorRef
\* Required
ReferenceType, filterable, sortable
Reference to the vendor for this transaction. Query the Vendor name list resource to determine the appropriate Vendor object for this reference. Use Vendor.Id and Vendor.Name from that object for VendorRef.value and VendorRef.name, respectively.- Line \[0..n\]
\* Required
Line
Individual line items of a transaction.
Valid Line types include:
ItemBasedExpenseLine and AccountBasedExpenseLineItemBasedExpenseLine

AccountBasedExpenseLine- SyncToken
\* Required for update
read only
system defined
String
Version number of the object. It is used to lock an object for use by one app at a time. As soon as an application modifies an object, its SyncToken is incremented. Attempts to modify an object specifying an older SyncToken fails. Only the latest version of the object is maintained by QuickBooks Online.

- CurrencyRef
\* Conditionally required

CurrencyRefType
Reference to the currency in which all amounts on the associated transaction are expressed. This must be defined if multicurrency is enabled for the company.
Multicurrency is enabled for the company if Preferences.MultiCurrencyEnabled is set to true. Read more about multicurrency support [here](https://developer.intuit.com/app/developer/qbo/docs/develop/tutorials/manage-multiple-currencies "Currency"). Required if multicurrency is enabled for the company.- GlobalTaxCalculation
\* Conditionally requiredGlobalTaxCalculationEnum
Method in which tax is applied. Allowed values are:
TaxExcluded,
TaxInclusive, and
NotApplicable. Not applicable to US companies; required for non-US companies.

- TxnDate
Optional
Date, filterable, sortable
The date entered by the user when this transaction occurred.
For posting transactions, this is the posting date that affects the financial statements. If the date is not supplied, the current date on the server is used.Sort order is ASC by default.

- APAccountRef
Optional
ReferenceType, filterable, sortable
Specifies to which AP account the bill is credited. Query the Account name list resource to determine the appropriate Account object for this reference. Use Account.Id and Account.Name from that object for APAccountRef.value and APAccountRef.name, respectively. The specified account must have Account.Classification set to Liability and Account.AccountSubType set to AccountsPayable.
If the company has a single AP account, the account is implied. However, it is recommended that the AP Account be explicitly specified in all cases to prevent unexpected errors when relating transactions to each other.- SalesTermRef
Optional
ReferenceType, filterable, sortable
Reference to the Term associated with the transaction. Query the Term name list resource to determine the appropriate Term object for this reference. Use Term.Id and Term.Name from that object for SalesTermRef.value and SalesTermRef.name, respectively.- LinkedTxn \[0..n\]
Optional
LinkedTxn
Zero or more transactions linked to this Bill object. The LinkedTxn.TxnType can be set to PurchaseOrder, BillPaymentCheck or if using Minor Version 55 and above ReimburseCharge. Use LinkedTxn.TxnId as the ID of the transaction.- TotalAmt
Optional
read only
BigDecimal, filterable, sortable
Indicates the total amount of the transaction. This includes the total of all the charges, allowances, and taxes. Calculated by QuickBooks business logic; any value you supply is over-written by QuickBooks.

- TransactionLocationType
Optional
minorVersion: 4

String
The account location. Valid values include:

- WithinFrance
- FranceOverseas
- OutsideFranceWithEU
- OutsideEU

For France locales, only.

DueDate

Optional

Date, filterable, sortable

Date when the payment of the transaction is due. If date is not provided, the number of days specified in
SalesTermRef added the transaction date will be used.

Show child attributes

MetaData

Optional

ModificationMetaData

Descriptive information about the object. The MetaData values are set by Data Services and are read only for all applications.DocNumber

Optional

max character: maximum of 21 chars

String, filterable, sortable

Reference number for the transaction. If not explicitly provided at create time, a custom value can be provided. If no value is supplied, the resulting DocNumber is null.
Throws an error when duplicate DocNumber is sent in the request.
Recommended best practice: check the setting of Preferences:OtherPrefs  before setting DocNumber. If a duplicate DocNumber needs to be supplied, add the query parameter name/value pair, include=allowduplicatedocnum to the URI.
Sort order is ASC by default.

PrivateNote

Optional

max character: max of 4000 chars

String

User entered, organization-private note about the transaction. This note does not appear on the invoice to the customer. This field maps to the Memo field on the Invoice form.

TxnTaxDetail

Optional![](https://uxfabric.intuitcdn.net/developer-homepage-ui/4d92c03e306bedd2.png)
TxnTaxDetail

This data type provides information for taxes charged on the transaction as a whole. It captures the details of all taxes calculated for the transaction based on the tax codes referenced by the transaction. This can be calculated by QuickBooks business logic or you may supply it when adding a transaction.
If sales tax is disabled (Preferences.TaxPrefs.UsingSalesTax is set to false) then TxnTaxDetail is ignored and not stored.ExchangeRate

Optional

Decimal

The number of home currency units it takes to equal one unit of currency specified by CurrencyRef. Applicable if multicurrency is enabled for the company.

DepartmentRef

Optional

ReferenceType

A reference to a Department object specifying the location of the transaction, as defined using location tracking in QuickBooks Online. Query the Department name list resource to determine the appropriate department object for this reference. Use Department.Id and Department.Name from that object for DepartmentRef.value and DepartmentRef.name, respectively.IncludeInAnnualTPAR

Optional

minorVersion: 40Boolean

Include the supplier in the annual TPAR. TPAR stands for Taxable Payments Annual Report. The TPAR is mandated by ATO to get the details payments that businesses make to contractors for providing services. Some government entities also need to report the grants they have paid in a TPAR.

HomeBalance

read only

minorVersion: 3

Decimal

Convenience field containing the amount in Balance expressed in terms of the home currency. Calculated by QuickBooks business logic. Value is valid only when CurrencyRef is specified and available when endpoint is evoked with the minorversion=3 query parameter. Applicable if multicurrency is enabled for the company.

RecurDataRef

read only

minorVersion: 52

ReferenceType

A reference to the Recurring Transaction. It captures what recurring transaction template the Bill was created from.Balance

read only

Decimal, filterable

The balance reflecting any payments made against the transaction. Initially set to the value of
TotalAmt. A Balance of 0 indicates the bill is fully paid. Calculated by QuickBooks business logic; any value you supply is over-written by QuickBooks.

Copied!

SAMPLE OBJECT

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

{

"Bill": {

"SyncToken": "2",

"domain": "QBO",

"APAccountRef": {

"name": "Accounts Payable (A/P)",

"value": "33"

},

"VendorRef": {

"name": "Norton Lumber and Building

Materials",

"value": "46"

},

"TxnDate": "2014-11-06",

"TotalAmt": 103.55,

"CurrencyRef": {

"name": "United States Dollar",

"value": "USD"

},

"LinkedTxn": \[\
\
{\
\
"TxnId": "118",\
\
"TxnType": "BillPaymentCheck"\
\
}\
\
\],

"SalesTermRef": {

"value": "3"

},

"DueDate": "2014-12-06",

"sparse": false,

"Line": \[\
\
{\
\
"Description": "Lumber",\
\
"DetailType":\
\
"AccountBasedExpenseLineDetail",\
\
"ProjectRef": {\
\
"value": "39298034"\
\
},\
\
"Amount": 103.55,\
\
"Id": "1",\
\
"AccountBasedExpenseLineDetail": {\
\
"TaxCodeRef": {\
\
"value": "TAX"\
\
},\
\
"AccountRef": {\
\
"name": "Job Expenses:Job Materials\
\
:Decks and Patios",\
\
"value": "64"\
\
},\
\
"BillableStatus": "Billable",\
\
"CustomerRef": {\
\
"name": "Travis Waldron",\
\
"value": "26"\
\
}\
\
}\
\
}\
\
\],

"Balance": 0,

"Id": "25",

"MetaData": {

"CreateTime": "2014-11-06T15:37:25-08:00"

          ,

"LastUpdatedTime": "2015-02-09T10:11:11

-08:00"

}

},

"time": "2015-02-09T10:17:20.251-08:00"

}## Create a bill

### Request Body

The minimum elements to create an bill are listed here.

### Account Object Attributes

- VendorRef
\* Required
ReferenceType, filterable
Reference to the vendor for this transaction. Query the Vendor name list resource to determine the appropriate Vendor object for this reference. Use Vendor.Id and Vendor.Name from that object for VendorRef.value and VendorRef.name, respectively.Show child attributes

- Line \[0..n\]
\* Required
Line
The minimum line item required for the request.
- CurrencyRef
\* Conditionally required

CurrencyRefType
Reference to the currency in which all amounts on the associated transaction are expressed. This must be defined if multicurrency is enabled for the company.Multicurrency is enabled for the company if Preferences.MultiCurrencyEnabled is set to true. Read more about multicurrency support [here](https://developer.intuit.com/app/developer/qbo/docs/develop/tutorials/manage-multiple-currencies "Currency"). Required if multicurrency is enabled for the company.
### Returns

The bill response body.

Copied!

Request URL

1

2

3

4

5

POST /v3/company/<realmID>/bill

Contenttype:application/json

ProductionBaseURL:https://quickbooks.api

.intuit.com

SandboxBaseURL:https://sandbox-quickbooks.api

.intuit.com;

Copied!

Request Body

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

{

"Line": \[\
\
{\
\
"DetailType":\
\
"AccountBasedExpenseLineDetail",\
\
"Amount": 200.0,\
\
"Id": "1",\
\
"AccountBasedExpenseLineDetail": {\
\
"AccountRef": {\
\
"value": "7"\
\
}\
\
}\
\
}\
\
\],

"VendorRef": {

"value": "56"

}

}Try it

### **Sign in to explore our APIs**

You must be signed in with your developer credentials and have an active test company to explore our APIs. Once you sign in you can create a test company if you don’t have one already.Sign in

Copied!

Returns

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

{

"Bill": {

"SyncToken": "0",

"domain": "QBO",

"VendorRef": {

"name": "Bob's Burger Joint",

"value": "56"

},

"TxnDate": "2014-12-31",

"TotalAmt": 200.0,

"APAccountRef": {

"name": "Accounts Payable (A/P)",

"value": "33"

},

"Id": "151",

"sparse": false,

"Line": \[\
\
{\
\
"DetailType":\
\
"AccountBasedExpenseLineDetail",\
\
"Amount": 200.0,\
\
"Id": "1",\
\
"AccountBasedExpenseLineDetail": {\
\
"TaxCodeRef": {\
\
"value": "NON"\
\
},\
\
"AccountRef": {\
\
"name": "Advertising",\
\
"value": "7"\
\
},\
\
"BillableStatus": "NotBillable"\
\
}\
\
}\
\
\],

"Balance": 200.0,

"DueDate": "2014-12-31",

"MetaData": {

"CreateTime": "2014-12-31T09:59:18-08:00"

          ,

"LastUpdatedTime": "2014-12-31T09:59:18

-08:00"

}

},

"time": "2014-12-31T09:59:17.449-08:00"

}## Delete a bill

This operation deletes the bill object specified in the request body. Include a minimum of Bill.Id and Bill.SyncToken in the request body. You must unlink any linked transactions associated with the bill object before deleting it.

### Request Body

### Account Object Attributes

- SyncToken
\* Required
read only
system defined
String
Version number of the object. It is used to lock an object for use by one app at a time. As soon as an application modifies an object, its SyncToken is incremented. Attempts to modify an object specifying an older SyncToken fails. Only the latest version of the object is maintained by QuickBooks Online.

- id
\* Required
read only
system defined
String, filterable, sortable
Unique identifier for this object.### Returns

Returns the delete response.

Copied!

Request URL

1

2

3

4

POST /v3/company/<realmID>/bill?operation=delete

ProductionBaseURL:https://quickbooks.api

.intuit.com

SandboxBaseURL:https://sandbox-quickbooks.api

.intuit.com

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

;

Copied!

Request Body

1

2

3

4

{

"SyncToken": "0",

"Id": "108"

}Try it

### **Sign in to explore our APIs**

You must be signed in with your developer credentials and have an active test company to explore our APIs. Once you sign in you can create a test company if you don’t have one already.Sign in

Copied!

Returns

1

2

3

4

5

6

7

8

{

"Bill": {

"status": "Deleted",

"domain": "QBO",

"Id": "108"

},

"time": "2015-05-26T13:14:34.775-07:00"

}

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

## Query a bill

### Returns

Returns the results of the query.

Copied!

Request URL

1

2

3

4

5

GET /v3/company/<realmID>/query?query

=<selectStatement>

Contenttype:application/text

ProductionBaseURL:https://quickbooks.api

.intuit.com

SandboxBaseURL:https://sandbox-quickbooks.api

.intuit.com;

Copied!

Sample Query

1

select \* from bill maxresults 2

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Try it

### **Sign in to explore our APIs**

You must be signed in with your developer credentials and have an active test company to explore our APIs. Once you sign in you can create a test company if you don’t have one already.Sign in

Copied!

Returns

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

66

67

68

69

70

71

72

73

74

75

76

77

78

79

80

81

82

83

84

85

86

87

88

89

90

91

92

93

94

95

96

97

98

99

100

101

102

103

104

105

106

107

108

109

{

"QueryResponse": {

"startPosition": 1,

"totalCount": 2,

"Bill": \[\
\
{\
\
"SyncToken": "2",\
\
"domain": "QBO",\
\
"VendorRef": {\
\
"name": "Norton Lumber and Building\
\
Materials",\
\
"value": "46"\
\
},\
\
"TxnDate": "2014-10-07",\
\
"TotalAmt": 225.0,\
\
"APAccountRef": {\
\
"name": "Accounts Payable (A/P)",\
\
"value": "33"\
\
},\
\
"Id": "150",\
\
"sparse": false,\
\
"Line": \[\
\
{\
\
"DetailType":\
\
"ItemBasedExpenseLineDetail",\
\
"Amount": 100.0,\
\
"Id": "1",\
\
"ItemBasedExpenseLineDetail": {\
\
"TaxCodeRef": {\
\
"value": "NON"\
\
},\
\
"Qty": 8,\
\
"BillableStatus": "NotBillable",\
\
"UnitPrice": 10,\
\
"ItemRef": {\
\
"name": "Pump",\
\
"value": "11"\
\
}\
\
},\
\
"Description": "Fountain Pump"\
\
},\
\
{\
\
"DetailType":\
\
"ItemBasedExpenseLineDetail",\
\
"Amount": 125.0,\
\
"Id": "2",\
\
"ItemBasedExpenseLineDetail": {\
\
"TaxCodeRef": {\
\
"value": "NON"\
\
},\
\
"Qty": 1,\
\
"BillableStatus": "NotBillable",\
\
"UnitPrice": 125,\
\
"ItemRef": {\
\
"name": "Rock Fountain",\
\
"value": "5"\
\
}\
\
},\
\
"Description": "Rock Fountain"\
\
}\
\
\],\
\
"Balance": 225.0,\
\
"DueDate": "2014-10-07",\
\
"MetaData": {\
\
"CreateTime": "2014-10-15T13:55:31\
\
-07:00",\
\
"LastUpdatedTime": "2014-10-15T14:24\
\
:54-07:00"\
\
}\
\
},\
\
{\
\
"SyncToken": "0",\
\
"domain": "QBO",\
\
"VendorRef": {\
\
"name": "Bob's Burger Joint",\
\
"value": "56"\
\
},\
\
"TxnDate": "2014-10-15",\
\
"TotalAmt": 200.0,\
\
"APAccountRef": {\
\
"name": "Accounts Payable (A/P)",\
\
"value": "33"\
\
},\
\
"Id": "149",\
\
"sparse": false,\
\
"Line": \[\
\
{\
\
"DetailType":\
\
"AccountBasedExpenseLineDetail\
\
",\
\
"Amount": 200.0,\
\
"Id": "1",\
\
"AccountBasedExpenseLineDetail": {\
\
"TaxCodeRef": {\
\
"value": "NON"\
\
},\
\
"AccountRef": {\
\
"name": "Advertising",\
\
"value": "7"\
\
},\
\
"BillableStatus": "NotBillable"\
\
}\
\
}\
\
\],\
\
"Balance": 200.0,\
\
"DueDate": "2014-10-15",\
\
"MetaData": {\
\
"CreateTime": "2014-10-15T13:48:00\
\
-07:00",\
\
"LastUpdatedTime": "2014-10-15T13:48\
\
:00-07:00"\
\
}\
\
}\
\
\],

"maxResults": 2

},

"time": "2014-10-15T14:41:39.98-07:00"

}

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

## Read a bill

Retrieves the details of a bill that has been previously created.

### Returns

The bill response body.

Copied!

Request URL

1

2

3

4

GET /v3/company/<realmID>/bill/<billId>

ProductionBaseURL:https://quickbooks.api.intuit.com

SandboxBaseURL:https://sandbox-quickbooks.api.intuit.com;

Try it

### **Sign in to explore our APIs**

You must be signed in with your developer credentials and have an active test company to explore our APIs. Once you sign in you can create a test company if you don’t have one already.Sign in

Copied!

Returns

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

{

"Bill": {

"SyncToken": "2",

"domain": "QBO",

"APAccountRef": {

"name": "Accounts Payable (A/P)",

"value": "33"

},

"VendorRef": {

"name": "Norton Lumber and Building

Materials",

"value": "46"

},

"TxnDate": "2014-11-06",

"TotalAmt": 103.55,

"CurrencyRef": {

"name": "United States Dollar",

"value": "USD"

},

"LinkedTxn": \[\
\
{\
\
"TxnId": "118",\
\
"TxnType": "BillPaymentCheck"\
\
}\
\
\],

"SalesTermRef": {

"value": "3"

},

"DueDate": "2014-12-06",

"sparse": false,

"Line": \[\
\
{\
\
"Description": "Lumber",\
\
"DetailType":\
\
"AccountBasedExpenseLineDetail",\
\
"ProjectRef": {\
\
"value": "39298034"\
\
},\
\
"Amount": 103.55,\
\
"Id": "1",\
\
"AccountBasedExpenseLineDetail": {\
\
"TaxCodeRef": {\
\
"value": "TAX"\
\
},\
\
"AccountRef": {\
\
"name": "Job Expenses:Job Materials\
\
:Decks and Patios",\
\
"value": "64"\
\
},\
\
"BillableStatus": "Billable",\
\
"CustomerRef": {\
\
"name": "Travis Waldron",\
\
"value": "26"\
\
}\
\
}\
\
}\
\
\],

"Balance": 0,

"Id": "25",

"MetaData": {

"CreateTime": "2014-11-06T15:37:25-08:00"

          ,

"LastUpdatedTime": "2015-02-09T10:11:11

-08:00"

}

},

"time": "2015-02-09T10:17:20.251-08:00"

}## Full update a bill

Use this operation to update any of the writable fields of an existing bill object. The request body must include all writable fields of the existing object as returned in a read response. Writable fields omitted from the request body are set to NULL. The ID of the object to update is specified in the request body.

### Request Body

### Account Object Attributes

- Id
\* Required for update
read only
system defined
String, filterable, sortable
Unique identifier for this object.
Sort order is ASC by default.

- VendorRef
\* Required
ReferenceType, filterable, sortable
Reference to the vendor for this transaction. Query the Vendor name list resource to determine the appropriate Vendor object for this reference. Use Vendor.Id and Vendor.Name from that object for VendorRef.value and VendorRef.name, respectively.

Show child attributes

- Line \[0..n\]
\* Required
Line
Individual line items of a transaction.
Valid Line types include:
ItemBasedExpenseLine and AccountBasedExpenseLineItemBasedExpenseLine

AccountBasedExpenseLine- SyncToken
\* Required for update
read only
system defined
String
Version number of the object. It is used to lock an object for use by one app at a time. As soon as an application modifies an object, its SyncToken is incremented. Attempts to modify an object specifying an older SyncToken fails. Only the latest version of the object is maintained by QuickBooks Online.

- CurrencyRef
\* Conditionally required

CurrencyRefType
Reference to the currency in which all amounts on the associated transaction are expressed. This must be defined if multicurrency is enabled for the company.
Multicurrency is enabled for the company if Preferences.MultiCurrencyEnabled is set to true. Read more about multicurrency support [here](https://developer.intuit.com/app/developer/qbo/docs/develop/tutorials/manage-multiple-currencies "Currency"). Required if multicurrency is enabled for the company.- GlobalTaxCalculation
\* Conditionally requiredGlobalTaxCalculationEnum
Method in which tax is applied. Allowed values are:
TaxExcluded,
TaxInclusive, and
NotApplicable. Not applicable to US companies; required for non-US companies.

- TxnDate
Optional
Date, filterable, sortable
The date entered by the user when this transaction occurred.
For posting transactions, this is the posting date that affects the financial statements. If the date is not supplied, the current date on the server is used.Sort order is ASC by default.

- APAccountRef
Optional
ReferenceType, filterable, sortable
Specifies to which AP account the bill is credited. Query the Account name list resource to determine the appropriate Account object for this reference. Use Account.Id and Account.Name from that object for APAccountRef.value and APAccountRef.name, respectively. The specified account must have Account.Classification set to Liability and Account.AccountSubType set to AccountsPayable.
If the company has a single AP account, the account is implied. However, it is recommended that the AP Account be explicitly specified in all cases to prevent unexpected errors when relating transactions to each other.

Show child attributes

- SalesTermRef
Optional
ReferenceType, filterable, sortable
Reference to the Term associated with the transaction. Query the Term name list resource to determine the appropriate Term object for this reference. Use Term.Id and Term.Name from that object for SalesTermRef.value and SalesTermRef.name, respectively.- LinkedTxn \[0..n\]
Optional
LinkedTxn
Zero or more transactions linked to this Bill object. The LinkedTxn.TxnType can be set to PurchaseOrder, BillPaymentCheck or if using Minor Version 55 and above ReimburseCharge. Use LinkedTxn.TxnId as the ID of the transaction.- TotalAmt
Optional
read only
BigDecimal, filterable, sortable
Indicates the total amount of the transaction. This includes the total of all the charges, allowances, and taxes. Calculated by QuickBooks business logic; any value you supply is over-written by QuickBooks.

- TransactionLocationType
Optional
minorVersion: 4![](https://uxfabric.intuitcdn.net/developer-homepage-ui/597e2ebf6899d127.png)String
The account location. Valid values include:

- WithinFrance
- FranceOverseas
- OutsideFranceWithEU
- OutsideEU

For France locales, only.

DueDate

Optional

Date, filterable, sortable

Date when the payment of the transaction is due. If date is not provided, the number of days specified in
SalesTermRef added the transaction date will be used.MetaData

Optional

ModificationMetaData

Descriptive information about the object. The MetaData values are set by Data Services and are read only for all applications.

Show child attributes

DocNumber

Optional

max character: maximum of 21 chars

String, filterable, sortable

Reference number for the transaction. If not explicitly provided at create time, a custom value can be provided. If no value is supplied, the resulting DocNumber is null.
Throws an error when duplicate DocNumber is sent in the request.
Recommended best practice: check the setting of Preferences:OtherPrefs  before setting DocNumber. If a duplicate DocNumber needs to be supplied, add the query parameter name/value pair, include=allowduplicatedocnum to the URI.
Sort order is ASC by default.

PrivateNote

Optional

max character: max of 4000 chars

String

User entered, organization-private note about the transaction. This note does not appear on the invoice to the customer. This field maps to the Memo field on the Invoice form.

TxnTaxDetail

Optional

![](https://uxfabric.intuitcdn.net/developer-homepage-ui/5cd866378f4464a0.png)

![](https://uxfabric.intuitcdn.net/developer-homepage-ui/4d92c03e306bedd2.png)

![](https://uxfabric.intuitcdn.net/developer-homepage-ui/822d5e6fe32a9ee4.png)

![](https://uxfabric.intuitcdn.net/developer-homepage-ui/c6c67c6deb464402.png)

TxnTaxDetail

This data type provides information for taxes charged on the transaction as a whole. It captures the details of all taxes calculated for the transaction based on the tax codes referenced by the transaction. This can be calculated by QuickBooks business logic or you may supply it when adding a transaction.
If sales tax is disabled (Preferences.TaxPrefs.UsingSalesTax is set to false) then TxnTaxDetail is ignored and not stored.ExchangeRate

Optional

Decimal

The number of home currency units it takes to equal one unit of currency specified by CurrencyRef. Applicable if multicurrency is enabled for the company.

DepartmentRef

Optional

ReferenceType

A reference to a Department object specifying the location of the transaction, as defined using location tracking in QuickBooks Online. Query the Department name list resource to determine the appropriate department object for this reference. Use Department.Id and Department.Name from that object for DepartmentRef.value and DepartmentRef.name, respectively.IncludeInAnnualTPAR

Optional

minorVersion: 40Boolean

Include the supplier in the annual TPAR. TPAR stands for Taxable Payments Annual Report. The TPAR is mandated by ATO to get the details payments that businesses make to contractors for providing services. Some government entities also need to report the grants they have paid in a TPAR.

HomeBalance

read only

minorVersion: 3

Decimal

Convenience field containing the amount in Balance expressed in terms of the home currency. Calculated by QuickBooks business logic. Value is valid only when CurrencyRef is specified and available when endpoint is evoked with the minorversion=3 query parameter. Applicable if multicurrency is enabled for the company.

RecurDataRef

read only

minorVersion: 52

ReferenceType

A reference to the Recurring Transaction. It captures what recurring transaction template the Bill was created from.Balance

read only

Decimal, filterable

The balance reflecting any payments made against the transaction. Initially set to the value of
TotalAmt. A Balance of 0 indicates the bill is fully paid. Calculated by QuickBooks business logic; any value you supply is over-written by QuickBooks.

### Returns

The bill response body.

Copied!

Request URL

1

2

3

4

5

POST /v3/company/<realmID>/bill

Contenttype:application/json

ProductionBaseURL:https://quickbooks.api

.intuit.com

SandboxBaseURL:https://sandbox-quickbooks.api

.intuit.com

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

;

Copied!

Request Body

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

66

67

68

69

70

71

72

73

74

75

76

77

78

79

80

81

82

83

84

85

86

87

88

89

90

91

92

93

{

"DocNumber": "56789",

"SyncToken": "1",

"domain": "QBO",

"APAccountRef": {

"name": "Accounts Payable",

"value": "49"

},

"VendorRef": {

"name": "Bayshore CalOil Service",

"value": "81"

},

"TxnDate": "2014-04-04",

"TotalAmt": 200.0,

"CurrencyRef": {

"name": "United States Dollar",

"value": "USD"

},

"PrivateNote": "This is a updated memo.",

"SalesTermRef": {

"value": "12"

},

"DepartmentRef": {

"name": "Garden Services",

"value": "1"

},

"DueDate": "2013-06-09",

"sparse": false,

"Line": \[\
\
{\
\
"Description": "Gasoline",\
\
"DetailType":\
\
"AccountBasedExpenseLineDetail",\
\
"ProjectRef": {\
\
"value": "39298034"\
\
},\
\
"Amount": 200.0,\
\
"Id": "1",\
\
"AccountBasedExpenseLineDetail": {\
\
"TaxCodeRef": {\
\
"value": "TAX"\
\
},\
\
"AccountRef": {\
\
"name": "Automobile",\
\
"value": "75"\
\
},\
\
"BillableStatus": "Billable",\
\
"CustomerRef": {\
\
"name": "Blackwell, Edward",\
\
"value": "20"\
\
},\
\
"MarkupInfo": {\
\
"Percent": 10\
\
}\
\
}\
\
}\
\
\],

"Balance": 200.0,

"Id": "890",

"MetaData": {

"CreateTime": "2014-04-04T12:38:01-07:00",

"LastUpdatedTime": "2014-04-04T12:48:56-07

:00"

}

}Try it

### **Sign in to explore our APIs**

You must be signed in with your developer credentials and have an active test company to explore our APIs. Once you sign in you can create a test company if you don’t have one already.Sign in

Copied!

Returns

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

66

{

"Bill": {

"DocNumber": "56789",

"SyncToken": "2",

"domain": "QBO",

"APAccountRef": {

"name": "Accounts Payable",

"value": "49"

},

"VendorRef": {

"name": "Bayshore CalOil Service",

"value": "81"

},

"TxnDate": "2014-04-04",

"TotalAmt": 200.0,

"CurrencyRef": {

"name": "United States Dollar",

"value": "USD"

},

"PrivateNote": "This is a updated memo.",

"SalesTermRef": {

"value": "12"

},

"DepartmentRef": {

"name": "Garden Services",

"value": "1"

},

"DueDate": "2013-06-09",

"sparse": false,

"Line": \[\
\
{\
\
"Description": "Gasoline",\
\
"DetailType":\
\
"AccountBasedExpenseLineDetail",\
\
"ProjectRef": {\
\
"value": "39298034"\
\
},\
\
"Amount": 200.0,\
\
"Id": "1",\
\
"AccountBasedExpenseLineDetail": {\
\
"TaxCodeRef": {\
\
"value": "TAX"\
\
},\
\
"AccountRef": {\
\
"name": "Automobile",\
\
"value": "75"\
\
},\
\
"BillableStatus": "Billable",\
\
"CustomerRef": {\
\
"name": "Blackwell, Edward",\
\
"value": "20"\
\
},\
\
"MarkupInfo": {\
\
"Percent": 10\
\
}\
\
}\
\
}\
\
\],

"Balance": 200.0,

"Id": "890",

"MetaData": {

"CreateTime": "2014-04-04T12:38:01-07:00"

          ,

"LastUpdatedTime": "2014-04-04T12:58:16

-07:00"

}

},

"time": "2014-04-04T12:58:16.491-07:00"

}

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## CompanyInfo
The CompanyInfo object contains basic company information. In QuickBooks, company info and preferences are displayed in the same place under preferences, so it may be confusing to figure out from user interface which fields may belong to this object. But in general, properties such as company addresses or name are considered company information. Some attributes may exist in both CompanyInfo and Preferences objects.

## The companyinfo object

### Account Object Attributes

- Id
read only
system defined
String, filterable, sortable
Unique identifier for this object.
Sort order is ASC by default.

- SyncToken
\* Required for update
read only
system defined
String
Version number of the object. It is used to lock an object for use by one app at a time. As soon as an application modifies an object, its SyncToken is incremented. Attempts to modify an object specifying an older SyncToken fails. Only the latest version of the object is maintained by QuickBooks Online.

- CompanyName
\* Required for update
max character: Maximum of 1024 chars
String
The name of the company.

- CompanyAddr
\* Required for update
PhysicalAddress
Company Address as described in preference.

If a physical address is updated from within the transaction object, the QuickBooks Online API flows individual address components differently into the Line elements of the transaction response then when the transaction was first created:- Line1 and Line2 elements are populated with the customer name and company name.
- Original Line1 through Line 5 contents, City, SubDivisionCode, and PostalCode flow into Line3 through Line5as a free format strings.

Show more details

Show child attributes

- LegalAddr
Optional
PhysicalAddress
Legal Address given to the government for any government communication.

If a physical address is updated from within the transaction object, the QuickBooks Online API flows individual address components differently into the Line elements of the transaction response then when the transaction was first created:- Line1 and Line2 elements are populated with the customer name and company name.
- Original Line1 through Line 5 contents, City, SubDivisionCode, and PostalCode flow into Line3 through Line5as a free format strings.
- SupportedLanguages
Optional
String
Comma separated list of languages.

- Country
Optional
String
Country name to which the company belongs for financial calculations.

- Email
Optional
max character: max 100 chars
EmailAddress
Default email address.- WebAddr
Optional
max character: max 1000 chars
WebSiteAddress
Website address.- NameValue \[0..n\]
Optional
NameValue pairs
Any other preference not covered with the standard set of attributes. See Data Services Extensions, below, for special reserved name/value pairs.
NameValue.Name--Name of the element.
NameValue.Value--Value of the element.
Show Data Services Extensions

- FiscalYearStartMonth
Optional
MonthEnum
The start month of fiscal year.

- CustomerCommunicationAddr
Optional
PhysicalAddress
Address of the company as given to their customer, sometimes the address given to the customer mail address is different from Company address. If a physical address is updated from within the transaction object, the QuickBooks Online API flows individual address components differently into the Line elements of the transaction response then when the transaction was first created:- Line1 and Line2 elements are populated with the customer name and company name.
- Original Line1 through Line 5 contents, City, SubDivisionCode, and PostalCode flow into Line3 through Line5as a free format strings.

Show more details- PrimaryPhone
Optional
TelephoneNumber
Primary phone number.- LegalName
Optional
max character: Maximum of 1024 chars
String
The legal name of the company.

- EmployerId
Optional
String
If your QuickBooks company has defined an EIN in company settings, this value is returned.

- MetaData
Optional
ModificationMetaData
Descriptive information about the object. The MetaData values are set by Data Services and are read only for all applications.- CompanyStartDate
read only
system defined
DateTime
DateTime when company file was created. This field and
Metadata.CreateTimecontain the same value.
Copied!

SAMPLE OBJECT

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

66

67

68

69

70

71

72

73

74

75

76

77

78

79

80

81

82

83

84

85

86

87

88

89

90

91

92

93

94

95

96

97

{

"CompanyInfo": {

"SyncToken": "4",

"domain": "QBO",

"LegalAddr": {

"City": "Mountain View",

"Country": "US",

"Line1": "2500 Garcia Ave",

"PostalCode": "94043",

"CountrySubDivisionCode": "CA",

"Id": "1"

},

"SupportedLanguages": "en",

"CompanyName": "Larry's Bakery",

"Country": "US",

"CompanyAddr": {

"City": "Mountain View",

"Country": "US",

"Line1": "2500 Garcia Ave",

"PostalCode": "94043",

"CountrySubDivisionCode": "CA",

"Id": "1"

},

"sparse": false,

"Id": "1",

"WebAddr": {},

"FiscalYearStartMonth": "January",

"CustomerCommunicationAddr": {

"City": "Mountain View",

"Country": "US",

"Line1": "2500 Garcia Ave",

"PostalCode": "94043",

"CountrySubDivisionCode": "CA",

"Id": "1"

},

"PrimaryPhone": {

"FreeFormNumber": "(650)944-4444"

},

"LegalName": "Larry's Bakery",

"CompanyStartDate": "2015-06-05",

"EmployerId": "123456789",

"Email": {

"Address": "donotreply@intuit.com"

},

"NameValue": \[\
\
{\
\
"Name": "NeoEnabled",\
\
"Value": "true"\
\
},\
\
{\
\
"Name": "IndustryType",\
\
"Value": "Bread and Bakery Product Manufacturing"\
\
},\
\
{\
\
"Name": "IndustryCode",\
\
"Value": "31181"\
\
},\
\
{\
\
"Name": "SubscriptionStatus",\
\
"Value": "PAID"\
\
},\
\
{\
\
"Name": "OfferingSku",\
\
"Value": "QuickBooks Online Plus"\
\
},\
\
{\
\
"Name": "PayrollFeature",\
\
"Value": "true"\
\
},\
\
{\
\
"Name": "AccountantFeature",\
\
"Value": "false"\
\
},\
\
{\
\
"Name": "IsQbdtMigrated",\
\
"Value": "true"\
\
},\
\
{\
\
"Name": "MigrationDate",\
\
"Value": "2024-09-14T01:47:34-07:00"\
\
},\
\
{\
\
"Name": "QBOIndustryType",\
\
"Value": "Manufacturing Businesses"\
\
},\
\
{\
\
"Name": "AssignedTime",\
\
"Value": "2024-09-14T01:47:34-07:00"\
\
}\
\
\],

"MetaData": {

"CreateTime": "2015-06-05T13:55:54-07:00",

"LastUpdatedTime": "2015-07-06T08:51:50-07:00"

}

},

"time": "2015-07-10T09:38:58.155-07:00"

}

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

## Query companyinfo

### Returns

Returns the results of the query.

Copied!

Request URL

1

2

3

4

5

GET /v3/company/<realmID>/query?query=<selectStatement>

Contenttype:text/plain

ProductionBaseURL:https://quickbooks.api.intuit.com

SandboxBaseURL:https://sandbox-quickbooks.api.intuit.com

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

;

Copied!

Sample Query

1

select \* from CompanyInfoTry it

### **Sign in to explore our APIs**

You must be signed in with your developer credentials and have an active test company to explore our APIs. Once you sign in you can create a test company if you don’t have one already.Sign in

Copied!

Returns

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

66

67

68

69

70

71

72

73

74

75

76

77

78

79

80

81

82

83

84

85

86

87

88

89

90

91

92

93

94

95

96

97

{

"CompanyInfo": {

"SyncToken": "4",

"domain": "QBO",

"LegalAddr": {

"City": "Mountain View",

"Country": "US",

"Line1": "2500 Garcia Ave",

"PostalCode": "94043",

"CountrySubDivisionCode": "CA",

"Id": "1"

},

"SupportedLanguages": "en",

"CompanyName": "Larry's Bakery",

"Country": "US",

"CompanyAddr": {

"City": "Mountain View",

"Country": "US",

"Line1": "2500 Garcia Ave",

"PostalCode": "94043",

"CountrySubDivisionCode": "CA",

"Id": "1"

},

"sparse": false,

"Id": "1",

"WebAddr": {},

"FiscalYearStartMonth": "January",

"CustomerCommunicationAddr": {

"City": "Mountain View",

"Country": "US",

"Line1": "2500 Garcia Ave",

"PostalCode": "94043",

"CountrySubDivisionCode": "CA",

"Id": "1"

},

"PrimaryPhone": {

"FreeFormNumber": "(650)944-4444"

},

"LegalName": "Larry's Bakery",

"CompanyStartDate": "2015-06-05",

"EmployerId": "123456789",

"Email": {

"Address": "donotreply@intuit.com"

},

"NameValue": \[\
\
{\
\
"Name": "NeoEnabled",\
\
"Value": "true"\
\
},\
\
{\
\
"Name": "IndustryType",\
\
"Value": "Bread and Bakery Product Manufacturing"\
\
},\
\
{\
\
"Name": "IndustryCode",\
\
"Value": "31181"\
\
},\
\
{\
\
"Name": "SubscriptionStatus",\
\
"Value": "PAID"\
\
},\
\
{\
\
"Name": "OfferingSku",\
\
"Value": "QuickBooks Online Plus"\
\
},\
\
{\
\
"Name": "PayrollFeature",\
\
"Value": "true"\
\
},\
\
{\
\
"Name": "AccountantFeature",\
\
"Value": "false"\
\
},\
\
{\
\
"Name": "IsQbdtMigrated",\
\
"Value": "true"\
\
},\
\
{\
\
"Name": "MigrationDate",\
\
"Value": "2024-09-14T01:47:34-07:00"\
\
},\
\
{\
\
"Name": "QBOIndustryType",\
\
"Value": "Manufacturing Businesses"\
\
},\
\
{\
\
"Name": "AssignedTime",\
\
"Value": "2024-09-14T01:47:34-07:00"\
\
}\
\
\],

"MetaData": {

"CreateTime": "2015-06-05T13:55:54-07:00",

"LastUpdatedTime": "2015-07-06T08:51:50-07:00"

}

},

"time": "2015-07-10T09:38:58.155-07:00"

}

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

## Read companyinfo

Retrieves the details of the CompanyInfo object.

### Returns

Returns the companyinfo object.

Copied!

Request URL

1

2

3

4

GET /v3/company/<realmID>/companyinfo/<realmID>

ProductionBaseURL:https://quickbooks.api.intuit.com

SandboxBaseURL:https://sandbox-quickbooks.api.intuit.com;

Try it

### **Sign in to explore our APIs**

You must be signed in with your developer credentials and have an active test company to explore our APIs. Once you sign in you can create a test company if you don’t have one already.Sign in

Copied!

Returns

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

66

67

68

69

70

71

72

73

74

75

76

77

78

79

80

81

82

83

84

85

86

87

88

89

90

91

92

93

94

95

96

97

{

"CompanyInfo": {

"SyncToken": "4",

"domain": "QBO",

"LegalAddr": {

"City": "Mountain View",

"Country": "US",

"Line1": "2500 Garcia Ave",

"PostalCode": "94043",

"CountrySubDivisionCode": "CA",

"Id": "1"

},

"SupportedLanguages": "en",

"CompanyName": "Larry's Bakery",

"Country": "US",

"CompanyAddr": {

"City": "Mountain View",

"Country": "US",

"Line1": "2500 Garcia Ave",

"PostalCode": "94043",

"CountrySubDivisionCode": "CA",

"Id": "1"

},

"sparse": false,

"Id": "1",

"WebAddr": {},

"FiscalYearStartMonth": "January",

"CustomerCommunicationAddr": {

"City": "Mountain View",

"Country": "US",

"Line1": "2500 Garcia Ave",

"PostalCode": "94043",

"CountrySubDivisionCode": "CA",

"Id": "1"

},

"PrimaryPhone": {

"FreeFormNumber": "(650)944-4444"

},

"LegalName": "Larry's Bakery",

"CompanyStartDate": "2015-06-05",

"EmployerId": "123456789",

"Email": {

"Address": "donotreply@intuit.com"

},

"NameValue": \[\
\
{\
\
"Name": "NeoEnabled",\
\
"Value": "true"\
\
},\
\
{\
\
"Name": "IndustryType",\
\
"Value": "Bread and Bakery Product Manufacturing"\
\
},\
\
{\
\
"Name": "IndustryCode",\
\
"Value": "31181"\
\
},\
\
{\
\
"Name": "SubscriptionStatus",\
\
"Value": "PAID"\
\
},\
\
{\
\
"Name": "OfferingSku",\
\
"Value": "QuickBooks Online Plus"\
\
},\
\
{\
\
"Name": "PayrollFeature",\
\
"Value": "true"\
\
},\
\
{\
\
"Name": "AccountantFeature",\
\
"Value": "false"\
\
},\
\
{\
\
"Name": "IsQbdtMigrated",\
\
"Value": "true"\
\
},\
\
{\
\
"Name": "MigrationDate",\
\
"Value": "2024-09-14T01:47:34-07:00"\
\
},\
\
{\
\
"Name": "QBOIndustryType",\
\
"Value": "Manufacturing Businesses"\
\
},\
\
{\
\
"Name": "AssignedTime",\
\
"Value": "2024-09-14T01:47:34-07:00"\
\
}\
\
\],

"MetaData": {

"CreateTime": "2015-06-05T13:55:54-07:00",

"LastUpdatedTime": "2015-07-06T08:51:50-07:00"

}

},

"time": "2015-07-10T09:38:58.155-07:00"

}

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

## Full update companyinfo

Available with minor version 11. Use this operation to update any of the writable fields of the companyinfo object. The request body must include all writable fields of the existing object as returned in a read response. Writable fields omitted from the request body are set to NULL. The ID of the object to update is specified in the request body.

### Request Body

### Account Object Attributes

- Id
read only
system defined
String, filterable, sortable
Unique identifier for this object.
Sort order is ASC by default.

- SyncToken
\* Required for update
read only
system defined
String
Version number of the object. It is used to lock an object for use by one app at a time. As soon as an application modifies an object, its SyncToken is incremented. Attempts to modify an object specifying an older SyncToken fails. Only the latest version of the object is maintained by QuickBooks Online.

- CompanyName
\* Required for update
max character: Maximum of 1024 chars
String
The name of the company.

- CompanyAddr
\* Required for update
PhysicalAddress
Company Address as described in preference.

If a physical address is updated from within the transaction object, the QuickBooks Online API flows individual address components differently into the Line elements of the transaction response then when the transaction was first created:- Line1 and Line2 elements are populated with the customer name and company name.
- Original Line1 through Line 5 contents, City, SubDivisionCode, and PostalCode flow into Line3 through Line5as a free format strings.

Show more details

Show child attributes

- LegalAddr
Optional
PhysicalAddress
Legal Address given to the government for any government communication.

If a physical address is updated from within the transaction object, the QuickBooks Online API flows individual address components differently into the Line elements of the transaction response then when the transaction was first created:- Line1 and Line2 elements are populated with the customer name and company name.
- Original Line1 through Line 5 contents, City, SubDivisionCode, and PostalCode flow into Line3 through Line5as a free format strings.
- SupportedLanguages
Optional
String
Comma separated list of languages.

- Country
Optional
String
Country name to which the company belongs for financial calculations.

- Email
Optional
max character: max 100 chars
EmailAddress
Default email address.- WebAddr
Optional
max character: max 1000 chars
WebSiteAddress
Website address.- NameValue \[0..n\]
Optional
NameValue pairs
Any other preference not covered with the standard set of attributes. See Data Services Extensions, below, for special reserved name/value pairs.
NameValue.Name--Name of the element.
NameValue.Value--Value of the element.
Show Data Services Extensions

- FiscalYearStartMonth
Optional
MonthEnum
The start month of fiscal year.

- CustomerCommunicationAddr
Optional
PhysicalAddress
Address of the company as given to their customer, sometimes the address given to the customer mail address is different from Company address. If a physical address is updated from within the transaction object, the QuickBooks Online API flows individual address components differently into the Line elements of the transaction response then when the transaction was first created:- Line1 and Line2 elements are populated with the customer name and company name.
- Original Line1 through Line 5 contents, City, SubDivisionCode, and PostalCode flow into Line3 through Line5as a free format strings.

Show more details- PrimaryPhone
Optional
TelephoneNumber
Primary phone number.

Show child attributes

- LegalName
Optional
max character: Maximum of 1024 chars
String
The legal name of the company.

- EmployerId
Optional
String
If your QuickBooks company has defined an EIN in company settings, this value is returned.

- MetaData
Optional
ModificationMetaData
Descriptive information about the object. The MetaData values are set by Data Services and are read only for all applications.- CompanyStartDate
read only
system defined
DateTime
DateTime when company file was created. This field and
Metadata.CreateTimecontain the same value.
### Returns

The invoice response body.

Copied!

Request URL

1

2

3

4

5

POST /v3/company/<realmID>/companyinfo

Contenttype:application/json

ProductionBaseURL:https://quickbooks.api.intuit.com

SandboxBaseURL:https://sandbox-quickbooks.api.intuit.com

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

;

Copied!

Request Body

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

66

67

68

69

70

71

72

73

74

75

76

77

78

79

80

81

82

83

84

85

86

87

88

89

90

91

92

93

{

"SyncToken": "3",

"CompanyName": "Larry's Bakery",

"CompanyAddr": {

"City": "Mountain View",

"Country": "US",

"Line1": "2500 Garcia Ave",

"PostalCode": "94043",

"CountrySubDivisionCode": "CA",

"Id": "1"

},

"sparse": false,

"Id": "1",

"WebAddr": {},

"FiscalYearStartMonth": "January",

"CustomerCommunicationAddr": {

"City": "Mountain View",

"Country": "US",

"Line1": "2500 Garcia Ave",

"PostalCode": "94043",

"CountrySubDivisionCode": "CA",

"Id": "1"

},

"PrimaryPhone": {

"FreeFormNumber": "(650)944-4444"

},

"LegalName": "Larry Smith's Bakery",

"CompanyStartDate": "2015-06-05",

"Email": {

"Address": "donotreply@intuit.com"

},

"NameValue": \[\
\
{\
\
"Name": "NeoEnabled",\
\
"Value": "true"\
\
},\
\
{\
\
"Name": "IndustryType",\
\
"Value": "Bread and Bakery Product Manufacturing"\
\
},\
\
{\
\
"Name": "IndustryCode",\
\
"Value": "31181"\
\
},\
\
{\
\
"Name": "SubscriptionStatus",\
\
"Value": "PAID"\
\
},\
\
{\
\
"Name": "OfferingSku",\
\
"Value": "QuickBooks Online Plus"\
\
},\
\
{\
\
"Name": "PayrollFeature",\
\
"Value": "true"\
\
},\
\
{\
\
"Name": "AccountantFeature",\
\
"Value": "false"\
\
},\
\
{\
\
"Name": "IsQbdtMigrated",\
\
"Value": "true"\
\
},\
\
{\
\
"Name": "MigrationDate",\
\
"Value": "2024-09-14T01:47:34-07:00"\
\
},\
\
{\
\
"Name": "QBOIndustryType",\
\
"Value": "Manufacturing Businesses"\
\
},\
\
{\
\
"Name": "AssignedTime",\
\
"Value": "2024-09-14T01:47:34-07:00"\
\
}\
\
\],

"MetaData": {

"CreateTime": "2015-06-05T13:55:54-07:00",

"LastUpdatedTime": "2015-07-06T08:51:50-07:00"

}

}

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Try it

### **Sign in to explore our APIs**

You must be signed in with your developer credentials and have an active test company to explore our APIs. Once you sign in you can create a test company if you don’t have one already.Sign in

Copied!

Returns

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

66

67

68

69

70

71

72

73

74

75

76

77

78

79

80

81

82

83

84

85

86

87

88

89

90

91

92

93

94

95

96

97

{

"CompanyInfo": {

"SyncToken": "4",

"domain": "QBO",

"LegalAddr": {

"City": "Mountain View",

"Country": "US",

"Line1": "2500 Garcia Ave",

"PostalCode": "94043",

"CountrySubDivisionCode": "CA",

"Id": "1"

},

"SupportedLanguages": "en",

"CompanyName": "Larry's Bakery",

"Country": "US",

"CompanyAddr": {

"City": "Mountain View",

"Country": "US",

"Line1": "2500 Garcia Ave",

"PostalCode": "94043",

"CountrySubDivisionCode": "CA",

"Id": "1"

},

"sparse": false,

"Id": "1",

"WebAddr": {},

"FiscalYearStartMonth": "January",

"CustomerCommunicationAddr": {

"City": "Mountain View",

"Country": "US",

"Line1": "2500 Garcia Ave",

"PostalCode": "94043",

"CountrySubDivisionCode": "CA",

"Id": "1"

},

"PrimaryPhone": {

"FreeFormNumber": "(650)944-4444"

},

"LegalName": "Larry Smith's Bakery",

"CompanyStartDate": "2015-06-05",

"EmployerId": "123456789",

"Email": {

"Address": "donotreply@intuit.com"

},

"NameValue": \[\
\
{\
\
"Name": "NeoEnabled",\
\
"Value": "true"\
\
},\
\
{\
\
"Name": "IndustryType",\
\
"Value": "Bread and Bakery Product Manufacturing"\
\
},\
\
{\
\
"Name": "IndustryCode",\
\
"Value": "31181"\
\
},\
\
{\
\
"Name": "SubscriptionStatus",\
\
"Value": "PAID"\
\
},\
\
{\
\
"Name": "OfferingSku",\
\
"Value": "QuickBooks Online Plus"\
\
},\
\
{\
\
"Name": "PayrollFeature",\
\
"Value": "true"\
\
},\
\
{\
\
"Name": "AccountantFeature",\
\
"Value": "false"\
\
},\
\
{\
\
"Name": "IsQbdtMigrated",\
\
"Value": "true"\
\
},\
\
{\
\
"Name": "MigrationDate",\
\
"Value": "2024-09-14T01:47:34-07:00"\
\
},\
\
{\
\
"Name": "QBOIndustryType",\
\
"Value": "Manufacturing Businesses"\
\
},\
\
{\
\
"Name": "AssignedTime",\
\
"Value": "2024-09-14T01:47:34-07:00"\
\
}\
\
\],

"MetaData": {

"CreateTime": "2015-06-05T13:55:54-07:00",

"LastUpdatedTime": "2015-07-06T08:51:50-07:00"

}

},

"time": "2015-07-10T09:38:58.155-07:00"

}

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

