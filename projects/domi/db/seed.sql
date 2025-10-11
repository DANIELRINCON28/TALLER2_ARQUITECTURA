USE cine_patterns;
INSERT INTO products (sku,name,weight_grams,fragile) VALUES
('VEL-AROMA','Vela aromática', 300, 1),
('TE-VERDE','Té verde 250g', 250, 0),
('TAZA-CE','Taza cerámica', 400, 1),
('CUCH-META','Cuchillo metálico', 150, 0),
('LIB-AG','Agenda pequeña', 200, 0)
ON DUPLICATE KEY UPDATE name=VALUES(name), weight_grams=VALUES(weight_grams), fragile=VALUES(fragile);
