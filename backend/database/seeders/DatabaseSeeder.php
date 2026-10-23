<?php

namespace Database\Seeders;

use App\Models\Product;
use App\Models\User;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;

class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        // Pengguna admin untuk pengujian API dan login frontend
        User::firstOrCreate(
<<<<<<< HEAD
            ['email' => 'admin@toko.local'],
            [
                'name' => 'Muhammad Abel Abhinaya',
=======
            ['email' => 'admin@ugm.ac.id'],
            [
                'name' => 'Abel Administrator',
>>>>>>> origin/main
                'password' => Hash::make('password123'),
            ]
        );

        // Seeding sampel data katalog produk toko
        $products = [
            [
                'name' => 'Kemeja Oxford Katun Lengan Panjang',
                'sku' => 'PRD-OXF-001',
                'category' => 'Pakaian',
                'price' => 175000.00,
                'stock' => 35,
                'status' => 'available',
                'description' => 'Kemeja katun premium potongan regular fit, nyaman dipakai untuk suasana kasual maupun formal.',
            ],
            [
                'name' => 'Sepatu Sneakers Kanvas Klasik',
                'sku' => 'PRD-SNK-002',
                'category' => 'Alas Kaki',
                'price' => 289000.00,
                'stock' => 20,
                'status' => 'available',
                'description' => 'Sepatu kasual dengan sol karet vulkanisir tahan aus dan insole busa empuk.',
            ],
            [
                'name' => 'Tas Ransel Laptop Anti Air 20L',
                'sku' => 'PRD-BAG-003',
                'category' => 'Aksesoris',
                'price' => 345000.00,
                'stock' => 14,
                'status' => 'available',
                'description' => 'Ransel material poliester tahan cipratan air dengan kompartemen laptop hingga 15.6 inci.',
            ],
            [
                'name' => 'Earphone Wireless TWS Bass Pro',
                'sku' => 'PRD-AUD-004',
                'category' => 'Elektronik',
                'price' => 220000.00,
                'stock' => 4,
                'status' => 'low_stock',
                'description' => 'Earphone nirkabel Bluetooth 5.3 dengan latensi rendah dan daya tahan baterai 24 jam.',
            ],
            [
                'name' => 'Kaos Polos Heavyweight Cotton 24s',
                'sku' => 'PRD-TEE-005',
                'category' => 'Pakaian',
                'price' => 85000.00,
                'stock' => 50,
                'status' => 'available',
                'description' => 'Kaos basic bahan katun combed 24s tebal tidak terawang dan menyerap keringat.',
            ],
            [
                'name' => 'Dompet Kulit Bifold Minimalis',
                'sku' => 'PRD-WLT-006',
                'category' => 'Aksesoris',
                'price' => 125000.00,
                'stock' => 0,
                'status' => 'out_of_stock',
                'description' => 'Dompet kulit sintetis premium dengan 6 slot kartu dan 2 kompartemen uang kertas.',
            ],
        ];

        foreach ($products as $product) {
            Product::firstOrCreate(
                ['sku' => $product['sku']],
                $product
            );
        }
    }
}
