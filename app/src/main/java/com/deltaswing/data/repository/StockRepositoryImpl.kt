package com.deltaswing.data.repository

import com.deltaswing.BuildConfig
import com.deltaswing.data.local.dao.StockDao
import com.deltaswing.data.local.entity.StockEntity
import com.deltaswing.data.remote.api.AlphaVantageApi
import com.deltaswing.domain.model.PricePoint
import com.deltaswing.domain.model.Stock
import com.deltaswing.domain.repository.StockRepository
import com.google.firebase.firestore.FirebaseFirestore
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.tasks.await
import java.util.UUID
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class StockRepositoryImpl @Inject constructor(
    private val stockDao: StockDao,
    private val api: AlphaVantageApi,
    private val firestore: FirebaseFirestore
) : StockRepository {

    private val apiKey = BuildConfig.ALPHA_VANTAGE_API_KEY

    override fun getStocks(userId: String): Flow<List<Stock>> {
        return stockDao.getStocksByUser(userId).map { entities ->
            entities.map { it.toDomain() }
        }
    }

    override suspend fun getStock(stockId: String): Stock? {
        return stockDao.getStock(stockId)?.toDomain()
    }

    override suspend fun addStock(stock: Stock): String {
        val id = stock.id.ifEmpty { UUID.randomUUID().toString() }
        val stockWithId = stock.copy(id = id, lastUpdated = System.currentTimeMillis())
        stockDao.insertStock(StockEntity.fromDomain(stockWithId))
        syncStockToFirestore(stockWithId)
        return id
    }

    override suspend fun updateStock(stock: Stock) {
        val updated = stock.copy(lastUpdated = System.currentTimeMillis())
        stockDao.updateStock(StockEntity.fromDomain(updated))
        syncStockToFirestore(updated)
    }

    override suspend fun deleteStock(stockId: String) {
        val stock = stockDao.getStock(stockId) ?: return
        stockDao.deleteStock(stockId)
        try {
            firestore.collection("users")
                .document(stock.userId)
                .collection("stocks")
                .document(stockId)
                .delete()
                .await()
        } catch (_: Exception) { }
    }

    override suspend fun fetchCurrentPrice(symbol: String): Double? {
        return try {
            val response = api.getGlobalQuote(symbol = symbol, apiKey = apiKey)
            response.globalQuote?.price?.toDoubleOrNull()
        } catch (_: Exception) {
            null
        }
    }

    override suspend fun fetchPriceHistory(symbol: String): List<PricePoint> {
        return try {
            val response = api.getDailyTimeSeries(symbol = symbol, apiKey = apiKey)
            response.timeSeries?.entries?.take(30)?.map { (date, data) ->
                PricePoint(
                    date = date,
                    open = data.open?.toDoubleOrNull() ?: 0.0,
                    high = data.high?.toDoubleOrNull() ?: 0.0,
                    low = data.low?.toDoubleOrNull() ?: 0.0,
                    close = data.close?.toDoubleOrNull() ?: 0.0,
                    volume = data.volume?.toLongOrNull() ?: 0L
                )
            }?.sortedBy { it.date } ?: emptyList()
        } catch (_: Exception) {
            emptyList()
        }
    }

    override suspend fun refreshPrices(userId: String) {
        val stocks = stockDao.getStocksByUserOnce(userId)
        stocks.forEach { entity ->
            val price = fetchCurrentPrice(entity.symbol)
            if (price != null) {
                val updated = entity.copy(
                    currentPrice = price,
                    lastUpdated = System.currentTimeMillis()
                )
                stockDao.updateStock(updated)
            }
        }
    }

    override suspend fun syncWithFirestore(userId: String) {
        try {
            val snapshot = firestore.collection("users")
                .document(userId)
                .collection("stocks")
                .get()
                .await()

            val remoteStocks = snapshot.documents.mapNotNull { doc ->
                doc.toObject(FirestoreStock::class.java)?.toDomain(doc.id, userId)
            }

            val localStocks = stockDao.getStocksByUserOnce(userId)
            val localMap = localStocks.associateBy { it.id }
            val remoteMap = remoteStocks.associateBy { it.id }

            // Merge: remote wins for newer, local wins for newer
            remoteStocks.forEach { remote ->
                val local = localMap[remote.id]
                if (local == null || remote.lastUpdated > local.lastUpdated) {
                    stockDao.insertStock(StockEntity.fromDomain(remote))
                }
            }

            // Push local-only stocks to Firestore
            localStocks.forEach { local ->
                if (!remoteMap.containsKey(local.id)) {
                    syncStockToFirestore(local.toDomain())
                }
            }
        } catch (_: Exception) { }
    }

    private suspend fun syncStockToFirestore(stock: Stock) {
        try {
            val data = hashMapOf(
                "symbol" to stock.symbol,
                "basePrice" to stock.basePrice,
                "deltaPercentage" to stock.deltaPercentage,
                "currentPrice" to stock.currentPrice,
                "lastUpdated" to stock.lastUpdated
            )
            firestore.collection("users")
                .document(stock.userId)
                .collection("stocks")
                .document(stock.id)
                .set(data)
                .await()
        } catch (_: Exception) { }
    }

    private data class FirestoreStock(
        val symbol: String = "",
        val basePrice: Double = 0.0,
        val deltaPercentage: Double = 5.0,
        val currentPrice: Double? = null,
        val lastUpdated: Long = 0L
    ) {
        fun toDomain(id: String, userId: String) = Stock(
            id = id,
            userId = userId,
            symbol = symbol,
            basePrice = basePrice,
            deltaPercentage = deltaPercentage,
            currentPrice = currentPrice,
            lastUpdated = lastUpdated
        )
    }
}
