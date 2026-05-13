USE FinancialEngineeringDB;
GO

SELECT 
-- 1. Simple Interest
CAST(4500 * 0.07 * 5 AS DECIMAL(10,2)) AS SimpleInterest,

-- 2. Compound Interest
CAST(12000 * POWER(1 + 0.065, 8) AS DECIMAL(10,2)) AS CompoundAmount,

-- 3. Hire Purchase
CAST((18700 * (1 + (0.11 * 3))) / 36 AS DECIMAL(10,2)) AS MonthlyInstallment,

-- 4. Inflation
CAST(1550 * POWER(1 + 0.055, 12) AS DECIMAL(10,2)) AS FutureCost,

-- 5. Reducing Depreciation
CAST(480000 * POWER(1 - 0.18, 6) AS DECIMAL(10,2)) AS BookValue,

-- 6. Quarterly Compound
CAST(95000 * POWER(1 + (0.09 / 4), 16) AS DECIMAL(10,2)) AS QuarterlyCompoundValue,

-- 7. Loan Accrual
CAST((30000 * POWER(1 + (0.14 / 12), 12)) - 30000 AS DECIMAL(10,2)) AS LoanInterest,

-- 8. Doubling Time
CAST(1 / 0.125 AS DECIMAL(10,2)) AS YearsToDouble,

-- 9. Effective Annual Rate (4 decimal places)
CAST(POWER(1 + (0.132 / 12), 12) - 1 AS DECIMAL(10,4)) AS EffectiveAnnualRate,

-- 10. Semi-Annual Growth
CAST(2500000 * POWER(1 + (0.15 / 2), 20) AS DECIMAL(15,2)) AS FinalInvestment;