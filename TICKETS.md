# Prioritized Roadmap

## Add Database

1. Implement In-Memory Database
2. Implement DB schema (define table relationships with comments)
3. DB Func: ADD
4. DB Func: GET
5. DB Func: UPDATE
6. DB Func: DELETE
7. Create models for internal and external accounts
8. Create models for organization user and internal super user

## Enable External Account Creation

1. Create App initial state / no accounts component
2. Create App returning user / connected accounts component
3. Create LinkExternalAccount button
4. Handle Plaid Account link (POST /accounts/external)

## Enable Internal Account Creation

1. POST /accounts/internal/
2. GET /accounts/internal/{id}
3. PUT /accounts/internal/{id}
4. DELETE /accounts/internal/{id}

## Enable Payments

1. Create model/table for payments
2. POST /payment/debit
3. POST /payment/credit
4. GET /accounts/{account_id}/payments
5. Create PaymentsTable component
6. Create AccountSelect dropdown component

## Enable Defered Payment Processing

1. Implement queue
2. Use Queue for payment processing instead of real-time
