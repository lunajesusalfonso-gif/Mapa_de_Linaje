SELECT m.mes, SUM(v.monto) AS venta
FROM dwh.fact_ventas v
JOIN dwh.dim_calendario m ON m.fecha = v.fecha
JOIN dwh.metas_comerciales g ON g.mes = m.mes
GROUP BY m.mes;
