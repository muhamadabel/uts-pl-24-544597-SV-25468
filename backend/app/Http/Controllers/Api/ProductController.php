<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Product;
use Illuminate\Http\Request;

class ProductController extends Controller
{
    /**
     * Menampilkan seluruh daftar produk toko.
     * Mendukung pencarian (search) dan filter kategori.
     */
    public function index(Request $request)
    {
        $query = Product::query();

        if ($request->filled('search')) {
            $search = $request->input('search');
            $query->where(function ($q) use ($search) {
                $q->where('name', 'like', "%{$search}%")
                  ->orWhere('sku', 'like', "%{$search}%");
            });
        }

        if ($request->filled('category')) {
            $query->where('category', $request->input('category'));
        }

        $products = $query->latest()->get();

        return response()->json([
            'status' => 'success',
            'data' => $products,
        ], 200);
    }

    /**
     * Menyimpan data produk baru ke basis data.
     * Mengembalikan status HTTP 201 Created jika sukses,
     * atau 422 Unprocessable Content bila validasi gagal.
     */
    public function store(Request $request)
    {
        $validated = $request->validate([
            'name' => 'required|string|max:255',
            'sku' => 'required|string|max:50|unique:products,sku',
            'category' => 'required|string|max:100',
            'price' => 'required|numeric|min:0',
            'stock' => 'required|integer|min:0',
            'status' => 'required|in:available,low_stock,out_of_stock,discontinued',
            'description' => 'nullable|string',
        ]);

        $product = Product::create($validated);

        return response()->json([
            'status' => 'success',
            'message' => 'Produk berhasil ditambahkan.',
            'data' => $product,
        ], 201);
    }

    /**
     * Menampilkan satu data produk spesifik berdasarkan ID.
     */
    public function show($id)
    {
        $product = Product::find($id);

        if (!$product) {
            return response()->json([
                'status' => 'error',
                'message' => 'Produk tidak ditemukan.',
            ], 404);
        }

        return response()->json([
            'status' => 'success',
            'data' => $product,
        ], 200);
    }

    /**
     * Memperbarui data produk yang tersimpan.
     */
    public function update(Request $request, $id)
    {
        $product = Product::find($id);

        if (!$product) {
            return response()->json([
                'status' => 'error',
                'message' => 'Produk tidak ditemukan.',
            ], 404);
        }

        $validated = $request->validate([
            'name' => 'sometimes|required|string|max:255',
            'sku' => 'sometimes|required|string|max:50|unique:products,sku,' . $id,
            'category' => 'sometimes|required|string|max:100',
            'price' => 'sometimes|required|numeric|min:0',
            'stock' => 'sometimes|required|integer|min:0',
            'status' => 'sometimes|required|in:available,low_stock,out_of_stock,discontinued',
            'description' => 'nullable|string',
        ]);

        $product->update($validated);

        return response()->json([
            'status' => 'success',
            'message' => 'Produk berhasil diperbarui.',
            'data' => $product,
        ], 200);
    }

    /**
     * Menghapus satu data produk dari basis data.
     */
    public function destroy($id)
    {
        $product = Product::find($id);

        if (!$product) {
            return response()->json([
                'status' => 'error',
                'message' => 'Produk tidak ditemukan.',
            ], 404);
        }

        $product->delete();

        return response()->json([
            'status' => 'success',
            'message' => 'Produk berhasil dihapus.',
        ], 200);
    }
}
