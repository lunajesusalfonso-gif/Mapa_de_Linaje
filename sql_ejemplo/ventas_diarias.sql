SELECT f.fecha, p.sku, SUM(f.monto) AS venta
FROM dwh.fact_ventas f
JOIN dwh.dim_producto p ON p.id = f.producto_id
JOIN dwh.dim_cliente c ON c.id = f.cliente_id
GROUP BY f.fecha, p.sku;
