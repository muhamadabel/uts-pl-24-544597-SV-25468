<?php

use App\Http\Controllers\Api\AuthController;
use App\Http\Controllers\Api\ProductController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| API Routes - UTS Konstruksi & Evolusi Perangkat Lunak
| Mahasiswa: Muhammad Abel Abhinaya Riananto (544597)
<<<<<<< HEAD
| Tema: Sistem Manajemen Katalog Produk Toko
=======
| Tema: Sistem Inventaris Peralatan Produksi Multimedia & Laboratorium
>>>>>>> origin/main
|--------------------------------------------------------------------------
*/

// Endpoint login publik (tanpa token)
Route::post('/login', [AuthController::class, 'login']);

// Endpoint terproteksi Sanctum (seluruh endpoint selain login wajib token)
Route::middleware('auth:sanctum')->group(function () {
    Route::post('/logout', [AuthController::class, 'logout']);
    Route::get('/user', function (Request $request) {
        return response()->json([
            'status' => 'success',
            'data' => $request->user(),
        ]);
    });
    Route::apiResource('products', ProductController::class);
});
