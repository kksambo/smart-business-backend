PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;

-- =====================================================
-- USERS TABLE
-- =====================================================
INSERT OR REPLACE INTO users (id, email, username, hashed_password, business_name, business_type, is_active, created_at, updated_at) VALUES 
(1, 'sicelo.sambo@smart.com', 'sicelo.sambo', '$2b$12$6rIMmPjsRyZrqzP3aarjmexDpancqlXCuRSzJKzpZuPBLDF92fn8a', 'Sambo Electronics', 'Electronics Retail', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(2, 'vuthlari.maswanganyi@smart.com', 'vuthlari.maswanganyi', '$2b$12$6rIMmPjsRyZrqzP3aarjmexDpancqlXCuRSzJKzpZuPBLDF92fn8a', 'Maswanganyi Trading', 'General Trading', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(3, 'mhangwani.karabo@smart.com', 'mhangwani.karabo', '$2b$12$6rIMmPjsRyZrqzP3aarjmexDpancqlXCuRSzJKzpZuPBLDF92fn8a', 'Karabo Supplies', 'Office Supplies', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(4, 'mapulaa.mpelane@smart.com', 'mapulaa.mpelane', '$2b$12$6rIMmPjsRyZrqzP3aarjmexDpancqlXCuRSzJKzpZuPBLDF92fn8a', 'Mpelane Fashion', 'Fashion Retail', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00');

-- =====================================================
-- PRODUCTS TABLE
-- =====================================================
-- Owner 1: Sambo Electronics
INSERT OR REPLACE INTO products (id, owner_id, name, category, cost_price, selling_price, quantity, supplier, image_url, description, sku, is_active, created_at, updated_at) VALUES 
(1, 1, 'Laptop', 'Electronics', 400, 750, 45, 'Tech Suppliers Ltd', NULL, 'High quality laptop', 'SKU-1-0001', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(2, 1, 'Smartphone', 'Electronics', 180, 350, 59, 'Tech Suppliers Ltd', NULL, 'High quality smartphone', 'SKU-1-0002', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(3, 1, 'Headphones', 'Electronics', 30, 80, 70, 'Audio Tech', NULL, 'High quality headphones', 'SKU-1-0003', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(4, 1, 'USB Cable', 'Accessories', 2, 8, 32, 'Cable Co', NULL, 'High quality usb cable', 'SKU-1-0004', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(5, 1, 'Phone Case', 'Accessories', 3, 12, 63, 'Case Masters', NULL, 'High quality phone case', 'SKU-1-0005', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(6, 1, 'Screen Protector', 'Accessories', 1, 5, 89, 'Protection Plus', NULL, 'High quality screen protector', 'SKU-1-0006', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(7, 1, 'Power Bank', 'Electronics', 15, 45, 56, 'Power Tech', NULL, 'High quality power bank', 'SKU-1-0007', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(8, 1, 'Keyboard', 'Electronics', 25, 60, 39, 'Input Devices Inc', NULL, 'High quality keyboard', 'SKU-1-0008', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(9, 1, 'Mouse', 'Electronics', 10, 25, 89, 'Input Devices Inc', NULL, 'High quality mouse', 'SKU-1-0009', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(10, 1, 'Webcam', 'Electronics', 20, 50, 37, 'Vision Tech', NULL, 'High quality webcam', 'SKU-1-0010', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00');

-- Owner 2: Maswanganyi Trading
INSERT OR REPLACE INTO products (id, owner_id, name, category, cost_price, selling_price, quantity, supplier, image_url, description, sku, is_active, created_at, updated_at) VALUES 
(11, 2, 'Rice 5kg', 'Food', 25, 45, 66, 'Food Corp', NULL, 'High quality rice 5kg', 'SKU-2-0001', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(12, 2, 'Cooking Oil 2L', 'Food', 15, 28, 57, 'Oil Traders', NULL, 'High quality cooking oil 2l', 'SKU-2-0002', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(13, 2, 'Sugar 2kg', 'Food', 12, 22, 69, 'Sweet Supplies', NULL, 'High quality sugar 2kg', 'SKU-2-0003', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(14, 2, 'Soap Bars', 'Household', 2, 5, 45, 'Clean Corp', NULL, 'High quality soap bars', 'SKU-2-0004', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(15, 2, 'Toothpaste', 'Personal Care', 3, 8, 76, 'Care Products', NULL, 'High quality toothpaste', 'SKU-2-0005', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(16, 2, 'Shampoo 500ml', 'Personal Care', 8, 18, 35, 'Hair Care Ltd', NULL, 'High quality shampoo 500ml', 'SKU-2-0006', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(17, 2, 'Laundry Detergent', 'Household', 20, 35, 41, 'Clean Corp', NULL, 'High quality laundry detergent', 'SKU-2-0007', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(18, 2, 'Batteries AA', 'Electronics', 1, 3, 67, 'Power Tech', NULL, 'High quality batteries aa', 'SKU-2-0008', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(19, 2, 'Matches Box', 'Household', 0.5, 2, 86, 'Utility Supplies', NULL, 'High quality matches box', 'SKU-2-0009', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(20, 2, 'Plastic Bags', 'Household', 0.1, 0.5, 48, 'Packaging Co', NULL, 'High quality plastic bags', 'SKU-2-0010', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00');

-- Owner 3: Karabo Supplies
INSERT OR REPLACE INTO products (id, owner_id, name, category, cost_price, selling_price, quantity, supplier, image_url, description, sku, is_active, created_at, updated_at) VALUES 
(21, 3, 'A4 Paper Pack', 'Stationery', 8, 15, 56, 'Paper Corp', NULL, 'High quality a4 paper pack', 'SKU-3-0001', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(22, 3, 'Ballpoint Pens', 'Stationery', 1, 3, 57, 'Writing Tools', NULL, 'High quality ballpoint pens', 'SKU-3-0002', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(23, 3, 'Notebooks', 'Stationery', 5, 12, 46, 'Book Makers', NULL, 'High quality notebooks', 'SKU-3-0003', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(24, 3, 'Desk Lamp', 'Office', 15, 45, 87, 'Office Essentials', NULL, 'High quality desk lamp', 'SKU-3-0004', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(25, 3, 'Stapler', 'Office', 4, 10, 60, 'Office Tools', NULL, 'High quality stapler', 'SKU-3-0005', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(26, 3, 'Printer Paper', 'Stationery', 12, 25, 32, 'Paper Corp', NULL, 'High quality printer paper', 'SKU-3-0006', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(27, 3, 'Whiteboard Markers', 'Office', 2, 6, 49, 'Writing Tools', NULL, 'High quality whiteboard markers', 'SKU-3-0007', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(28, 3, 'File Folders', 'Office', 1, 3, 45, 'Organization Co', NULL, 'High quality file folders', 'SKU-3-0008', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(29, 3, 'Calculator', 'Office', 8, 20, 68, 'Office Tools', NULL, 'High quality calculator', 'SKU-3-0009', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(30, 3, 'Correction Tape', 'Stationery', 1, 4, 49, 'Writing Tools', NULL, 'High quality correction tape', 'SKU-3-0010', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00');

-- Owner 4: Mpelane Fashion
INSERT OR REPLACE INTO products (id, owner_id, name, category, cost_price, selling_price, quantity, supplier, image_url, description, sku, is_active, created_at, updated_at) VALUES 
(31, 4, 'T-Shirt', 'Clothing', 8, 25, 71, 'Fashion House', NULL, 'High quality t-shirt', 'SKU-4-0001', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(32, 4, 'Jeans', 'Clothing', 20, 60, 49, 'Denim Co', NULL, 'High quality jeans', 'SKU-4-0002', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(33, 4, 'Sneakers', 'Footwear', 25, 80, 67, 'Shoe Factory', NULL, 'High quality sneakers', 'SKU-4-0003', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(34, 4, 'Dress', 'Clothing', 15, 45, 84, 'Fashion House', NULL, 'High quality dress', 'SKU-4-0004', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(35, 4, 'Jacket', 'Clothing', 30, 90, 79, 'Outerwear Ltd', NULL, 'High quality jacket', 'SKU-4-0005', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(36, 4, 'Belt', 'Accessories', 5, 15, 90, 'Accessory Makers', NULL, 'High quality belt', 'SKU-4-0006', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(37, 4, 'Cap', 'Accessories', 3, 12, 43, 'Headwear Co', NULL, 'High quality cap', 'SKU-4-0007', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(38, 4, 'Socks Pack', 'Clothing', 2, 8, 48, 'Sock Factory', NULL, 'High quality socks pack', 'SKU-4-0008', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(39, 4, 'Scarf', 'Accessories', 4, 14, 90, 'Accessory Makers', NULL, 'High quality scarf', 'SKU-4-0009', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00'),
(40, 4, 'Sunglasses', 'Accessories', 6, 20, 44, 'Vision Wear', NULL, 'High quality sunglasses', 'SKU-4-0010', 1, '2026-05-10 12:00:00', '2026-05-10 12:00:00');

-- =====================================================
-- CUSTOMERS TABLE
-- =====================================================
-- Owner 1 Customers
INSERT OR REPLACE INTO customers (id, owner_id, name, email, phone, total_purchases, visit_count, created_at) VALUES 
(1, 1, 'Thabo Molefe', 'thabo.molefe@gmail.com', '2761-428-3836', 0, 0, '2026-05-10 12:00:00'),
(2, 1, 'Lerato Nkosi', 'lerato.nkosi@gmail.com', '2766-246-6283', 0, 0, '2026-05-10 12:00:00'),
(3, 1, 'Sipho Zulu', 'sipho.zulu@gmail.com', '2761-902-5610', 0, 0, '2026-05-10 12:00:00'),
(4, 1, 'Nomsa Khumalo', 'nomsa.khumalo@gmail.com', '2769-190-5206', 0, 0, '2026-05-10 12:00:00'),
(5, 1, 'Jabu Mthembu', 'jabu.mthembu@gmail.com', '2769-283-9344', 0, 0, '2026-05-10 12:00:00'),
(6, 1, 'Zinhle Ndlovu', 'zinhle.ndlovu@gmail.com', '2763-286-6486', 0, 0, '2026-05-10 12:00:00'),
(7, 1, 'Themba Sithole', 'themba.sithole@gmail.com', '2763-581-9161', 0, 0, '2026-05-10 12:00:00'),
(8, 1, 'Ayanda Cele', 'ayanda.cele@gmail.com', '2774-951-3907', 0, 0, '2026-05-10 12:00:00'),
(9, 1, 'Sibusiso Nkosi', 'sibusiso.nkosi@gmail.com', '2783-466-9945', 0, 0, '2026-05-10 12:00:00'),
(10, 1, 'Nomvula Dlamini', 'nomvula.dlamini@gmail.com', '2766-871-1937', 0, 0, '2026-05-10 12:00:00'),
(11, 1, 'Bongani Nkosi', 'bongani.nkosi@gmail.com', '2765-533-1301', 0, 0, '2026-05-10 12:00:00'),
(12, 1, 'Thandiwe Mkhize', 'thandiwe.mkhize@gmail.com', '2778-166-4577', 0, 0, '2026-05-10 12:00:00'),
(13, 1, 'Sifiso Buthelezi', 'sifiso.buthelezi@gmail.com', '2762-240-3040', 0, 0, '2026-05-10 12:00:00'),
(14, 1, 'Zanele Nkosi', 'zanele.nkosi@gmail.com', '2761-976-4238', 0, 0, '2026-05-10 12:00:00'),
(15, 1, 'Mthokozisi Mthembu', 'mthokozisi.mthembu@gmail.com', '2762-224-9461', 0, 0, '2026-05-10 12:00:00'),
(16, 1, 'Nokuthula Zulu', 'nokuthula.zulu@gmail.com', '2769-409-2626', 0, 0, '2026-05-10 12:00:00'),
(17, 1, 'Sandile Nkosi', 'sandile.nkosi@gmail.com', '2780-322-8416', 0, 0, '2026-05-10 12:00:00'),
(18, 1, 'Phumzile Mthembu', 'phumzile.mthembu@gmail.com', '2788-143-8361', 0, 0, '2026-05-10 12:00:00'),
(19, 1, 'Thulani Nkosi', 'thulani.nkosi@gmail.com', '2764-487-5586', 0, 0, '2026-05-10 12:00:00'),
(20, 1, 'Ntombifuthi Dlamini', 'ntombifuthi.dlamini@gmail.com', '2765-135-8255', 0, 0, '2026-05-10 12:00:00');

-- Owner 2 Customers
INSERT OR REPLACE INTO customers (id, owner_id, name, email, phone, total_purchases, visit_count, created_at) VALUES 
(21, 2, 'Thabo Molefe', 'thabo.molefe@gmail.com', '2781-804-2088', 0, 0, '2026-05-10 12:00:00'),
(22, 2, 'Lerato Nkosi', 'lerato.nkosi@gmail.com', '2783-818-7375', 0, 0, '2026-05-10 12:00:00'),
(23, 2, 'Sipho Zulu', 'sipho.zulu@gmail.com', '2779-389-9549', 0, 0, '2026-05-10 12:00:00'),
(24, 2, 'Nomsa Khumalo', 'nomsa.khumalo@gmail.com', '2771-670-3394', 0, 0, '2026-05-10 12:00:00'),
(25, 2, 'Jabu Mthembu', 'jabu.mthembu@gmail.com', '2785-268-7507', 0, 0, '2026-05-10 12:00:00'),
(26, 2, 'Zinhle Ndlovu', 'zinhle.ndlovu@gmail.com', '2773-440-8690', 0, 0, '2026-05-10 12:00:00'),
(27, 2, 'Themba Sithole', 'themba.sithole@gmail.com', '2782-751-2245', 0, 0, '2026-05-10 12:00:00'),
(28, 2, 'Ayanda Cele', 'ayanda.cele@gmail.com', '2766-732-7810', 0, 0, '2026-05-10 12:00:00'),
(29, 2, 'Sibusiso Nkosi', 'sibusiso.nkosi@gmail.com', '2787-916-7433', 0, 0, '2026-05-10 12:00:00'),
(30, 2, 'Nomvula Dlamini', 'nomvula.dlamini@gmail.com', '2766-810-5889', 0, 0, '2026-05-10 12:00:00'),
(31, 2, 'Bongani Nkosi', 'bongani.nkosi@gmail.com', '2760-768-5379', 0, 0, '2026-05-10 12:00:00'),
(32, 2, 'Thandiwe Mkhize', 'thandiwe.mkhize@gmail.com', '2763-496-1325', 0, 0, '2026-05-10 12:00:00'),
(33, 2, 'Sifiso Buthelezi', 'sifiso.buthelezi@gmail.com', '2783-709-9299', 0, 0, '2026-05-10 12:00:00'),
(34, 2, 'Zanele Nkosi', 'zanele.nkosi@gmail.com', '2774-179-5223', 0, 0, '2026-05-10 12:00:00'),
(35, 2, 'Mthokozisi Mthembu', 'mthokozisi.mthembu@gmail.com', '2772-154-8074', 0, 0, '2026-05-10 12:00:00'),
(36, 2, 'Nokuthula Zulu', 'nokuthula.zulu@gmail.com', '2765-936-3742', 0, 0, '2026-05-10 12:00:00'),
(37, 2, 'Sandile Nkosi', 'sandile.nkosi@gmail.com', '2769-881-7174', 0, 0, '2026-05-10 12:00:00'),
(38, 2, 'Phumzile Mthembu', 'phumzile.mthembu@gmail.com', '2789-769-2592', 0, 0, '2026-05-10 12:00:00'),
(39, 2, 'Thulani Nkosi', 'thulani.nkosi@gmail.com', '2763-363-4440', 0, 0, '2026-05-10 12:00:00'),
(40, 2, 'Ntombifuthi Dlamini', 'ntombifuthi.dlamini@gmail.com', '2782-725-5030', 0, 0, '2026-05-10 12:00:00');

-- Owner 3 Customers
INSERT OR REPLACE INTO customers (id, owner_id, name, email, phone, total_purchases, visit_count, created_at) VALUES 
(41, 3, 'Thabo Molefe', 'thabo.molefe@gmail.com', '2774-210-8558', 0, 0, '2026-05-10 12:00:00'),
(42, 3, 'Lerato Nkosi', 'lerato.nkosi@gmail.com', '2764-235-9721', 0, 0, '2026-05-10 12:00:00'),
(43, 3, 'Sipho Zulu', 'sipho.zulu@gmail.com', '2777-245-7456', 0, 0, '2026-05-10 12:00:00'),
(44, 3, 'Nomsa Khumalo', 'nomsa.khumalo@gmail.com', '2777-439-8442', 0, 0, '2026-05-10 12:00:00'),
(45, 3, 'Jabu Mthembu', 'jabu.mthembu@gmail.com', '2788-263-1899', 0, 0, '2026-05-10 12:00:00'),
(46, 3, 'Zinhle Ndlovu', 'zinhle.ndlovu@gmail.com', '2784-194-3551', 0, 0, '2026-05-10 12:00:00'),
(47, 3, 'Themba Sithole', 'themba.sithole@gmail.com', '2767-200-1547', 0, 0, '2026-05-10 12:00:00'),
(48, 3, 'Ayanda Cele', 'ayanda.cele@gmail.com', '2777-945-3621', 0, 0, '2026-05-10 12:00:00'),
(49, 3, 'Sibusiso Nkosi', 'sibusiso.nkosi@gmail.com', '2788-799-7477', 0, 0, '2026-05-10 12:00:00'),
(50, 3, 'Nomvula Dlamini', 'nomvula.dlamini@gmail.com', '2782-180-1219', 0, 0, '2026-05-10 12:00:00'),
(51, 3, 'Bongani Nkosi', 'bongani.nkosi@gmail.com', '2761-452-9212', 0, 0, '2026-05-10 12:00:00'),
(52, 3, 'Thandiwe Mkhize', 'thandiwe.mkhize@gmail.com', '2780-990-9486', 0, 0, '2026-05-10 12:00:00'),
(53, 3, 'Sifiso Buthelezi', 'sifiso.buthelezi@gmail.com', '2769-123-2953', 0, 0, '2026-05-10 12:00:00'),
(54, 3, 'Zanele Nkosi', 'zanele.nkosi@gmail.com', '2778-631-6178', 0, 0, '2026-05-10 12:00:00'),
(55, 3, 'Mthokozisi Mthembu', 'mthokozisi.mthembu@gmail.com', '2762-471-1534', 0, 0, '2026-05-10 12:00:00'),
(56, 3, 'Nokuthula Zulu', 'nokuthula.zulu@gmail.com', '2785-952-3199', 0, 0, '2026-05-10 12:00:00'),
(57, 3, 'Sandile Nkosi', 'sandile.nkosi@gmail.com', '2762-894-6534', 0, 0, '2026-05-10 12:00:00'),
(58, 3, 'Phumzile Mthembu', 'phumzile.mthembu@gmail.com', '2765-500-6405', 0, 0, '2026-05-10 12:00:00'),
(59, 3, 'Thulani Nkosi', 'thulani.nkosi@gmail.com', '2775-384-1936', 0, 0, '2026-05-10 12:00:00'),
(60, 3, 'Ntombifuthi Dlamini', 'ntombifuthi.dlamini@gmail.com', '2772-499-2662', 0, 0, '2026-05-10 12:00:00');

-- Owner 4 Customers
INSERT OR REPLACE INTO customers (id, owner_id, name, email, phone, total_purchases, visit_count, created_at) VALUES 
(61, 4, 'Thabo Molefe', 'thabo.molefe@gmail.com', '2777-745-1736', 0, 0, '2026-05-10 12:00:00'),
(62, 4, 'Lerato Nkosi', 'lerato.nkosi@gmail.com', '2778-367-5980', 0, 0, '2026-05-10 12:00:00'),
(63, 4, 'Sipho Zulu', 'sipho.zulu@gmail.com', '2780-875-8521', 0, 0, '2026-05-10 12:00:00'),
(64, 4, 'Nomsa Khumalo', 'nomsa.khumalo@gmail.com', '2775-475-8038', 0, 0, '2026-05-10 12:00:00'),
(65, 4, 'Jabu Mthembu', 'jabu.mthembu@gmail.com', '2761-111-4053', 0, 0, '2026-05-10 12:00:00'),
(66, 4, 'Zinhle Ndlovu', 'zinhle.ndlovu@gmail.com', '2789-473-9740', 0, 0, '2026-05-10 12:00:00'),
(67, 4, 'Themba Sithole', 'themba.sithole@gmail.com', '2782-665-8580', 0, 0, '2026-05-10 12:00:00'),
(68, 4, 'Ayanda Cele', 'ayanda.cele@gmail.com', '2760-849-8401', 0, 0, '2026-05-10 12:00:00'),
(69, 4, 'Sibusiso Nkosi', 'sibusiso.nkosi@gmail.com', '2773-438-6482', 0, 0, '2026-05-10 12:00:00'),
(70, 4, 'Nomvula Dlamini', 'nomvula.dlamini@gmail.com', '2775-750-6501', 0, 0, '2026-05-10 12:00:00'),
(71, 4, 'Bongani Nkosi', 'bongani.nkosi@gmail.com', '2766-847-8773', 0, 0, '2026-05-10 12:00:00'),
(72, 4, 'Thandiwe Mkhize', 'thandiwe.mkhize@gmail.com', '2779-203-3837', 0, 0, '2026-05-10 12:00:00'),
(73, 4, 'Sifiso Buthelezi', 'sifiso.buthelezi@gmail.com', '2784-576-4113', 0, 0, '2026-05-10 12:00:00'),
(74, 4, 'Zanele Nkosi', 'zanele.nkosi@gmail.com', '2770-475-1847', 0, 0, '2026-05-10 12:00:00'),
(75, 4, 'Mthokozisi Mthembu', 'mthokozisi.mthembu@gmail.com', '2776-447-2417', 0, 0, '2026-05-10 12:00:00'),
(76, 4, 'Nokuthula Zulu', 'nokuthula.zulu@gmail.com', '2773-511-1123', 0, 0, '2026-05-10 12:00:00'),
(77, 4, 'Sandile Nkosi', 'sandile.nkosi@gmail.com', '2789-100-3301', 0, 0, '2026-05-10 12:00:00'),
(78, 4, 'Phumzile Mthembu', 'phumzile.mthembu@gmail.com', '2764-598-1263', 0, 0, '2026-05-10 12:00:00'),
(79, 4, 'Thulani Nkosi', 'thulani.nkosi@gmail.com', '2766-207-3575', 0, 0, '2026-05-10 12:00:00'),
(80, 4, 'Ntombifuthi Dlamini', 'ntombifuthi.dlamini@gmail.com', '2772-819-5317', 0, 0, '2026-05-10 12:00:00');

-- =====================================================
-- BUSINESS_LOCATIONS TABLE (corrected table name)
-- =====================================================
-- Owner 1 Locations
INSERT OR REPLACE INTO business_locations (id, owner_id, name, latitude, longitude, region, total_sales, description, created_at) VALUES 
(1, 1, 'Polokwane Central', -23.8962, 29.4486, 'Polokwane', 0, 'Sales location in Polokwane, Limpopo', '2026-05-10 12:00:00'),
(2, 1, 'Thohoyandou Mall', -22.9456, 30.4848, 'Thohoyandou', 0, 'Sales location in Thohoyandou, Limpopo', '2026-05-10 12:00:00'),
(3, 1, 'Tzaneen Market', -23.8332, 30.1596, 'Tzaneen', 0, 'Sales location in Tzaneen, Limpopo', '2026-05-10 12:00:00'),
(4, 1, 'Phalaborwa Gateway', -23.942, 31.1411, 'Phalaborwa', 0, 'Sales location in Phalaborwa, Limpopo', '2026-05-10 12:00:00'),
(5, 1, 'Mokopane Plaza', -24.1833, 29.0167, 'Mokopane', 0, 'Sales location in Mokopane, Limpopo', '2026-05-10 12:00:00'),
(6, 1, 'Louis Trichardt Centre', -23.0439, 29.9032, 'Louis Trichardt', 0, 'Sales location in Louis Trichardt, Limpopo', '2026-05-10 12:00:00'),
(7, 1, 'Musina Border Post', -22.3486, 30.0417, 'Musina', 0, 'Sales location in Musina, Limpopo', '2026-05-10 12:00:00'),
(8, 1, 'Lephalale Mall', -23.6667, 27.75, 'Lephalale', 0, 'Sales location in Lephalale, Limpopo', '2026-05-10 12:00:00');

-- Owner 2 Locations
INSERT OR REPLACE INTO business_locations (id, owner_id, name, latitude, longitude, region, total_sales, description, created_at) VALUES 
(9, 2, 'Polokwane Metro', -23.8934, 29.445, 'Polokwane', 0, 'Sales location in Polokwane, Limpopo', '2026-05-10 12:00:00'),
(10, 2, 'Sekhukhune Market', -24.2956, 30.4578, 'Sekhukhune', 0, 'Sales location in Sekhukhune, Limpopo', '2026-05-10 12:00:00'),
(11, 2, 'Giyani Plaza', -23.276, 30.6262, 'Giyani', 0, 'Sales location in Giyani, Limpopo', '2026-05-10 12:00:00'),
(12, 2, 'Middelburg Hub', -25.7714, 29.4635, 'Middelburg', 0, 'Sales location in Middelburg, Limpopo', '2026-05-10 12:00:00'),
(13, 2, 'Lebowakgomo Square', -24.3055, 29.467, 'Lebowakgomo', 0, 'Sales location in Lebowakgomo, Limpopo', '2026-05-10 12:00:00'),
(14, 2, 'Phalaborwa Mall', -24.0587, 31.1331, 'Phalaborwa', 0, 'Sales location in Phalaborwa, Limpopo', '2026-05-10 12:00:00'),
(15, 2, 'Musina Trade', -22.342, 30.0402, 'Musina', 0, 'Sales location in Musina, Limpopo', '2026-05-10 12:00:00'),
(16, 2, 'Mokopane Centre', -24.1782, 29.0154, 'Mokopane', 0, 'Sales location in Mokopane, Limpopo', '2026-05-10 12:00:00');

-- Owner 3 Locations
INSERT OR REPLACE INTO business_locations (id, owner_id, name, latitude, longitude, region, total_sales, description, created_at) VALUES 
(17, 3, 'Polokwane Business Park', -23.901, 29.453, 'Polokwane', 0, 'Sales location in Polokwane, Limpopo', '2026-05-10 12:00:00'),
(18, 3, 'Tzaneen Office Park', -23.829, 30.157, 'Tzaneen', 0, 'Sales location in Tzaneen, Limpopo', '2026-05-10 12:00:00'),
(19, 3, 'Sibasa Commerce', -22.957, 30.4638, 'Thohoyandou', 0, 'Sales location in Thohoyandou, Limpopo', '2026-05-10 12:00:00'),
(20, 3, 'Louis Trichardt Business', -23.042, 29.904, 'Louis Trichardt', 0, 'Sales location in Louis Trichardt, Limpopo', '2026-05-10 12:00:00'),
(21, 3, 'Mokopane Office Zone', -24.183, 29.019, 'Mokopane', 0, 'Sales location in Mokopane, Limpopo', '2026-05-10 12:00:00'),
(22, 3, 'Phalaborwa Admin', -23.945, 31.14, 'Phalaborwa', 0, 'Sales location in Phalaborwa, Limpopo', '2026-05-10 12:00:00'),
(23, 3, 'Giyani Office', -23.274, 30.628, 'Giyani', 0, 'Sales location in Giyani, Limpopo', '2026-05-10 12:00:00'),
(24, 3, 'Lephalale Business', -23.668, 27.752, 'Lephalale', 0, 'Sales location in Lephalale, Limpopo', '2026-05-10 12:00:00');

-- Owner 4 Locations
INSERT OR REPLACE INTO business_locations (id, owner_id, name, latitude, longitude, region, total_sales, description, created_at) VALUES 
(25, 4, 'Polokwane Fashion Street', -23.897, 29.447, 'Polokwane', 0, 'Sales location in Polokwane, Limpopo', '2026-05-10 12:00:00'),
(26, 4, 'Tzaneen Trend Mall', -23.832, 30.16, 'Tzaneen', 0, 'Sales location in Tzaneen, Limpopo', '2026-05-10 12:00:00'),
(27, 4, 'Thohoyandou Style Square', -22.946, 30.485, 'Thohoyandou', 0, 'Sales location in Thohoyandou, Limpopo', '2026-05-10 12:00:00'),
(28, 4, 'Phalaborwa Fashion Corner', -23.943, 31.142, 'Phalaborwa', 0, 'Sales location in Phalaborwa, Limpopo', '2026-05-10 12:00:00'),
(29, 4, 'Mokopane Style Plaza', -24.184, 29.017, 'Mokopane', 0, 'Sales location in Mokopane, Limpopo', '2026-05-10 12:00:00'),
(30, 4, 'Louis Trichardt Style Hub', -23.044, 29.905, 'Louis Trichardt', 0, 'Sales location in Louis Trichardt, Limpopo', '2026-05-10 12:00:00'),
(31, 4, 'Musina Style Post', -22.349, 30.042, 'Musina', 0, 'Sales location in Musina, Limpopo', '2026-05-10 12:00:00'),
(32, 4, 'Lephalale Fashion Mall', -23.667, 27.751, 'Lephalale', 0, 'Sales location in Lephalale, Limpopo', '2026-05-10 12:00:00');

-- =====================================================
-- SALES TABLE
-- =====================================================
-- Owner 1 Sales
INSERT OR REPLACE INTO sales (id, owner_id, customer_id, location_id, total_amount, total_cost, profit, payment_method, notes, created_at) VALUES 
(1, 1, 13, 3, 1750, 890, 860, 'cash', NULL, '2026-05-07 12:00:00'),
(2, 1, 17, 3, 251, 89, 162, 'cash', NULL, '2026-05-04 12:00:00'),
(3, 1, 6, 8, 159, 59, 100, 'mobile', NULL, '2026-05-01 12:00:00'),
(4, 1, 20, 1, 590, 270, 320, 'cash', NULL, '2026-04-28 12:00:00'),
(5, 1, 1, 5, 16, 4, 12, 'card', NULL, '2026-04-25 12:00:00'),
(6, 1, 7, 4, 108, 42, 66, 'card', NULL, '2026-04-22 12:00:00'),
(7, 1, 5, 5, 25, 10, 15, 'cash', NULL, '2026-04-19 12:00:00'),
(8, 1, 13, 2, 90, 30, 60, 'cash', NULL, '2026-04-16 12:00:00'),
(9, 1, 18, 4, 1130, 570, 560, 'card', NULL, '2026-04-13 12:00:00'),
(10, 1, 14, 2, 1154, 576, 578, 'mobile', NULL, '2026-04-10 12:00:00');

-- Owner 2 Sales
INSERT OR REPLACE INTO sales (id, owner_id, customer_id, location_id, total_amount, total_cost, profit, payment_method, notes, created_at) VALUES 
(11, 2, 24, 12, 1.5, 0.3, 1.2, 'cash', NULL, '2026-05-07 12:00:00'),
(12, 2, 33, 16, 6, 1.5, 4.5, 'mobile', NULL, '2026-05-04 12:00:00'),
(13, 2, 37, 16, 135, 75, 60, 'card', NULL, '2026-05-01 12:00:00'),
(14, 2, 33, 12, 136, 75.2, 60.8, 'mobile', NULL, '2026-04-28 12:00:00'),
(15, 2, 26, 11, 86, 42, 44, 'card', NULL, '2026-04-25 12:00:00'),
(16, 2, 38, 12, 5.5, 1.3, 4.2, 'card', NULL, '2026-04-22 12:00:00'),
(17, 2, 38, 13, 108, 55, 53, 'cash', NULL, '2026-04-19 12:00:00'),
(18, 2, 30, 11, 18, 6.5, 11.5, 'card', NULL, '2026-04-16 12:00:00'),
(19, 2, 34, 12, 143, 74, 69, 'card', NULL, '2026-04-13 12:00:00'),
(20, 2, 23, 10, 73.5, 36.3, 37.2, 'card', NULL, '2026-04-10 12:00:00');

-- Owner 3 Sales
INSERT OR REPLACE INTO sales (id, owner_id, customer_id, location_id, total_amount, total_cost, profit, payment_method, notes, created_at) VALUES 
(21, 3, 54, 20, 96, 39, 57, 'cash', NULL, '2026-05-07 12:00:00'),
(22, 3, 52, 18, 20, 8, 12, 'mobile', NULL, '2026-05-04 12:00:00'),
(23, 3, 57, 21, 17, 5, 12, 'mobile', NULL, '2026-05-01 12:00:00'),
(24, 3, 55, 24, 19, 7, 12, 'cash', NULL, '2026-04-28 12:00:00'),
(25, 3, 60, 23, 24, 10, 14, 'card', NULL, '2026-04-25 12:00:00'),
(26, 3, 46, 21, 68, 29, 39, 'card', NULL, '2026-04-22 12:00:00'),
(27, 3, 50, 18, 32, 12, 20, 'mobile', NULL, '2026-04-19 12:00:00'),
(28, 3, 43, 18, 71, 32, 39, 'cash', NULL, '2026-04-16 12:00:00'),
(29, 3, 50, 19, 48, 23, 25, 'card', NULL, '2026-04-13 12:00:00'),
(30, 3, 54, 18, 39, 18, 21, 'cash', NULL, '2026-04-10 12:00:00');

-- Owner 4 Sales
INSERT OR REPLACE INTO sales (id, owner_id, customer_id, location_id, total_amount, total_cost, profit, payment_method, notes, created_at) VALUES 
(31, 4, 79, 28, 400, 132, 268, 'card', NULL, '2026-05-07 12:00:00'),
(32, 4, 79, 31, 150, 50, 100, 'cash', NULL, '2026-05-04 12:00:00'),
(33, 4, 63, 29, 80, 24, 56, 'mobile', NULL, '2026-05-01 12:00:00'),
(34, 4, 76, 30, 89, 25, 64, 'card', NULL, '2026-04-28 12:00:00'),
(35, 4, 80, 31, 95, 31, 64, 'mobile', NULL, '2026-04-25 12:00:00'),
(36, 4, 69, 25, 118, 35, 83, 'mobile', NULL, '2026-04-22 12:00:00'),
(37, 4, 72, 26, 14, 4, 10, 'cash', NULL, '2026-04-19 12:00:00'),
(38, 4, 72, 28, 204, 66, 138, 'cash', NULL, '2026-04-16 12:00:00'),
(39, 4, 61, 29, 115, 38, 77, 'mobile', NULL, '2026-04-13 12:00:00'),
(40, 4, 73, 28, 118, 33, 85, 'card', NULL, '2026-04-10 12:00:00');

-- =====================================================
-- SALES_ITEMS TABLE
-- =====================================================
-- Owner 1 Sales Items
INSERT OR REPLACE INTO sales_items (id, sale_id, product_id, quantity, unit_price, cost_price, subtotal) VALUES 
(1, 1, 3, 2, 80, 30, 160),
(2, 1, 1, 2, 750, 400, 1500),
(3, 1, 7, 2, 45, 15, 90),
(4, 2, 7, 3, 45, 15, 135),
(5, 2, 10, 2, 50, 20, 100),
(6, 2, 4, 2, 8, 2, 16),
(7, 3, 6, 3, 5, 1, 15),
(8, 3, 5, 2, 12, 3, 24),
(9, 3, 8, 2, 60, 25, 120),
(10, 4, 3, 3, 80, 30, 240),
(11, 4, 2, 1, 350, 180, 350),
(12, 5, 4, 2, 8, 2, 16),
(13, 6, 4, 1, 8, 2, 8),
(14, 6, 10, 2, 50, 20, 100),
(15, 7, 9, 1, 25, 10, 25),
(16, 8, 7, 2, 45, 15, 90),
(17, 9, 2, 3, 350, 180, 1050),
(18, 9, 3, 1, 80, 30, 80),
(19, 10, 3, 1, 80, 30, 80),
(20, 10, 2, 3, 350, 180, 1050),
(21, 10, 5, 2, 12, 3, 24);

-- Owner 2 Sales Items
INSERT OR REPLACE INTO sales_items (id, sale_id, product_id, quantity, unit_price, cost_price, subtotal) VALUES 
(22, 11, 20, 3, 0.5, 0.1, 1.5),
(23, 12, 19, 3, 2, 0.5, 6),
(24, 13, 11, 3, 45, 25, 135),
(25, 14, 11, 3, 45, 25, 135),
(26, 14, 20, 2, 0.5, 0.1, 1),
(27, 15, 14, 3, 5, 2, 15),
(28, 15, 17, 1, 35, 20, 35),
(29, 15, 16, 2, 18, 8, 36),
(30, 16, 19, 2, 2, 0.5, 4),
(31, 16, 20, 3, 0.5, 0.1, 1.5),
(32, 17, 18, 2, 3, 1, 6),
(33, 17, 16, 1, 18, 8, 18),
(34, 17, 12, 3, 28, 15, 84),
(35, 18, 15, 2, 8, 3, 16),
(36, 18, 19, 1, 2, 0.5, 2),
(37, 19, 17, 1, 35, 20, 35),
(38, 19, 12, 3, 28, 15, 84),
(39, 19, 15, 3, 8, 3, 24),
(40, 20, 12, 2, 28, 15, 56),
(41, 20, 20, 3, 0.5, 0.1, 1.5),
(42, 20, 15, 2, 8, 3, 16);

-- Owner 3 Sales Items
INSERT OR REPLACE INTO sales_items (id, sale_id, product_id, quantity, unit_price, cost_price, subtotal) VALUES 
(43, 21, 23, 3, 12, 5, 36),
(44, 21, 29, 3, 20, 8, 60),
(45, 22, 25, 2, 10, 4, 20),
(46, 23, 30, 2, 4, 1, 8),
(47, 23, 22, 3, 3, 1, 9),
(48, 24, 28, 1, 3, 1, 3),
(49, 24, 23, 1, 12, 5, 12),
(50, 24, 30, 1, 4, 1, 4),
(51, 25, 23, 2, 12, 5, 24),
(52, 26, 30, 3, 4, 1, 12),
(53, 26, 26, 2, 25, 12, 50),
(54, 26, 27, 1, 6, 2, 6),
(55, 27, 30, 2, 4, 1, 8),
(56, 27, 23, 2, 12, 5, 24),
(57, 28, 26, 2, 25, 12, 50),
(58, 28, 22, 3, 3, 1, 9),
(59, 28, 23, 1, 12, 5, 12),
(60, 29, 23, 1, 12, 5, 12),
(61, 29, 27, 1, 6, 2, 6),
(62, 29, 21, 2, 15, 8, 30),
(63, 30, 21, 1, 15, 8, 15),
(64, 30, 23, 2, 12, 5, 24);

-- Owner 4 Sales Items
INSERT OR REPLACE INTO sales_items (id, sale_id, product_id, quantity, unit_price, cost_price, subtotal) VALUES 
(65, 31, 34, 2, 45, 15, 90),
(66, 31, 40, 2, 20, 6, 40),
(67, 31, 35, 3, 90, 30, 270),
(68, 32, 32, 1, 60, 20, 60),
(69, 32, 34, 2, 45, 15, 90),
(70, 33, 38, 1, 8, 2, 8),
(71, 33, 36, 2, 15, 5, 30),
(72, 33, 39, 3, 14, 4, 42),
(73, 34, 37, 3, 12, 3, 36),
(74, 34, 39, 2, 14, 4, 28),
(75, 34, 31, 1, 25, 8, 25),
(76, 35, 34, 1, 45, 15, 45),
(77, 35, 31, 2, 25, 8, 50),
(78, 36, 38, 3, 8, 2, 24),
(79, 36, 33, 1, 80, 25, 80),
(80, 36, 39, 1, 14, 4, 14),
(81, 37, 39, 1, 14, 4, 14),
(82, 38, 38, 3, 8, 2, 24),
(83, 38, 32, 3, 60, 20, 180),
(84, 39, 35, 1, 90, 30, 90),
(85, 39, 31, 1, 25, 8, 25),
(86, 40, 39, 3, 14, 4, 42),
(87, 40, 40, 2, 20, 6, 40),
(88, 40, 37, 3, 12, 3, 36);

COMMIT;