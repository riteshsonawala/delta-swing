package com.deltaswing.domain.repository

import com.deltaswing.domain.model.PricePoint
import com.deltaswing.domain.model.Stock
import kotlinx.coroutines.flow.Flow

interface StockRepository {
    fun getStocks(userId: String): Flow<List<Stock>>
    suspend fun getStock(stockId: String): Stock?
    suspend fun addStock(stock: Stock): String
    suspend fun updateStock(stock: Stock)
    suspend fun deleteStock(stockId: String)
    suspend fun fetchCurrentPrice(symbol: String): Double?
    suspend fun fetchPriceHistory(symbol: String): List<PricePoint>
    suspend fun refreshPrices(userId: String)
    suspend fun syncWithFirestore(userId: String)
}
