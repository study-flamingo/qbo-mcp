# Account Object

## Create an Account

### Overview
- Account name must be unique.
- The `Account.Name` attribute must not contain double quotes (") or colon (:).
- The `Account.AcctNum` attribute must not contain a colon (:).

### Request Body
The minimum elements to create an Account object are listed here.

### Attributes

*   **Name**
    *   Required
    *   Max characters: 100
    *   Type: String
    *   Filterable, Sortable
    *   Description: User-recognizable name for the Account.

*   **AcctNum**
    *   Conditionally required
    *   Type: String
    *   Description: User-defined account number to help the user in identifying the account within the chart-of-accounts and in deciding what should be posted to the account. The `Account.AcctNum` attribute must not contain colon (:).

### France Locales Specifics

For France locales:
- Name must be unique.
- Length must be between 6 and 20 characters.
- Must start with the account number from the master category list.
- Name limited to alpha-numeric characters.
- Required for France locales.

### Attributes (Continued)

*   **TaxCodeRef**
    *   Conditionally required
    *   MinorVersion: 3
    *   Type: ReferenceType
    *   Description: Reference to the default tax code used by this account. Tax codes are referenced by the `TaxCode.Id` in the `TaxCode` object. Available when endpoint is invoked with the `minorversion=3` query parameter. For global locales, only. Required for France locales.
    *   Show child attributes

*   **AccountType**
    *   Conditionally required
    *   Type: AccountTypeEnum
    *   Filterable
    *   Description: A detailed account classification that specifies the use of this account. The type is based on the Classification. Required if `AccountSubType` is not specified.
    *   Show child attributes

*   **AccountSubType**
    *   Conditionally required
    *   Type: String
    *   Filterable
    *   Description: The account sub-type classification and is based on the `AccountType` value. Required if `AccountType` is not specified.
    *   Show child attributes

## Returns
Returns the newly created Account object.

## API Endpoints

### Request URL

```
POST /v3/company/<company_id>/account?minorversion=75
```

### Request Headers

```
Content-type: application/json
```

### Base URLs

*   **Production Base URL**: `https://quickbooks.api.intuit.com`
*   **Sandbox Base URL**: `https://sandbox-quickbooks.api.intuit.com`

### Example Request Body

```json
{
  "Name": "MyJobs_test",
  "AccountType": "Accounts Receivable"
}
```

### Example Response

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

## Query an Account

### Overview
Returns the results of the query.

### Request URL

```
GET /v3/company/<company_id>/query?query=<selectStatement>&minorversion=75
```

### Request Headers

```
Content-type: text/plain
```

### Base URLs

*   **Production Base URL**: `https://quickbooks.api.intuit.com`
*   **Sandbox Base URL**: `https://sandbox-quickbooks.api.intuit.com`

### Sample Query

```
select * from Account where Metadata.CreateTime > '2014-12-31'
```

### Example Response

```json
{
  "QueryResponse": {
    "startPosition": 1,
    "Account": [
      {
        "FullyQualifiedName": "Canadian Accounts Receivable",
        "domain": "QBO",
        "Name": "Canadian Accounts Receivable",
        "Classification": "Asset",
        "AccountSubType": "AccountsReceivable",
        "CurrencyRef": {
          "name": "United States Dollar",
          "value": "USD"
        },
        "CurrentBalanceWithSubAccounts": 0,
        "sparse": false,
        "MetaData": {
          "CreateTime": "2015-06-23T09:38:18-07:00",
          "LastUpdatedTime": "2015-06-23T09:38:18-07:00"
        },
        "AccountType": "Accounts Receivable",
        "CurrentBalance": 0,
        "Active": true,
        "SyncToken": "0",
        "Id": "92",
        "SubAccount": false
      },
      {
        "FullyQualifiedName": "MyClients",
        "domain": "QBO",
        "Name": "MyClients",
        "Classification": "Asset",
        "AccountSubType": "AccountsReceivable",
        "CurrencyRef": {
          "name": "United States Dollar",
          "value": "USD"
        },
        "CurrentBalanceWithSubAccounts": 0,
        "sparse": false,
        "MetaData": {
          "CreateTime": "2015-07-13T12:34:47-07:00",
          "LastUpdatedTime": "2015-07-13T12:34:47-07:00"
        },
        "AccountType": "Accounts Receivable",
        "CurrentBalance": 0,
        "Active": true,
        "SyncToken": "0",
        "Id": "93",
        "SubAccount": false
      },
      {
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
          "CreateTime": "2015-01-13T10:29:27-08:00",
          "LastUpdatedTime": "2015-01-13T10:29:27-08:00"
        },
        "AccountType": "Accounts Receivable",
        "CurrentBalance": 0,
        "Active": true,
        "SyncToken": "0",
        "Id": "91",
        "SubAccount": false
      }
    ],
    "maxResults": 3
  },
  "time": "2015-07-13T12:35:57.651-07:00"
}
```

## Read an Account

### Overview
Retrieves the details of an Account object that has been previously created.

### Returns
Returns the Account object.

### Request URL

```
GET /v3/company/<company_id>/account/<accountId>?minorversion=75
```

### Base URLs

*   **Production Base URL**: `https://quickbooks.api.intuit.com`
*   **Sandbox Base URL**: `https://sandbox-quickbooks.api.intuit.com`

### Example Response

```json
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
```

## Full Update an Account

### Overview
Use this operation to update any of the writable fields of an existing account object. The request body must include all writable fields of the existing object as returned in a read response. Writable fields omitted from the request body are set to NULL. The ID of the object to update is specified in the request body.

### Attributes

*   **Id**
    *   Required for update
    *   Read only, System defined
    *   Type: String
    *   Filterable, Sortable
    *   Description: Unique identifier for this object. Sort order is ASC by default.

*   **Name**
    *   Required
    *   Max characters: 100
    *   Type: String
    *   Filterable, Sortable
    *   Description: User recognizable name for the Account. `Account.Name` attribute must not contain double quotes (") or colon (:).

*   **SyncToken**
    *   Required for update
    *   Read only, System defined
    *   Type: String
    *   Description: Version number of the object. It is used to lock an object for use by one app at a time. As soon as an application modifies an object, its SyncToken is incremented. Attempts to modify an object specifying an older SyncToken fails. Only the latest version of the object is maintained by QuickBooks Online.

*   **AcctNum**
    *   Conditionally required
    *   Type: String
    *   Description: User-defined account number to help the user in identifying the account within the chart-of-accounts and in deciding what should be posted to the account. The `Account.AcctNum` attribute must not contain colon (:).
    *   Name must be unique.
    *   For French Locales:
        *   Length must be between 6 and 20 characters.
        *   Must start with the account number from the master category list.
        *   Name limited to alpha-numeric characters.
    *   Max length for `Account.AcctNum`:
        *   AU & CA: 20 characters.
        *   US, UK & IN: 7 characters.

*   **CurrencyRef**
    *   Optional
    *   Read only
    *   Type: CurrencyRef
    *   Description: Reference to the currency in which this account holds amounts.
    *   Show child attributes

*   **ParentRef**
    *   Optional
    *   Type: ReferenceType
    *   Filterable, Sortable
    *   Description: Specifies the Parent AccountId if this represents a SubAccount.
    *   Show child attributes

*   **Description**
    *   Optional
    *   Max characters: 100
    *   Type: String
    *   Filterable, Sortable
    *   Description: User entered description for the account, which may include user entered information to guide bookkeepers/accountants in deciding what journal entries to post to the account.

*   **Active**
    *   Optional
    *   Type: Boolean
    *   Filterable
    *   Description: Whether or not active inactive accounts may be hidden from most display purposes and may not be posted to.

*   **MetaData**
    *   Optional
    *   Type: ModificationMetaData
    *   Description: Descriptive information about the object. The MetaData values are set by Data Services and are read only for all applications.
    *   Show child attributes

*   **SubAccount**
    *   Read only, System defined
    *   Type: Boolean
    *   Filterable, Sortable
    *   Description: Specifies whether this object represents a parent (false) or subaccount (true). Please note that accounts of these types - OpeningBalanceEquity, UndepositedFunds, RetainedEarnings, CashReceiptIncome, CashExpenditureExpense, ExchangeGainOrLoss cannot have a sub account and cannot be a sub account of another account.

*   **Classification**
    *   Read only, System defined
    *   Type: String
    *   Filterable
    *   Description: The classification of an account. Not supported for non-posting accounts. Valid values include: Asset, Equity, Expense, Liability, Revenue.

*   **FullyQualifiedName**
    *   Read only, System defined
    *   Type: String
    *   Filterable, Sortable
    *   Description: Fully qualified name of the object; derived from Name and ParentRef. The fully qualified name prepends the topmost parent, followed by each subaccount separated by colons and takes the form of `Parent:Account1:SubAccount1:SubAccount2`. System generated. Limited to 5 levels.

*   **TxnLocationType**
    *   MinorVersion: 5
    *   Type: String
    *   Description: The account location. Valid values include: `WithinFrance`, `FranceOverseas`, `OutsideFranceWithEU`, `OutsideEU`. For France locales, only.

*   **AccountType**
    *   Type: AccountTypeEnum
    *   Filterable
    *   Description: A detailed account classification that specifies the use of this account. The type is based on the Classification.
    *   Show child attributes

*   **CurrentBalanceWithSubAccounts**
    *   Read only
    *   Type: Decimal
    *   Filterable, Sortable
    *   Description: Specifies the cumulative balance amount for the current Account and all its sub-accounts.

*   **AccountAlias**
    *   MinorVersion: 5
    *   Type: String
    *   Description: A user friendly name for the account. It must be unique across all account categories. For France locales, only. For example, if an account is created under category 211 with AccountAlias of Terrains, then the system does not allow creation of an account with same AccountAlias of Terrains for any other category except 211. In other words, 211001 and 215001 accounts cannot have same AccountAlias because both belong to different account category. For France locales, only.

*   **TaxCodeRef**
    *   MinorVersion: 3
    *   Type: ReferenceType
    *   Description: Reference to the default tax code used by this account. Tax codes are referenced by the `TaxCode.Id` in the `TaxCode` object. Available when endpoint is invoked with the `minorversion=3` query parameter. For global locales, only.
    *   Show child attributes

*   **AccountSubType**
    *   Type: String
    *   Filterable
    *   Description: The account sub-type classification and is based on the `AccountType` value.
    *   Show child attributes

*   **CurrentBalance**
    *   Read only
    *   Type: Decimal
    *   Filterable, Sortable
    *   Description: Specifies the balance amount for the current Account. Valid for Balance Sheet accounts.

### Request URL

```
POST /v3/company/<company_id>/account?minorversion=75
```

### Request Headers

```
Content-type: application/json
```

### Base URLs

*   **Production Base URL**: `https://quickbooks.api.intuit.com`
*   **Sandbox Base URL**: `https://sandbox-quickbooks.api.intuit.com`

### Example Request Body

```json
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
```

### Example Response

```json
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