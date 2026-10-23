<?php

namespace Database\Factories;

use App\Models\Product;
use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Str;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\Product>
 */
class ProductFactory extends Factory
{
    protected $model = Product::class;

    /**
     * Definisi nilai baku atribut model.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        $categories = ['Pakaian', 'Alas Kaki', 'Aksesoris', 'Elektronik', 'Perlengkapan'];
        $statuses = ['available', 'low_stock', 'out_of_stock'];

        return [
            'name' => fake()->words(3, true),
            'sku' => 'PRD-' . strtoupper(Str::random(6)),
            'category' => fake()->randomElement($categories),
            'price' => fake()->randomFloat(2, 25000, 1500000),
            'stock' => fake()->numberBetween(0, 100),
            'status' => fake()->randomElement($statuses),
            'description' => fake()->sentence(10),
        ];
    }
}
