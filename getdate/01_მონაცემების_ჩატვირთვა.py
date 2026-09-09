# Databricks notebook source
# DBTITLE 1,01. მონაცემების ჩატვირთვა
# MAGIC %md
# MAGIC # 01. მონაცემების ჩატვირთვა
# MAGIC
# MAGIC ეს ნოუთბუქი აკოპირებს მონაცემებს getdata.default სქემიდან getdata.raw სქემაში შეუცვლელად.

# COMMAND ----------

# DBTITLE 1,01. SQL: მონაცემების ჩატვირთვა
# MAGIC %sql
# MAGIC -- ============================================================================
# MAGIC -- 01. მონაცემების ჩატვირთვა შეუცვლელად getdata.raw სქემაში
# MAGIC -- ============================================================================
# MAGIC -- ეს ნოუთბუქი აკოპირებს მონაცემებს getdata.default სქემიდან getdata.raw სქემაში
# MAGIC -- მონაცემები ინახავა შეუცვლელად, როგორც საწყის წყაროში.
# MAGIC -- ============================================================================
# MAGIC
# MAGIC -- სქემის შექმნა თუ არ არსებობს
# MAGIC CREATE SCHEMA IF NOT EXISTS getdata.raw;
# MAGIC
# MAGIC -- 1. loan ცხრილის კოპირება (მთავარი სესხების ცხრილი)
# MAGIC CREATE TABLE IF NOT EXISTS getdata.raw.loan AS
# MAGIC SELECT * FROM getdata.default.loan;
# MAGIC
# MAGIC -- 2. loanbalance ცხრილის კოპირება (სესხების ბალანსები)
# MAGIC CREATE TABLE IF NOT EXISTS getdata.raw.loanbalance AS
# MAGIC SELECT * FROM getdata.default.loanbalance;
# MAGIC
# MAGIC -- 3. loanfinance ცხრილის კოპირება (სესხების ფინანსური მონაცემები)
# MAGIC CREATE TABLE IF NOT EXISTS getdata.raw.loanfinance AS
# MAGIC SELECT * FROM getdata.default.loanfinance;
# MAGIC
# MAGIC -- 4. loantype ცხრილის კოპირება (სესხის ტიპების დიმენსია)
# MAGIC CREATE TABLE IF NOT EXISTS getdata.raw.loantype AS
# MAGIC SELECT * FROM getdata.default.loantype;
# MAGIC
# MAGIC -- 5. loandisbursetype ცხრილის კოპირება (გაცემის ტიპების დიმენსია)
# MAGIC CREATE TABLE IF NOT EXISTS getdata.raw.loandisbursetype AS
# MAGIC SELECT * FROM getdata.default.loandisbursetype;
# MAGIC
# MAGIC -- 6. loanproductgroup ცხრილის კოპირება (პროდუქტის ჯგუფების დიმენსია)
# MAGIC CREATE TABLE IF NOT EXISTS getdata.raw.loanproductgroup AS
# MAGIC SELECT * FROM getdata.default.loanproductgroup;
# MAGIC
# MAGIC -- 7. date ცხრილის კოპირება (თარიღების დიმენსია)
# MAGIC CREATE TABLE IF NOT EXISTS getdata.raw.date AS
# MAGIC SELECT * FROM getdata.default.date;

# COMMAND ----------

