# Architectural and Technical Decisions

## Decision 1: Monetary Values Representation
- **Decision**: Represent all monetary figures using Python `Decimal` and database `Numeric(18, 2)`.
- **Reason**: Floating-point types introduce rounding and truncation inaccuracies that are unacceptable in personal finance applications.
- **Alternatives**: Float / Double, Integer cents.
- **Tradeoff**: Slight serialization and arithmetic overhead compared to primitive integers or floats, but guarantees financial precision.
- **Status**: Accepted

## Decision 2: Derived Account Balance vs Mutable Column
- **Decision**: Calculate account balances as `opening_balance + sum(transaction_effects)` rather than a mutable `current_balance` column.
- **Reason**: Prevents drift, race conditions, and ledger reconciliation bugs. Preserves full auditability.
- **Alternatives**: Mutable balance column updated on every transaction.
- **Tradeoff**: Requires aggregations, mitigated by indexing `(account_id, date)` and caching/snapshotting if needed in high-volume scenarios.
- **Status**: Accepted

## Decision 3: Double-Entry Transfers
- **Decision**: Transfers are modeled as two atomic transaction records (one debit/withdrawal on source, one credit/deposit on destination) sharing a common `transfer_id`.
- **Reason**: Preserves symmetry in ledger reporting, per-account transaction history, and clean category attribution.
- **Alternatives**: Single transaction with `from_account_id` and `to_account_id`.
- **Tradeoff**: Requires database transaction to create/update/delete pairs, but guarantees uniform querying per account.
- **Status**: Accepted

## Decision 4: Modular Monolith Backend Architecture
- **Decision**: Structure the application as a modular monolith in FastAPI, with clear domain boundaries (`accounts`, `categories`, `transactions`, `budgets`, `goals`, `investments`, `analytics`, etc.).
- **Reason**: Keeps all business logic coherent and maintainable without the operational complexity and latency of microservices.
- **Alternatives**: Distributed microservices, flat single-folder structure.
- **Tradeoff**: Monolith deployment, but domain boundaries make future service extraction trivial if ever necessary.
- **Status**: Accepted
