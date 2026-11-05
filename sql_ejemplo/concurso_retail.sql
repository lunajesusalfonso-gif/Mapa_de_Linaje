SELECT t.tienda, SUM(v.monto) AS venta
FROM dwh.fact_ventas v
JOIN dwh.dim_tienda t ON t.id = v.tienda_id
GROUP BY t.tienda;
