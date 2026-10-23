<?php

namespace Tests\Feature;

use App\Models\Product;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class ProductApiTest extends TestCase
{
    use RefreshDatabase;

    /**
     * Uji 1 (CPMK1 Soal 1a & 1c): Akses ke endpoint produk tanpa token ditolak dengan status 401 Unauthorized.
     */
    public function test_cannot_access_products_without_token_returns_401(): void
    {
        $response = $this->getJson('/api/products');

        $response->assertStatus(401);
    }

    /**
     * Uji 2 (CPMK1 Soal 1a): Login pengguna dengan kredensial valid mengembalikan token Sanctum dan status 200.
     */
    public function test_user_can_login_with_valid_credentials(): void
    {
        $user = User::factory()->create([
            'email' => 'admin@toko.local',
            'password' => bcrypt('password123'),
        ]);

        $response = $this->postJson('/api/login', [
            'email' => 'admin@toko.local',
            'password' => 'password123',
        ]);

        $response->assertStatus(200)
            ->assertJsonStructure([
                'message',
                'access_token',
                'token_type',
                'user' => ['id', 'name', 'email'],
            ]);
    }

    /**
     * Uji 3 (CPMK1 Soal 1c): Validasi login gagal (format email salah atau field kosong) mengembalikan status 422.
     */
    public function test_login_validation_failure_returns_422(): void
    {
        $response = $this->postJson('/api/login', [
            'email' => 'bukan-email-valid',
            'password' => '',
        ]);

        $response->assertStatus(422)
            ->assertJsonValidationErrors(['email', 'password']);
    }

    /**
     * Uji 4 (CPMK1 Soal 1b & 1c): Menambah produk baru dengan data valid mengembalikan status 201 Created dan tersimpan di database.
     */
    public function test_can_create_product_with_valid_token_returns_201(): void
    {
        $user = User::factory()->create();

        $payload = [
            'name' => 'Jaket Parka Outdoor Tahan Angin',
            'sku' => 'PRD-JKT-101',
            'category' => 'Pakaian',
            'price' => 389000.00,
            'stock' => 15,
            'status' => 'available',
            'description' => 'Jaket parka dengan lapisan fleece hangat dan tudung kepala anti angin.',
        ];

        $response = $this->actingAs($user, 'sanctum')->postJson('/api/products', $payload);

        $response->assertStatus(201)
            ->assertJsonPath('status', 'success')
            ->assertJsonPath('data.sku', 'PRD-JKT-101');

        $this->assertDatabaseHas('products', [
            'sku' => 'PRD-JKT-101',
        ]);
    }

    /**
     * Uji 5 (CPMK1 Soal 1c): Validasi tambah produk gagal (field kosong, harga negatif) mengembalikan status 422 Unprocessable Content.
     */
    public function test_create_product_validation_failure_returns_422(): void
    {
        $user = User::factory()->create();

        $response = $this->actingAs($user, 'sanctum')->postJson('/api/products', [
            'name' => '',
            'sku' => '',
            'category' => '',
            'price' => -100,
            'stock' => -5,
            'status' => 'status_tidak_valid',
        ]);

        $response->assertStatus(422)
            ->assertJsonValidationErrors(['name', 'sku', 'category', 'price', 'stock', 'status']);
    }

    /**
     * Uji 6 (CPMK1 Soal 1b): Menampilkan seluruh daftar produk toko (CRUD - Index / Read All).
     */
    public function test_can_list_all_products(): void
    {
        $user = User::factory()->create();
        Product::factory()->count(4)->create();

        $response = $this->actingAs($user, 'sanctum')->getJson('/api/products');

        $response->assertStatus(200)
            ->assertJsonPath('status', 'success')
            ->assertJsonCount(4, 'data');
    }

    /**
     * Uji 7 (CPMK1 Soal 1b): Menampilkan detail satu produk berdasarkan ID (CRUD - Show / Read One).
     */
    public function test_can_show_single_product(): void
    {
        $user = User::factory()->create();
        $product = Product::factory()->create();

        $response = $this->actingAs($user, 'sanctum')->getJson("/api/products/{$product->id}");

        $response->assertStatus(200)
            ->assertJsonPath('status', 'success')
            ->assertJsonPath('data.id', $product->id);
    }

    /**
     * Uji 8 (CPMK1 Soal 1b): Memperbarui data produk toko (CRUD - Update).
     */
    public function test_can_update_product(): void
    {
        $user = User::factory()->create();
        $product = Product::factory()->create([
            'status' => 'available',
            'stock' => 10,
        ]);

        $response = $this->actingAs($user, 'sanctum')->putJson("/api/products/{$product->id}", [
            'status' => 'low_stock',
            'stock' => 2,
        ]);

        $response->assertStatus(200)
            ->assertJsonPath('status', 'success')
            ->assertJsonPath('data.status', 'low_stock');

        $this->assertDatabaseHas('products', [
            'id' => $product->id,
            'status' => 'low_stock',
            'stock' => 2,
        ]);
    }

    /**
     * Uji 9 (CPMK1 Soal 1b): Menghapus data produk dari basis data (CRUD - Delete / Destroy).
     */
    public function test_can_delete_product(): void
    {
        $user = User::factory()->create();
        $product = Product::factory()->create();

        $response = $this->actingAs($user, 'sanctum')->deleteJson("/api/products/{$product->id}");

        $response->assertStatus(200)
            ->assertJsonPath('status', 'success');

        $this->assertDatabaseMissing('products', [
            'id' => $product->id,
        ]);
    }

    /**
     * Uji 10 (CPMK1 Soal 1a): Logout mencabut token akses pengguna pada Sanctum.
     */
    public function test_user_can_logout_and_revoke_token(): void
    {
        $user = User::factory()->create();
        $token = $user->createToken('auth_token')->plainTextToken;

        $response = $this->withHeader('Authorization', 'Bearer ' . $token)
            ->postJson('/api/logout');

        $response->assertStatus(200)
            ->assertJsonPath('message', 'Logout berhasil');

        $this->assertCount(0, $user->tokens);
    }
}
