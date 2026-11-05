SELECT s.sku, s.almacen, s.existencia
FROM dwh.fact_inventario s
JOIN dwh.dim_producto p ON p.id = s.producto_id
JOIN dwh.dim_almacen a ON a.id = s.almacen_id;
