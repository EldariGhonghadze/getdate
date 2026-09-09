# Databricks notebook source
# DBTITLE 1,03. ანალიზის მომზადება
# MAGIC %md
# MAGIC # 03. ანალიზის მომზადება
# MAGIC
# MAGIC ეს ნოუთბუქი ქმნის აგრეგირებულ ანალიზურ ხედებს დაშბორდისთვის.

# COMMAND ----------

# DBTITLE 1,03. SQL: ანალიზური ხედები
# MAGIC %sql
# MAGIC -- ============================================================================
# MAGIC -- 03. ანალიზური ხედების მომზადება დაშბორდისთვის
# MAGIC -- ============================================================================
# MAGIC -- ეს ნოუთბუქი ქმნის აგრეგირებულ ხედებს გასუფთავებული მონაცემებიდან.
# MAGIC -- შესრულების წესრიგი: გაუშვით 01 და 02 ნოუთბუქები ჯერ.
# MAGIC -- ============================================================================
# MAGIC
# MAGIC -- 1. KPI შეჯამება
# MAGIC CREATE TABLE IF NOT EXISTS getdata.calculated.vw_kpi_summary AS
# MAGIC SELECT 
# MAGIC   loan_status,
# MAGIC   COUNT(DISTINCT LoanKey) AS loan_count,
# MAGIC   ROUND(COUNT(DISTINCT LoanKey) * 100.0 / SUM(COUNT(DISTINCT LoanKey)) OVER (), 2) AS pct_of_total,
# MAGIC   ROUND(AVG(AgreementInterestRate), 4) AS avg_interest_rate,
# MAGIC   SUM(CASE WHEN is_refinanced = 'დიახ' THEN 1 ELSE 0 END) AS refinanced_count
# MAGIC FROM getdata.calculated.loan_cleaned
# MAGIC GROUP BY loan_status
# MAGIC ORDER BY loan_count DESC;
# MAGIC
# MAGIC -- 2. სესხები ტიპის მიხედვით
# MAGIC CREATE TABLE IF NOT EXISTS getdata.calculated.vw_loans_by_type AS
# MAGIC SELECT loan_type, loan_status, COUNT(DISTINCT LoanKey) AS loan_count
# MAGIC FROM getdata.calculated.loan_cleaned
# MAGIC GROUP BY loan_type, loan_status
# MAGIC ORDER BY loan_type, loan_status;
# MAGIC
# MAGIC -- 3. სესხები პროდუქტის ჯგუფის მიხედვით
# MAGIC CREATE TABLE IF NOT EXISTS getdata.calculated.vw_loans_by_product AS
# MAGIC SELECT product_group, loan_status, COUNT(DISTINCT LoanKey) AS loan_count
# MAGIC FROM getdata.calculated.loan_cleaned
# MAGIC GROUP BY product_group, loan_status
# MAGIC ORDER BY product_group, loan_status;
# MAGIC
# MAGIC -- 4. ყოველთვიური ბალანსის დინამიკა
# MAGIC CREATE TABLE IF NOT EXISTS getdata.calculated.vw_balance_trends AS
# MAGIC SELECT DATE_TRUNC('month', Date) AS month, loan_status, ROUND(SUM(BalanceAmount), 2) AS total_balance
# MAGIC FROM getdata.calculated.loanbalance_cleaned
# MAGIC GROUP BY DATE_TRUNC('month', Date), loan_status
# MAGIC ORDER BY month, loan_status;
# MAGIC
# MAGIC -- 5. პრობლემური სესხების ფინანსები
# MAGIC CREATE TABLE IF NOT EXISTS getdata.calculated.vw_loan_financials AS
# MAGIC WITH monthly_agg AS (
# MAGIC   SELECT DATE_TRUNC('month', Date) AS month,
# MAGIC     ROUND(SUM(TotalPaidPrincipalAmount), 2) AS total_paid_principal,
# MAGIC     ROUND(SUM(TotalPaidInterestAmount), 2) AS total_paid_interest,
# MAGIC     ROUND(SUM(TotalPaidOverduePenaltyAmount), 2) AS total_paid_penalty
# MAGIC   FROM getdata.calculated.loanfinance_cleaned
# MAGIC   WHERE loan_status = 'პრობლემური'
# MAGIC   GROUP BY DATE_TRUNC('month', Date)
# MAGIC )
# MAGIC SELECT month, 'გადახდილი ძირი' AS metric, total_paid_principal AS amount FROM monthly_agg
# MAGIC UNION ALL
# MAGIC SELECT month, 'გადახდილი პროცენტი' AS metric, total_paid_interest AS amount FROM monthly_agg
# MAGIC UNION ALL
# MAGIC SELECT month, 'გადახდილი ჯარიმა' AS metric, total_paid_penalty AS amount FROM monthly_agg
# MAGIC ORDER BY month, metric;
# MAGIC
# MAGIC -- 6. სესხები გაცემის ტიპის მიხედვით
# MAGIC CREATE TABLE IF NOT EXISTS getdata.calculated.vw_loans_by_disbursement AS
# MAGIC SELECT disbursement_type, loan_status, COUNT(DISTINCT LoanKey) AS loan_count
# MAGIC FROM getdata.calculated.loan_cleaned
# MAGIC GROUP BY disbursement_type, loan_status
# MAGIC ORDER BY disbursement_type, loan_status;
# MAGIC
# MAGIC -- 7. პრობლემური სესხების დეტალური მონაცემები
# MAGIC CREATE TABLE IF NOT EXISTS getdata.calculated.vw_problem_loan_detail AS
# MAGIC SELECT LoanKey, loan_type, product_group, disbursement_type, AgreementStartDate, AgreementEndDate, AgreementInterestRate, is_refinanced
# MAGIC FROM getdata.calculated.loan_cleaned
# MAGIC WHERE loan_status = 'პრობლემური'
# MAGIC ORDER BY AgreementStartDate;

# COMMAND ----------

