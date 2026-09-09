# Databricks notebook source
# DBTITLE 1,02. მონაცემების გასუფთავება
# MAGIC %md
# MAGIC # 02. მონაცემების გასუფთავება
# MAGIC
# MAGIC ეს ნოუთბუქი ასუფთავებს მონაცემებს getdata.raw სქემიდან და ინახავს getdata.calculated სქემაში.

# COMMAND ----------

# DBTITLE 1,02. SQL: მონაცემების გასუფთავება
# MAGIC %sql
# MAGIC -- ============================================================================
# MAGIC -- 02. მონაცემების გასუფთავება და შენახვა getdata.calculated სქემაში
# MAGIC -- ============================================================================
# MAGIC -- ეს ნოუთბუქი ასუფთავებს მონაცემებს getdata.raw სქემიდან და ინახავს
# MAGIC -- დამუშავებულ მონაცემებს getdata.calculated სქემაში.
# MAGIC -- შესრულების წესრიგი: გაუშვით 01_მონაცემების_ჩატვირთვა ნოუთბუქი ჯერ.
# MAGIC -- ============================================================================
# MAGIC
# MAGIC -- სქემის შექმნა თუ არ არსებობს
# MAGIC CREATE SCHEMA IF NOT EXISTS getdata.calculated;
# MAGIC
# MAGIC -- 1. loan ცხრილის გასუფთავება
# MAGIC CREATE TABLE IF NOT EXISTS getdata.calculated.loan_cleaned AS
# MAGIC SELECT 
# MAGIC   l.LoanKey,
# MAGIC   l.ValidFrom,
# MAGIC   l.ValidTo,
# MAGIC   lt.LoanTypeNameLat AS loan_type,
# MAGIC   pg.LoanProductGroupName AS product_group,
# MAGIC   dt.DisbursementTypeName AS disbursement_type,
# MAGIC   l.AgreementStartDate,
# MAGIC   l.AgreementEndDate,
# MAGIC   l.AgreementInterestRate,
# MAGIC   CASE 
# MAGIC     WHEN l.IsProblemLoan = 1 THEN 'პრობლემური'
# MAGIC     ELSE 'ჯანსაღი'
# MAGIC   END AS loan_status,
# MAGIC   CASE 
# MAGIC     WHEN l.IsRefinanced = 1 THEN 'დიახ'
# MAGIC     ELSE 'არა'
# MAGIC   END AS is_refinanced
# MAGIC FROM getdata.raw.loan l
# MAGIC JOIN getdata.raw.loantype lt 
# MAGIC   ON l.LoanTypeKey = lt.LoanTypeKey
# MAGIC JOIN getdata.raw.loanproductgroup pg 
# MAGIC   ON l.LoanProductGroupKey = pg.LoanProductGroupKey
# MAGIC LEFT JOIN getdata.raw.loandisbursetype dt 
# MAGIC   ON l.DisbursementTypeKey = dt.DisbursementTypeKey
# MAGIC WHERE l.ValidTo > current_timestamp();
# MAGIC
# MAGIC -- 2. loanbalance ცხრილის გასუფთავება
# MAGIC CREATE TABLE IF NOT EXISTS getdata.calculated.loanbalance_cleaned AS
# MAGIC SELECT 
# MAGIC   lb.Date,
# MAGIC   lc.LoanKey,
# MAGIC   lc.loan_status,
# MAGIC   lc.loan_type,
# MAGIC   lc.product_group,
# MAGIC   lb.AgreementAmount,
# MAGIC   lb.BalanceAmount,
# MAGIC   lb.PrincipalAmount
# MAGIC FROM getdata.raw.loanbalance lb
# MAGIC JOIN getdata.calculated.loan_cleaned lc 
# MAGIC   ON lb.LoanKey = lc.LoanKey;
# MAGIC
# MAGIC -- 3. loanfinance ცხრილის გასუფთავება
# MAGIC CREATE TABLE IF NOT EXISTS getdata.calculated.loanfinance_cleaned AS
# MAGIC SELECT 
# MAGIC   lf.Date,
# MAGIC   lc.LoanKey,
# MAGIC   lc.loan_status,
# MAGIC   lc.loan_type,
# MAGIC   lc.product_group,
# MAGIC   lf.TotalWithDrawnAmount,
# MAGIC   lf.TotalPaidPrincipalAmount,
# MAGIC   lf.TotalPaidInterestAmount,
# MAGIC   lf.TotalPaidOverduePenaltyAmount,
# MAGIC   lf.TotalForgivenPrincipalAmount,
# MAGIC   lf.TotalForgivenInterestAmount
# MAGIC FROM getdata.raw.loanfinance lf
# MAGIC JOIN getdata.calculated.loan_cleaned lc 
# MAGIC   ON lf.LoanKey = lc.LoanKey;

# COMMAND ----------

